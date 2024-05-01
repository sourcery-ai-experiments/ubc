"""Cells imported from the PDK."""

from functools import cache, partial

import gdsfactory as gf
from gdsfactory import Component
from gdsfactory.typings import (
    Callable,
    ComponentReference,
    ComponentSpec,
    CrossSectionSpec,
    Label,
    LayerSpec,
    List,
    Optional,
    Port,
    Tuple,
)

from ubcpdk import tech
from ubcpdk.config import CONFIG
from ubcpdk.import_gds import import_gc, import_gds
from ubcpdk.tech import (
    LAYER,
    LAYER_STACK,
    add_pins_bbox_siepic,
)

um = 1e-6


@gf.cell
def bend_euler_sc(**kwargs) -> Component:
    kwargs.pop("cross_section", None)
    return gf.components.bend_euler(cross_section="xs_sc_devrec", **kwargs)


bend_euler180_sc = partial(bend_euler_sc, angle=180)
bend = bend_euler_sc


@gf.cell(post_process=(tech.add_pins_bbox_siepic,), include_module=True)
def straight(length: float = 1.0, npoints: int = 2, cross_section="xs_sc"):
    return gf.components.straight(
        length=length, npoints=npoints, cross_section=cross_section
    )


straight_heater_metal = partial(gf.c.straight_heater_metal, straight=straight)
bend_s = partial(
    gf.components.bend_s,
    cross_section="xs_sc",
)

info1550te = dict(polarization="te", wavelength=1.55)
info1310te = dict(polarization="te", wavelength=1.31)
info1550tm = dict(polarization="tm", wavelength=1.55)
info1310tm = dict(polarization="tm", wavelength=1.31)
thermal_phase_shifter_names = [
    "thermal_phase_shifter_multimode_500um",
    "thermal_phase_shifter_te_1310_500um",
    "thermal_phase_shifter_te_1310_500um_lowloss",
    "thermal_phase_shifter_te_1550_500um_lowloss",
]

prefix_te1550 = prefix_tm1550 = prefix_te1310 = prefix_tm1130 = "o2"


def clean_name(name: str) -> str:
    return name.replace("_", ".")


def thermal_phase_shifter0() -> gf.Component:
    """Return thermal_phase_shifters fixed cell."""
    return import_gds(
        "thermal_phase_shifters.gds", cellname=thermal_phase_shifter_names[0]
    )


def thermal_phase_shifter1() -> gf.Component:
    """Return thermal_phase_shifters fixed cell."""
    return import_gds(
        "thermal_phase_shifters.gds", cellname=thermal_phase_shifter_names[1]
    )


def thermal_phase_shifter2() -> gf.Component:
    """Return thermal_phase_shifters fixed cell."""
    return import_gds(
        "thermal_phase_shifters.gds", cellname=thermal_phase_shifter_names[2]
    )


def thermal_phase_shifter3() -> gf.Component:
    """Return thermal_phase_shifters fixed cell."""
    return import_gds(
        "thermal_phase_shifters.gds", cellname=thermal_phase_shifter_names[3]
    )


def ebeam_BondPad() -> gf.Component:
    """Return ebeam_BondPad fixed cell."""
    return import_gds("ebeam_BondPad.gds")


def ebeam_adiabatic_te1550() -> gf.Component:
    """Return ebeam_adiabatic_te1550 fixed cell."""
    return import_gds("ebeam_adiabatic_te1550.gds")


def ebeam_adiabatic_tm1550() -> gf.Component:
    """Return ebeam_adiabatic_tm1550 fixed cell."""
    return import_gds("ebeam_adiabatic_tm1550.gds")


def ebeam_bdc_te1550() -> gf.Component:
    """Return ebeam_bdc_te1550 fixed cell."""
    return import_gds("ebeam_bdc_te1550.gds")


def ebeam_bdc_tm1550() -> gf.Component:
    """Return ebeam_bdc_tm1550 fixed cell."""
    return import_gds("ebeam_bdc_tm1550.gds")


def ebeam_crossing4() -> gf.Component:
    """Return ebeam_crossing4 fixed cell."""
    return import_gds("ebeam_crossing4.gds")


