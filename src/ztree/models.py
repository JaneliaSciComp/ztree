from pydantic import BaseModel, Field
from typing import Mapping, Union, Literal

LeafType = Literal['array', 'group']

class Attrs(BaseModel):
    class Config:
        extra = "allow"

class Leaf(BaseModel):
    type: LeafType
    attrs: Attrs

class Array(Leaf):
    type: LeafType = Field('array', const=True)

class Group(Leaf):
    type: LeafType = Field('group', const=True)
    values: Mapping[str, Union["Group", Array]] = {}