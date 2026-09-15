import json
import os
import subprocess
import time

def make_attr_float_add(size):
    return {
        "flow": {"type": "flow", "value": "signal"},
        "size": {"type": "integer", "value": size},
        **{f"input{i}-dimensions": {"type": "integer", "value": 1} for i in range(size)},
        **{f"type{i}": {"type": "type", "value": "float"} for i in range(size)}
    }

def make_attr_float_mult():
    return {
        "flow": {"type": "flow", "value": "signal"},
        "input0-dimensions": {"type": "integer", "value": 1},
        "input1-dimensions": {"type": "integer", "value": 1},
        "size": {"type": "integer", "value": 2},
        "type0": {"type": "type", "value": "float"},
        "type1": {"type": "type", "value": "float"}
    }

def make_attr_float_switch(size):
    return {
        "case-type": {"type": "type", "value": "float"},
        "flow": {"type": "flow", "value": "signal"},
        "instances": {"type": "integer", "value": 1},
        "selection-type": {"type": "type", "value": "integer"},
        "size": {"type": "integer", "value": size}
    }

def base_patch(name, identifier, description, tags, input_order):
    return {
        "formatVersion": {"major": 1, "minor": 1, "patch": 0},
        "patch": {
            "connections": [],
            "inputOrder": input_order,
            "meta": {
                "author": "Andreas - IP26 Production",
                "category": "effect",
                "description": description,
                "displayName": name,
                "identifier": identifier,
                "license": "MIT",
                "mail": "",
                "name": name,
                "tags": tags,
                "type": "effect",
                "url": "https://github.com/zzdree/ip26-zzfx",
                "vendor": "IP26 Production",
                "version": "1.0.0"
            },
            "nextNodeId": 300,
            "nodes": {},
            "ui": {"pan": {"x": 0.0, "y": 0.0}, "zoom": 1.0}
        },
        "resources": {},
        "ui": {}
    }

def node_texture_in(nid, x=-600, y=0):
    return {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": x, "y": y},
        "class": {"id": "77697265-B2A2-4C1C-8C4C-2915D78CC8E9", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "texture2d", "value": None}},
        "name": "Texture In",
        "thumbnail_visible": True
    }

def node_texture_out(nid, x=1500, y=0):
    return {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": x, "y": y},
        "class": {"id": "77697265-BEEA-4D38-8EE5-0EBA4CBD0AEE", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "texture2d", "value": None}},
        "name": "Texture Out",
        "thumbnail_visible": True
    }

def node_trigger_in(nid, name="Punch!", x=-600, y=100):
    return {
        "attributes": {"flow": {"type": "flow", "value": "event"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": x, "y": y},
        "class": {"id": "77697265-e61f-42c0-862a-0dca04e14569", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "trigger", "value": None}},
        "hidden": ["input", "instances", "flow"],
        "name": name,
        "thumbnail_visible": True
    }

def node_bool_in(nid, name, def_val=False, x=-600, y=100):
    return {
        "attributes": {"bool-view": {"type": "integer", "value": 0}, "flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 140, "x": x, "y": y},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": def_val}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": name,
        "thumbnail_visible": True
    }

def node_float_in(nid, name, min_v, max_v, def_v, x=-600, y=200):
    return {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": float(max_v)},
            "min": {"type": "float", "value": float(min_v)},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": x, "y": y},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": float(def_v)}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": name,
        "thumbnail_visible": True
    }

def node_int_in(nid, name, min_v, max_v, def_v, x=-600, y=300):
    return {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "integer", "value": int(max_v)},
            "min": {"type": "integer", "value": int(min_v)},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": x, "y": y},
        "class": {"id": "77697265-2649-4abb-b38f-4e1005183415", "version": 2},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "integer", "value": int(def_v)}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": name,
        "thumbnail_visible": True
    }

def node_color_in(nid, name, def_v, x=-600, y=400):
    return {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
        "bounds": {"height": 82, "width": 140, "x": x, "y": y},
        "class": {"id": "77697265-4C9E-4F75-B4F0-5415B713EA1B", "version": 3},
        "clock": "video",
        "color": "ffea1f48",
        "constants": {"input": {"type": "color", "value": def_v}},
        "hidden": ["input", "instances", "flow", "options-count", "widget"],
        "name": name,
        "thumbnail_visible": True
    }

def node_video_mixer(nid, mode=0, x=1000, y=0):
    return {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "input-count": {"type": "integer", "value": 2},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 154, "width": 195, "x": x, "y": y},
        "class": {"id": "77697265-A270-4D60-911C-A88B1BE6369A", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "bypass": {"type": "bool", "value": False},
            "input1": {"type": "texture2d", "value": None},
            "input2": {"type": "texture2d", "value": None},
            "mode": {"type": "integer", "value": mode},
            "opacity1": {"type": "float", "value": 1.0},
            "opacity2": {"type": "float", "value": 0.0}
        },
        "hidden": ["bypass", "input-count", "bitdepth", "resolution-absolute", "resolution-relative", "resolution-mode", "instances"],
        "name": "Video Mixer",
        "thumbnail_visible": True
    }

