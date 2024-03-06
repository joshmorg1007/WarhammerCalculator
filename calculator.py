from enum import Enum
from math import ceil

Rerolls = Enum("Rerolls", ["NONE", "SINGLE", "ONES", "FULL"])


def caclulate_hit(
    number_of_attacks: float,
    balistic_or_weapon_skill: int,
    rerolls: Rerolls = Rerolls.NONE,
    hit_modifier: int = 0,
    has_lethal_hits: bool = False,
    sustained_hits: int = 0,
    crit_on: int = 6,
) -> tuple[float, float]:
    if balistic_or_weapon_skill == None:
        return number_of_attacks, 0
    modified_balistic_or_weapon_skill = balistic_or_weapon_skill
    if hit_modifier < 0:
        modified_balistic_or_weapon_skill = min(
            6, modified_balistic_or_weapon_skill + (-1 * hit_modifier)
        )
    elif hit_modifier > 0:
        modified_balistic_or_weapon_skill = max(
            2, modified_balistic_or_weapon_skill + (-1 * hit_modifier)
        )

    modified_balistic_or_weapon_skill = min(modified_balistic_or_weapon_skill, crit_on)
    hits = number_of_attacks * ((6 - modified_balistic_or_weapon_skill + 1) / 6)
    misses = number_of_attacks - hits
    lethals = 0
    sustained = 0

    if has_lethal_hits:
        lethals = number_of_attacks * (6 - crit_on + 1) / 6
        match rerolls:
            case Rerolls.NONE:
                lethals = number_of_attacks * (6 - crit_on + 1) / 6
            case Rerolls.SINGLE:
                lethals += (6 - crit_on + 1) / 6
            case Rerolls.ONES:
                lethals += (number_of_attacks / 6) * (6 - crit_on + 1) / 6
            case Rerolls.FULL:
                lethals += misses * (6 - crit_on + 1) / 6

    if sustained_hits > 0:
        sustained = sustained_hits * (number_of_attacks * (6 - crit_on + 1) / 6)
        match rerolls:
            case Rerolls.NONE:
                sustained = sustained_hits * (number_of_attacks * (6 - crit_on + 1) / 6)
            case Rerolls.SINGLE:
                sustained += sustained_hits * ((6 - crit_on + 1) / 6)
            case Rerolls.ONES:
                sustained += sustained_hits * (
                    (number_of_attacks / 6) * (6 - crit_on + 1) / 6
                )
            case Rerolls.FULL:
                sustained += sustained_hits * (misses * (6 - crit_on + 1) / 6)

    match rerolls:
        case Rerolls.NONE:
            return hits - lethals + sustained, lethals
        case Rerolls.SINGLE:
            return (
                hits
                + ((6 - modified_balistic_or_weapon_skill + 1) / 6)
                - lethals
                + sustained,
                lethals,
            )
        case Rerolls.ONES:
            return (
                hits
                + number_of_attacks
                / 6
                * ((6 - modified_balistic_or_weapon_skill + 1) / 6)
                - lethals
                + sustained,
                lethals,
            )
        case Rerolls.FULL:
            return (
                hits
                + misses * ((6 - modified_balistic_or_weapon_skill + 1) / 6)
                - lethals
                + sustained,
                lethals,
            )


def caclculate_wound(
    number_of_hits: float,
    attack_str: int,
    target_toughness: int,
    rerolls: Rerolls = Rerolls.NONE,
    wound_modifier: int = 0,
    wound_bypasses: float = 0,
    has_dev_wounds: bool = False,
    crit_on: int = 6,
) -> tuple[float, float]:
    modified_wound = 0
    if attack_str > target_toughness:
        if attack_str >= 2 * target_toughness:
            modified_wound = 2
        else:
            modified_wound = 3
    elif attack_str == target_toughness:
        modified_wound = 4
    elif attack_str < target_toughness:
        if attack_str * 2 <= target_toughness:
            modified_wound = 6
        else:
            modified_wound = 5

    if wound_modifier < 0:
        modified_wound = min(6, modified_wound + (-1 * wound_modifier))
    elif wound_modifier > 0:
        modified_wound = max(2, modified_wound + (-1 * wound_modifier))

    modified_wound = min(modified_wound, crit_on)

    wounds = number_of_hits * ((6 - modified_wound + 1) / 6)
    not_wounds = number_of_hits - wounds
    dev_wounds = 0
    if has_dev_wounds:
        dev_wounds = number_of_hits * (6 - crit_on + 1) / 6
        match rerolls:
            case Rerolls.NONE:
                dev_wounds = number_of_hits * (6 - crit_on + 1) / 6
            case Rerolls.SINGLE:
                dev_wounds += (6 - crit_on + 1) / 6
            case Rerolls.ONES:
                dev_wounds += (number_of_hits / 6) * (6 - crit_on + 1) / 6
            case Rerolls.FULL:
                dev_wounds += not_wounds * (6 - crit_on + 1) / 6
    match rerolls:
        case Rerolls.NONE:
            return wounds + wound_bypasses - dev_wounds, dev_wounds
        case Rerolls.SINGLE:
            return (
                wounds + ((6 - modified_wound + 1) / 6) + wound_bypasses - dev_wounds,
                dev_wounds,
            )
        case Rerolls.ONES:
            return (
                wounds
                + number_of_hits / 6 * ((6 - modified_wound + 1) / 6)
                + wound_bypasses
                - dev_wounds,
                dev_wounds,
            )
        case Rerolls.FULL:
            return (
                wounds
                + not_wounds * ((6 - modified_wound + 1) / 6)
                + wound_bypasses
                - dev_wounds,
                dev_wounds,
            )


