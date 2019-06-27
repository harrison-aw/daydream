import dnd35.concepts as concepts


class TestDice:
    def test_create_d6(self):
        dice = concepts.Dice(6)
        assert str(dice) == 'd6'

    def test_create_4d8(self):
        dice = concepts.Dice(8, 4)
        assert str(dice) == '4d8'

    def test_create_larger_dice_pool(self):
        dice = concepts.Dice(3, None, [(6, 6), (8, 10)])
        assert str(dice) == 'd3 + 6d6 + 10d8'

    def test_repr_executes(self):
        dice = concepts.Dice(3, None, [(6, 6)])
        repr_ = repr(dice)
        new_dice = eval(repr_, {'Dice': concepts.Dice})
        assert dice == new_dice

    def test_hash_matches(self):
        dice1 = concepts.Dice(3, None, [(6, 6)])
        dice2 = concepts.Dice(3, None, [(6, 6)])
        assert hash(dice1) == hash(dice2)

    def test_add_dice_pools(self):
        dice1 = concepts.Dice(3, None, [(6, 6)])
        dice2 = concepts.Dice(3, None, [(6, 6)])
        desired = concepts.Dice(pool=[(3, None), (3, None), (6, 12)])
        assert dice1 + dice2 == desired

    def test_in_place_addition(self):
        dice1 = concepts.Dice(3, None, [(6, 6)])
        dice2 = concepts.Dice(3, None, [(6, 6)])
        dice1 += dice2

        desired = concepts.Dice(pool=[(3, None), (3, None), (6, 12)])
        assert dice1 == desired

    def test_easy_average(self):
        dice = concepts.Dice(6)
        assert dice.average == 3.5

    def test_hard_average(self):
        dice = concepts.Dice(3, None, [(6, 6), (8, 10)])
        assert dice.average == 68.0


class TestBonus:
    def test_handles_simple_init(self):
        bonus = concepts.Bonus(unnamed=10)
        assert bonus == 10

    def test_handles_conditional(self):
        bonus = concepts.Bonus('+1 racial bonus on attack rolls against orcs and goblinoids.')
        assert bonus == 0
        assert str(bonus) == '+1 racial bonus on attack rolls against orcs and goblinoids.'

    def test_repr_is_readable(self):
        bonus = concepts.Bonus(unnamed=10)
        assert repr(bonus) == 'Bonus(unnamed=10)'

    def test_repr_is_evaluable(self):
        bonus = concepts.Bonus('test conditional', racial=10)
        repr_ = repr(bonus)
        bonus2 = eval(repr_, {'Bonus': concepts.Bonus})
        assert bonus == bonus2

    def test_hash_satisfies_equality(self):
        bonus1 = concepts.Bonus('test', unnamed=2)
        bonus2 = concepts.Bonus('test', unnamed=2)
        assert bonus1 == bonus2
        assert hash(bonus1) == hash(bonus2)

    def test_undefined_typed_bonuses_return_zero(self):
        bonus = concepts.Bonus(dodge=3)
        assert bonus['wrong'] == 0

    def test_adding_bonuses(self):
        bonus1 = concepts.Bonus('+1 test', '+1 too', unnamed=3, dodge=2, racial=3)
        bonus2 = concepts.Bonus('+1 test', unnamed=1, dodge=2, racial=2)

        bonus_sum = bonus1 + bonus2

        desired = concepts.Bonus('+1 test', '+1 too', unnamed=4, dodge=4, racial=3)
        assert bonus_sum == desired

    def test_bonus_string(self):
        bonus = concepts.Bonus(dodge=3)
        assert str(bonus) == '+3'

    def test_conditional_string(self):
        bonus = concepts.Bonus('+1 if blind', racial=1)
        assert str(bonus) == '+1\n+1 if blind'

    def test_iteration(self):
        bonus = concepts.Bonus('+1 test', '+1 too', unnamed=3, dodge=2, racial=3)
        assert set(bonus) == {'unnamed', 'dodge', 'racial'}