# =============================================================================
# 1. BUILD ZZ-PUSHER (Elastic Zoom Kick & Solid Flash Kejut)
# =============================================================================
def build_zz_pusher():
    patch = base_patch(
        "zz-pusher",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e210",
        "IP26 Modular Suite: Elastic Zoom Kick & Solid Flash Kejut (Click Trigger & Piano Mode).",
        ["ip26", "pusher", "bumper", "zoom", "punch", "kejut", "worship"],
        [0, 10, 11, 12, 13, 14, 15, 16]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_trigger_in(10, "Punch!", -600, 100)
    nodes["11"] = node_bool_in(11, "Push", False, -600, 200)
    nodes["12"] = node_float_in(12, "Push Amount", 0.0, 1.0, 0.35, -600, 300)
    nodes["13"] = node_float_in(13, "Push Decay", 0.02, 1.0, 0.15, -600, 400)
    nodes["14"] = node_float_in(14, "Flash Intensity", 0.0, 1.0, 0.40, -600, 500)
    nodes["15"] = node_color_in(15, "Flash Color", [1.0, 1.0, 1.0, 1.0], -600, 600)
    nodes["16"] = node_bool_in(16, "Bypass", False, -600, 700)

    # Trigger Envelope via Attack Release (0.0s instant attack, Decay release)
    nodes["20"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 130, "width": 195, "x": -350, "y": 100},
        "class": {"id": "77697265-D980-43B3-9237-6683B154A5B0", "version": 1},
        "clock": "video",
        "color": "fff26eb5",
        "constants": {
            "attack-time": {"type": "float", "value": 0.0},
            "linear": {"type": "bool", "value": False},
            "release": {"type": "trigger", "value": None},
            "release-time": {"type": "float", "value": 0.15},
            "reset": {"type": "trigger", "value": None},
            "restart-at-zero": {"type": "bool", "value": False},
            "trigger": {"type": "trigger", "value": None}
        },
        "name": "Punch Envelope",
        "thumbnail_visible": True
    }
    conn(10, "output", 20, "trigger")
    conn(13, "output", 20, "release-time")

    # Piano Push Smooth
    nodes["21"] = {
        "attributes": {"input0-type": {"type": "type", "value": "float"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 58, "width": 195, "x": -350, "y": 250},
        "class": {"id": "77697265-86ce-4e85-a02d-34f915fca74e", "version": 1},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"duration": {"type": "float", "value": 0.15}, "input0": {"type": "float", "value": 0.0}},
        "name": "Push Smooth",
        "thumbnail_visible": True
    }
    conn(11, "output", 21, "input0")
    conn(13, "output", 21, "duration")

    # Combine Envelopes: Add 20 + 21
    nodes["22"] = {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": -100, "y": 150},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Total Env Add",
        "thumbnail_visible": True
    }
    conn(20, "output", 22, "input0")
    conn(21, "output0", 22, "input1")

    # Clamp Env to 0..1
    nodes["23"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "max-dimensions": {"type": "integer", "value": 1},
            "max-type": {"type": "type", "value": "float"},
            "min-dimensions": {"type": "integer", "value": 1},
            "min-type": {"type": "type", "value": "float"},
            "value-dimensions": {"type": "integer", "value": 1},
            "value-type": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 80, "y": 150},
        "class": {"id": "77697265-7557-4053-ABEC-73E2A9786804", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"max": {"type": "float", "value": 1.0}, "min": {"type": "float", "value": 0.0}, "value": {"type": "float", "value": 0.0}},
        "name": "Clamp Env",
        "thumbnail_visible": True
    }
    conn(22, "output0", 23, "value")

    # Target Zoom: Clamp Env * Push Amount
    nodes["24"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 260, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Zoom Scale",
        "thumbnail_visible": True
    }
    conn(23, "output", 24, "input0")
    conn(12, "output", 24, "input1")

    # Total Scale: 1.0 + Zoom Scale
    nodes["25"] = {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 440, "y": 150},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Total Scale",
        "thumbnail_visible": True
    }
    conn(24, "output0", 25, "input1")

    # Scale Float2
    nodes["26"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 620, "y": 150},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 1.0}},
        "name": "Scale Vec2",
        "thumbnail_visible": True
    }
    conn(25, "output0", 26, "input0")
    conn(25, "output0", 26, "input1")

    # Transform (Centered Zoom)
    nodes["27"] = {
        "attributes": {
            "anchor-type": {"type": "type", "value": "float2"},
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "texture2d"},
            "instances": {"type": "integer", "value": 1},
            "rotation-type": {"type": "type", "value": "float"},
            "scale-type": {"type": "type", "value": "float2"},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 130, "width": 195, "x": 800, "y": 0},
        "class": {"id": "77697265-9225-4009-9D2D-5F898E94CC33", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "anchor": {"type": "float2", "value": [0.0, 0.0]},
            "input": {"type": "texture2d", "value": None},
            "rotation": {"type": "float", "value": 0.0},
            "scale": {"type": "float2", "value": [1.0, 1.0]},
            "translation": {"type": "float2", "value": [0.0, 0.0]}
        },
        "name": "Push Zoom",
        "thumbnail_visible": True
    }
    conn(0, "output", 27, "input")
    conn(26, "output", 27, "scale")

    # Flash Source (Solid Color)
    nodes["28"] = {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 58, "width": 195, "x": 800, "y": 350},
        "class": {"id": "77697265-E8EC-4F1B-901A-CFFC104D3B07", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"bypass": {"type": "bool", "value": False}, "color": {"type": "color", "value": [1.0, 1.0, 1.0, 1.0]}},
        "name": "Flash Source",
        "thumbnail_visible": True
    }
    conn(15, "output", 28, "color")

    # Flash Opacity = Clamp Env * Flash Intensity
    nodes["29"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 620, "y": 350},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Flash Opacity Calc",
        "thumbnail_visible": True
    }
    conn(23, "output", 29, "input0")
    conn(14, "output", 29, "input1")

    # Video Mixer for Flash (Add mode 11)
    nodes["30"] = node_video_mixer(30, 11, 1050, 0)
    conn(27, "output0", 30, "input1")
    conn(28, "output", 30, "input2")
    conn(29, "output0", 30, "opacity2")

    # Video Mixer for Bypass Switch
    nodes["31"] = node_video_mixer(31, 0, 1300, 0)
    conn(30, "output", 31, "input1")
    conn(0, "output", 31, "input2")
    conn(16, "output", 31, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 1550, 0)
    conn(31, "output", 1, "input")

    return patch

