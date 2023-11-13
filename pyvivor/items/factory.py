from abc import ABC, abstractmethod

import pygame

from pyvivor.utils import FONT_PATH
from .core import (
    Weapon,
    Item,
    Armor,
    Pierce,
    Health,
    CritChance,
    CritDmg,
    AttackSpeed,
    BetterExp,
    BetterGold,
    MovementSpeed,
    PickupRange,
    LifeRegen,
    link_items
)


COLOR = 'brown'


class ItemFactory(ABC):

    def __init__(self, user):
        self.user = user
        self.items = []
        self.current_item = None
        self.equipped_item = None
        self.surface = None
        self.upgrade_level = self.get_upgrade_level()
        self.title_font = pygame.font.Font(FONT_PATH, 32)
        self.sign_font = pygame.font.Font(FONT_PATH, 18)
        self.minus_sign = self.sign_font.render("-", True, 'white')
        self.plus_sign = self.sign_font.render("+", True, 'white')

        self.sell_item_hit_box = None
        self.buy_item_hit_box = None

    @abstractmethod
    def generate_items(self) -> list[Item]:
        raise NotImplementedError

    def get_item_from_name(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None

    def get_upgrade_level(self):
        if not self.equipped_item:
            return -1
        return self.items.index(self.equipped_item)

    def show_item(self):
        if not self.current_item:
            return self.items[0]
        return self.current_item.updates_to if self.current_item.updates_to else self.current_item

    def buy_item(self):
        if self.equipped_item and not self.equipped_item.updates_to:
            return False
        item = self.current_item.updates_to if self.current_item else self.items[0]
        if self.user.gold < item.cost:
            return False
        self.user.gold -= item.cost
        target = type(self).__name__.replace('Factory', '').lower()
        self.user.items[target] = item.name
        self.current_item = item
        self.equipped_item = item
        self.upgrade_level = self.get_upgrade_level()

    def sell_item(self):
        if not self.equipped_item:
            return False
        self.user.gold += self.equipped_item.cost
        target = type(self).__name__.replace('Factory', '').lower()
        self.user.items[target] = self.current_item.updates_from.name if self.current_item.updates_from else None

        current_item = self.get_item_from_name(self.user.items[target])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None
        self.upgrade_level = self.get_upgrade_level()

        return True

    def update(self):
        item = self.get_item_surface()
        self.surface.blit(item.surface, (0, 0))
        self.draw_upgrades(item)

    def get_item_surface(self):
        item = self.show_item()
        item.update()
        self.surface = pygame.Surface((item.rectangle.width, item.rectangle.height + 100),
                                      pygame.SRCALPHA).convert_alpha()
        return item

    def draw_upgrades(self, item):

        rect = item.surface.get_rect()
        rect.height = 50
        rect.top = item.rectangle.bottom + 50
        pygame.draw.rect(self.surface, 'white', rect, 0)

        upgrade_rect_width = rect.width - 80
        upgrade_rect_height = 30
        upgrade_rect = pygame.Rect(rect.left + 40, rect.top + 10, upgrade_rect_width, upgrade_rect_height)

        self.draw_bar(upgrade_rect)
        self.draw_minus_sign(upgrade_rect)
        self.draw_plus_sign(upgrade_rect)

    def draw_bar(self, rect):
        color = pygame.Color(255, 255, 255, 50)
        sub_rect = rect.copy()
        sub_rect.width = rect.width - 2
        sub_rect.height = rect.height - 2
        sub_rect.left += 1
        sub_rect.top += 1

        # Bars
        pygame.draw.rect(self.surface, color, sub_rect, 0, 0)
        section_width = rect.width // len(self.items)
        if self.upgrade_level > -1:
            filled_bar_width = section_width * (self.upgrade_level + 1) - 1
            filled_bar = pygame.Rect(rect.left + 1, rect.top + 1, filled_bar_width, rect.height - 2)
            pygame.draw.rect(self.surface, 'green', filled_bar, 0, 0)

        # Separators
        for i in range(1, len(self.items)):
            x = i * section_width
            y = rect.centery
            point_top = (x + rect.left, y - rect.height // 2)
            point_bottom = (x + rect.left, y + rect.height // 2)
            pygame.draw.line(self.surface, 'white', point_top, point_bottom, 2)

    def draw_minus_sign(self, rect):
        minus_circle = pygame.draw.circle(self.surface, COLOR, (rect.left - 20, rect.centery), 10)
        self.surface.blit(self.minus_sign, (minus_circle.centerx - self.minus_sign.get_width() // 2,
                                            minus_circle.centery - self.minus_sign.get_height() // 2))
        self.sell_item_hit_box = pygame.Rect(minus_circle.left, minus_circle.top, 20, 20)

    def draw_plus_sign(self, rect):
        plus_circle = pygame.draw.circle(self.surface, COLOR, (rect.right + 20, rect.centery), 10)
        self.surface.blit(self.plus_sign, (plus_circle.centerx - self.plus_sign.get_width() // 2,
                                           plus_circle.centery - self.plus_sign.get_height() // 2))
        self.buy_item_hit_box = pygame.Rect(plus_circle.left, plus_circle.top, 20, 20)


class WeaponFactory(ItemFactory):
    def __init__(self, user):
        super().__init__(user)
        self.items = self.generate_items()
        current_item = self.get_item_from_name(self.user.items["weapon"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("DAMAGE", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def update(self):
        item = self.get_item_surface()
        self.surface.blit(self.title_text, (0, 0))
        pygame.draw.line(self.surface, 'white', (0, 40), (item.rectangle.width, 40), 2)
        self.surface.blit(item.surface, (0, 50))
        self.draw_upgrades(item)

    def generate_items(self) -> list[Item]:
        cannon1 = Weapon("Simple Canon", "Will slightly upgrade the default attack", 50, 5)
        cannon2 = Weapon("Heat Canon", "Adds heat to your projectiles for better damage", 100, 10)
        cannon3 = Weapon("Laser Canon", "Concentrate your projectiles for even more damage", 200, 15)
        cannon4 = Weapon("Plasma Canon", "Upgrade your laser concentration to its limits", 500, 20)
        cannon5 = Weapon("Dark Matter Canon", "Ultimate weapon upgrade", 500, 25)
        link_items(cannon1, cannon2)
        link_items(cannon2, cannon3)
        link_items(cannon3, cannon4)
        link_items(cannon4, cannon5)
        return [cannon1, cannon2, cannon3, cannon4, cannon5]


class ArmourFactory(WeaponFactory):
    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["armour"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("ARMOUR", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        armour1 = Armor("Simple Armour", "Will slightly upgrade your armour", 50, 10)
        armour2 = Armor("Heat Armour", "Adds heat to your armour for better protection", 100, 20)
        armour3 = Armor("Laser Armour", "Concentrate your armour for even more protection", 200, 30)
        armour4 = Armor("Plasma Armour", "Upgrade your laser concentration to its limits", 500, 40)
        armour5 = Armor("Dark Matter Armour", "Ultimate armour upgrade", 500, 50)
        link_items(armour1, armour2)
        link_items(armour2, armour3)
        link_items(armour3, armour4)
        link_items(armour4, armour5)
        return [armour1, armour2, armour3, armour4, armour5]


class PierceFactory(WeaponFactory):

    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["pierce"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("PIERCE", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        pierce_1 = Pierce("Pierce lvl 1", "Pierce +1", 50, 1)
        pierce_2 = Pierce("Pierce lvl 2", "Pierce +1", 100, 2)
        pierce_3 = Pierce("Pierce lvl 3", "Pierce +1", 200, 3)
        link_items(pierce_1, pierce_2)
        link_items(pierce_2, pierce_3)
        return [pierce_1, pierce_2, pierce_3]


class HealthFactory(WeaponFactory):
    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["health"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("HEALTH", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        health_1 = Health("Health lvl 1", "+20 HP", 50, 20)
        health_2 = Health("Health lvl 2", "+40 HP", 100, 40)
        health_3 = Health("Health lvl 3", "+60 HP", 200, 60)
        health_4 = Health("Health lvl 4", "+80 HP", 200, 80)
        health_5 = Health("Health lvl 5", "+100 HP", 200, 100)
        link_items(health_1, health_2)
        link_items(health_2, health_3)
        link_items(health_3, health_4)
        link_items(health_4, health_5)
        return [health_1, health_2, health_3, health_4, health_5]


class CritChanceFactory(WeaponFactory):
    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["critchance"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("CRIT.", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        crit_1 = CritChance("Crit lvl 1", "+5% crit chance", 50, 5)
        crit_2 = CritChance("Crit lvl 2", "+10% crit chance", 100, 10)
        crit_3 = CritChance("Crit lvl 3", "+15% crit chance", 200, 15)
        crit_4 = CritChance("Crit lvl 4", "+20% crit chance", 200, 20)
        crit_5 = CritChance("Crit lvl 5", "+25% crit chance", 200, 25)
        link_items(crit_1, crit_2)
        link_items(crit_2, crit_3)
        link_items(crit_3, crit_4)
        link_items(crit_4, crit_5)
        return [crit_1, crit_2, crit_3, crit_4, crit_5]


class CritDmgFactory(WeaponFactory):
    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["critdmg"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("CRIT. DMG.", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        crit_1 = CritDmg("Crit dmg lvl 1", "+10% crit damage", 50, 0.1)
        crit_2 = CritDmg("Crit dmg lvl 2", "+20% crit damage", 100, 0.2)
        crit_3 = CritDmg("Crit dmg lvl 3", "+30% crit damage", 200, 0.3)
        crit_4 = CritDmg("Crit dmg lvl 4", "+40% crit damage", 200, 0.4)
        crit_5 = CritDmg("Crit dmg lvl 5", "+50% crit damage", 200, 0.5)
        link_items(crit_1, crit_2)
        link_items(crit_2, crit_3)
        link_items(crit_3, crit_4)
        link_items(crit_4, crit_5)
        return [crit_1, crit_2, crit_3, crit_4, crit_5]


class AttackSpeedFactory(WeaponFactory):
    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["attackspeed"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("ATK. SPEED", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        attk_speed_1 = AttackSpeed("Atk. speed lvl 1", "-4% Attack cooldown", 50, 4)
        attk_speed_2 = AttackSpeed("Atk. speed lvl 1 lvl 2", "-8% Attack cooldown", 100, 8)
        attk_speed_3 = AttackSpeed("Atk. speed lvl 1 lvl 3", "-12% Attack cooldown", 200, 12)
        attk_speed_4 = AttackSpeed("Atk. speed lvl 1 lvl 4", "-16% Attack cooldown", 300, 16)
        attk_speed_5 = AttackSpeed("Atk. speed lvl 1 lvl 5", "-20% Attack cooldown", 500, 20)
        link_items(attk_speed_1, attk_speed_2)
        link_items(attk_speed_2, attk_speed_3)
        link_items(attk_speed_3, attk_speed_4)
        link_items(attk_speed_4, attk_speed_5)
        return [attk_speed_1, attk_speed_2, attk_speed_3, attk_speed_4, attk_speed_5]


class BetterExpFactory(WeaponFactory):
    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["betterexp"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("MORE EXP.", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        exp_1 = BetterExp("Experience lvl 1", "10% increased experience", 50, 0.1)
        exp_2 = BetterExp("Experience lvl 2", "20% increased experience", 100, 0.2)
        exp_3 = BetterExp("Experience lvl 3", "30% increased experience", 200, 0.3)
        exp_4 = BetterExp("Experience lvl 4", "40% increased experience", 300, 0.4)
        exp_5 = BetterExp("Experience lvl 5", "50% increased experience", 500, 0.5)
        link_items(exp_1, exp_2)
        link_items(exp_2, exp_3)
        link_items(exp_3, exp_4)
        link_items(exp_4, exp_5)
        return [exp_1, exp_2, exp_3, exp_4, exp_5]


class BetterGoldFactory(WeaponFactory):
    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["bettergold"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("MORE GOLD", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        gold_1 = BetterGold("Gold lvl 1", "10% increased gold", 50, 0.1)
        gold_2 = BetterGold("Gold lvl 2", "20% increased gold", 100, 0.2)
        gold_3 = BetterGold("Gold lvl 3", "30% increased gold", 200, 0.3)
        gold_4 = BetterGold("Gold lvl 4", "40% increased gold", 300, 0.4)
        gold_5 = BetterGold("Gold lvl 5", "50% increased gold", 500, 0.5)
        link_items(gold_1, gold_2)
        link_items(gold_2, gold_3)
        link_items(gold_3, gold_4)
        link_items(gold_4, gold_5)
        return [gold_1, gold_2, gold_3, gold_4, gold_5]


class MovementSpeedFactory(WeaponFactory):
    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["movementspeed"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("VELOCITY", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        velocity_1 = MovementSpeed("Velocity lvl 1", "10% increased gold", 50, 0.1)
        velocity_2 = MovementSpeed("Velocity lvl 2", "20% increased gold", 100, 0.2)
        velocity_3 = MovementSpeed("Velocity lvl 3", "30% increased gold", 200, 0.3)
        velocity_4 = MovementSpeed("Velocity lvl 4", "40% increased gold", 300, 0.4)
        velocity_5 = MovementSpeed("Velocity lvl 5", "50% increased gold", 500, 0.5)
        link_items(velocity_1, velocity_2)
        link_items(velocity_2, velocity_3)
        link_items(velocity_3, velocity_4)
        link_items(velocity_4, velocity_5)
        return [velocity_1, velocity_2, velocity_3, velocity_4, velocity_5]


class PickupRangeFactory(WeaponFactory):
    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["pickuprange"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("PICK UP R.", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        pick_up_range_1 = PickupRange("Pick up lvl 1", "10% pick up range", 50, 24)
        pick_up_range_2 = PickupRange("Pick up lvl 2", "20% pick up range", 100, 48)
        pick_up_range_3 = PickupRange("Pick up lvl 3", "30% pick up range", 200, 72)
        pick_up_range_4 = PickupRange("Pick up lvl 4", "40% pick up range", 300, 96)
        pick_up_range_5 = PickupRange("Pick up lvl 5", "50% pick up range", 500, 120)
        link_items(pick_up_range_1, pick_up_range_2)
        link_items(pick_up_range_2, pick_up_range_3)
        link_items(pick_up_range_3, pick_up_range_4)
        link_items(pick_up_range_4, pick_up_range_5)
        return [pick_up_range_1, pick_up_range_2, pick_up_range_3, pick_up_range_4, pick_up_range_5]


class LifeRegenFactory(WeaponFactory):
    def __init__(self, user):
        super().__init__(user)
        current_item = self.get_item_from_name(self.user.items["liferegen"])
        self.current_item = current_item if current_item else None
        self.equipped_item = current_item if current_item else None

        self.title_text = self.title_font.render("LIFE REGEN", True, 'white')
        self.upgrade_level = self.get_upgrade_level()

    def generate_items(self) -> list[Item]:
        regen_1 = LifeRegen("Life Regen lvl 1", "10% increased life regen", 50, 0.4)
        regen_2 = LifeRegen("Life Regen lvl 2", "20% increased life regen", 100, 0.8)
        regen_3 = LifeRegen("Life Regen lvl 3", "30% increased life regen", 200, 1.2)
        regen_4 = LifeRegen("Life Regen lvl 4", "40% increased life regen", 300, 1.6)
        regen_5 = LifeRegen("Life Regen lvl 5", "50% increased life regen", 500, 2)
        link_items(regen_1, regen_2)
        link_items(regen_2, regen_3)
        link_items(regen_3, regen_4)
        link_items(regen_4, regen_5)
        return [regen_1, regen_2, regen_3, regen_4, regen_5]

