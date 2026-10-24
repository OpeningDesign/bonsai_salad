bl_info = {
    "name": "Bonsai Salad",
    "author": "carlopav",
    "version": (0, 0, 10),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Bonsai Salad",
    "description": "A collection of miscellaneous scripts and tools",
    "category": "3D View",
}

import sys

import bpy

# The tools import Bonsai at module level, so they are only imported once Bonsai has loaded.
# Blender may enable this add-on before Bonsai, and importing bonsai.tool on its own then fails
# part-way through a circular import, leaving Bonsai's own modules holding a half-built bonsai.tool.
_modules = []
_WAIT_INTERVAL = 0.5
_WAIT_ATTEMPTS = 120
_attempts_left = 0


def _is_bonsai_loaded():
    return "bonsai.bim" in sys.modules and hasattr(sys.modules.get("bonsai.tool"), "Ifc")


def _register_modules():
    from . import panels
    from . import sheets_to_pdf
    from . import ifc_dxf
    from . import dxf_ifc
    from . import mep
    from . import ifc_cleanup
    from . import drawing_diff
    from . import urban_parameters
    from . import daylight_ventilation
    from . import ifc_spaces
    from . import invarianza_idraulica

    # The category panels first: a tool panel's bl_parent_id must already exist.
    modules = [
        panels,
        sheets_to_pdf,
        ifc_dxf,
        dxf_ifc,
        mep,
        ifc_cleanup,
        drawing_diff,
        urban_parameters,
        daylight_ventilation,
        ifc_spaces,
        invarianza_idraulica,
    ]
    for module in modules:
        module.register()
        _modules.append(module)


def _register_when_bonsai_loaded():
    global _attempts_left
    if _is_bonsai_loaded():
        _register_modules()
        return None
    _attempts_left -= 1
    if _attempts_left <= 0:
        print("Bonsai Salad: Bonsai is not enabled. Enable Bonsai, then re-enable Bonsai Salad.")
        return None
    return _WAIT_INTERVAL


def register():
    global _attempts_left
    if _is_bonsai_loaded():
        _register_modules()
    else:
        _attempts_left = _WAIT_ATTEMPTS
        bpy.app.timers.register(_register_when_bonsai_loaded, first_interval=0.0, persistent=True)


def unregister():
    if bpy.app.timers.is_registered(_register_when_bonsai_loaded):
        bpy.app.timers.unregister(_register_when_bonsai_loaded)
    for module in reversed(_modules):
        module.unregister()
    _modules.clear()
