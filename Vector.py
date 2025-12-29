# Vector classes for working with coordinates. These are implemented as immutable dataclasses
# so that they can be hashed (stored in sets, etc.).
from dataclasses import dataclass
from typing_extensions import Self
from math import sqrt

# Two-dimensional vector
@dataclass(frozen = True)
class Vector:
	x: int
	y: int

	def __add__(self, v: Self) -> Self:
		return type(self)(self.x + v.x, self.y + v.y)

	def __sub__(self, v: Self) -> Self:
		return type(self)(self.x - v.x, self.y - v.y)

	def __neg__(self) -> Self:
		return type(self)(-self.x, -self.y)

	def __mul__(self, c: int) -> Self:
		return type(self)(c * self.x, c * self.y)

	def __rmul__(self, c: int) -> Self:
		return self * c
	
	# Manhattan distance
	def __len__(self) -> int:
		return abs(self.x) + abs(self.y)
	
	# Euclidean distance
	def __abs__(self) -> float:
		return sqrt(self.x**2 + self.y**2)

	def __str__(self) -> str:
		return f"({self.x},{self.y})"

	def in_range(self, xmin: int, xmax: int, ymin: int, ymax: int) -> bool:
		return self.x >= xmin and self.x <= xmax and self.y >= ymin and self.y <= ymax

	def in_range_sq(self, size):
		return self.in_range(0, size - 1, 0, size - 1)

	def rotate_cw(self) -> Self:
		return type(self)(self.y, -self.x)

	def rotate_ccw(self) -> Self:
		return type(self)(-self.y, self.x)
	
	# Vector dot product
	def dot(self, v: Self) -> int:
		return self.x*v.x + self.y*v.y
	
	# Vector cross product (magnitude only)
	def cross(self, v: Self) -> int:
		return self.x*v.y - v.x*self.y

# Three-dimensional vector
@dataclass(frozen = True)
class Vector3:
	x: int
	y: int
	z: int

	def __add__(self, v: Self) -> Self:
		return type(self)(self.x + v.x, self.y + v.y, self.z + v.z)

	def __sub__(self, v: Self) -> Self:
		return type(self)(self.x - v.x, self.y - v.y, self.z - v.z)

	def __neg__(self) -> Self:
		return type(self)(-self.x, -self.y, -self.z)

	def __mul__(self, c: int) -> Self:
		return type(self)(c * self.x, c * self.y, c * self.z)

	def __rmul__(self, c: int) -> Self:
		return self * c
	
	# Manhattan distance
	def __len__(self) -> int:
		return abs(self.x) + abs(self.y) + abs(self.z)
	
	# Euclidean distance
	def __abs__(self) -> float:
		return sqrt(self.x**2 + self.y**2 + self.z**2)

	def __str__(self) -> str:
		return f"({self.x},{self.y},{self.z})"

	def in_range(self, xmin: int, xmax: int, ymin: int, ymax: int, zmin, zmax) -> bool:
		return self.x >= xmin and self.x <= xmax and self.y >= ymin and self.y <= ymax and self.z >= zmin and self.z <= zmax

	def in_range_sq(self, size):
		return self.in_range(0, size - 1, 0, size - 1, 0, size - 1)

	# Vector dot product
	def dot(self, v: Self) -> int:
		return self.x*v.x + self.y*v.y + self.z*v.z
	
	# Vector cross product
	def cross(self, v: Self) -> Self:
		return type(self)(self.y*v.z - self.z*v.y, self.z*v.x - self.x*v.z, self.x*v.y - v.x*self.y)


# Helpful constants
up = Vector(0, 1)
down = Vector(0, -1)
left = Vector(-1, 0)
right = Vector(1, 0)
upleft = Vector(-1, 1)
upright = Vector(1, 1)
downleft = Vector(-1, -1)
downright = Vector(1, -1)
null = Vector(0, 0)