@gf.cell
def straight_one_pin(length=1, cross_section=tech.strip_bbox) -> gf.Component:
    c = gf.Component()
    add_pins_left = partial(tech.add_pins_siepic, prefix="o1", pin_length=0.1)
    s = c << gf.components.straight(length=length, cross_section=cross_section)
    c.add_ports(s.ports)
    add_pins_left(c)
    c.absorb(s)
    return c


@gf.cell
def ebeam_crossing4_2ports() -> gf.Component:
    """Return ebeam_crossing4 fixed cell."""
    c = gf.Component()
    x = c << ebeam_crossing4()
    s1 = c << straight_one_pin()
    s2 = c << straight_one_pin()

    s1.connect("o1", x.ports["o2"])
    s2.connect("o1", x.ports["o4"])

    c.add_port(name="o1", port=x.ports["o1"])
    c.add_port(name="o4", port=x.ports["o3"])
    return c


def ebeam_splitter_adiabatic_swg_te1550() -> gf.Component:
    """Return ebeam_splitter_adiabatic_swg_te1550 fixed cell."""
    return import_gds("ebeam_splitter_adiabatic_swg_te1550.gds")


def ebeam_splitter_swg_assist_te1310() -> gf.Component:
    """Return ebeam_splitter_swg_assist_te1310 fixed cell."""
    return import_gds("ebeam_splitter_swg_assist_te1310.gds")


def ebeam_splitter_swg_assist_te1550() -> gf.Component:
    """Return ebeam_splitter_swg_assist_te1550 fixed cell."""
    return import_gds("ebeam_splitter_swg_assist_te1550.gds")


def ebeam_swg_edgecoupler() -> gf.Component:
    """Return ebeam_swg_edgecoupler fixed cell."""
    return import_gds("ebeam_swg_edgecoupler.gds")


def ebeam_terminator_te1310() -> gf.Component:
    """Return ebeam_terminator_te1310 fixed cell."""
    return import_gds("ebeam_terminator_te1310.gds")


def ebeam_terminator_te1550() -> gf.Component:
    """Return ebeam_terminator_te1550 fixed cell."""
    return import_gds("ebeam_terminator_te1550.gds")


def ebeam_terminator_tm1550() -> gf.Component:
    """Return ebeam_terminator_tm1550 fixed cell."""
    return import_gds("ebeam_terminator_tm1550.gds")


def ebeam_y_1550() -> gf.Component:
    """Return ebeam_y_1550 fixed cell."""
    return import_gds("ebeam_y_1550.gds")


def ebeam_y_adiabatic() -> gf.Component:
    """Return ebeam_y_adiabatic fixed cell."""
    return import_gds("ebeam_y_adiabatic.gds")


def ebeam_y_adiabatic_tapers() -> gf.Component:
    """Return ebeam_y_adiabatic fixed cell."""
    y = import_gds("ebeam_y_adiabatic.gds")
    return gf.add_tapers(y)


def ebeam_y_adiabatic_1310() -> gf.Component:
    """Return ebeam_y_adiabatic_1310 fixed cell."""
    return import_gds("ebeam_y_adiabatic_1310.gds")


def metal_via() -> gf.Component:
    """Return metal_via fixed cell."""
    return import_gds("metal_via.gds")


def photonic_wirebond_surfacetaper_1310() -> gf.Component:
    """Return photonic_wirebond_surfacetaper_1310 fixed cell."""
    return import_gds("photonic_wirebond_surfacetaper_1310.gds")


def photonic_wirebond_surfacetaper_1550() -> gf.Component:
    """Return photonic_wirebond_surfacetaper_1550 fixed cell."""
    return import_gds("photonic_wirebond_surfacetaper_1550.gds")


@gf.cell
def gc_te1310() -> gf.Component:
    """Return ebeam_gc_te1310 fixed cell."""
    c = gf.Component()
    gc = import_gc("ebeam_gc_te1310.gds")
    gc_ref = c << gc
    c.add_ports(gc_ref.ports)
    c.copy_child_info(gc)
    name = prefix_te1310
    c.add_port(
        name=name,
        port_type=name,
        center=(25, 0),
        layer=(1, 0),
        width=9,
    )
    c.info.update(info1310te)
    return c


