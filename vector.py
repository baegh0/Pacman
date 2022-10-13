from math import sqrt, acos
from math import pi
PI_2 = pi / 2.0


class Vector:
    # def __init__(self, x=0, y=0, z=0, li=None):
    def __init__(self, *li):
        self.dims = len(li)
        self.data = []
        self.x = self.y = self.z = 0
        for el in li:
            self.data.append(float(el))
        self.x = self.data[0]
        if self.dims < 2:
            self.data.append(0.0)
            self.dims = 2
        if self.dims < 3:
            self.data.append(0.0)
            self.dims = 3
        self.y = self.data[1]
        self.z = self.data[2]

    @classmethod
    def create(cls, pta, ptb):       # create a Vector from pta to ptb
        x = float(ptb.x - pta.x)
        y = float(ptb.y - pta.y)
        z = float(ptb.z - pta.z)
        return cls(x, y, z)

    @classmethod
    def ihat(cls): return cls(1.0, 0.0, 0.0)

    @classmethod
    def jhat(cls): return cls(*[0.0, 1.0, 0.0])

    @classmethod
    def khat(cls): return cls(0.0, 0.0, 1.0)

    def __str__(self):
        s = [f'{int(i) if i == int(i) else round(i, 3)}' for i in self.data]
        s = ','.join(s)
        return '(' + s + ')'

    def idx(self, idx): return self.data[idx]

    def setidx(self, idx, val): self.data[idx] = val

    def __add__(self, o):
        if isinstance(o, float):
            return Vector(self.x + o, self.y + o, self.z + o)
        self.check_dims(self, o)
        return Vector(*[self.data[i] + o.data[i] for i in range(self.dims)])
        # return Vector(self.x + o.x, self.y + o.y, self.z + o.z)

    def __radd__(self, o): return self + o

    def __sub__(self, v): return self + -v

    def __rsub__(self, o): return -(o - self)

    def __mul__(self, k: float):
        return Vector(*[self.data[i] * k for i in range(self.dims)])
        # return Vector(k * self.x, k * self.y, k * self.z)

    def __rmul__(self, k: float): return self * k   # rmul means k * v (v is on the right)

    def __truediv__(self, k: float): return self * (1.0 / k)

    def __neg__(self):
        # return Vector(*[-self.data[i] for i in range(self.dims)])
        return Vector(-self.x, -self.y, -self.z)

    def __eq__(self, v):
        self.check_dims(self, v)
        for i in range(self.dims):
            if self.data[i] != v.data[i]: return False
        return True
        # return self.x == v.x and self.y == v.y and self.z == v.z

    def __ne__(self, v): return not (self == v)

    def magnitude(self): return sqrt(self.dot(self))

    def norm(self): return self.magnitude()

    def normalize(self):
        mag = self.magnitude()
        return (self * 1.0 / mag) if mag != 0.0 else Vector()

    def angle(self, v):
        mag = self.magnitude()
        vmag = v.magnitude()
        cos_phi = self.dot(v) / (mag * vmag)
        return acos(cos_phi)

    def dot(self, v):
        self.check_dims(self, v)
        dot_prod = 0
        for i in range(self.dims):
            dot_prod += self.data[i] * v.data[i]
        return dot_prod
        # return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        self.check_dims(self, v)
        dims = [2, 3]
        if self.dims not in dims: raise ValueError('cross product attempted with dimensions != 2 or 3')
        return Vector(self.y * v.z - self.z * v.y,
                      self.z * v.x - self.x * v.z,
                      self.x * v.y - self.y * v.x)
    @staticmethod
    def check_dims(u, v):
        if u.dims != v.dims:
            raise ValueError('dimensions of u and v not equal')

    @staticmethod
    def run_tests():
        a = Vector(1, 2, 3)
        b = Vector(4, 5, 6)
        c = Vector(5, 6, 2/7, 8/3)
        d = Vector(10, 11, 12, 13, 14, 15, 16)
        for i in range(a.dims):
            print(f'a[{i}] = {a.idx(i)}', end='  ')
            a.setidx(i, 10 * a.idx(i))
        print(f'a = {a}')
        print(f'b = {b}')
        print(f'c = {c}')
        print(f'd = {d}')
        assert(a + b == b + a)
        assert(--a == a)
        assert(a - b == -(b - a))
        assert(3.0 * a == a * 3.0)
        assert(a + 5.0 == 5.0 + a)
        assert(3.0 * a / 3.0 == a)

        i = Vector.ihat()
        j = Vector.jhat()
        k = Vector.khat()
        print(f'ihat is: {i}')
        print(f'jhat is: {j}')
        print(f'khat is: {k}')
        assert(i.dot(j) == j.dot(k) == k.dot(i) == 0)
        assert(i.magnitude() == 1.0)
        assert(j.magnitude() == 1.0)
        assert(k.magnitude() == 1.0)
        print('mags')

        assert(PI_2 == i.angle(j) and PI_2 == j.angle(k) and PI_2 == k.angle(i))
        assert(i.cross(j) == k and j.cross(k) == i and k.cross(i) == j)
        print('crosses')
        print("Vector.run_tests() passed!")
