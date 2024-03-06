import unittest
from calculator import (
    caclulate_hit,
    caclculate_wound,
    caclulate_not_saved,
    caclulate_dmg,
    get_dice_average,
    Rerolls,
)


class TestHitCalulcations(unittest.TestCase):
    def test_hit_modifier(self):
        self.assertGreater(
            caclulate_hit(10, 4, Rerolls.NONE, 1)[0],
            caclulate_hit(10, 4, Rerolls.NONE, 0)[0],
        )
        self.assertGreater(
            caclulate_hit(10, 4, Rerolls.NONE, 0)[0],
            caclulate_hit(10, 4, Rerolls.NONE, -1)[0],
        )

    def test_unmodified_hit_no_rerolls(self):
        self.assertAlmostEqual(caclulate_hit(10, 4)[0], 5)
        self.assertAlmostEqual(caclulate_hit(10, 3)[0], 20 / 3)
        self.assertAlmostEqual(caclulate_hit(10, 2)[0], 25 / 3)

    def test_unmodified_hit_single_reroll(self):
        self.assertAlmostEqual(caclulate_hit(15, 4, Rerolls.SINGLE)[0], 8)
        self.assertAlmostEqual(caclulate_hit(15, 3, Rerolls.SINGLE)[0], 10 + (2 / 3))
        self.assertAlmostEqual(
            caclulate_hit(15, 2, Rerolls.SINGLE)[0], 25 / 2 + (5 / 6)
        )

    def test_unmodified_hit_reroll_ones(self):
        self.assertAlmostEqual(caclulate_hit(12, 4, Rerolls.ONES)[0], 6 + 1)
        self.assertAlmostEqual(caclulate_hit(12, 3, Rerolls.ONES)[0], 8 + (4 / 3))
        self.assertAlmostEqual(caclulate_hit(12, 2, Rerolls.ONES)[0], 10 + (5 / 3))

    def test_unmodified_hit_reroll_full(self):
        self.assertAlmostEqual(
            caclulate_hit(13, 4, Rerolls.FULL)[0], (13 / 2) + (13 / 4)
        )
        self.assertAlmostEqual(
            caclulate_hit(13, 3, Rerolls.FULL)[0], (26 / 3) + (26 / 9)
        )
        self.assertAlmostEqual(
            caclulate_hit(13, 2, Rerolls.FULL)[0], (65 / 6) + (65 / 36)
        )

    def test_modified_hit_roll(self):
        self.assertAlmostEqual(caclulate_hit(10, 4, Rerolls.NONE, 1)[0], 20 / 3)
        self.assertAlmostEqual(caclulate_hit(10, 3, Rerolls.NONE, 1)[0], 25 / 3)
        self.assertAlmostEqual(caclulate_hit(10, 2, Rerolls.NONE, 1)[0], 25 / 3)

        self.assertAlmostEqual(caclulate_hit(10, 6, Rerolls.NONE, -1)[0], 5 / 3)
        self.assertAlmostEqual(caclulate_hit(10, 5, Rerolls.NONE, -1)[0], 5 / 3)
        self.assertAlmostEqual(caclulate_hit(10, 2, Rerolls.NONE, -1)[0], 20 / 3)

    def test_hit_roll_lethal_hits(self):
        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.NONE, 1, has_lethal_hits=True)[0], 5
        )
        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.NONE, 1, has_lethal_hits=True)[1], 5 / 3
        )

        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.SINGLE, 0, has_lethal_hits=True)[0],
            5.5 - (10 / 6 + 1 / 6),
        )
        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.SINGLE, 0, has_lethal_hits=True)[1],
            5 / 3 + 1 / 6,
        )

        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.ONES, 0, has_lethal_hits=True)[0],
            (5 + 5 / 6) - (10 / 6 + 5 / 18),
        )
        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.ONES, 0, has_lethal_hits=True)[1],
            (10 / 6 + 5 / 18),
        )

        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.FULL, 0, has_lethal_hits=True)[0],
            7.5 - (5 / 3 + 5 / 6),
        )
        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.FULL, 0, has_lethal_hits=True)[1],
            (5 / 3 + 5 / 6),
        )

    def test_hit_roll_sustained_hits(self):
        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.NONE, 0, sustained_hits=1)[0], 5 + 10 / 6
        )

        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.SINGLE, 0, sustained_hits=1)[0],
            5.5 + 10 / 6 + 1 / 6,
        )

        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.ONES, 0, sustained_hits=1)[0],
            5 + 5 / 6 + 10 / 6 + 10 / 36,
        )

        self.assertAlmostEqual(
            caclulate_hit(10, 4, Rerolls.FULL, 0, sustained_hits=1)[0],
            7.5 + 10 / 6 + 5 / 6,
        )

    def test_hit_roll_sustained_and_lethal(self):
        self.assertAlmostEqual(
            caclulate_hit(
                10, 4, Rerolls.NONE, 1, has_lethal_hits=True, sustained_hits=1
            )[0],
            20 / 3,
        )
        self.assertAlmostEqual(
            caclulate_hit(
                10, 4, Rerolls.NONE, 1, has_lethal_hits=True, sustained_hits=1
            )[1],
            5 / 3,
        )

        self.assertAlmostEqual(
            caclulate_hit(
                10, 4, Rerolls.SINGLE, 0, has_lethal_hits=True, sustained_hits=1
            )[0],
            5.5,
        )
        self.assertAlmostEqual(
            caclulate_hit(
                10, 4, Rerolls.SINGLE, 0, has_lethal_hits=True, sustained_hits=1
            )[1],
            5 / 3 + 1 / 6,
        )

        self.assertAlmostEqual(
            caclulate_hit(
                10, 4, Rerolls.ONES, 0, has_lethal_hits=True, sustained_hits=1
            )[0],
            (5 + 5 / 6),
        )
        self.assertAlmostEqual(
            caclulate_hit(
                10, 4, Rerolls.ONES, 0, has_lethal_hits=True, sustained_hits=1
            )[1],
            (10 / 6 + 5 / 18),
        )

        self.assertAlmostEqual(
            caclulate_hit(
                10, 4, Rerolls.FULL, 0, has_lethal_hits=True, sustained_hits=1
            )[0],
            7.5,
        )
        self.assertAlmostEqual(
            caclulate_hit(
                10, 4, Rerolls.FULL, 0, has_lethal_hits=True, sustained_hits=1
            )[1],
            (5 / 3 + 5 / 6),
        )

    def test_hit_with_modified_crit(self):
        self.assertAlmostEqual(caclulate_hit(10, 4, crit_on=5)[0], 5)
        self.assertAlmostEqual(caclulate_hit(10, 6, crit_on=5)[0], 10 / 3)
        self.assertAlmostEqual(
            caclulate_hit(10, 4, crit_on=5, has_lethal_hits=True)[0], 5 / 3
        )
        self.assertAlmostEqual(
            caclulate_hit(10, 4, crit_on=5, has_lethal_hits=True)[1], 10 / 3
        )

        self.assertAlmostEqual(
            caclulate_hit(10, 4, crit_on=5, has_lethal_hits=True, sustained_hits=1)[0],
            5,
        )
        self.assertAlmostEqual(
            caclulate_hit(10, 4, crit_on=5, has_lethal_hits=True, sustained_hits=1)[1],
            10 / 3,
        )