@gf.cell
def gc_te1310_8deg() -> gf.Component:
    """Return ebeam_gc_te1310_8deg fixed cell."""
    c = gf.Component()
    gc = import_gc("ebeam_gc_te1310_8deg.gds")
    gc_ref = c << gc
    c.add_ports(gc_ref.ports)
    c.copy_child_info(gc)
    name = prefix_te1310
    c.add_port(
        name=name,
        port_type=name,
        center=(25, 0),
        layer=(1, 0),
        width=9,
    )
    c.info.update(info1310te)
    return c


@gf.cell
def gc_te1310_broadband() -> gf.Component:
    """Return ebeam_gc_te1310_broadband fixed cell."""
    c = gf.Component()
    gc = import_gc("ebeam_gc_te1310_broadband.gds")
    gc_ref = c << gc
    c.add_ports(gc_ref.ports)
    c.copy_child_info(gc)
    name = prefix_te1310
    c.add_port(
        name=name,
        port_type=name,
        center=(25, 0),
        layer=(1, 0),
        width=9,
    )
    c.info.update(info1310te)
    return c


@gf.cell
def gc_te1550() -> gf.Component:
    """Return ebeam_gc_te1550 fixed cell."""
    c = gf.Component()
    gc = import_gc("ebeam_gc_te1550.gds")
    gc_ref = c << gc
    c.add_ports(gc_ref.ports)
    c.copy_child_info(gc)
    name = prefix_te1550
    c.add_port(
        name=name,
        port_type=name,
        center=(25, 0),
        layer=(1, 0),
        width=9,
    )
    c.info.update(info1550te)
    return c


@gf.cell
def gc_te1550_90nmSlab() -> gf.Component:
    """Return ebeam_gc_te1550_90nmSlab fixed cell."""
    c = gf.Component()
    gc = import_gc("ebeam_gc_te1550_90nmSlab.gds")
    gc_ref = c << gc
    c.add_ports(gc_ref.ports)
    c.copy_child_info(gc)
    name = prefix_te1550
    c.add_port(
        name=name,
        port_type=name,
        center=(25, 0),
        layer=(1, 0),
        width=9,
    )
    c.info.update(info1550te)
    return c


@gf.cell
def gc_te1550_broadband() -> gf.Component:
    """Return ebeam_gc_te1550_broadband fixed cell."""
    c = gf.Component()
    gc = import_gc("ebeam_gc_te1550_broadband.gds")
    gc_ref = c << gc
    c.add_ports(gc_ref.ports)
    c.copy_child_info(gc)
    name = prefix_te1550
    c.add_port(
        name=name,
        port_type=name,
        center=(25, 0),
        layer=(1, 0),
        width=9,
    )
    c.info.update(info1550te)
    return c


@gf.cell
def gc_tm1550() -> gf.Component:
    """Return ebeam_gc_tm1550 fixed cell."""
    c = gf.Component()
    gc = import_gc("ebeam_gc_tm1550.gds")
    gc_ref = c << gc
    c.add_ports(gc_ref.ports)
    c.copy_child_info(gc)
    name = prefix_tm1550
    c.add_port(
        name=name,
        port_type=name,
        center=(25, 0),
        layer=(1, 0),
        width=9,
    )
    c.info.update(info1550tm)
    return c


mzi = partial(
    gf.components.mzi,
    splitter=ebeam_y_1550,
    bend=bend_euler_sc,
    straight=straight,
    cross_section="xs_sc",
)

mzi_heater = partial(
    gf.components.mzi_phase_shifter,
    bend=bend_euler_sc,
    straight=straight,
    splitter=ebeam_y_1550,
)

via_stack_heater_mtop = partial(
    gf.components.via_stack,
    size=(10, 10),
    layers=(LAYER.M1_HEATER, LAYER.M2_ROUTER),
    vias=(None, None),
)


def get_input_label_text(
    port: Port,
    gc: ComponentReference,
    component_name: Optional[str] = None,
    username: str = CONFIG.username,
) -> str:
    """Return label for port and a grating coupler.

    Args:
        port: component port.
        gc: grating coupler reference.
        component_name: optional component name.
        username: for the label.
    """
    polarization = gc.info.get("polarization")
    wavelength = gc.info.get("wavelength")

    assert polarization.upper() in [
        "TE",
        "TM",
    ], f"Not valid polarization {polarization.upper()!r} in [TE, TM]"
    assert (
        isinstance(wavelength, int | float) and 1.0 < wavelength < 2.0
    ), f"{wavelength} is Not valid 1000 < wavelength < 2000"

    name = component_name or port.parent.metadata_child.get("name")
    name = clean_name(name)
    # return f"opt_{polarization.upper()}_{int(wavelength * 1000.0)}_device_{username}-{name}-{gc_index}-{port.name}"
    return f"opt_in_{polarization.upper()}_{int(wavelength * 1000.0)}_device_{username}-{name}"


