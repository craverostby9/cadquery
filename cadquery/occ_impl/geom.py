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
        if mag < 1e-10:
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
        return Vector(self._wrapped.Multiplied(1.0 / divisor))

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y, -self.z)

    def __repr__(self) -> str:
        return f"Vector({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return (
            abs(self.x - other.x) < 1e-9
            and abs(self.y - other.y) < 1e-9
            and abs(self.z - other.z) < 1e-9
        )

    def toPnt(self) -> gp_Pnt:  # noqa: N802
        """Convert to an OCC gp_Pnt."""
        return gp_Pnt(self.x, self.y, self.z)

    def toDir(self) -> gp_Dir:  # noqa: N802
        """Convert to an OCC gp_Dir (unit direction)."""
        n = self.normalized()
        return gp_Dir(n.x, n.y, n.z)

    def getAngle(self, other: "Vector") -> float:  # noqa: N802
        """Return the angle in degrees between this and another vector."""
        return degrees(self._wrapped.Angle(other._wrapped))

    def projectToPlane(self, plane: "Plane") -> "Vector":  # noqa: N802
        """Project this vector onto the given plane."""
        base = plane.origin
        normal = plane.zDir
        # Component along normal
        along_normal = self.dot(normal)
        return self - (normal * along_normal)


class Plane:
    """An infinite plane defined by an origin point and normal direction.

    Used extensively in CadQuery for workplane operations.
    """

    _x_dir: Vector
    _y_dir: Vector
    _z_dir: Vector
    origin: Vector

    def __init__(
        self,
        origin: Union[Vector, Tuple],
        xDir: Optional[Union[Vector, Tuple]] = None,  # noqa: N803
        normal: Union[Vector, Tuple] = (0, 0, 1),
    ):
        self.origin = Vector(origin) if not isinstance(origin, Vector) else origin
        self._z_dir = (
            Vector(normal) if not isinstance(normal, Vector) else normal
        ).normalized()

        if xDir is None:
            # Auto-compute x direction perpendicular to normal
            if abs(self._z_dir.x) < 0.9:
                ref = Vector(1, 0, 0)
            else:
                ref = Vector(0, 1, 0)
            self._x_dir = ref.cross(self._z_dir).normalized()
        else:
            self._x_dir = (
                Vector(xDir) if not isinstance(xDir, Vector) else xDir
            ).normalized()

        self._y_dir = self._z_dir.cross(self._x_dir).normalized()

    @property
    def xDir(self) -> Vector:  # noqa: N802
        return self._x_dir

    @property
    def yDir(self) -> Vector:  # noqa: N802
        return self._y_dir

    @property
    def zDir(self) -> Vector:  # noqa: N802
        return self._z_dir

    def __repr__(self) -> str:
        return (
            f"Plane(origin={self.origin}, "
            f"xDir={self._x_dir}, "
            f"normal={self._z_dir})"
        )