class TestWoundCalculations(unittest.TestCase):
    def test_wound_modifier(self):
        self.assertGreater(
            caclculate_wound(5, 3, 6, Rerolls.NONE, 1)[0],
            caclculate_wound(5, 3, 6, Rerolls.NONE, 0)[0],
        )
        self.assertGreater(
            caclculate_wound(5, 4, 6, Rerolls.NONE, 0)[0],
            caclculate_wound(5, 4, 6, Rerolls.NONE, -1)[0],
        )

    def test_unmodified_wound_roll(self):
        self.assertAlmostEqual(caclculate_wound(5, 3, 6, Rerolls.NONE, 0)[0], 5 / 6)
        self.assertAlmostEqual(caclculate_wound(5, 4, 6, Rerolls.NONE, 0)[0], 5 / 3)
        self.assertAlmostEqual(caclculate_wound(5, 6, 6, Rerolls.NONE, 0)[0], 5 / 2)
        self.assertAlmostEqual(caclculate_wound(5, 7, 6, Rerolls.NONE, 0)[0], 10 / 3)
        self.assertAlmostEqual(caclculate_wound(5, 12, 6, Rerolls.NONE, 0)[0], 25 / 6)

    def test_modified_wound_roll(self):
        self.assertAlmostEqual(caclculate_wound(5, 3, 6, Rerolls.NONE, -1)[0], 5 / 6)
        self.assertAlmostEqual(caclculate_wound(5, 4, 6, Rerolls.NONE, -1)[0], 5 / 6)
        self.assertAlmostEqual(caclculate_wound(5, 6, 6, Rerolls.NONE, -1)[0], 5 / 3)
        self.assertAlmostEqual(caclculate_wound(5, 7, 6, Rerolls.NONE, -1)[0], 5 / 2)
        self.assertAlmostEqual(caclculate_wound(5, 12, 6, Rerolls.NONE, -1)[0], 10 / 3)

        self.assertAlmostEqual(caclculate_wound(5, 3, 6, Rerolls.NONE, 1)[0], 5 / 3)
        self.assertAlmostEqual(caclculate_wound(5, 4, 6, Rerolls.NONE, 1)[0], 5 / 2)
        self.assertAlmostEqual(caclculate_wound(5, 6, 6, Rerolls.NONE, 1)[0], 10 / 3)
        self.assertAlmostEqual(caclculate_wound(5, 7, 6, Rerolls.NONE, 1)[0], 25 / 6)
        self.assertAlmostEqual(caclculate_wound(5, 12, 6, Rerolls.NONE, 1)[0], 25 / 6)

    def test_wound_roll_bypass(self):
        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.NONE, wound_bypasses=4)[0], 5 + 4
        )

        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.SINGLE, wound_bypasses=4)[0],
            5.5 + 4,
        )

        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.ONES, wound_bypasses=4)[0],
            (5 + 5 / 6) + 4,
        )

        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.FULL, wound_bypasses=4)[0],
            7.5 + 4,
        )

    def test_wound_roll_dev_wounds(self):
        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.NONE, 0, 0, True)[0], 5 - 10 / 6
        )
        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.NONE, 0, 0, True)[1], 10 / 6
        )

        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.SINGLE, 0, 0, True)[0],
            5.5 - (10 / 6 + 1 / 6),
        )
        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.SINGLE, 0, 0, True)[1], (10 / 6 + 1 / 6)
        )

        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.ONES, 0, 0, True)[0],
            (5 + 5 / 6) - (10 / 6 + 5 / 18),
        )
        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.ONES, 0, 0, True)[1], (10 / 6 + 5 / 18)
        )

        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.FULL, 0, 0, True)[0],
            7.5 - (5 / 3 + 5 / 6),
        )
        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, Rerolls.FULL, 0, 0, True)[1], (5 / 3 + 5 / 6)
        )

    def test_wound_roll_modified_crit(self):
        self.assertAlmostEqual(caclculate_wound(10, 4, 4, crit_on=5)[0], 5)
        self.assertAlmostEqual(caclculate_wound(10, 2, 4, crit_on=4)[0], 5)
        self.assertAlmostEqual(
            caclculate_wound(10, 2, 4, crit_on=4, has_dev_wounds=True)[0], 0
        )
        self.assertAlmostEqual(
            caclculate_wound(10, 2, 4, crit_on=4, has_dev_wounds=True)[1], 5
        )

        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, crit_on=5, has_dev_wounds=True)[0], 5 / 3
        )
        self.assertAlmostEqual(
            caclculate_wound(10, 4, 4, crit_on=5, has_dev_wounds=True)[1], 10 / 3
        )


