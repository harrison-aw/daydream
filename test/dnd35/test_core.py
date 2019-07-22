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

"""Tests for core functionality."""

import dnd35e.core as core


# pylint: disable=too-few-public-methods
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