# =============================================================================
# 2. BUILD ZZ-CHASER (1-Screen Full, Custom Grid 1-10, Bounce, Directions, Piano Hold)
# =============================================================================
def build_zz_chaser():
    patch = base_patch(
        "zz-chaser",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e220",
        "IP26 Modular Suite: 1-Screen Dedicated Piano Chaser with Custom Grid 1-10 & Bounce.",
        ["ip26", "chaser", "grid", "slices", "runner", "bounce", "worship"],
        [0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Chase (Hold)", False, -600, 100)
    nodes["11"] = node_int_in(11, "Direction", 0, 7, 0, -600, 200) # 0: L->R, 1: R->L, 2: U->D, 3: D->U, 4: Center->Out H, 5: Out->Center H, 6: Center->Out V, 7: Out->Center V
    nodes["12"] = node_bool_in(12, "Bounce", False, -600, 300)
    nodes["13"] = node_int_in(13, "Grid Slices X", 1, 10, 5, -600, 400)
    nodes["14"] = node_int_in(14, "Grid Slices Y", 1, 10, 1, -600, 500)
    nodes["15"] = node_bool_in(15, "Snap to Grid", True, -600, 600)
    nodes["16"] = node_float_in(16, "Chase Speed", 0.1, 8.0, 1.5, -600, 700)
    nodes["17"] = node_color_in(17, "Chase Color", [1.0, 0.75, 0.2, 1.0], -600, 800)
    nodes["18"] = node_float_in(18, "Chase Intensity", 0.0, 1.0, 1.0, -600, 900)
    nodes["19"] = node_bool_in(19, "Bypass", False, -600, 1000)

    # Oscillators
    nodes["30"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": True}},
        "bounds": {"height": 130, "width": 195, "x": -350, "y": 200},
        "class": {"id": "77697265-F95F-41D8-8FC4-DF0DC56E1051", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.0}, "frequency": {"type": "float", "value": 1.5}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Saw Osc",
        "thumbnail_visible": True
    }
    conn(16, "output", 30, "frequency")

    nodes["31"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": True}},
        "bounds": {"height": 130, "width": 195, "x": -350, "y": 350},
        "class": {"id": "77697265-9890-41DC-A93D-9F3913A78FEB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.0}, "frequency": {"type": "float", "value": 1.5}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Bounce Osc",
        "thumbnail_visible": True
    }
    conn(16, "output", 31, "frequency")

    # Switch Bounce: 0=Saw, 1=Triangle -> raw_phase
    nodes["32"] = {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 100, "width": 195, "x": -100, "y": 250},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "selection": {"type": "integer", "value": 0}},
        "name": "Bounce Switch",
        "thumbnail_visible": True
    }
    conn(12, "output", 32, "selection")
    conn(30, "output", 32, "input0")
    conn(31, "output", 32, "input1")

    # 1.0 - raw_phase (Inverted)
    nodes["33"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "has-max": {"type": "bool", "value": False}, "has-min": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "unit": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
        "bounds": {"height": 50, "width": 80, "x": 120, "y": 150},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 1.0}},
        "name": "Const 1.0",
        "thumbnail_visible": False
    }
    nodes["34"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 230, "y": 150},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Invert Phase",
        "thumbnail_visible": True
    }
    conn(33, "output", 34, "input0")
    conn(32, "output", 34, "input1")

    # Center-Out Math: abs(phase - 0.5) * 2.0
    nodes["35"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 120, "y": 300},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.5}},
        "name": "Phase Sub 0.5",
        "thumbnail_visible": True
    }
    conn(32, "output", 35, "input0")

    # Direction Switch for Phase X (0: L->R, 1: R->L, 4: Center-Out, 5: Out-Center)
    nodes["36"] = {
        "attributes": make_attr_float_switch(8),
        "bounds": {"height": 180, "width": 195, "x": 400, "y": 100},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(8)},
        "name": "Switch Phase X",
        "thumbnail_visible": True
    }
    conn(11, "output", 36, "selection")
    conn(32, "output", 36, "input0") # 0: L->R
    conn(34, "output0", 36, "input1") # 1: R->L
    conn(32, "output", 36, "input4") # 4: Center->Out
    conn(34, "output0", 36, "input5") # 5: Out->Center

    # Direction Switch for Phase Y (2: U->D, 3: D->U, 6: Center-Out, 7: Out-Center)
    nodes["37"] = {
        "attributes": make_attr_float_switch(8),
        "bounds": {"height": 180, "width": 195, "x": 400, "y": 350},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(8)},
        "name": "Switch Phase Y",
        "thumbnail_visible": True
    }
    conn(11, "output", 37, "selection")
    conn(34, "output0", 37, "input2") # 2: U->D
    conn(32, "output", 37, "input3") # 3: D->U
    conn(32, "output", 37, "input6") # 6: Center->Out V
    conn(34, "output0", 37, "input7") # 7: Out->Center V

    # Grid Slice Width: 2.0 / Grid Slices X
    nodes["40"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "has-max": {"type": "bool", "value": False}, "has-min": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "unit": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
        "bounds": {"height": 50, "width": 80, "x": 620, "y": 550},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 2.0}},
        "name": "Canvas Width 2.0",
        "thumbnail_visible": False
    }
    nodes["41"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 730, "y": 550},
        "class": {"id": "77697265-0D55-485E-813D-706DD5DFE88D", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 2.0}, "input1": {"type": "float", "value": 5.0}},
        "name": "Slice Width Calc",
        "thumbnail_visible": True
    }
    conn(40, "output", 41, "input0")
    conn(13, "output", 41, "input1")

    # Quantize Phase X
    nodes["42"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "input0-type": {"type": "type", "value": "float"},
            "input1-type": {"type": "type", "value": "float"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 130, "x": 620, "y": 100},
        "class": {"id": "77697265-548F-4EF6-9B00-F3005FEC8687", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.4}},
        "name": "Quantize X",
        "thumbnail_visible": True
    }
    conn(36, "output", 42, "input0")
    conn(41, "output0", 42, "input1")

    # Continuous Coord X (-1.0 + Phase * 2.0)
    nodes["43"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 620, "y": 250},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 2.0}},
        "name": "Continuous Scale X",
        "thumbnail_visible": True
    }
    conn(36, "output", 43, "input0")
    conn(40, "output", 43, "input1")

    # Switch Snap X
    nodes["44"] = {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 100, "width": 195, "x": 800, "y": 150},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "selection": {"type": "integer", "value": 1}},
        "name": "Switch Snap X",
        "thumbnail_visible": True
    }
    conn(15, "output", 44, "selection")
    conn(43, "output0", 44, "input0")
    conn(42, "output0", 44, "input1")

    # Translation Vec2
    nodes["45"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 1020, "y": 200},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Translation Vec2",
        "thumbnail_visible": True
    }
    conn(44, "output", 45, "input0")

    # Rectangle Shape
    nodes["46"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": 1020, "y": 400},
        "class": {"id": "77697265-4db6-4573-8aa7-42362bc44931", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"height": {"type": "float", "value": 2.0}, "round": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]}, "width": {"type": "float", "value": 0.4}},
        "name": "Chase Bar Shape",
        "thumbnail_visible": True
    }
    conn(41, "output0", 46, "width")

    # Move Shape
    nodes["47"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "procedural"},
            "instances": {"type": "integer", "value": 1},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 58, "width": 195, "x": 1250, "y": 300},
        "class": {"id": "77697265-0e5a-4bfd-b136-e4f68P3cc463", "version": 3},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {"input": {"type": "procedural", "value": None}, "translation": {"type": "float2", "value": [0.0, 0.0]}},
        "name": "Move Beam",
        "thumbnail_visible": True
    }
    conn(46, "output", 47, "input")
    conn(45, "output", 47, "translation")

    # Render Beam
    nodes["48"] = {
        "attributes": {
            "aa-blend": {"type": "bool", "value": False},
            "bitdepth": {"type": "integer", "value": 0},
            "camera-type": {"type": "type", "value": "float"},
            "instances": {"type": "integer", "value": 1},
            "material-dimensions": {"type": "integer", "value": 1},
            "material-type": {"type": "type", "value": "color"},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]},
            "shape-dimensions": {"type": "integer", "value": 1},
            "shape-type": {"type": "type", "value": "procedural"}
        },
        "bounds": {"height": 82, "width": 195, "x": 1250, "y": 450},
        "class": {"id": "77697265-EA26-47D6-985A-B4D5DC314BF7", "version": 2},
        "clock": "video",
        "color": "ff2dc18a",
        "constants": {"material": {"type": "color", "value": [1.0, 0.75, 0.2, 1.0]}, "shape": {"type": "procedural", "value": None}},
        "name": "Render Beam",
        "thumbnail_visible": True
    }
    conn(47, "output", 48, "shape")
    conn(17, "output", 48, "material")

    # Gate: Chase (10) * Intensity (18)
    nodes["49"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 1250, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Chase Gate",
        "thumbnail_visible": True
    }
    conn(10, "output", 49, "input0")
    conn(18, "output", 49, "input1")

    # Video Mixer for Beam
    nodes["50"] = node_video_mixer(50, 11, 1500, 0)
    conn(0, "output", 50, "input1")
    conn(48, "output0", 50, "input2")
    conn(49, "output0", 50, "opacity2")

    # Video Mixer for Bypass Switch
    nodes["51"] = node_video_mixer(51, 0, 1750, 0)
    conn(50, "output", 51, "input1")
    conn(0, "output", 51, "input2")
    conn(19, "output", 51, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 2000, 0)
    conn(51, "output", 1, "input")

    return patch