def get_input_labels(
    io_gratings: List[ComponentReference],
    ordered_ports: List[Port],
    component_name: str,
    layer_label: Tuple[int, int] = (10, 0),
    gc_port_name: str = "o1",
    port_index: int = 1,
    get_input_label_text_function: Callable = get_input_label_text,
) -> List[Label]:
    """Return list of labels for all component ports.

    Args:
        io_gratings: list of grating_coupler references.
        ordered_ports: list of ports.
        component_name: name.
        layer_label: for the label.
        gc_port_name: grating_coupler port.
        port_index: index of the port.
        get_input_label_text_function: function.

    """
    gc = io_gratings[port_index]
    port = ordered_ports[1]

    text = get_input_label_text_function(
        port=port, gc=gc, component_name=component_name
    )
    layer, texttype = gf.get_layer(layer_label)
    label = Label(
        text=text,
        origin=gc.ports[gc_port_name].center,
        anchor="o",
        layer=layer,
        texttype=texttype,
    )
    return [label]


@gf.cell_with_child(include_module=True)
def add_fiber_array(
    component: ComponentSpec = straight,
    component_name: Optional[str] = None,
    gc_port_name: str = "o1",
    get_input_labels_function: Callable = get_input_labels,
    with_loopback: bool = False,
    optical_routing_type: int = 0,
    fanout_length: float = 0.0,
    grating_coupler: ComponentSpec = gc_te1550,
    cross_section: CrossSectionSpec = "xs_sc",
    layer_label: LayerSpec = LAYER.TEXT,
    straight: ComponentSpec = straight,
    **kwargs,
) -> Component:
    """Returns component with grating couplers and labels on each port.

    Routes all component ports south.
    Can add align_ports loopback reference structure on the edges.

    Args:
        component: to connect.
        component_name: for the label.
        gc_port_name: grating coupler input port name 'o1'.
        get_input_labels_function: function to get input labels for grating couplers.
        with_loopback: True, adds loopback structures.
        optical_routing_type: None: autoselection, 0: no extension.
        fanout_length: None  # if None, automatic calculation of fanout length.
        grating_coupler: grating coupler instance, function or list of functions.
        cross_section: spec.
        layer_label: for label.
        straight: straight component.

    """
    c = gf.Component()

    component = gf.routing.add_fiber_array(
        straight=straight,
        bend=bend,
        component=component,
        component_name=component_name,
        grating_coupler=grating_coupler,
        gc_port_name=gc_port_name,
        get_input_labels_function=get_input_labels_function,
        get_input_label_text_function=get_input_label_text,
        with_loopback=with_loopback,
        optical_routing_type=optical_routing_type,
        layer_label=layer_label,
        fanout_length=fanout_length,
        cross_section=cross_section,
        **kwargs,
    )
    ref = c << component
    ref.rotate(-90)
    c.add_ports(ref.ports)
    c.copy_child_info(component)

    return c


L = 1.55 / 4 / 2 / 2.44


@gf.cell
def dbg(
    w0: float = 0.5,
    dw: float = 0.1,
    n: int = 100,
    l1: float = L,
    l2: float = L,
) -> gf.Component:
    """Includes two ports.

    Args:
        w0: width.
        dw: delta width.
        n: number of elements.
        l1: length teeth1.
        l2: length teeth2.
    """
    c = gf.Component()
    s = gf.components.straight(length=l1, cross_section=tech.strip_simple)
    g = c << gf.components.dbr(
        w1=w0 - dw / 2,
        w2=w0 + dw / 2,
        n=n,
        l1=l1,
        l2=l2,
        cross_section=tech.strip_simple,
    )
    s1 = c << s
    s2 = c << s
    s1.connect("o2", g.ports["o1"])
    s2.connect("o2", g.ports["o2"])

    c.add_port("o1", port=s1.ports["o1"])
    c.add_port("o2", port=s2.ports["o1"])
    c = add_pins_bbox_siepic(c)
    return c


