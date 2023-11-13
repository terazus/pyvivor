from ..defaults import (
    CLAW_ATTACK_BASE_DAMAGE,
    CLAW_ATTACK_BASE_COOLDOWN,
    CLAW_ATTACK_BASE_PIERCE_COUNT,
    CLAW_ATTACK_BASE_PROJECTILE_SPEED,
    CLAW_ATTACK_BASE_PROJECTILE_WIDTH,
    CLAW_ATTACK_BASE_RANGE
)
from .base_attack import BaseAttack


class ClawAttack(BaseAttack):
    name = "Claw Attack"

    def __init__(self):
        super().__init__()
        self.cooldown = CLAW_ATTACK_BASE_COOLDOWN
        self.projectile_speed = CLAW_ATTACK_BASE_PROJECTILE_SPEED
        self.projectile_width = CLAW_ATTACK_BASE_PROJECTILE_WIDTH
        self.range = CLAW_ATTACK_BASE_RANGE
        self.damage = CLAW_ATTACK_BASE_DAMAGE
        self.pierce_count = CLAW_ATTACK_BASE_PIERCE_COUNT


