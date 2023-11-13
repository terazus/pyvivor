import pygame

from pyvivor.utils import FONT_PATH


TEXT_COLOR = 'brown'


class Item:

    def __init__(self, name, description, cost):
        self.name = name
        self.description = description
        self.cost = cost

        # Text
        self.text_font = pygame.font.Font(FONT_PATH, 16)
        self.name_text = self.text_font.render(self.name, True, TEXT_COLOR)
        self.cost_text = self.text_font.render(f"Price: {self.cost} gold", True, TEXT_COLOR)

        # Surfaces
        self.surface = None
        self.rectangle = pygame.Rect(0, 0, 300, self.name_text.get_height() + self.cost_text.get_height() + 20)

        # Items links
        self.updates_from = None
        self.updates_to = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Item name must be a string")
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Item description must be a string")
        self._description = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if not any(isinstance(value, t) for t in [float, int]):
            raise TypeError("Item cost must be an integer")
        self._cost = value

    def update(self):
        self.draw()

    def draw(self):
        self.surface = pygame.Surface((self.rectangle.width, self.rectangle.height), pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(self.surface, 'white', self.rectangle, 0)
        self.surface.blit(self.name_text, (self.rectangle.centerx - self.name_text.get_width() // 2, 10))
        self.surface.blit(self.cost_text, (self.rectangle.centerx - self.cost_text.get_width() // 2, 30))

    def __eq__(self, other_name):
        return other_name == self.name if isinstance(other_name, str) else other_name.name == self.name


class Weapon(Item):
    def __init__(self, name, description, cost, base_damage=0):
        super().__init__(name, description, cost)
        self.damage = base_damage
        self.damage_text = self.text_font.render(f"Damage: +{base_damage}", True, TEXT_COLOR)
        self.rectangle.height += self.damage_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.damage_text, (self.rectangle.centerx - self.damage_text.get_width() // 2, 50))

    def apply(self, player):
        player.attack.damage += self.damage


class Armor(Item):
    def __init__(self, name, description, cost, armour=0):
        super().__init__(name, description, cost)
        self.armour = armour
        self.armour_text = self.text_font.render(f"Armour: +{armour}", True, TEXT_COLOR)
        self.rectangle.height += self.armour_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.armour_text, (self.rectangle.centerx - self.armour_text.get_width() // 2, 50))

    def apply(self, player):
        player.armour += self.armour


class Pierce(Item):
    def __init__(self, name, description, cost, pierce=0):
        super().__init__(name, description, cost)
        self.pierce = pierce
        self.pierce_text = self.text_font.render(f"Extra pierce: +{pierce}", True, TEXT_COLOR)
        self.rectangle.height += self.pierce_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.pierce_text, (self.rectangle.centerx - self.pierce_text.get_width() // 2, 50))

    def apply(self, player):
        player.attack.pierce_count = self.pierce


class Health(Item):
    def __init__(self, name, description, cost, health=0):
        super().__init__(name, description, cost)
        self.health = health
        self.health_text = self.text_font.render(f"Extra HP: +{health}", True, TEXT_COLOR)
        self.rectangle.height += self.health_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.health_text, (self.rectangle.centerx - self.health_text.get_width() // 2, 50))

    def apply(self, player):
        player.max_health += self.health
        player.current_health += self.health


class CritChance(Item):
    def __init__(self, name, description, cost, crit=1):
        super().__init__(name, description, cost)
        self.crit = crit
        self.crit_text = self.text_font.render(f"Crit. Chance: +{crit}%", True, TEXT_COLOR)
        self.rectangle.height += self.crit_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.crit_text, (self.rectangle.centerx - self.crit_text.get_width() // 2, 50))

    def apply(self, player):
        player.attack.critical_chance += self.crit


class CritDmg(Item):
    def __init__(self, name, description, cost, multiplier=0.1):
        super().__init__(name, description, cost)
        self.multiplier = multiplier
        self.crit_text = self.text_font.render(f"Crit. Damage: +{multiplier * 100:.0f}%", True, TEXT_COLOR)
        self.rectangle.height += self.crit_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.crit_text, (self.rectangle.centerx - self.crit_text.get_width() // 2, 50))

    def apply(self, player):
        player.attack.critical_multiplier += self.multiplier


class AttackSpeed(Item):
    def __init__(self, name, description, cost, cd=2):
        super().__init__(name, description, cost)
        self.cd = cd
        self.attack_speed_text = self.text_font.render(f"Atk. Speed: +{cd}%", True, TEXT_COLOR)
        self.rectangle.height += self.attack_speed_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.attack_speed_text,
                          (self.rectangle.centerx - self.attack_speed_text.get_width() // 2, 50))

    def apply(self, player):
        player.attack.cooldown_multiplier -= self.cd / 100


class BetterExp(Item):
    def __init__(self, name, description, cost, multiplier=0.1):
        super().__init__(name, description, cost)
        self.multiplier = multiplier
        self.exp_text = self.text_font.render(f"Better Exp: +{multiplier * 100:.0f}%", True, TEXT_COLOR)
        self.rectangle.height += self.exp_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.exp_text, (self.rectangle.centerx - self.exp_text.get_width() // 2, 50))

    def apply(self, player):
        player.experience_rate += self.multiplier


class BetterGold(Item):
    def __init__(self, name, description, cost, multiplier=0.1):
        super().__init__(name, description, cost)
        self.multiplier = multiplier
        self.gold_text = self.text_font.render(f"Better Gold: +{multiplier * 100:.0f}%", True, TEXT_COLOR)
        self.rectangle.height += self.gold_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.gold_text, (self.rectangle.centerx - self.gold_text.get_width() // 2, 50))

    def apply(self, player):
        player.gold_rate += self.multiplier


class MovementSpeed(Item):
    def __init__(self, name, description, cost, factor=0.1):
        super().__init__(name, description, cost)
        self.factor = factor
        self.gold_text = self.text_font.render(f"Velocity: +{factor*20:.0f}%", True, TEXT_COLOR)
        self.rectangle.height += self.gold_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.gold_text, (self.rectangle.centerx - self.gold_text.get_width() // 2, 50))

    def apply(self, player):
        player.movement_speed = player.movement_speed + self.factor / 2.5


class PickupRange(Item):
    def __init__(self, name, description, cost, value=12):
        super().__init__(name, description, cost)
        self.value = value
        self.pickup_text = self.text_font.render(f"Pickup Range: +{100*value//120}%", True, TEXT_COLOR)
        self.rectangle.height += self.pickup_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.pickup_text, (self.rectangle.centerx - self.pickup_text.get_width() // 2, 50))

    def apply(self, player):
        player.pickup_range += self.value


class LifeRegen(Item):
    def __init__(self, name, description, cost, value=0.4):
        super().__init__(name, description, cost)
        self.value = value
        self.regen_text = self.text_font.render(f"Life Regen: +{value}/sec", True, TEXT_COLOR)
        self.rectangle.height += self.regen_text.get_height()

    def update(self):
        self.draw()
        self.surface.blit(self.regen_text, (self.rectangle.centerx - self.regen_text.get_width() // 2, 50))

    def apply(self, player):
        player.life_regen += self.value


def link_items(item1: Item, item2: Item) -> None:
    if not isinstance(item1, Item) or not isinstance(item2, Item):
        raise TypeError("Items must be instances of Item class")

    item1.updates_to = item2
    item2.updates_from = item1
