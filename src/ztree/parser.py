import zarr
from pydantic import ValidationError
from typing import Union, Tuple, Dict, Any, Callable, Iterable
import click
from ztree.multiscale import MultiscaleGroup
from ztree.models import Array, Group
import json
from rich import print_json
from zarr.storage import FSStore


def visit(
    obj: Union[zarr.hierarchy.Group, zarr.core.Array]
) -> Tuple[str, Union[Array, Group]]:
    tree = {}
    name: str = obj.basename

    # if it has .shape, it is an array
    if hasattr(obj, "dtype"):
        tree = Array(name=name, attrs=dict(obj.attrs)).dict()
        return name, tree
    else:
        tree = Group(name=name, attrs=dict(obj.attrs)).dict()

    keys: Iterable[str] = sorted(getattr(obj, "keys", lambda: [])())

    for k in keys:
        tree["values"][k] = visit(obj[k])[-1]

    return tree


def walk_fsstore_hierarchy(url: str, path: str) -> Union[Array, Group]:
    store = zarr.FSStore(url, anon=True)
    node = zarr.open(store, path=path, mode="r")
    elements = visit(node)
    return elements


def walk_n5_hierarchy(url: str, path: str) -> Tuple[str, Union[Array, Group]]:
    store = zarr.N5FSStore(url, anon=True)
    node = zarr.open(store, path=path, mode="r")
    elements = visit(node)
    return elements


def validate_n5_tree(
    url: str,
    path: str,
    cls: Union[Callable[[Dict[str, Any]], Group], Callable[[Dict[str, Any]], Array]],
) -> Tuple[str, Union[Array, Group]]:
    name, tree = walk_n5_hierarchy(url, path)
    return name, cls(**tree)


def main(url: str, path: str):
    """
    Walk a tree and validate it
    """
    if url.endswith(".n5"):
        name, tree = walk_n5_hierarchy(url, path)
    elif url.endswith(".zarr"):
        name, tree = walk_fsstore_hierarchy(url, path)
    err = dict()
    try:
        validated = MultiscaleGroup(**tree)
    except ValidationError as ve:
        err = ve.json()
    return name, tree, err


@click.command()
@click.argument("url", type=str)
@click.argument("path", type=str, default="")
def main_cli(url: str, path: str = ""):
    name, tree, err = main(url, path)
    print_json(json.dumps(tree))
    print_json(err)


if __name__ == "__main__":
    main_cli()
