from dnd35.core import Aggregator


class TestAggregator:
    def test_aggregates_from_children(self):
        class Leaf:
            def __init__(self, x=1):
                self.x = x

        class Branch(Aggregator):
            def __init__(self, x=3):
                super().__init__()
                self.x = x
                self.leaf = Leaf()

        class Root(Aggregator):
            def __init__(self, x=2):
                super().__init__()
                self._x = x
                self.leaf = Leaf()
                self.other_leaves = [Leaf(i) for i in range(10)]
                self.branch = Branch()

            @property
            def x(self):
                return self._x

        instance = Root()
        assert instance.x == 52
