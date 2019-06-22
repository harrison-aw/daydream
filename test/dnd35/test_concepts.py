from pytest import raises

from dnd35.concepts import Conditional


class TestConditional:
    def test_repr_can_be_evaluated(self):
        c = Conditional(3, '+1 if predicate')
        assert repr(c) == "Conditional(3, '+1 if predicate')"

    def test_adding_conditionals(self):
        a = Conditional(3, '+1 if predicate')
        b = Conditional(1, '+4 if condition')
        sum_ = a + b
        assert (repr(sum_)
                == "Conditional(4, '+1 if predicate', '+4 if condition')")

    def test_adding_conditionals_and_integers(self):
        a = Conditional(3, '+1 if predicate')
        sum_ = a + 4
        assert repr(sum_) == "Conditional(7, '+1 if predicate')"

    def test_comparing_conditionals(self):
        a = Conditional(3, '+1 if predicate')
        b = Conditional(4, '+2 if condition')
        assert a < b

    def test_comparing_conditional_and_integers(self):
        a = Conditional(3, '+1 if predicate')
        assert a < 4

    def test_comparing_conditional_and_strings(self):
        a = Conditional(3, '+1 if predicate')
        with raises(TypeError):
            a < 'a'
