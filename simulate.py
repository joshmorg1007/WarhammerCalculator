from calculator import Rerolls
import random


def sim_roll(num: int, target: int, crit: int) -> [int, int, int]:
    hits = 0
    crits = 0
    ones = 0
    for _ in range(num):
        roll = random.randrange(1, 6 + 1, 1)
        if roll >= crit:
            hits += 1
            crits += 1
        elif roll >= target:
            hits += 1
        elif roll == 1:
            ones += 1
    return hits, crits, ones


def sim_hit_roll(
    number_of_attacks: int,
    balistic_or_weapon_skill: int,
    rerolls: Rerolls = Rerolls.NONE,
    hit_modifier: int = 0,
    has_lethal_hits: bool = False,
    sustained_hits: int = 0,
    crit_on: int = 6,
) -> tuple[int, int]:
    if balistic_or_weapon_skill is not None:
        modified_balistic_skill = balistic_or_weapon_skill + -1 * hit_modifier
        modified_balistic_skill = max(2, min(modified_balistic_skill, 6))
    else:
        modified_balistic_skill = 1

    hits, crits, ones = sim_roll(number_of_attacks, modified_balistic_skill, crit_on)
    misses = number_of_attacks - hits

    lethals = 0
    match rerolls:
        case Rerolls.NONE:
            pass
        case Rerolls.SINGLE:
            if misses > 0:
                new_hits, new_crits, _ = sim_roll(1, modified_balistic_skill, crit_on)
                hits += new_hits
                crits += new_crits
        case Rerolls.ONES:
            new_hits, new_crits, _ = sim_roll(ones, modified_balistic_skill, crit_on)
            hits += new_hits
            crits += new_crits
        case Rerolls.FULL:
            new_hits, new_crits, _ = sim_roll(misses, modified_balistic_skill, crit_on)
            hits += new_hits
            crits += new_crits

    if sustained_hits > 0:
        hits += sustained_hits * crits
    if has_lethal_hits:
        lethals = crits
        hits -= crits
    return hits, lethals


def sim_wound_roll(
    number_of_hits: float,
    attack_str: int,
    target_toughness: int,
    rerolls: Rerolls = Rerolls.NONE,
    wound_modifier: int = 0,
    wound_bypasses: float = 0,
    has_dev_wounds: bool = False,
    crit_on: int = 6,
) -> tuple[int, int]:
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

    modified_wound += -1 * wound_modifier

    modified_wound = max(2, min(modified_wound, 6))

    hits, crits, ones = sim_roll(number_of_hits, modified_wound, crit_on)
    misses = number_of_hits - hits

    dev_wounds = 0
    match rerolls:
        case Rerolls.NONE:
            pass
        case Rerolls.SINGLE:
            if misses > 0:
                new_hits, new_crits, _ = sim_roll(1, modified_wound, crit_on)
                hits += new_hits
                crits += new_crits
        case Rerolls.ONES:
            new_hits, new_crits, _ = sim_roll(ones, modified_wound, crit_on)
            hits += new_hits
            crits += new_crits
        case Rerolls.FULL:
            new_hits, new_crits, _ = sim_roll(misses, modified_wound, crit_on)
            hits += new_hits
            crits += new_crits

    if has_dev_wounds:
        dev_wounds = crits
        hits -= crits
    return hits + wound_bypasses, dev_wounds


def sim_not_saved(
    number_of_wounds: float,
    weapon_AP: int,
    target_save: int,
    target_invuln: int = 10,
    rerolls: Rerolls = Rerolls.NONE,
    save_modifier: int = 0,
    has_cover: bool = False,
    save_bypasses: int = 0,
) -> int:
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

    saves, _, ones = sim_roll(number_of_wounds, save, 7)

    not_saved = number_of_wounds - saves
    match rerolls:
        case Rerolls.NONE:
            pass
        case Rerolls.SINGLE:
            if not_saved > 0:
                new_saves, _, _ = sim_roll(1, save, 7)
                saves += new_saves
        case Rerolls.ONES:
            new_saves, _, _ = sim_roll(ones, save, 7)
            saves += new_saves
        case Rerolls.FULL:
            new_saves, _, _ = sim_roll(not_saved, save, 7)
            saves += new_saves

    return number_of_wounds - saves + save_bypasses


