# pylint: disable=W,C,R

import dnd35.concepts as concepts


class TestDice:
    def test_create_d6(self):
        dice = concepts.Dice(6)
        assert str(dice) == 'd6'

    def test_create_4d8(self):
        dice = concepts.Dice(8, 4)
        assert str(dice) == '4d8'

    def test_hash(self):
        dice1 = concepts.Dice(8, 4, pool=[(6, 10)])
        dice2 = concepts.Dice(pool=[(6, 10), (8, 4)])
        assert dice1 == dice2
        assert hash(dice1) == hash(dice2)

    def test_create_larger_dice_pool(self):
        dice = concepts.Dice(3, None, [(6, 6), (8, 10)])
        assert str(dice) == 'd3 + 6d6 + 10d8'

    def test_repr_executes(self):
        dice = concepts.Dice(3, None, [(6, 6)])
        new_dice = eval(repr(dice), {'Dice': concepts.Dice})
        assert dice == new_dice

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


class TestModifier:
    def test_handles_simple_init(self):
        modifier = concepts.Modifier(unnamed=10)
        assert modifier == 10

    def test_handles_conditional(self):
        modifier = concepts.Modifier('+1 racial bonus on attack rolls '
                                     'against orcs and goblinoids.')
        assert modifier == 0
        assert str(modifier) == '+1 racial bonus on attack rolls ' \
                                'against orcs and goblinoids.'

    def test_repr_is_readable(self):
        modifier = concepts.Modifier(unnamed=10)
        assert repr(modifier) == 'Modifier(unnamed=10)'

    def test_repr_is_evaluable(self):
        modifier = concepts.Modifier('test conditional', racial=10)
        repr_ = repr(modifier)
        modifier_evaluated = eval(repr_, {'Modifier': concepts.Modifier})
        assert modifier == modifier_evaluated

    def test_undefined_typed_bonuses_return_zero(self):
        modifier = concepts.Modifier(dodge=3)
        assert modifier['wrong'] == 0

    def test_adding_bonuses(self):
        modifier1 = concepts.Modifier('+1 test', '+1 too',
                                      unnamed=3, dodge=2, racial=3)
        modifier2 = concepts.Modifier('+1 test',
                                      unnamed=1, dodge=2, racial=2)

        sum_ = modifier1 + modifier2

        desired = concepts.Modifier('+1 test', '+1 too',
                                    unnamed=4, dodge=4, racial=3)
        assert sum_ == desired

    def test_bonus_string(self):
        modifier = concepts.Modifier(dodge=3)
        assert str(modifier) == '+3'

    def test_conditional_string(self):
        modifier = concepts.Modifier('+1 if blind', racial=1)
        assert str(modifier) == '+1\n+1 if blind'

    def test_iteration(self):
        modifier = concepts.Modifier('+1 test', '+1 too',
                                     unnamed=3, dodge=2, racial=3)
        assert set(modifier) == {'unnamed', 'dodge', 'racial'}


class TestProgression:
    def test_create_save(self):
        good_save = concepts.Progression('save', 2, 3, 3, 4, 4)
        assert good_save[2] == concepts.Modifier(save=3)

    def test_repr_evaluates(self):
        good_save = concepts.Progression('save', 2, 3, 3, 4, 4)
        good_save_copy = eval(repr(good_save),
                              {'Progression': concepts.Progression})
        assert good_save == good_save_copy


class TestSize:
    def test_repr_is_evaluable(self):
        small = concepts.Size(-1)
        assert eval(repr(small), {'Size': concepts.Size}) == small

    def test_small_attack_bonus(self):
        small = concepts.Size(-1)
        assert small.attack_bonus == 1

    def test_small_armor_class(self):
        small = concepts.Size(-1)
        assert small.armor_class == 1

    def test_small_grapple(self):
        small = concepts.Size(-1)
        assert small.grapple == -4

    def test_small_hide(self):
        small = concepts.Size(-1)
        assert small.hide == 4


class TestAbilityScore:
    def test_positive_modifier(self):
        score = concepts.AbilityScore(17)
        assert score.modifier == 3

    def test_negative_modifier(self):
        score = concepts.AbilityScore(7)
        assert score.modifier == -2


class TestAbilityType:
    def test_repr_evaluates(self):
        ability = concepts.AbilityType('Supernatural', 'Su')
        ability_copy = eval(repr(ability),
                            {'AbilityType': concepts.AbilityType})
        assert ability == ability_copy

    def test_str(self):
        ability = concepts.AbilityType('Supernatural', 'Su')
        assert str(ability) == 'Supernatural (Su)'


class TestAbility:
    def test_static_ability(self):
        stonecunning = concepts.Ability(
            'Stonecunning',
            search=concepts.Modifier('+2 racial bonus to notice '
                                     'unusual stonework')
        )
        assert str(stonecunning.search) == '+2 racial bonus to notice' \
                                           ' unusual stonework'

    def test_sneak_attack(self):
        sneak_attack = concepts.Ability(
            'Sneak attack +1d6',
            damage=concepts.Dice(6, 1)
        )
        assert str(sneak_attack) == 'Sneak attack +1d6'

    def test_delete_features(self):
        ability = concepts.Ability('Test', test=10)

        assert ability.test == 10
        del ability.test
        assert ability == concepts.Ability('Test')
