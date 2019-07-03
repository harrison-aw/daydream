# pylint: disable=W,C,R

import dnd35.core


class TestAggregator:
    def test_aggregates_from_children(self):
        class Leaf:
            def __init__(self, x=1):
                self.x = x

        class Branch(dnd35.core.Aggregator):
            def __init__(self, x=3):
                super().__init__()
                self.x = x
                self.leaf = Leaf()

        class Root(dnd35.core.Aggregator):
            def __init__(self, x=2):
                super().__init__()
                self._x = x
                self.leaf = Leaf()
                self.branch = Branch()

            @property
            def x(self):
                return self._x

        instance = Root()
        assert instance.x == 7
