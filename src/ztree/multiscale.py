from typing import List, Mapping
from ztree.models import Group, Array, Attrs

from pydantic import BaseModel

class SpatialTransform(BaseModel):
    axes: List[str]
    scale: List[float]
    translate: List[float]


class PixelResolution(BaseModel):
    dimensions: List[float]
    unit: str


class MultiscaleArrayAttrs(Attrs):
    downsamplingFactors: List[str]
    transform: SpatialTransform


class MultiscaleGroupAttrs(Attrs):
    transform: SpatialTransform
    pixelResolution: PixelResolution
    scales: List[List[str]]


class MultiscaleArray(Array):
    attrs: MultiscaleArrayAttrs


class MultiscaleGroup(Group):
    attrs: MultiscaleGroupAttrs
    values: Mapping[str, MultiscaleArray]