# =============================================================================
# 3. BUILD ZZ-WIPER (Full Screen Scanner Beam, Continuous, No Grid)
# =============================================================================
def build_zz_wiper():
    patch = base_patch(
        "zz-wiper",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e250",
        "IP26 Modular Suite: Full-Screen Continuous Scanner Beam & Curtain Wipe (Piano Mode).",
        ["ip26", "wiper", "curtain", "scanner", "beam", "continuous", "worship"],
        [0, 10, 11, 12, 13, 14, 15, 16, 17]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Wiper (Hold)", False, -600, 150)
    nodes["11"] = node_int_in(11, "Direction", 0, 5, 0, -600, 250) # 0: L->R, 1: R->L, 2: U->D, 3: D->U, 4: Center->Out, 5: Out->Center
    nodes["12"] = node_bool_in(12, "Bounce", False, -600, 350)
    nodes["13"] = node_float_in(13, "Wipe Speed", 0.1, 6.0, 1.2, -600, 450)
    nodes["14"] = node_float_in(14, "Bar Width", 0.02, 1.0, 0.35, -600, 550)
    nodes["15"] = node_color_in(15, "Bar Color", [1.0, 1.0, 1.0, 1.0], -600, 650)
    nodes["16"] = node_float_in(16, "Wipe Intensity", 0.0, 1.0, 1.0, -600, 750)
    nodes["17"] = node_bool_in(17, "Bypass", False, -600, 850)

    # Oscillators
    nodes["20"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": -350, "y": 200},
        "class": {"id": "77697265-F95F-41D8-8FC4-DF0DC56E1051", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.0}, "frequency": {"type": "float", "value": 1.2}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Saw Forward",
        "thumbnail_visible": True
    }
    conn(13, "output", 20, "frequency")

    nodes["21"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": -350, "y": 350},
        "class": {"id": "77697265-9890-41DC-A93D-9F3913A78FEB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.0}, "frequency": {"type": "float", "value": 1.2}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Bounce Osc",
        "thumbnail_visible": True
    }
    conn(13, "output", 21, "frequency")

    # Switch Bounce: 0=Saw, 1=Triangle
    nodes["22"] = {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 100, "width": 195, "x": -100, "y": 250},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "selection": {"type": "integer", "value": 0}},
        "name": "Bounce Switch",
        "thumbnail_visible": True
    }
    conn(12, "output", 22, "selection")
    conn(20, "output", 22, "input0")
    conn(21, "output", 22, "input1")

    # Inverted Saw (* -1.0)
    nodes["23"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 150, "y": 250},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": -1.0}},
        "name": "Invert Direction",
        "thumbnail_visible": True
    }
    conn(22, "output", 23, "input0")

    # Switch Direction (Translation X)
    nodes["24"] = {
        "attributes": make_attr_float_switch(6),
        "bounds": {"height": 150, "width": 195, "x": 350, "y": 150},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(6)},
        "name": "Switch Trans X",
        "thumbnail_visible": True
    }
    conn(11, "output", 24, "selection")
    conn(22, "output", 24, "input0") # 0: L->R
    conn(23, "output0", 24, "input1") # 1: R->L

    # Switch Direction (Translation Y)
    nodes["25"] = {
        "attributes": make_attr_float_switch(6),
        "bounds": {"height": 150, "width": 195, "x": 350, "y": 350},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(6)},
        "name": "Switch Trans Y",
        "thumbnail_visible": True
    }
    conn(11, "output", 25, "selection")
    conn(23, "output0", 25, "input2") # 2: U->D
    conn(22, "output", 25, "input3") # 3: D->U

    # Translation Vec2
    nodes["26"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 580, "y": 250},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Translation Vec2",
        "thumbnail_visible": True
    }
    conn(24, "output", 26, "input0")
    conn(25, "output", 26, "input1")

    # Switch Bar Width & Height
    nodes["27"] = {
        "attributes": make_attr_float_switch(6),
        "bounds": {"height": 150, "width": 195, "x": 350, "y": 550},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.35}, "input1": {"type": "float", "value": 0.35}, "input2": {"type": "float", "value": 2.0}, "input3": {"type": "float", "value": 2.0}, "input4": {"type": "float", "value": 0.35}, "input5": {"type": "float", "value": 0.35}},
        "name": "Switch Bar Width",
        "thumbnail_visible": True
    }
    conn(11, "output", 27, "selection")
    conn(14, "output", 27, "input0")
    conn(14, "output", 27, "input1")
    conn(14, "output", 27, "input4")
    conn(14, "output", 27, "input5")

    nodes["28"] = {
        "attributes": make_attr_float_switch(6),
        "bounds": {"height": 150, "width": 195, "x": 350, "y": 750},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 2.0}, "input1": {"type": "float", "value": 2.0}, "input2": {"type": "float", "value": 0.35}, "input3": {"type": "float", "value": 0.35}, "input4": {"type": "float", "value": 2.0}, "input5": {"type": "float", "value": 2.0}},
        "name": "Switch Bar Height",
        "thumbnail_visible": True
    }
    conn(11, "output", 28, "selection")
    conn(14, "output", 28, "input2")
    conn(14, "output", 28, "input3")

    # Procedural Rectangle
    nodes["29"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": 580, "y": 600},
        "class": {"id": "77697265-4db6-4573-8aa7-42362bc44931", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"height": {"type": "float", "value": 2.0}, "round": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]}, "width": {"type": "float", "value": 0.35}},
        "name": "Wiper Bar Shape",
        "thumbnail_visible": True
    }
    conn(27, "output", 29, "width")
    conn(28, "output", 29, "height")

    # Move Shape
    nodes["30"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "procedural"},
            "instances": {"type": "integer", "value": 1},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 58, "width": 195, "x": 800, "y": 450},
        "class": {"id": "77697265-0e5a-4bfd-b136-e4f68P3cc463", "version": 3},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {"input": {"type": "procedural", "value": None}, "translation": {"type": "float2", "value": [0.0, 0.0]}},
        "name": "Move Beam",
        "thumbnail_visible": True
    }
    conn(29, "output", 30, "input")
    conn(26, "output", 30, "translation")

    # Render Beam
    nodes["31"] = {
        "attributes": {
            "aa-blend": {"type": "bool", "value": False},
            "bitdepth": {"type": "integer", "value": 0},
            "camera-type": {"type": "type", "value": "float"},
            "instances": {"type": "integer", "value": 1},
            "material-dimensions": {"type": "integer", "value": 1},
            "material-type": {"type": "type", "value": "color"},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]},
            "shape-dimensions": {"type": "integer", "value": 1},
            "shape-type": {"type": "type", "value": "procedural"}
        },
        "bounds": {"height": 82, "width": 195, "x": 1050, "y": 450},
        "class": {"id": "77697265-EA26-47D6-985A-B4D5DC314BF7", "version": 2},
        "clock": "video",
        "color": "ff2dc18a",
        "constants": {"material": {"type": "color", "value": [1.0, 1.0, 1.0, 1.0]}, "shape": {"type": "procedural", "value": None}},
        "name": "Render Beam",
        "thumbnail_visible": True
    }
    conn(30, "output", 31, "shape")
    conn(15, "output", 31, "material")

    # Wiper Gate: Wiper (10) * Intensity (16)
    nodes["32"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 1050, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Wiper Gate",
        "thumbnail_visible": True
    }
    conn(10, "output", 32, "input0")
    conn(16, "output", 32, "input1")

    # Video Mixer for Wiper (Add mode 11)
    nodes["33"] = node_video_mixer(33, 11, 1300, 0)
    conn(0, "output", 33, "input1")
    conn(31, "output0", 33, "input2")
    conn(32, "output0", 33, "opacity2")

    # Video Mixer for Bypass Switch
    nodes["34"] = node_video_mixer(34, 0, 1550, 0)
    conn(33, "output", 34, "input1")
    conn(0, "output", 34, "input2")
    conn(17, "output", 34, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 1800, 0)
    conn(34, "output", 1, "input")

    return patch

