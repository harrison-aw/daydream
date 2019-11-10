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


class TestReference:
    """Test for reference subclasses"""

    def test_dereference(self):
        class MyTest:
            def __init__(self, x):
                self.x = x
        test = MyTest(5)

        value = core.Reference('x', MyTest)

        assert value.dereference(test) == 5

    def test_dereference_recursively(self):
        class MyTest:
            def __init__(self, x):
                self.x = x
        test = MyTest(5)

        value = core.Reference('y', 'Unknown',
                               core.Reference('x', MyTest))

        assert value.dereference(test) == core.Reference('y', 'Unknown', 5)

    def test_repr_evaluates(self):
        reference = core.Reference('x', 'Test', 5)

        evaluated = eval(repr(reference), {'Reference': core.Reference})

        assert reference == evaluated

    def test_adding_to_reference(self):
        class MyTest:
            def __init__(self, x):
                self.x = x

        test = MyTest(5)

        reference = core.Reference('x', 'MyTest')
        reference += 8

        assert reference.dereference(test) == 13


class TestAggregator:
    """Test for aggregator subclasses."""

    def test_aggregates_from_children(self):
        """Ensure that attributes with the same name are all combined."""
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
        class Leaf:
            def __init__(self):
                self.x = core.Reference('y', 'Root')

        class Root(core.Aggregator):
            def __init__(self, y):
                super().__init__()
                self.leaf = Leaf()
                self.y = y

        root = Root(5)

        assert root.x == 5

    def test_aggregator_dereferences_recursively(self):
        class Leaf:
            def __init__(self):
                self.x = core.Reference('y', 'Root',
                                        core.Reference('z', 'Root'))

        class Root(core.Aggregator):
            def __init__(self, y, z):
                super().__init__()
                self.leaf = Leaf()
                self.y = y
                self.z = z

        root = Root(5, 3)

        assert root.x == 8

    def test_aggregator_always_dereferences_nested_references(self):
        class Leaf:
            """A simple object with a `test` attribute."""

            def __init__(self):
                self.test = core.Reference('x', 'Root',
                                           core.Reference('other', 'Branch'))

        class Branch(core.Aggregator):
            """An object with a `test` attribute that needs aggregated."""

            def __init__(self, test=3, other=4):
                super().__init__()
                self.test = test
                self.other = other
                self.leaf = Leaf()

        class Root(core.Aggregator):
            """An object with a `test` attribute that needs aggregated."""

            def __init__(self, test=2):
                super().__init__()
                self.x = 2
                self._test = test
                self.branch = Branch()

            @property
            def test(self):
                """Return the private `test` attribute."""
                return self._test

        instance = Root()
        assert instance.test == 11