@gf.cell
def terminator_short(**kwargs) -> gf.Component:
    c = gf.Component()
    s = gf.components.taper(**kwargs, cross_section=tech.strip_simple)
    s1 = c << s
    c.add_port("o1", port=s1.ports["o1"])
    c = add_pins_bbox_siepic(c)
    return c


@gf.cell
def dbr(
    w0: float = 0.5,
    dw: float = 0.1,
    n: int = 100,
    l1: float = L,
    l2: float = L,
    cross_section: CrossSectionSpec = tech.strip_simple,
    **kwargs,
) -> gf.Component:
    """Returns distributed bragg reflector.

    Args:
        w0: width.
        dw: delta width.
        n: number of elements.
        l1: length teeth1.
        l2: length teeth2.
        cross_section: spec.
        kwargs: cross_section settings.
    """
    c = gf.Component()

    xs = gf.get_cross_section(cross_section, **kwargs)

    # add_pins_left = partial(add_pins_siepic, prefix="o1")
    s = c << gf.components.straight(length=l1, cross_section=xs)
    _dbr = gf.components.dbr(
        w1=w0 - dw / 2,
        w2=w0 + dw / 2,
        n=n,
        l1=l1,
        l2=l2,
        cross_section=xs,
    )
    dbr = c << _dbr
    s.connect("o2", dbr.ports["o1"])
    c.add_port("o1", port=s.ports["o1"])
    return add_pins_bbox_siepic(c)


@gf.cell(post_process=(tech.add_pins_bbox_siepic,), include_module=True)
def coupler(**kwargs) -> gf.Component:
    return gf.components.coupler(**kwargs).flatten()


@gf.cell(post_process=(tech.add_pins_bbox_siepic,), include_module=True)
def coupler_ring(**kwargs) -> gf.Component:
    return gf.components.coupler_ring(**kwargs).flatten()


@gf.cell(post_process=(tech.add_pins_bbox_siepic,), include_module=True)
def mmi1x2(**kwargs) -> gf.Component:
    return gf.components.mmi1x2(**kwargs)


@cache
def dbr_cavity(dbr=dbr, coupler=coupler, **kwargs) -> gf.Component:
    dbr = dbr(**kwargs)
    return gf.components.cavity(component=dbr, coupler=coupler)


@cache
def dbr_cavity_te(component="dbr_cavity", **kwargs) -> gf.Component:
    component = gf.get_component(component, **kwargs)
    return add_fiber_array(component=component)


spiral = partial(gf.components.spiral_external_io, cross_section=tech.xs_sc_devrec)

ebeam_dc_halfring_straight = coupler_ring


@gf.cell
def ebeam_dc_halfring_straight(
    gap: float = 0.2,
    radius: float = 5.0,
    length_x: float = 4.0,
    siepic: bool = True,
    model: str = "ebeam_dc_halfring_straight",
    **kwargs,
) -> gf.Component:
    r"""Return a ring coupler.

    Args:
        gap: spacing between parallel coupled straight waveguides.
        radius: of the bends.
        length_x: length of the parallel coupled straight waveguides.
        cross_section: cross_section spec.
        siepic: if True adds siepic.
        kwargs: cross_section settings for bend and coupler.

    .. code::

           2             3
           |             |
            \           /
             \         /
           ---=========---
         1    length_x    4


    """

    c = gf.Component()
    ref = c << coupler_ring(gap=gap, radius=radius, length_x=length_x, **kwargs)
    thickness = LAYER_STACK.get_layer_to_thickness()
    c.add_ports(ref.ports)

    if siepic:
        x = tech.xs_sc_simple
        c.info["model"] = model
        c.info["gap"] = gap
        c.info["radius"] = radius
        c.info["wg_thickness"] = thickness[LAYER.WG]
        c.info["wg_width"] = x.width
        c.info["Lc"] = length_x

    return c


