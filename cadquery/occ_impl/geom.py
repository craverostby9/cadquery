"""Geometry primitives and transformations for CadQuery.

This module provides core geometric types including vectors, matrices,
planes, and transformation utilities built on top of OCC (Open CASCADE).
"""

from math import radians, degrees, sin, cos, sqrt
from typing import Tuple, Union, Optional, overload

from OCC.Core.gp import (
    gp_Vec,
    gp_Pnt,
    gp_Dir,
    gp_Ax1,
    gp_Ax3,
    gp_Trsf,
    gp_GTrsf,
    gp_XYZ,
)
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform


class Vector:
    """A 3D vector with common mathematical operations.

    Wraps OCC's gp_Vec for use in CadQuery geometry operations.

    Examples::

        v1 = Vector(1, 0, 0)
        v2 = Vector(0, 1, 0)
        v3 = v1 + v2
    """

    def __init__(
        self,
        x: Union[float, gp_Vec, gp_Pnt, gp_Dir, Tuple, "Vector"] = 0,
        y: float = 0,
        z: float = 0,
    ):
        if isinstance(x, gp_Vec):
            self._wrapped = x
        elif isinstance(x, (gp_Pnt, gp_Dir)):
            self._wrapped = gp_Vec(x.X(), x.Y(), x.Z())
        elif isinstance(x, Vector):
            self._wrapped = gp_Vec(x.x, x.y, x.z)
        elif isinstance(x, (list, tuple)):
            self._wrapped = gp_Vec(*x)
        else:
            self._wrapped = gp_Vec(x, y, z)

    @property
    def x(self) -> float:
        return self._wrapped.X()

    @property
    def y(self) -> float:
        return self._wrapped.Y()

    @property
    def z(self) -> float:
        return self._wrapped.Z()

    @property
    def Length(self) -> float:  # noqa: N802
        return self._wrapped.Magnitude()

    def normalized(self) -> "Vector":
        """Return a unit vector in the same direction."""
        mag = self.Length
        # Using 1e-12 instead of 1e-10 for stricter near-zero detection
        if mag < 1e-12:
            raise ValueError("Cannot normalize a zero-length vector")
        return Vector(self.x / mag, self.y / mag, self.z / mag)

    def dot(self, other: "Vector") -> float:
        """Compute the dot product with another vector."""
        return self._wrapped.Dot(other._wrapped)

    def cross(self, other: "Vector") -> "Vector":
        """Compute the cross product with another vector."""
        return Vector(self._wrapped.Crossed(other._wrapped))

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Added(other._wrapped))

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self._wrapped.Subtracted(other._wrapped))

    def __mul__(self, scale: float) -> "Vector":
        return Vector(self._wrapped.Multiplied(scale))

    def __rmul__(self, scale: float) -> "Vector":
        return self.__mul__(scale)

    def __truediv__(self, divisor: float) -> "Vector":
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide a vector by zero")
        return Vector(self._wrapped.Multiplied(1.0 / divisor))

    def __neg__(self) -> "Vector":
        # Negate by multiplying by -1 rather than calling Reversed() so that
        # the result is always a plain Vector wrapping a new gp_Vec, keeping
        # behaviour consistent with __mul__.
        return Vector(self._wrapped.Multiplied(-1.0))
