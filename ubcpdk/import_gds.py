from functools import cache, partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec
from numpy import arctan2, degrees, isclose, ndarray

from ubcpdk.config import PATH
from ubcpdk.tech import LAYER

layer = LAYER.WG
port_width = 0.5


def guess_port_orientaton(position: ndarray, name: str, label: str, n: int) -> int:
    """Assumes ports with x<0 have orientation=180 and ports with x>0  orientation=0."""
    p = position
    if "gc" in name:
        return 0
    if label == "opt1":
        return 180
    if p[1] > 0 and "crossing" in name:
        return 90
    if p[1] < 0 and "crossing" in name:
        return 270
    if n == 4:
        if label in {"opt1", "opt2"}:
            return 180
        if label in {"opt3", "opt4"}:
            return 0
    return 180 if p[0] <= 0 else 0


def remove_pins(component) -> Component:
    """Remove pins."""
    component.remove_layers(layers=(LAYER.DEVREC, LAYER.PORT, LAYER.PORTE))
    component.paths = []
    component._bb_valid = False
    return component


def remove_pins_recursive(component):
    component = remove_pins(component)
    if component.references:
        for ref in component.references:
            rcell = ref.parent
            ref.parent = remove_pins_recursive(rcell)
    return component


def add_ports_from_siepic_pins(
    component: Component,
    pin_layer_optical: LayerSpec = "PORT",
    port_layer_optical: LayerSpec | None = None,
    pin_layer_electrical: LayerSpec = "PORTE",
    port_layer_electrical: LayerSpec | None = None,
) -> Component:
    """Add ports from SiEPIC-type cells, where the pins are defined as paths.

    Looks for label, path pairs.

    Args:
        component: component.
        pin_layer_optical: layer for optical pins.
        port_layer_optical: layer for optical ports.
        pin_layer_electrical: layer for electrical pins.
        port_layer_electrical: layer for electrical ports.
    """
    pin_layers = {"optical": pin_layer_optical, "electrical": pin_layer_electrical}

    import gdsfactory as gf

    pin_layer_optical = gf.get_layer(pin_layer_optical)
    port_layer_optical = gf.get_layer(port_layer_optical)
    pin_layer_electrical = gf.get_layer(pin_layer_electrical)
    port_layer_electrical = gf.get_layer(port_layer_electrical)

    c = component
    labels = c.get_labels()

    for path in c.paths:
        p1, p2 = path.spine()

        path_layers = list(zip(path.layers, path.datatypes))

        # Find the center of the path
        center = (p1 + p2) / 2

        # Find the label closest to the pin
        label = None
        for i, _label in enumerate(labels):
            if (
                all(isclose(_label.origin, center))
                or all(isclose(_label.origin, p1))
                or all(isclose(_label.origin, p2))
            ):
                label = _label
                labels.pop(i)
        if label is None:
            print(
                f"Warning: label not found for path: in center={center} p1={p1} p2={p2}"
            )
            continue
        if pin_layer_optical in path_layers:
            port_type = "optical"
            port_layer = port_layer_optical or None
        elif pin_layer_electrical in path_layers:
            port_type = "electrical"
            port_layer = port_layer_electrical or None
        else:
            continue

        port_name = str(label.text)

        # If the port name is already used, add a number to it
        i = 1
        while port_name in c.ports:
            port_name += f"_{i}"

        angle = round(degrees(arctan2(p2[1] - p1[1], p2[0] - p1[0])) % 360)

        port = gf.Port(
            name=port_name,
            center=center,
            width=path.widths()[0][0],
            orientation=angle,
            layer=port_layer or pin_layers[port_type],
            port_type=port_type,
        )
        c.add_port(port)
    c.auto_rename_ports()
    return c


add_ports_from_siepic_pins = partial(
    add_ports_from_siepic_pins,
    pin_layer_optical=LAYER.PORT,
    pin_layer_electrical=LAYER.PORTE,
    port_layer_optical=LAYER.WG,
)


@cache
def import_gds(gdspath, **kwargs):
    c = gf.import_gds(
        gdspath,
        gdsdir=PATH.gds,
        library="Design kits/ebeam",
        model=gdspath.split(".")[0],
        **kwargs,
    )
    add_ports_from_siepic_pins(c)
    return c


@cache
def import_gc(gdspath, info=None, **kwargs):
    """Import grating coupler GDS file and add ports to it."""
    c = import_gds(gdspath, **kwargs)

    if info is not None:
        c.info.update(info)
    return gf.functions.mirror(component=c)


if __name__ == "__main__":
    # from gdsfactory.write_cells import get_import_gds_script
    # script = get_import_gds_script(dirpath=PATH.gds, module="ubcpdk.components")
    # print(script)

    # gdsname = "ebeam_crossing4.gds"
    gdsname = "ebeam_y_1550.gds"
    c = gf.Component("my_component")
    wg1 = c << import_gds(gdsname)
    wg2 = c << import_gds(gdsname)
    wg2.move((100, 0))
    c.show(show_ports=False)
