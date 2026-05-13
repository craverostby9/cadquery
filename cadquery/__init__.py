"""CadQuery - A parametric 3D CAD scripting framework built on top of OCCT.

CadQuery is a Python library that provides an intuitive, Pythonic interface
for building 3D CAD models using the OpenCASCADE Technology (OCCT) geometry
kernel via the pythonOCC bindings.

Basic usage::

    import cadquery as cq

    result = cq.Workplane("XY").box(10, 10, 10)

Unit constants are provided for convenience. All values are in millimeters::

    import cadquery as cq

    result = cq.Workplane("XY").box(2 * cq.IN, 1 * cq.IN, 0.5 * cq.IN)
"""

from .cq import Workplane, CQContext
from .occ_impl.shapes import (
    Shape,
    Solid,
    Shell,
    Face,
    Wire,
    Edge,
    Vertex,
    Compound,
)
from .occ_impl.geom import Vector, Matrix, Plane, Location
from .assembly import Assembly, ConstraintSpec
from .sketch import Sketch
from .selectors import (
    NearestToPointSelector,
    ParallelDirSelector,
    DirectionSelector,
    PerpendicularDirSelector,
    TypeSelector,
    DirectionMinMaxSelector,
    RadiusNthSelector,
    CenterNthSelector,
    LengthNthSelector,
    AreaNthSelector,
    StringSyntaxSelector,
)
from .exporters import (
    exportShape,
    importShape,
    ExportTypes,
    ImportTypes,
)

__version__ = "2.4.0"
__author__ = "CadQuery Contributors"
__license__ = "Apache License 2.0"

# Expose commonly used constants at the package level
# Using metric as primary unit system (1 unit = 1 mm)
MM = 1.0
CM = 10.0
M = 1000.0
IN = 25.4
FT = 304.8
# Additional unit I find useful for PCB/electronics work
MIL = 0.0254  # 1 mil (thou) = 0.0254 mm
UM = 0.001    # 1 micrometer = 0.001 mm, handy for tight tolerances

# Aliases I keep forgetting exist -- personal shortcuts
INCH = IN   # more readable alias for IN
FOOT = FT   # more readable alias for FT

__all__ = [
    # Core workplane
    "Workplane",
    "CQContext",
    # Shape types
    "Shape",
    "Solid",
    "Shell",
    "Face",
    "Wire",
    "Edge",
    "Vertex",
    "Compound",
    # Geometry primitives
    "Vector",
    "Matrix",
    "Plane",
    "Location",
    # Assembly
    "Assembly",
    "ConstraintSpec",
    # Sketch
    "Sketch",
    # Selectors
    "NearestToPointSelector",
    "ParallelDirSelector",
    "DirectionSelector",
    "PerpendicularDirSelector",
    "TypeSelector",
    "DirectionMinMaxSelector",
    "RadiusNthSelector",
    "CenterNthSelector",
    "LengthNthSelector",
    "AreaNthSelector",
    "StringSyntaxSelector",
    # Exporters / Importers
    "exportShape",
    "importShape",
    "ExportTypes",
    "ImportTypes",
    # Unit constants
    "MM",
    "CM",
    "M",
    "IN",
    "FT",
    "MIL",
    "UM",
    "INCH",
    "FOOT",
]