# =============================================================================
# 4. BUILD ZZ-STROBE (Stock Strobe Reimagined with Piano Hold & Flash/Blackout/Invert)
# =============================================================================
def build_zz_strobe():
    patch = base_patch(
        "zz-strobe",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e230",
        "IP26 Modular Suite: High-Speed Multi-Rate Flash Strobe (Piano Hold & Modes).",
        ["ip26", "strobe", "flash", "speed", "pulse", "blackout", "worship"],
        [0, 10, 11, 12, 13, 14, 15]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Strobe (Hold)", False, -600, 150)
    nodes["11"] = node_float_in(11, "Strobe Rate", 2.0, 30.0, 14.0, -600, 250)
    nodes["12"] = node_int_in(12, "Strobe Mode", 0, 2, 0, -600, 350) # 0: Flash (Add), 1: Blackout Cut, 2: Invert
    nodes["13"] = node_color_in(13, "Strobe Color", [1.0, 1.0, 1.0, 1.0], -600, 450)
    nodes["14"] = node_float_in(14, "Strobe Intensity", 0.0, 1.0, 1.0, -600, 550)
    nodes["15"] = node_bool_in(15, "Bypass", False, -600, 650)

    # Pulse Clock Oscillator
    nodes["20"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": True}},
        "bounds": {"height": 130, "width": 195, "x": -350, "y": 200},
        "class": {"id": "77697265-6256-4856-911C-5465AE6BF656", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "amplitude": {"type": "float", "value": 1.0},
            "frequency": {"type": "float", "value": 14.0},
            "offset": {"type": "float", "value": 0.0},
            "phase-offset": {"type": "float", "value": 0.0},
            "pulse-width": {"type": "float", "value": 0.5},
            "reset-phase": {"type": "trigger", "value": None}
        },
        "name": "Pulse Clock",
        "thumbnail_visible": True
    }
    conn(11, "output", 20, "frequency")

    # Strobe Active Gate: Strobe (10) * Pulse (20)
    nodes["21"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": -100, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Gate Pulse",
        "thumbnail_visible": True
    }
    conn(10, "output", 21, "input0")
    conn(20, "output", 21, "input1")

    # Multiply with Strobe Intensity
    nodes["22"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 100, "y": 250},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Final Strobe Opacity",
        "thumbnail_visible": True
    }
    conn(21, "output0", 22, "input0")
    conn(14, "output", 22, "input1")

    # Solid Color Source
    nodes["23"] = {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 58, "width": 195, "x": 100, "y": 400},
        "class": {"id": "77697265-E8EC-4F1B-901A-CFFC104D3B07", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"bypass": {"type": "bool", "value": False}, "color": {"type": "color", "value": [1.0, 1.0, 1.0, 1.0]}},
        "name": "Strobe Color Source",
        "thumbnail_visible": True
    }
    conn(13, "output", 23, "color")

    # Video Mixer (Add mode 11)
    nodes["24"] = node_video_mixer(24, 11, 350, 0)
    conn(0, "output", 24, "input1")
    conn(23, "output", 24, "input2")
    conn(22, "output0", 24, "opacity2")

    # Video Mixer for Bypass Switch
    nodes["25"] = node_video_mixer(25, 0, 600, 0)
    conn(24, "output", 25, "input1")
    conn(0, "output", 25, "input2")
    conn(15, "output", 25, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 850, 0)
    conn(25, "output", 1, "input")

    return patch

