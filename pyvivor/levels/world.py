import pygame

from .background import BackgroundStars, ForegroundFog
from pyvivor.utils import game_status, configurator
from pyvivor.units import Player, DestroyAnimation, EnemyFactory
from pyvivor.UI import GlobalTimer, LevelUpScreen
from pyvivor.buff import BuffManager


class World:
    def __init__(self):
        self.started = False
        self.grounds_sprites = pygame.sprite.Group()
        self.units_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.animations_sprites = pygame.sprite.Group()

        self.background = BackgroundStars(groups=self.grounds_sprites)
        self.main_camera = self.background.camera_handler
        self.foreground_slow = ForegroundFog(groups=self.grounds_sprites)
        self.foreground = ForegroundFog(speed='normal', groups=self.grounds_sprites)
        self.player = Player(groups=self.units_sprites)
        self.buff_manager = BuffManager(self.player)
        self.level_up_screen = LevelUpScreen(self.buff_manager)
        self.global_timer = None
        self.enemy_factory = EnemyFactory(groups=[self.enemies_sprites],
                                          player_position=configurator.game_screen.get_rect().center,
                                          enemy_distance=200)
        self.enemies = self.enemy_factory.generate_enemies(quantity=5)

    def run(self):
        self.background.update()
        self.foreground_slow.update()

        if game_status.started:
            if not self.global_timer:
                self.global_timer = GlobalTimer(configurator.game_screen.get_rect())

            self.global_timer.update()
            self.animations_sprites.update()
            self.player.update()
            if self.background.moved:
                [enemy.update_player_position(self.background.moved) for enemy in self.enemies]
            self.enemies_sprites.update()

            if game_status.paused or game_status.levelling_up:
                self.global_timer.run_pause()
            else:
                self.global_timer.get_timer()
                self.collide_enemies_and_bullets()
                self.enemies.extend(self.enemy_factory.timeline(self.global_timer.time))

            if game_status.levelling_up:
                self.level_up_screen.buff_manager.select_buffs()
                self.level_up_screen.update()
                self.level_up()

        self.foreground.update()
        self.clean_animations()

    def collide_enemies_and_bullets(self):
        damage = self.player.attack.damage
        for bullet in self.player.attack.projectiles:
            for enemy in self.enemies:
                if enemy.collides_with(bullet):
                    enemy.is_hit(damage)
                    if enemy.life <= 0:
                        DestroyAnimation([self.animations_sprites], (enemy.current_x, enemy.current_y))
                        enemy.kill()
                        self.enemies.remove(enemy)
                        self.player.gold += self.player.gold_rate * enemy.gold_value
                        self.player.experience += self.player.experience_rate * enemy.exp_value
                        if self.player.level_up:
                            game_status.levelling_up = True
                    if not self.player.attack.pierce:
                        bullet.kill()
                        if bullet in self.player.attack.projectiles:
                            self.player.attack.projectiles.remove(bullet)

    def collide_player_and_enemies(self):
        pass

    def clean_animations(self):
        for animation in self.animations_sprites:
            if animation.done:
                animation.kill()
                self.animations_sprites.remove(animation)

    def pause(self):
        game_status.paused = True
        for animation in self.animations_sprites:
            animation.alpha = 25
        self.global_timer.pause()

    def unpause(self):
        game_status.paused = False
        for animation in self.animations_sprites:
            animation.alpha = 255
        self.global_timer.unpause()

    def level_up(self):
        self.global_timer.pause()
        mouse = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        rectangles = self.buff_manager.buff_rects

        for i, rect in enumerate(rectangles):
            if mouse[0] and rect.collidepoint(mouse_position):
                buff_name = self.buff_manager.selected_buffs[i]
                buff = self.buff_manager.buff[buff_name]
                buffed = buff['apply']()
                if buffed:
                    self.buff_manager.selected_buffs = []
                    self.exit_level_up_screen()

    def exit_level_up_screen(self):
        game_status.levelling_up = False
        self.player.level_up = False
        self.level_up_screen.buff_manager.selected_buffs = []
        self.global_timer.unpause()