class TestSaveCalculations(unittest.TestCase):
    def test_unmodified_save(self):
        self.assertAlmostEqual(caclulate_not_saved(5, 0, 3), 5 / 3)
        self.assertAlmostEqual(caclulate_not_saved(7, 0, 2), 7 / 6)

    def test_straight_through(self):
        self.assertAlmostEqual(caclulate_not_saved(5, 0, 7), 5)

    def test_save_with_cover_no_AP(self):
        self.assertAlmostEqual(caclulate_not_saved(5, 0, 5, has_cover=True), 5 / 2)
        self.assertAlmostEqual(caclulate_not_saved(5, 0, 3, has_cover=True), 5 / 3)
        self.assertAlmostEqual(caclulate_not_saved(5, 0, 6, has_cover=True), 10 / 3)
        self.assertAlmostEqual(caclulate_not_saved(5, 0, 7, has_cover=True), 25 / 6)

    def test_save_with_cover_AP(self):
        self.assertAlmostEqual(caclulate_not_saved(5, 1, 5, has_cover=True), 10 / 3)
        self.assertAlmostEqual(caclulate_not_saved(5, 1, 3, has_cover=True), 5 / 3)
        self.assertAlmostEqual(caclulate_not_saved(5, 1, 2, has_cover=True), 5 / 6)
        self.assertAlmostEqual(caclulate_not_saved(5, 5, 3, has_cover=True), 5)
        self.assertAlmostEqual(caclulate_not_saved(5, 4, 3, has_cover=True), 25 / 6)

    def test_save_with_invuln(self):
        self.assertAlmostEqual(caclulate_not_saved(5, 0, 5, target_invuln=4), 5 / 2)
        self.assertAlmostEqual(caclulate_not_saved(5, 3, 2, target_invuln=4), 5 / 2)
        self.assertAlmostEqual(caclulate_not_saved(7, 0, 4, target_invuln=4), 7 / 2)

    def test_save_with_rerolls(self):
        self.assertAlmostEqual(
            caclulate_not_saved(5, 0, 5, rerolls=Rerolls.FULL), 20 / 9
        )
        self.assertAlmostEqual(
            caclulate_not_saved(5, 0, 5, rerolls=Rerolls.ONES), 55 / 18
        )
        self.assertAlmostEqual(caclulate_not_saved(5, 0, 5, rerolls=Rerolls.SINGLE), 3)

    def test_save_with_bypass(self):
        self.assertAlmostEqual(
            caclulate_not_saved(5, 0, 5, rerolls=Rerolls.NONE, save_bypasses=4),
            10 / 3 + 4,
        )
        self.assertAlmostEqual(
            caclulate_not_saved(5, 0, 5, rerolls=Rerolls.FULL, save_bypasses=4),
            20 / 9 + 4,
        )
        self.assertAlmostEqual(
            caclulate_not_saved(5, 0, 5, rerolls=Rerolls.ONES, save_bypasses=4),
            55 / 18 + 4,
        )
        self.assertAlmostEqual(
            caclulate_not_saved(5, 0, 5, rerolls=Rerolls.SINGLE, save_bypasses=4), 3 + 4
        )