# =============================================================================
# 5. BUILD ZZ-STROKE (Animated Snake Running Along Screen Perimeter with Fading Tail)
# =============================================================================
def build_zz_stroke():
    patch = base_patch(
        "zz-stroke",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e260",
        "IP26 Modular Suite: Animated Snake Border Running Around Screen Perimeter with Fading Tail (Piano Mode).",
        ["ip26", "stroke", "snake", "border", "inline", "perimeter", "glow", "worship"],
        [0, 10, 11, 12, 13, 14, 15, 16]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Stroke (Hold)", False, -600, 100)
    nodes["11"] = node_float_in(11, "Stroke Width", 0.005, 0.08, 0.025, -600, 200)
    nodes["12"] = node_float_in(12, "Snake Speed", 0.1, 4.0, 1.0, -600, 300)
    nodes["13"] = node_int_in(13, "Direction", 0, 1, 0, -600, 400) # 0: Clockwise, 1: Counter-Clockwise
    nodes["14"] = node_color_in(14, "Stroke Color", [0.0, 0.9, 1.0, 1.0], -600, 500)
    nodes["15"] = node_float_in(15, "Stroke Intensity", 0.0, 1.0, 1.0, -600, 600)
    nodes["16"] = node_bool_in(16, "Bypass", False, -600, 700)

    # 1. Outer Screen Rectangle (Normalized Full Canvas 2.0 x 2.0)
    nodes["20"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": -350, "y": 200},
        "class": {"id": "77697265-4db6-4573-8aa7-42362bc44931", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"height": {"type": "float", "value": 2.0}, "round": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]}, "width": {"type": "float", "value": 2.0}},
        "name": "Screen Rect",
        "thumbnail_visible": True
    }

    # 2. Edge Node: Converts full rectangle into perimeter border stroke frame
    nodes["21"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}, "mode": {"type": "integer", "value": 0}},
        "bounds": {"height": 58, "width": 195, "x": -100, "y": 200},
        "class": {"id": "77697265-ab950887-37ee-4fd2-9487-c856b6b75c83", "version": 2},
        "clock": "video",
        "color": "fff26eb5",
        "constants": {"input": {"type": "procedural", "value": None}, "thickness": {"type": "float", "value": 0.025}},
        "name": "Border Stroke",
        "thumbnail_visible": True
    }
    conn(20, "output", 21, "input")
    conn(11, "output", 21, "thickness")

    # 3. Shape Render: Renders the border frame texture (relative resolution mode 0)
    nodes["22"] = {
        "attributes": {
            "antialising-direction": {"type": "integer", "value": 0},
            "antialiasing": {"type": "float", "value": 4.0},
            "bitdepth": {"type": "integer", "value": 0},
            "material-dimensions": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]},
            "shape-dimensions": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 195, "x": 150, "y": 200},
        "class": {"id": "77697265-EA26-47D6-985A-B4D5DC314BF7", "version": 2},
        "clock": "video",
        "color": "ff2dc18a",
        "constants": {"material": {"type": "float4", "value": [1.0, 1.0, 1.0, 1.0]}, "shape": {"type": "procedural", "value": None}},
        "name": "Render Frame",
        "thumbnail_visible": True
    }
    conn(21, "output", 22, "shape")

    # 4. Sweep / Conical Gradient: Head=White [1,1,1,1], Tail=Transparent/Black [0,0,0,0]
    nodes["23"] = {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "method": {"type": "integer", "value": 0},
            "mode": {"type": "integer", "value": 0},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]},
            "type": {"type": "integer", "value": 2}
        },
        "bounds": {"height": 82, "width": 195, "x": -100, "y": 450},
        "class": {"id": "77697265-FCE2-4EBE-8C81-99C578524A24", "version": 1},
        "clock": "video",
        "color": "fff26eb5",
        "constants": {
            "bypass": {"type": "bool", "value": False},
            "color1": {"type": "float4", "value": [1.0, 1.0, 1.0, 1.0]},
            "color2": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]},
            "dither": {"type": "float", "value": 0.0}
        },
        "name": "Snake Sweep Gradient",
        "thumbnail_visible": True
    }

    # 5. Rotation Oscillator (Saw)
    nodes["24"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": -350, "y": 600},
        "class": {"id": "77697265-F95F-41D8-8FC4-DF0DC56E1051", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.0}, "frequency": {"type": "float", "value": 1.0}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Rotation Osc",
        "thumbnail_visible": True
    }
    conn(12, "output", 24, "frequency")

    # Inverted Saw (* -1.0) for Counter-Clockwise
    nodes["25"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": -100, "y": 650},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": -1.0}},
        "name": "Invert Rotation",
        "thumbnail_visible": True
    }
    conn(24, "output", 25, "input0")

    # Switch Direction (0=CW, 1=CCW)
    nodes["26"] = {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 100, "width": 195, "x": 100, "y": 600},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "selection": {"type": "integer", "value": 0}},
        "name": "Direction Switch",
        "thumbnail_visible": True
    }
    conn(13, "output", 26, "selection")
    conn(24, "output", 26, "input0")
    conn(25, "output0", 26, "input1")

    # 6. Transform: Rotate the Sweep Gradient around center
    nodes["27"] = {
        "attributes": {
            "anchor-type": {"type": "type", "value": "float2"},
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "texture2d"},
            "instances": {"type": "integer", "value": 1},
            "rotation-type": {"type": "type", "value": "float"},
            "scale-type": {"type": "type", "value": "float2"},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 130, "width": 195, "x": 150, "y": 450},
        "class": {"id": "77697265-9225-4009-9D2D-5F898E94CC33", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"anchor": {"type": "float2", "value": [0.0, 0.0]}, "input": {"type": "texture2d", "value": None}, "rotation": {"type": "float", "value": 0.0}, "scale": {"type": "float2", "value": [1.0, 1.0]}, "translation": {"type": "float2", "value": [0.0, 0.0]}},
        "name": "Rotate Sweep",
        "thumbnail_visible": True
    }
    conn(23, "output", 27, "input")
    conn(26, "output", 27, "rotation")

    # 7. Mask Mixer: Border Frame * Rotating Gradient (Multiply mode 0)
    nodes["28"] = node_video_mixer(28, 0, 420, 300)
    conn(22, "output0", 28, "input1")
    conn(27, "output0", 28, "input2")
    # Both opacities 1.0

    # 8. Colorize the Snake: Multiply with Stroke Color
    nodes["29"] = {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 58, "width": 195, "x": 420, "y": 550},
        "class": {"id": "77697265-E8EC-4F1B-901A-CFFC104D3B07", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"bypass": {"type": "bool", "value": False}, "color": {"type": "color", "value": [0.0, 0.9, 1.0, 1.0]}},
        "name": "Neon Color Source",
        "thumbnail_visible": True
    }
    conn(14, "output", 29, "color")

    nodes["30"] = node_video_mixer(30, 0, 680, 300)
    conn(28, "output", 30, "input1")
    conn(29, "output", 30, "input2")

    # 9. Gate: Stroke (10) * Stroke Intensity (15)
    nodes["31"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 680, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Stroke Gate",
        "thumbnail_visible": True
    }
    conn(10, "output", 31, "input0")
    conn(15, "output", 31, "input1")

    # 10. Blend Snake over Texture In (Add mode 11)
    nodes["32"] = node_video_mixer(32, 11, 950, 0)
    conn(0, "output", 32, "input1")
    conn(30, "output", 32, "input2")
    conn(31, "output0", 32, "opacity2")

    # 11. Bypass Switch
    nodes["33"] = node_video_mixer(33, 0, 1200, 0)
    conn(32, "output", 33, "input1")
    conn(0, "output", 33, "input2")
    conn(16, "output", 33, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 1450, 0)
    conn(33, "output", 1, "input")

    return patch

