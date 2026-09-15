def rage_apply(unit, value=10):
    unit.attack += value
    unit.defense -= 5
    print(
        f"[Эффект] {unit.name} впадает в бешенство! атака выросла на {value}, но броня упала на 5."
    )


def rage_remove(unit, value=10):
    unit.attack -= value
    unit.defense += 5
    print(f"[Эффект] ярость у {unit.name} утихла. характеристики вернулись в норму.")


def strength_apply(unit, value=5):
    unit.attack += value
    print(f"[Эффект] {unit.name} чувствует прилив сил! (+{value} к атаке)")


def strength_remove(unit, value=5):
    unit.attack -= value
    print(f"[Эффект] действие зелья силы на {unit.name} закончилось.")


def heal_tick(unit, value=10):
    unit.health += value
    unit.health = min(unit.max_health, unit.health)
    print(f"[Эффект] {unit.name} получает {value} HP от зелья лечения.")
    print(f"текущее хп {unit.name} = {unit.health}")


def poison_tick(unit, value=5):
    unit.health -= value
    print(f"[Эффект] {unit.name} теряет {value} HP от яда.")


def shield_apply(unit, value=10):
    unit.defense += value
    print(f"[Эффект] {unit.name} увеличивает броню на {value}")


def shield_remove(unit, value=10):
    unit.defense -= value
    print(f"[Эффект] {unit.name} действие щита закончилось")


EFFECTS = {
    "rage": {"on_apply": rage_apply, "on_remove": rage_remove},
    "strength": {"on_apply": strength_apply, "on_remove": strength_remove},
    "continuous_heal": {"on_tick": heal_tick},
    "poison": {"on_tick": poison_tick},
    "shield": {"on_apply": shield_apply, "on_remove": shield_remove},
}


class StatusEffect:
    def __init__(self, name, duration, effect_value=0):
        self.name = name
        self.duration = duration
        self.effect_value = effect_value

        config = EFFECTS.get(name, {})
        self.custom_apply = config.get("on_apply")
        self.custom_tick = config.get("on_tick")
        self.custom_remove = config.get("on_remove")

    def on_apply(self, unit):
        if self.custom_apply:
            self.custom_apply(
                unit, self.effect_value
            ) if self.effect_value else self.custom_apply(unit)

    def on_tick(self, unit):
        if self.custom_tick:
            self.custom_tick(
                unit, self.effect_value
            ) if self.effect_value else self.custom_tick(unit)
        self.duration -= 1

    def on_remove(self, unit):
        if self.custom_remove:
            self.custom_remove(
                unit, self.effect_value
            ) if self.effect_value else self.custom_remove(unit)


