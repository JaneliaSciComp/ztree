from pydantic import BaseModel, Field
from typing import Mapping, Union, Literal, Tuple

NodeType = Literal["array", "group"]


class Attrs(BaseModel):
    class Config:
        extra = "allow"


class Node(BaseModel):
    type: NodeType
    name: str
    attrs: Attrs


class Array(Node):
    type: NodeType = Field("array", const=True)


class Group(Node):
    type: NodeType = Field("group", const=True)
    values: Mapping[str, Union["Group", Array]] = {}
