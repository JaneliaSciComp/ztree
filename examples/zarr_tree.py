import json
import zarr
from rich import print_json
from ztree.parser import visit

zgroup = zarr.open(zarr.MemoryStore())
zgroup.attrs['foo'] = 100 # this will fail validation
zgroup.create_dataset(name='my_array', shape=(10,))
zgroup['my_array'].attrs['bar'] = '10' # this will fail validation

if __name__ == '__main__':
    name, tree = visit(zgroup)
    print_json(json.dumps({name: tree}))

