class ValueRange:
    def __init__(self):
        self._lower = None
        self._upper = None

    @classmethod
    def from_pair(cls, value1, value2):
        r = cls()
        r.extend(value1)
        r.extend(value2)
        return r

    def is_valid(self):
        return self._lower is not None

    def lower(self):
        return self._lower

    def upper(self):
        return self._upper

    def diameter(self):
        if self.is_valid():
            return self.upper() - self.lower()
        return 0

    def contains(self, value):
        return self.is_valid() and (self.lower() <= value <= self.upper())

    def extend(self, value):
        if not self.is_valid():
            self._lower = value
            self._upper = value
        else:
            self._lower = min(self._lower, value)
            self._upper = max(self._upper, value)


class XY:
    """
    Represent x,y coords with properly overloaded operations.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __mul__(self, factor):
        if isinstance(factor, XY):
            return XY(self.x * factor.x, self.y * factor.y)
        return XY(self.x * factor, self.y * factor)

    def __rmul__(self, factor):
        if isinstance(factor, XY):
            return XY(self.x * factor.x, self.y * factor.y)
        return XY(self.x * factor, self.y * factor)

    def __add__(self, other):
        return XY(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return XY(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"XY: {self.x}/{self.y}"

    def tuple(self):
        return self.x, self.y
