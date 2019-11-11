#  MIT License
#
#  Copyright (c) 2019 Anthony Harrison
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#  Copyright (c) 2019 Anthony Harrison
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

"""Tests for core functionality."""

import dnd35e.core as core

# pylint: disable=no-self-use


class TestReference:
    """Test for reference subclasses"""

    def test_dereference(self):
        """Ensure that references can be dereferenced."""
        # pylint: disable=too-few-public-methods
        class MyTest:
            """Mock class to use as target for reference."""

            def __init__(self, val):
                self.value = val

        test = MyTest(5)

        value = core.Reference('value', MyTest)

        assert value.dereference(test) == 5

    def test_dereference_recursively(self):
        """Ensure that nested references are properly dereferenced."""
        # pylint: disable=too-few-public-methods
        class MyTest:
            """Mock class to use as target for reference."""
            def __init__(self, val):
                self.value = val
        test = MyTest(5)

        value = core.Reference('x', 'Unknown',
                               core.Reference('value', MyTest))

        assert value.dereference(test) == core.Reference('x', 'Unknown', 5)

    def test_repr_evaluates(self):
        """Ensure that the repr can be evaluated."""
        reference = core.Reference('x', 'Test', 5)

        # pylint: disable=eval-used
        evaluated = eval(repr(reference), {'Reference': core.Reference})

        assert reference == evaluated

    def test_adding_to_reference(self):
        """Ensure that a reference is addable."""
        # pylint: disable=too-few-public-methods
        class MyTest:
            """Mock class to use as target for reference."""
            def __init__(self, val):
                self.value = val

        test = MyTest(5)

        reference = core.Reference('value', 'MyTest')
        reference += 8

        assert reference.dereference(test) == 13

    def test_name(self):
        """Ensure that the name of referenced attribute is available."""
        reference = core.Reference('x', 'Test', 5)

        assert reference.name == 'x'


class TestAggregator:
    """Test for aggregator subclasses."""

    def test_aggregates_from_children(self):
        """Ensure that attributes with the same name are all combined."""
        # pylint: disable=too-few-public-methods

        class Leaf:
            """A simple object with a `test` attribute."""

            def __init__(self, test=1):
                self.test = test

        class Branch(core.Aggregator):
            """An object with a `test` attribute that needs aggregated."""

            def __init__(self, test=3):
                super().__init__()
                self.test = test
                self.leaf = Leaf()

        class Root(core.Aggregator):
            """An object with a `test` attribute that needs aggregated."""

            def __init__(self, test=2):
                super().__init__()
                self._test = test
                self.leaf = Leaf()
                self.branch = Branch()

            @property
            def test(self):
                """Return the private `test` attribute."""
                return self._test

        instance = Root()
        assert instance.test == 7

    def test_aggregator_dereferences(self):
        """Ensure that aggregators handle references."""
        # pylint: disable=too-few-public-methods

        class Leaf:
            """A simple object with a reference."""

            def __init__(self):
                self.value = core.Reference('other', 'Root')

        class Root(core.Aggregator):
            """A simple aggregator."""

            def __init__(self, other):
                super().__init__()
                self.leaf = Leaf()
                self.other = other

        root = Root(5)

        assert root.value == 5

    def test_aggregator_dereferences_recursively(self):
        """Ensure that a multiple references to target are handled."""
        # pylint: disable=too-few-public-methods

        class Leaf:
            """A simple object with a reference."""

            def __init__(self):
                self.value = core.Reference('other', 'Root',
                                            core.Reference('another', 'Root'))

        class Root(core.Aggregator):
            """A simple aggregator."""

            def __init__(self, other, another):
                super().__init__()
                self.leaf = Leaf()
                self.other = other
                self.another = another

        root = Root(5, 3)

        assert root.value == 8

    def test_aggregator_always_dereferences_nested_references(self):
        """Ensure that a nested reference is dereferenced by aggregator."""
        # pylint: disable=too-few-public-methods

        class Leaf:
            """A simple object with a reference"""

            def __init__(self):
                self.value = core.Reference('other', 'Root',
                                            core.Reference('another', 'Branch'))

        class Branch(core.Aggregator):
            """An object with a `value` attribute that needs aggregated."""

            def __init__(self, value=3, another=4):
                super().__init__()
                self.value = value
                self.another = another
                self.leaf = Leaf()

        class Root(core.Aggregator):
            """An object with a `value` attribute that needs aggregated."""

            def __init__(self, value=2):
                super().__init__()
                self.other = 2
                self._value = value
                self.branch = Branch()

            @property
            def value(self):
                """Return the private `value` attribute."""
                return self._value

        instance = Root()
        assert instance.value == 11
