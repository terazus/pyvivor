import pygame

from pyvivor.utils import configurator, game_status, FONT_PATH, collide
from pyvivor.items import (
    WeaponFactory,
    ArmourFactory,
    PierceFactory,
    HealthFactory,
    CritChanceFactory,
    CritDmgFactory,
    AttackSpeedFactory,
    BetterExpFactory,
    BetterGoldFactory,
    MovementSpeedFactory,
    PickupRangeFactory,
    LifeRegenFactory
)


class ShopScreen:
    def __init__(self, user):

        # Data
        self.gold = user.gold
        self.user = user

        # Title
        self.title_font = pygame.font.Font(FONT_PATH, 50)
        self.title_text = self.title_font.render("SHOP", True, 'white')

        # RECTANGLE
        width = configurator.game_screen.get_width() - 100
        height = configurator.game_screen.get_height() - 200
        self.rectangle = pygame.Rect(50, 100, width, height)

        # GOLDS
        self.gold_rectangle = pygame.Rect(self.rectangle.left + 10, self.rectangle.top + 10, 200, 50)
        self.gold_font = pygame.font.Font(FONT_PATH, 25)

        # EXIT BUTTON
        width = 250
        height = 60
        self.exit_button_font = pygame.font.Font(FONT_PATH, 25)
        self.exit_button_text = self.exit_button_font.render("EXIT", True, 'brown')
        self.exit_button_rect = pygame.Rect(self.rectangle.right - width - 10, self.rectangle.bottom - height - 10,
                                            width, height)

        # ITEMS
        self.weapon_factory = WeaponFactory(user)
        self.armour_factory = ArmourFactory(user)
        self.pierce_factory = PierceFactory(user)
        self.health_factory = HealthFactory(user)
        self.crit_chance_factory = CritChanceFactory(user)
        self.crit_dmg_factory = CritDmgFactory(user)
        self.attack_speed_factory = AttackSpeedFactory(user)
        self.better_exp_factory = BetterExpFactory(user)
        self.better_gold_factory = BetterGoldFactory(user)
        self.movement_speed_factory = MovementSpeedFactory(user)
        self.pickup_range_factory = PickupRangeFactory(user)
        self.life_regen_factory = LifeRegenFactory(user)

    def update(self):
        configurator.game_screen.blit(self.title_text,
                                      (configurator.screen_width // 2 - self.title_text.get_width() // 2, 10))

        pygame.draw.rect(configurator.game_screen, 'brown', self.rectangle, 0)

        self.gold = self.user.gold
        gold_text = self.gold_font.render(f"Current gold: {self.gold}", True, 'white')
        text_pos = (configurator.game_screen.get_width() - gold_text.get_width() - 50, 10)
        configurator.game_screen.blit(gold_text, text_pos)
        self.create_buttons()
        self.draw_items()

    def create_buttons(self):
        pygame.draw.rect(configurator.game_screen, 'white', self.exit_button_rect, 0)
        configurator.game_screen.blit(self.exit_button_text,
                                      (self.exit_button_rect.centerx - self.exit_button_text.get_width() // 2,
                                       self.exit_button_rect.centery - self.exit_button_text.get_height() // 2))

    def exit_shop(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if mouse_pressed[0] and self.exit_button_rect.collidepoint(mouse_position):
            game_status.shopping = False
            self.user.save()
            return True
        return False

    def draw_items(self):
        self.weapon_factory.update()
        self.armour_factory.update()
        self.pierce_factory.update()
        self.health_factory.update()
        self.crit_chance_factory.update()
        self.crit_dmg_factory.update()
        self.attack_speed_factory.update()
        self.better_exp_factory.update()
        self.better_gold_factory.update()
        self.movement_speed_factory.update()
        self.pickup_range_factory.update()
        self.life_regen_factory.update()

        # Line 1
        configurator.game_screen.blit(self.weapon_factory.surface,
                                      (self.rectangle.left + 40, self.rectangle.top + 10))
        configurator.game_screen.blit(self.armour_factory.surface,
                                      (self.rectangle.left + 390, self.rectangle.top + 10))
        configurator.game_screen.blit(self.pierce_factory.surface,
                                      (self.rectangle.left + 750, self.rectangle.top + 10))
        configurator.game_screen.blit(self.health_factory.surface,
                                      (self.rectangle.left + 1110, self.rectangle.top + 10))
        configurator.game_screen.blit(self.crit_chance_factory.surface,
                                      (self.rectangle.left + 1470, self.rectangle.top + 10))

        # Line 2
        configurator.game_screen.blit(self.crit_dmg_factory.surface,
                                      (self.rectangle.left + 40, self.rectangle.top + 240))
        configurator.game_screen.blit(self.attack_speed_factory.surface,
                                      (self.rectangle.left + 390, self.rectangle.top + 240))
        configurator.game_screen.blit(self.better_exp_factory.surface,
                                      (self.rectangle.left + 750, self.rectangle.top + 240))
        configurator.game_screen.blit(self.better_gold_factory.surface,
                                      (self.rectangle.left + 1110, self.rectangle.top + 240))
        configurator.game_screen.blit(self.movement_speed_factory.surface,
                                      (self.rectangle.left + 1470, self.rectangle.top + 240))

        # Line 3
        configurator.game_screen.blit(self.pickup_range_factory.surface,
                                        (self.rectangle.left + 40, self.rectangle.top + 470))
        configurator.game_screen.blit(self.life_regen_factory.surface,
                                        (self.rectangle.left + 390, self.rectangle.top + 470))

    def handle_clicks(self, mouse_position, action="buy"):
        factories = [self.weapon_factory, self.armour_factory, self.pierce_factory, self.health_factory,
                     self.crit_chance_factory]
        self.click_line(line=factories, mouse_pos=mouse_position, action=action, offset_y=0)

        factories = [self.crit_dmg_factory, self.attack_speed_factory, self.better_exp_factory,
                     self.better_gold_factory, self.movement_speed_factory]
        self.click_line(line=factories, mouse_pos=mouse_position, action=action, offset_y=240)

        factories = [self.pickup_range_factory, self.life_regen_factory]
        self.click_line(line=factories, mouse_pos=mouse_position, action=action, offset_y=470)

    def click_line(self, line, mouse_pos, offset_y=0, action="buy"):
        for i, factory in enumerate(line):
            sign_rect = factory.sell_item_hit_box if action == "sell" else factory.buy_item_hit_box
            sign_rect.left += self.rectangle.left + 40 + (i * 350)
            sign_rect.top = sign_rect.top + offset_y
            if i > 1:
                sign_rect.left += 10 * (i - 1)
            sign_rect.top += self.rectangle.top + 10
            mouse_clicked = pygame.mouse.get_pressed()
            source = {"x": mouse_pos[0], "y": mouse_pos[1], "radius": 1}
            target = {"x": sign_rect.centerx, "y": sign_rect.centery, "radius": sign_rect.width}
            if collide(source, target) and mouse_clicked[0]:
                factory.sell_item() if action == "sell" else factory.buy_item()

    def __iter__(self):
        data = {
            'weapon': self.weapon_factory.equipped_item,
            'armour': self.armour_factory.equipped_item,
            'pierce': self.pierce_factory.equipped_item,
            'health': self.health_factory.equipped_item,
            'critchance': self.crit_chance_factory.equipped_item,
            'critdmg': self.crit_dmg_factory.equipped_item,
            'attackspeed': self.attack_speed_factory.equipped_item,
            'betterexp': self.better_exp_factory.equipped_item,
            'bettergold': self.better_gold_factory.equipped_item,
            'movementspeed': self.movement_speed_factory.equipped_item,
            'pickuprange': self.pickup_range_factory.equipped_item,
            'liferegen': self.life_regen_factory.equipped_item
        }
        yield from data.items()

