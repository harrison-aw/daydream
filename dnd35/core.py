"""Low-level, core functionality for DayDream3.5"""

from typing import Any, Set, Optional
from operator import add
from functools import reduce, total_ordering


class Aggregator:
    """Aggregate values from all objects attached to an instance."""

    def __init_subclass__(cls, ignore: Optional[Set] = None) -> None:
        """Setup attributes to access directly."""
        super().__init_subclass__()
        if ignore is None:
            ignore = set()
        cls._ignore = ignore

    def __init__(self) -> None:
        """Initialize attribute name tracker."""
        super().__setattr__('_instance_names', [])

    def __setattr__(self, name: str, value: Any) -> None:
        """Track any attributes that are added to an instance."""
        get = super().__getattribute__
        instance_names = get('_instance_names')
        ignore = get('_ignore')
        if name not in ignore and name not in instance_names:
            instance_names.append(name)
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        """Aggregate value from each attribute if name is not private."""
        get = super().__getattribute__

        # ignore private names and explicitly ignored names
        ignore = get('_ignore')
        if name.startswith('_') or name in ignore:
            return get(name)

        aggregation = []

        # aggregate the value on the actual instance
        try:
            aggregation.append(get(name))
        except AttributeError:
            pass

        # aggregate the values among all attributes
        for object_ in (get(n) for n in get('_instance_names') if n != name):
            try:
                subaggregation = (getattr(o, name, None) for o in object_)
                aggregation.extend(v for v in subaggregation if v is not None)
            except TypeError:
                try:
                    aggregation.append(getattr(object_, name))
                except AttributeError:
                    pass

        return reduce(add, aggregation)

    def __delattr__(self, name: str):
        """Remove deleted attributes from tracker."""
        try:
            super().__delattr__(name)
        except AttributeError:
            raise

        _instance_names = super().__getattribute__('_instance_names')
        i = _instance_names.index(name)
        del _instance_names[i]


@total_ordering
class Value:
    """Implements functionality comparing generalized numeric types."""

    def __init_subclass__(cls, value_name='value'):
        """Register the value to use for numerical operations."""
        super().__init_subclass__()
        cls._value_name = value_name

    def __eq__(self, other: Any) -> bool:
        value_name = self._value_name
        value = getattr(self, value_name)
        try:
            return value == getattr(other, value_name)
        except AttributeError:
            return NotImplemented

    def __lt__(self, other: Any) -> bool:
        value_name = self._value_name
        value = getattr(self, value_name)
        try:
            return value < getattr(other, value_name)
        except AttributeError:
            return value < other
