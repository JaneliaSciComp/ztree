import json
from rich import print_json
from ztree.models import Group, Array, Attrs, Union, Mapping
from ztree.parser import visit
import zarr
from pydantic import StrictStr, StrictInt, ValidationError

class MyArrayAttrs(Attrs):
    bar: StrictInt

class MyGroupAttrs(Attrs):
    foo: StrictStr

class MyArray(Array):
    attrs: MyArrayAttrs

class MyGroup(Group):
    attrs: MyGroupAttrs
    values: Mapping[str, Union["Group", MyArray]]


zgroup = zarr.open(zarr.MemoryStore())
zgroup.attrs['foo'] = 100 # this will fail validation

zgroup.create_dataset(name='my_array', shape=(10,))
zgroup['my_array'].attrs['bar'] = 3.14159 # this will fail validation

if __name__ == '__main__':
    name, tree = visit(zgroup)
    err = json.dumps(dict())
    try:
        validated = MyGroup(**tree)
    except ValidationError as ve:
        err = ve.json()
    print('Tree:')
    print_json(json.dumps({name: tree}))
    print('Error:')
    print_json(err)