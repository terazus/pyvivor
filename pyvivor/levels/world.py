import pygame

from .background import BackgroundScroller
from pyvivor.utils import game_status, configurator
from pyvivor.units import Player, DestroyAnimation, EnemyFactory, ExperienceGem
from pyvivor.UI import GlobalTimer, LevelUpScreen, GUI
from pyvivor.buff import BuffManager


class World:
    def __init__(self, pause_screen, shop):
        # Groups
        self.grounds_sprites = pygame.sprite.Group()
        self.units_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.animations_sprites = pygame.sprite.Group()
        self.gems_sprites = pygame.sprite.Group()
        self.damage_animations = []

        # Units
        self.player = Player(groups=self.units_sprites, shop=shop)
        self.enemy_factory = EnemyFactory(groups=[self.enemies_sprites],
                                          player_position=configurator.game_screen.get_rect().center,
                                          enemy_distance=200)
        self.enemies = self.enemy_factory.generate_enemies(quantity=5)

        # GUI
        self.gui = GUI(self.player)
        self.pause_screen = pause_screen
        self.pause_screen.player = self.player

        # Background
        self.background = BackgroundScroller(self.grounds_sprites)

        # Other
        self.buff_manager = BuffManager(self.player)
        self.level_up_screen = LevelUpScreen(self.buff_manager)
        self.global_timer = None

        self.kill_count = 0

    def run(self):
        self.background.update()
        if game_status.started:
            self.gui.update()
            self.gems_sprites.update()
            if not self.global_timer:
                self.global_timer = GlobalTimer(configurator.game_screen.get_rect())

            self.global_timer.update()
            self.animations_sprites.update()
            [animation.update() for animation in self.damage_animations]
            self.player.update()
            if self.background.moved:
                [enemy.update_player_position(self.background.moved) for enemy in self.enemies]
                [gem.update_player_position(self.background.moved) for gem in self.gems_sprites]
                [animation.update_player_position(self.background.moved) for animation in self.damage_animations]
                self.player.attack.update_player_position(self.background.moved)
            self.enemies_sprites.update()

            if game_status.paused or game_status.levelling_up or game_status.game_over:
                self.global_timer.run_pause()

            else:
                self.global_timer.get_timer()
                self.handle_collisions()
                self.enemies.extend(self.enemy_factory.timeline(self.global_timer.time))

            if game_status.levelling_up:
                self.level_up_screen.buff_manager.select_buffs()
                self.level_up_screen.update()
                self.level_up()

        self.clean_animations()

    def handle_collisions(self):
        damage, is_crit = self.player.attack.get_damage()

        # Enemies with player and bullets
        for enemy in self.enemies:
            if enemy.is_on_screen and enemy.collides_with(self.player) and enemy.can_attack:
                enemy.attack()
                self.player.is_hit(enemy.damage)

            for bullet in self.player.attack.projectiles:
                if enemy.collides_with(bullet):
                    enemy.is_hit(damage, is_crit, bullet)
                    if enemy.life <= 0:
                        damage_animations = enemy.damage_animations
                        for animation in damage_animations:
                            animation.enemy = None
                            self.damage_animations.append(animation)
                        DestroyAnimation([self.animations_sprites], (enemy.current_x, enemy.current_y))
                        ExperienceGem([self.gems_sprites], (enemy.current_x, enemy.current_y), enemy.exp_value)
                        enemy.kill()
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        self.player.gold += self.player.gold_rate * enemy.gold_value
                        self.kill_count += 1
                    bullet.pierce_count -= 1
                    if not bullet.can_pierce:
                        bullet.kill()
                        if bullet in self.player.attack.projectiles:
                            self.player.attack.projectiles.remove(bullet)

        # Gems with player
        for gem in self.gems_sprites:
            if gem.collides_with(self.player.pickup_range):
                gem.can_merge = False
                gem.move_to_player = True

            if gem.move_to_player and gem.collides_with(50):
                self.player.experience = self.player.experience + gem.worth * self.player.experience_rate
                gem.kill()
                if gem in self.gems_sprites:
                    self.gems_sprites.remove(gem)

        if self.player.level_up and not game_status.levelling_up:
            self.global_timer.pause()
            game_status.levelling_up = True

    def clean_animations(self):
        for animation in self.animations_sprites:
            if animation.done:
                animation.kill()
                self.animations_sprites.remove(animation)
        for animation in self.damage_animations:
            if animation.done:
                animation.kill()
                self.damage_animations.remove(animation)

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