class TestCalculateDMG(unittest.TestCase):
    def test_caculate_dmg_no_FNP(self):
        self.assertAlmostEqual(caclulate_dmg(2, 10, 2)[0], 20)
        self.assertAlmostEqual(caclulate_dmg(2, 10, 2)[1], 10)

        self.assertAlmostEqual(caclulate_dmg(2, 10, 3)[0], 20)
        self.assertAlmostEqual(caclulate_dmg(2, 10, 3)[1], 5)

        self.assertAlmostEqual(caclulate_dmg(5, 5, 1)[0], 25)
        self.assertAlmostEqual(caclulate_dmg(5, 5, 1)[1], 5)

        self.assertAlmostEqual(caclulate_dmg(5, 3, 6)[0], 15)
        self.assertAlmostEqual(caclulate_dmg(5, 3, 6)[1], 1 + 5 / 6)


class TestDiceAverage(unittest.TestCase):
    def test_dice_average(self):
        self.assertAlmostEqual(get_dice_average("2d6"), 7)
        self.assertAlmostEqual(get_dice_average("1d6"), 3.5)
        self.assertAlmostEqual(get_dice_average("1d3"), 2)
        self.assertAlmostEqual(get_dice_average("2d3"), 4)


if __name__ == "__main__":
    unittest.main()