def caclulate_not_saved(
    number_of_wounds: float,
    weapon_AP: int,
    target_save: int,
    target_invuln: int = 10,
    rerolls: Rerolls = Rerolls.NONE,
    save_modifier: int = 0,
    has_cover: bool = False,
    save_bypasses: int = 0,
) -> float:
    if save_modifier < 0:
        target_save = max(2, target_save + (-1 * save_modifier))
    elif save_modifier > 0:
        target_save = target_save + (-1 * save_modifier)
    save = target_save
    if has_cover:
        if weapon_AP != 0:
            weapon_AP -= 1
            target_save = target_save + weapon_AP
        else:
            target_save = max(3, target_save - 1)
    else:
        target_save = target_save + weapon_AP

    save = min(target_save, target_invuln)

    if save > 6:
        return number_of_wounds + save_bypasses

    saved = number_of_wounds * ((6 - save + 1) / 6)
    not_saved = number_of_wounds - saved
    match rerolls:
        case Rerolls.NONE:
            return not_saved + save_bypasses
        case Rerolls.SINGLE:
            return number_of_wounds - (saved + ((6 - save + 1) / 6)) + save_bypasses
        case Rerolls.ONES:
            return (
                number_of_wounds
                - (saved + number_of_wounds / 6 * ((6 - save + 1) / 6))
                + save_bypasses
            )
        case Rerolls.FULL:
            return (
                number_of_wounds
                - (saved + not_saved * ((6 - save + 1) / 6))
                + save_bypasses
            )


def caclulate_dmg(
    weapon_dmg: int,
    numbers_of_unsaved: float,
    enemy_wounds: int,
    feel_no_pain: int = None,
) -> tuple[float, float]:
    if feel_no_pain:
        weapon_dmg = weapon_dmg * (feel_no_pain - 1) / 6

    attacks_needed_to_kill_model = ceil(enemy_wounds / weapon_dmg)

    dead_models = numbers_of_unsaved // attacks_needed_to_kill_model
    overflow = numbers_of_unsaved - dead_models * attacks_needed_to_kill_model
    dead_models += (overflow * weapon_dmg) / enemy_wounds

    return weapon_dmg * numbers_of_unsaved, dead_models


def get_dice_average(dice_str: str):
    number_of_die, dice_value = dice_str.split("d")

    if number_of_die == "":
        number_of_die = 1
    dice_value = int(dice_value)

    average = 0
    for i in range(1, int(dice_value) + 1):
        average += i / int(dice_value)

    return int(number_of_die) * average


def get_average_dmg_for_weapon_profile(
    number_of_attacks: int,
    balistic_or_weapon_skill: int,
    attack_str: int,
    target_toughness: int,
    weapons_dmg: int,
    weapon_AP: int,
    target_save: int,
    enemy_wounds: int,
    wound_rerolls: Rerolls = Rerolls.NONE,
    wound_modifer: int = 0,
    hit_rerolls: Rerolls = Rerolls.NONE,
    hit_modifier: int = 0,
    target_invuln: int = 10,
    save_modifier: int = 0,
    save_rerolls: Rerolls = Rerolls.NONE,
    has_cover: bool = False,
    target_FNP: int = None,
    sustained_hits: int = 0,
    has_lethal_hits: bool = False,
    has_dev_wounds: bool = False,
    crit_hit_on: int = 6,
    crit_wound_on: int = 6,
    dmg_dice: str = None,
    attacks_dice: str = None,
    sustained_hits_dice: str = None,
):
    if dmg_dice:
        weapons_dmg += get_dice_average(dmg_dice)
    if attacks_dice:
        number_of_attacks += get_dice_average(attacks_dice)
    if sustained_hits_dice:
        sustained_hits += get_dice_average(sustained_hits_dice)
    hits, lethals = caclulate_hit(
        number_of_attacks,
        balistic_or_weapon_skill,
        rerolls=hit_rerolls,
        hit_modifier=hit_modifier,
        has_lethal_hits=has_lethal_hits,
        sustained_hits=sustained_hits,
        crit_on=crit_hit_on,
    )
    wounds, dev_wounds = caclculate_wound(
        hits,
        attack_str,
        target_toughness,
        rerolls=wound_rerolls,
        wound_modifier=wound_modifer,
        wound_bypasses=lethals,
        has_dev_wounds=has_dev_wounds,
        crit_on=crit_wound_on,
    )
    not_saved = caclulate_not_saved(
        wounds,
        weapon_AP,
        target_save,
        target_invuln,
        rerolls=save_rerolls,
        save_modifier=save_modifier,
        has_cover=has_cover,
        save_bypasses=dev_wounds,
    )
    dmg, models = caclulate_dmg(weapons_dmg, not_saved, enemy_wounds, target_FNP)

    return (
        hits + lethals,
        wounds + dev_wounds,
        not_saved,
        dmg,
        models,
    )