ring_single = partial(
    gf.components.ring_single,
    coupler_ring=coupler_ring,
    cross_section=tech.xs_sc,
    bend=bend,
    straight=straight,
    pass_cross_section_to_bend=False,
)
ring_double = partial(
    gf.components.ring_double,
    coupler_ring=coupler_ring,
    cross_section=tech.xs_sc,
    straight=straight,
)
ring_double_heater = partial(
    gf.components.ring_double_heater,
    coupler_ring=coupler_ring,
    via_stack=via_stack_heater_mtop,
    cross_section=tech.xs_sc,
    straight=straight,
    length_y=0.2,
)
ring_single_heater = partial(
    gf.components.ring_single_heater,
    coupler_ring=coupler_ring,
    via_stack=via_stack_heater_mtop,
    cross_section=tech.xs_sc,
    straight=straight,
)


ebeam_dc_te1550 = partial(
    gf.components.coupler,
)
taper = partial(gf.components.taper)
spiral = partial(gf.components.spiral_external_io)
ring_with_crossing = partial(
    gf.components.ring_single_dut,
    component=ebeam_crossing4_2ports,
    coupler=coupler_ring,
    port_name="o4",
    bend=bend,
    cross_section="xs_sc",
    straight=straight,
)


pad = partial(
    gf.components.pad,
    size=(75, 75),
    layer=LAYER.M2_ROUTER,
    bbox_layers=(LAYER.PAD_OPEN,),
    bbox_offsets=(-1.8,),
)


def add_label_electrical(component: Component, text: str, port_name: str = "e2"):
    """Adds labels for electrical port.

    Returns same component so it needs to be used as a decorator.
    """
    if port_name not in component.ports:
        raise ValueError(f"No port {port_name!r} in {list(component.ports.keys())}")

    component.add_label(
        text=text, position=component.ports[port_name].center, layer=LAYER.TEXT
    )
    return component


pad_array = partial(gf.components.pad_array, pad=pad, spacing=(125, 125))
add_pads_rf = partial(
    gf.routing.add_electrical_pads_top,
    component="ring_single_heater",
    pad_array=pad_array,
)
add_pads_dc = partial(
    gf.routing.add_electrical_pads_top_dc,
    component="ring_single_heater",
    pad_array=pad_array,
)


@cache
def add_fiber_array_pads_rf(
    component: ComponentSpec = "ring_single_heater",
    username: str = CONFIG.username,
    orientation: float = 0,
    **kwargs,
) -> Component:
    """Returns fiber array with label and electrical pads.

    Args:
        component: to add fiber array and pads.
        username: for the label.
        orientation: for adding pads.
        kwargs: for add_fiber_array.
    """
    c0 = gf.get_component(component)
    # text = f"elec_{username}-{clean_name(c0.name)}_G"
    # add_label = partial(add_label_electrical, text=text)
    c1 = add_pads_rf(component=c0, orientation=orientation)
    return add_fiber_array(component=c1, **kwargs)


@cache
def add_pads(
    component: ComponentSpec = "ring_single_heater",
    username: str = CONFIG.username,
    **kwargs,
) -> Component:
    """Returns fiber array with label and electrical pads.

    Args:
        component: to add fiber array and pads.
        username: for the label.
        kwargs: for add_fiber_array.
    """
    c0 = gf.get_component(component)
    # text = f"elec_{username}-{clean_name(c0.name)}_G"
    # add_label = partial(add_label_electrical, text=text)
    return add_pads_rf(component=c0, **kwargs)


if __name__ == "__main__":
    c = straight_heater_metal()
    # c.pprint_ports()
    # c = straight()
    # c = uc.ring_single_heater()
    # c = uc.add_fiber_array_pads_rf(c)

    # c = ring_double(length_y=10)
    # c = ring_with_crossing()
    # c = mmi1x2()
    # c = add_fiber_array(mzi)
    # c = coupler_ring()
    # c = dbr_cavity_te()
    # c = dbr_cavity()
    # c = ring_single(radius=12)
    # c = ring_double(radius=12, length_x=2, length_y=2)
    # c = bend_euler()
    # c = mzi()
    # c = spiral()
    # c = pad_array()
    # c = ring_double_heater()
    # c = ring_single_heater()
    # c = ebeam_y_1550()
    # c = ebeam_dc_halfring_straight()
    # c = ring_with_crossing()
    # c = ring_single()
    c.show(show_ports=False)
