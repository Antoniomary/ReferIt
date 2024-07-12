#!/usr/bin/python3


class Square:
    def __init__(self, side):
        if side <= 0:
            raise ValueError("size can't be <= 0")
        self._side = side

    @property
    def sth(self):
        return self._side

    @sth.setter
    def sth(self, val):
        if val <= 0:
            raise ValueError("size can't be <= 0")
        self._side = val

    def __str__(self):
        return 'Square [{}]'.format(self.sth)

    def __repr__(self):
        return 'Square [{}]'.format(self.sth)


class test:
    n = 7


print(test.n)