# =============================================================================
# MAIN BUILD & COMPILE PIPELINE
# =============================================================================
def main():
    target_dir = r"C:\ANDREAS\ip26-zzfx"
    os.chdir(target_dir)

    modules = [
        ("zz-pusher", "zz_pusher.wire", "zz_pusher.cwired", build_zz_pusher),
        ("zz-chaser", "zz_chaser.wire", "zz_chaser.cwired", build_zz_chaser),
        ("zz-strobe", "zz_strobe.wire", "zz_strobe.cwired", build_zz_strobe),
        ("zz-stroke", "zz_stroke.wire", "zz_stroke.cwired", build_zz_stroke),
        ("zz-wiper", "zz_wiper.wire", "zz_wiper.cwired", build_zz_wiper),
    ]

    HIDDEN_MAP = {
        ('77697265-999C-4F8B-8B9D-3646DC68AA69', 2): ['input', 'instances', 'flow', 'bool-view'],
        ('77697265-D235-4A6A-B661-02ABE55C72FF', 3): ['input', 'instances', 'flow', 'has-min', 'min', 'has-max', 'max', 'options-count', 'widget', 'unit'],
        ('77697265-A270-4D60-911C-A88B1BE6369A', 3): ['bypass', 'input-count', 'bitdepth', 'resolution-absolute', 'resolution-relative', 'resolution-mode', 'instances'],
        ('77697265-A9AF-4CB4-B10F-3968B36BB63B', 1): ['size', 'input0-dimensions', 'input1-dimensions', 'type0', 'type1', 'flow'],
        ('77697265-7557-4053-ABEC-73E2A9786804', 2): ['value-type', 'min-type', 'max-type', 'flow', 'value-dimensions', 'min-dimensions', 'max-dimensions'],
        ('77697265-A0D8-429A-A558-69BC58D0D425', 1): ['size', 'input0-dimensions', 'input1-dimensions', 'type0', 'type1', 'flow'],
        ('77697265-86ce-4e85-a02d-34f915fca74e', 1): ['input0-type', 'instances'],
        ('77697265-9225-4009-9D2D-5F898E94CC33', 2): ['flow', 'input-type', 'translation-type', 'rotation-type', 'scale-type', 'anchor-type', 'instances'],
        ('77697265-4C9E-4F75-B4F0-5415B713EA1B', 3): ['input', 'instances', 'flow', 'options-count', 'widget'],
        ('77697265-2649-4abb-b38f-4e1005183415', 2): ['input', 'instances', 'flow', 'has-min', 'min', 'has-max', 'max', 'options-count', 'widget', 'unit'],
        ('77697265-0D55-485E-813D-706DD5DFE88D', 1): ['flow', 'size', 'type0', 'input0-dimensions', 'type1', 'input1-dimensions'],
        ('77697265-F95F-41D8-8FC4-DF0DC56E1051', 1): ['instances', 'reset-phase', 'unipolar', 'anti-alias', 'amplitude', 'offset', 'phase-offset'],
        ('77697265-1296-4264-A646-5CE3BE529286', 1): ['input0-type', 'flow', 'input0-dimensions'],
        ('77697265-9890-41DC-A93D-9F3913A78FEB', 1): ['instances', 'reset-phase', 'unipolar', 'anti-alias', 'amplitude', 'offset', 'phase-offset'],
        ('77697265-6899-4A9C-82AB-949346033440', 3): ['selection-type', 'case-type', 'flow', 'size', 'instances'],
        ('77697265-548F-4EF6-9B00-F3005FEC8687', 1): ['input0-type', 'input1-type', 'flow', 'input0-dimensions', 'input1-dimensions'],
        ('77697265-4db6-4573-8aa7-42362bc44931', 2): ['instances', 'round'],
        ('77697265-0e5a-4bfd-b136-e4f68P3cc463', 3): ['input-type', 'translation-type', 'flow', 'instances'],
        ('77697265-EA26-47D6-985A-B4D5DC314BF7', 2): ['antialising-direction', 'antialiasing', 'shape-dimensions', 'material-dimensions', 'resolution-mode', 'resolution-relative', 'resolution-absolute', 'bitdepth'],
        ('77697265-6256-4856-911C-5465AE6BF656', 1): ['instances', 'reset-phase', 'unipolar', 'anti-alias', 'amplitude', 'offset', 'phase-offset', 'pulse-width'],
        ('77697265-E8EC-4F1B-901A-CFFC104D3B07', 1): ['instances', 'bypass', 'bitdepth', 'resolution-absolute', 'resolution-relative', 'resolution-mode'],
        ('77697265-ab950887-37ee-4fd2-9487-c856b6b75c83', 2): ['mode', 'instances'],
        ('77697265-FCE2-4EBE-8C81-99C578524A24', 1): ['bypass', 'dither', 'resolution-mode', 'resolution-relative', 'resolution-absolute', 'bitdepth', 'method', 'type', 'mode'],
        ('77697265-D980-43B3-9237-6683B154A5B0', 1): ['restart-at-zero', 'linear', 'instances', 'is-done'],
        ('77697265-e61f-42c0-862a-0dca04e14569', 1): ['input', 'instances', 'flow']
    }

    wire_dir = os.path.join(target_dir, "wire")
    cwired_dir = os.path.join(target_dir, "cwired")
    os.makedirs(wire_dir, exist_ok=True)
    os.makedirs(cwired_dir, exist_ok=True)

    # Clean up old outliner files
    for old_f in ["zz_outliner.wire", "zz_outliner.cwired"]:
        p1 = os.path.join(wire_dir, old_f)
        p2 = os.path.join(cwired_dir, old_f)
        if os.path.exists(p1): os.remove(p1)
        if os.path.exists(p2): os.remove(p2)

    print("=== BUILDING ZZ-SUITE PURE MODULAR PLUGINS ===")
    for name, wire_file, cwired_file, builder in modules:
        wire_path = os.path.join(wire_dir, wire_file)
        cwired_path = os.path.join(cwired_dir, cwired_file)
        print(f"Generating {wire_file}...")
        patch_data = builder()
        for nid, n in patch_data["patch"]["nodes"].items():
            cid = n.get("class", {}).get("id")
            cver = n.get("class", {}).get("version")
            if (cid, cver) in HIDDEN_MAP and "hidden" not in n:
                n["hidden"] = list(HIDDEN_MAP[(cid, cver)])
            if cid == "77697265-6899-4A9C-82AB-949346033440": # Switch node
                if "selection" not in n.get("constants", {}):
                    n.setdefault("constants", {})["selection"] = {"type": "integer", "value": 0}
        with open(wire_path, "w", encoding="utf-8") as f:
            json.dump(patch_data, f, indent=2)
        print(f"  -> Generated {wire_path} ({len(patch_data['patch']['nodes'])} nodes, {len(patch_data['patch']['connections'])} connections)")

    print("\n=== COMPILING WITH WIRE CLI ===")
    wire_exe = r"C:\Program Files\Resolume Wire\Wire.exe"
    for name, wire_file, cwired_file, builder in modules:
        wire_path = os.path.join(wire_dir, wire_file)
        cwired_path = os.path.join(cwired_dir, cwired_file)
        if os.path.exists(cwired_path):
            try:
                os.remove(cwired_path)
            except:
                pass
        print(f"Compiling {wire_file} -> {cwired_file}...")
        try:
            res = subprocess.run([wire_exe, "compile", wire_path, "-o", cwired_path], capture_output=True, text=True, timeout=60)
            if os.path.exists(cwired_path):
                size = os.path.getsize(cwired_path)
                print(f"  [SUCCESS] {cwired_file} compiled successfully! ({size} bytes)")
            else:
                print(f"  [FAILED] {cwired_file} was not created!")
                lines = (res.stdout + res.stderr).splitlines()
                for l in lines[-10:]:
                    print("   ", l)
        except Exception as e:
            print(f"  [ERROR] {e}")

if __name__ == "__main__":
    main()