def sim_dmg(
    weapon_dmg: int,
    numbers_of_unsaved: float,
    enemy_wounds: int,
    feel_no_pain: int = None,
) -> tuple[int, float]:
    number_of_models = 0
    dmg = 0
    current = enemy_wounds
    for _ in range(numbers_of_unsaved):
        if feel_no_pain:
            reduction, _, _ = sim_roll(weapon_dmg, feel_no_pain, 7)
        else:
            reduction = 0

        dmg += weapon_dmg - reduction
        current -= weapon_dmg - reduction

        if current <= 0:
            number_of_models += 1
            current = enemy_wounds

    if current <= enemy_wounds and current > 0:
        number_of_models += (enemy_wounds - current) / enemy_wounds
    return dmg, number_of_models


def get_dice(dice_str: str):
    number_of_die, dice_value = dice_str.split("d")

    if number_of_die == "":
        number_of_die = 1
    number_of_die = int(number_of_die)
    dice_value = int(dice_value)

    total = 0
    for _ in range(number_of_die):
        total += random.randrange(1, dice_value + 1, 1)

    return total


def get_simulated_dmg_for_weapon_profile(
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
        weapons_dmg += get_dice(dmg_dice)
    if attacks_dice:
        number_of_attacks += get_dice(attacks_dice)
    if sustained_hits_dice:
        sustained_hits += get_dice(sustained_hits_dice)

    hits, lethals = sim_hit_roll(
        number_of_attacks,
        balistic_or_weapon_skill,
        rerolls=hit_rerolls,
        hit_modifier=hit_modifier,
        has_lethal_hits=has_lethal_hits,
        sustained_hits=sustained_hits,
        crit_on=crit_hit_on,
    )
    wounds, dev_wounds = sim_wound_roll(
        hits,
        attack_str,
        target_toughness,
        rerolls=wound_rerolls,
        wound_modifier=wound_modifer,
        wound_bypasses=lethals,
        has_dev_wounds=has_dev_wounds,
        crit_on=crit_wound_on,
    )
    not_saved = sim_not_saved(
        wounds,
        weapon_AP,
        target_save,
        target_invuln,
        rerolls=save_rerolls,
        save_modifier=save_modifier,
        has_cover=has_cover,
        save_bypasses=dev_wounds,
    )
    dmg, models = sim_dmg(weapons_dmg, not_saved, enemy_wounds, target_FNP)

    return (
        hits + lethals,
        wounds + dev_wounds,
        not_saved,
        dmg,
        models,
    )


def get_average_simulated_dmg_for_weapon_profile(
    number_of_sims: int,
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
    total_hits = 0
    total_wounds = 0
    total_unsaved = 0
    total_dmg = 0
    total_models = 0
    for _ in range(number_of_sims):
        hits, wounds, not_saved, dmg, models = get_simulated_dmg_for_weapon_profile(
            number_of_attacks,
            balistic_or_weapon_skill,
            attack_str,
            target_toughness,
            weapons_dmg,
            weapon_AP,
            target_save,
            enemy_wounds,
            wound_rerolls,
            wound_modifer,
            hit_rerolls,
            hit_modifier,
            target_invuln,
            save_modifier,
            save_rerolls,
            has_cover,
            target_FNP,
            sustained_hits,
            has_lethal_hits,
            has_dev_wounds,
            crit_hit_on,
            crit_wound_on,
            dmg_dice,
            attacks_dice,
            sustained_hits_dice,
        )
        total_hits += hits
        total_wounds += wounds
        total_unsaved += not_saved
        total_dmg += dmg
        total_models += models
    return (
        total_hits / number_of_sims,
        total_wounds / number_of_sims,
        total_unsaved / number_of_sims,
        total_dmg / number_of_sims,
        total_models / number_of_sims,
    )
