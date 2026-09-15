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
                "version": "2.0.0"
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

def node_texture_out(nid, x=1600, y=0):
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

def node_color_in(nid, name, def_rgba, x=-600, y=400):
    return {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 140, "x": x, "y": y},
        "class": {"id": "77697265-4C9E-4F75-B4F0-5415B713EA1B", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "color", "value": list(def_rgba)}},
        "hidden": ["input", "instances", "flow", "options-count", "widget"],
        "name": name,
        "thumbnail_visible": True
    }

def node_video_mixer(nid, mode=0, x=1000, y=0, op2=0.0):
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
            "opacity2": {"type": "float", "value": float(op2)}
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
    nodes["12"] = node_float_in(12, "Push Amount", 0.0, 1.5, 0.45, -600, 300)
    nodes["13"] = node_float_in(13, "Push Decay", 0.05, 1.5, 0.25, -600, 400)
    nodes["14"] = node_float_in(14, "Flash Intensity", 0.0, 1.0, 0.50, -600, 500)
    nodes["15"] = node_color_in(15, "Flash Color", [1.0, 1.0, 1.0, 1.0], -600, 600)
    nodes["16"] = node_bool_in(16, "Bypass", False, -600, 700)

    # Trigger Envelope via Attack Release (0.0s instant attack, linear = True, restart-at-zero = True)
    nodes["20"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 130, "width": 195, "x": -350, "y": 100},
        "class": {"id": "77697265-D980-43B3-9237-6683B154A5B0", "version": 1},
        "clock": "video",
        "color": "fff26eb5",
        "constants": {
            "attack-time": {"type": "float", "value": 0.0},
            "linear": {"type": "bool", "value": True},
            "release": {"type": "trigger", "value": None},
            "release-time": {"type": "float", "value": 0.25},
            "reset": {"type": "trigger", "value": None},
            "restart-at-zero": {"type": "bool", "value": True},
            "trigger": {"type": "trigger", "value": None}
        },
        "name": "Punch Envelope",
        "thumbnail_visible": True
    }
    conn(10, "output", 20, "trigger")
    conn(13, "output", 20, "release-time")

    # Push Bool to Float (Switch node: 0 -> 0.0, 1 -> 1.0)
    nodes["21"] = {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 80, "width": 130, "x": -350, "y": 250},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 1.0}, "selection": {"type": "integer", "value": 0}},
        "name": "Bool To Float",
        "thumbnail_visible": False
    }
    conn(11, "output", 21, "selection")

    # Piano Push Smooth
    nodes["22"] = {
        "attributes": {"input0-type": {"type": "type", "value": "float"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 58, "width": 195, "x": -200, "y": 250},
        "class": {"id": "77697265-86ce-4e85-a02d-34f915fca74e", "version": 1},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"duration": {"type": "float", "value": 0.25}, "input0": {"type": "float", "value": 0.0}},
        "name": "Push Smooth",
        "thumbnail_visible": True
    }
    conn(21, "output", 22, "input0")
    conn(13, "output", 22, "duration")

    # Combine Envelopes: Add 20 + 22
    nodes["23"] = {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 0, "y": 150},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Total Env Add",
        "thumbnail_visible": True
    }
    conn(20, "output", 23, "input0")
    conn(22, "output0", 23, "input1")

    # Clamp Env to 0..1 (Note outlet is output0!)
    nodes["24"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "max-dimensions": {"type": "integer", "value": 1},
            "max-type": {"type": "type", "value": "float"},
            "min-dimensions": {"type": "integer", "value": 1},
            "min-type": {"type": "type", "value": "float"},
            "value-dimensions": {"type": "integer", "value": 1},
            "value-type": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 150, "y": 150},
        "class": {"id": "77697265-7557-4053-ABEC-73E2A9786804", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"max": {"type": "float", "value": 1.0}, "min": {"type": "float", "value": 0.0}, "value": {"type": "float", "value": 0.0}},
        "name": "Clamp Env",
        "thumbnail_visible": True
    }
    conn(23, "output0", 24, "value")

    # Target Zoom: Clamp Env (output0) * Push Amount
    nodes["25"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 320, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Zoom Mult",
        "thumbnail_visible": True
    }
    conn(24, "output0", 25, "input0")
    conn(12, "output", 25, "input1")

    # Total Scale: 1.0 + Zoom Mult
    nodes["26"] = {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 480, "y": 150},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Total Scale Add",
        "thumbnail_visible": True
    }
    conn(25, "output0", 26, "input1")

    # Scale Vec2
    nodes["27"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 640, "y": 150},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 1.0}},
        "name": "Scale Vec2",
        "thumbnail_visible": True
    }
    conn(26, "output0", 27, "input0")
    conn(26, "output0", 27, "input1")

    # Transform (Centered Zoom)
    nodes["28"] = {
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
    conn(0, "output", 28, "input")
    conn(27, "output", 28, "scale")

    # Flash Source (Solid Color)
    nodes["29"] = {
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
    conn(15, "output", 29, "color")

    # Flash Opacity = Clamp Env (output0) * Flash Intensity
    nodes["30"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 640, "y": 350},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Flash Opacity Calc",
        "thumbnail_visible": True
    }
    conn(24, "output0", 30, "input0")
    conn(14, "output", 30, "input1")

    # Video Mixer for Flash (Add mode 11)
    nodes["31"] = node_video_mixer(31, 11, 1050, 0)
    conn(28, "output0", 31, "input1")
    conn(29, "output", 31, "input2")
    conn(30, "output0", 31, "opacity2")

    # Video Mixer for Bypass Switch
    nodes["32"] = node_video_mixer(32, 0, 1300, 0)
    conn(31, "output", 32, "input1")
    conn(0, "output", 32, "input2")
    conn(16, "output", 32, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 1550, 0)
    conn(32, "output", 1, "input")

    return patch

# =============================================================================
# 2. BUILD ZZ-CHASER (1-Screen Full Screen Left-to-Right, Custom Grid 1-10, Bounce)
# =============================================================================
def build_zz_chaser():
    patch = base_patch(
        "zz-chaser",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e220",
        "IP26 Modular Suite: 1-Screen Dedicated Piano Chaser with Full L-to-R Grid Coverage & Bounce.",
        ["ip26", "chaser", "grid", "slices", "runner", "bounce", "worship"],
        [0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Chase (Hold)", True, -600, 100)
    nodes["11"] = node_int_in(11, "Direction", 0, 5, 0, -600, 200) # 0: L->R, 1: R->L, 2: U->D, 3: D->U, 4: Center->Out, 5: Out->Center
    nodes["12"] = node_bool_in(12, "Bounce", False, -600, 300)
    nodes["13"] = node_int_in(13, "Grid Slices X", 1, 10, 5, -600, 400)
    nodes["14"] = node_int_in(14, "Grid Slices Y", 1, 10, 1, -600, 500)
    nodes["15"] = node_bool_in(15, "Snap to Grid", True, -600, 600)
    nodes["16"] = node_float_in(16, "Chase Speed", 0.1, 8.0, 1.5, -600, 700)
    nodes["17"] = node_color_in(17, "Chase Color", [1.0, 0.75, 0.2, 1.0], -600, 800)
    nodes["18"] = node_float_in(18, "Chase Intensity", 0.0, 1.0, 1.0, -600, 900)
    nodes["19"] = node_bool_in(19, "Bypass", False, -600, 1000)

    # Oscillators
    # Saw Osc (0..1)
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

    # Bounce Osc (Triangle 0..1..0)
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

    # Inverted Phase: 1.0 - raw_phase (Subtract: 1.0 - 32)
    nodes["33"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 120, "y": 200},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Invert Phase",
        "thumbnail_visible": True
    }
    conn(32, "output", 33, "input1")

    # Center-Out Phase: raw_phase * 0.5 + 0.5
    nodes["34"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 120, "y": 350},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.5}},
        "name": "Center Phase Mult",
        "thumbnail_visible": False
    }
    conn(32, "output", 34, "input0")

    nodes["35"] = {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 260, "y": 350},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.5}, "input1": {"type": "float", "value": 0.0}},
        "name": "Center-Out Phase",
        "thumbnail_visible": False
    }
    conn(34, "output0", 35, "input1")

    # Switch Phase: 0: L->R (32), 1: R->L (33), 2: U->D (33), 3: D->U (32), 4: Center->Out (35), 5: Out->Center (32)
    nodes["36"] = {
        "attributes": make_attr_float_switch(6),
        "bounds": {"height": 150, "width": 195, "x": 420, "y": 200},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(6)},
        "name": "Switch Phase",
        "thumbnail_visible": True
    }
    conn(11, "output", 36, "selection")
    conn(32, "output", 36, "input0") # 0: L->R
    conn(33, "output0", 36, "input1") # 1: R->L
    conn(33, "output0", 36, "input2") # 2: U->D
    conn(32, "output", 36, "input3") # 3: D->U
    conn(35, "output0", 36, "input4") # 4: Center->Out
    conn(33, "output0", 36, "input5") # 5: Out->Center

    # Slice Width: 2.0 / Grid Slices X (e.g. 2.0 / 5 = 0.4)
    nodes["40"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 640, "y": 300},
        "class": {"id": "77697265-0D55-485E-813D-706DD5DFE88D", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 2.0}, "input1": {"type": "float", "value": 5.0}},
        "name": "Slice Width Calc",
        "thumbnail_visible": True
    }
    conn(13, "output", 40, "input1")

    # Half Width: Slice Width / 2.0 (e.g. 0.2)
    nodes["41"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 780, "y": 300},
        "class": {"id": "77697265-0D55-485E-813D-706DD5DFE88D", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.4}, "input1": {"type": "float", "value": 2.0}},
        "name": "Half Width Calc",
        "thumbnail_visible": False
    }
    conn(40, "output0", 41, "input0")

    # Leftmost Coordinate = -1.0 + Half Width (e.g. -1.0 + 0.2 = -0.8)
    nodes["42"] = {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 920, "y": 300},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": -1.0}, "input1": {"type": "float", "value": 0.2}},
        "name": "Left Edge Coord",
        "thumbnail_visible": False
    }
    conn(41, "output0", 42, "input1")

    # Phase * 1.999 (scale phase across screen width)
    nodes["43"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 640, "y": 100},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 1.999}},
        "name": "Phase Mult 2",
        "thumbnail_visible": False
    }
    conn(36, "output", 43, "input0")

    # Quantize Phase X by Slice Width -> produces 0.0, 0.4, 0.8, 1.2, 1.6
    nodes["44"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "input0-type": {"type": "type", "value": "float"},
            "input1-type": {"type": "type", "value": "float"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 130, "x": 780, "y": 100},
        "class": {"id": "77697265-548F-4EF6-9B00-F3005FEC8687", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.4}},
        "name": "Quantize Step",
        "thumbnail_visible": True
    }
    conn(43, "output0", 44, "input0")
    conn(40, "output0", 44, "input1")

    # Snapped X Position = Left Edge + Quantize Step (-0.8 + [0.0, 0.4, 0.8, 1.2, 1.6] = -0.8, -0.4, 0.0, +0.4, +0.8)
    nodes["45"] = {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 1060, "y": 100},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": -0.8}, "input1": {"type": "float", "value": 0.0}},
        "name": "Snapped X Pos",
        "thumbnail_visible": True
    }
    conn(42, "output0", 45, "input0")
    conn(44, "output0", 45, "input1")

    # Total Travel Span = 2.0 - Slice Width (Subtract node: 2.0 - 40)
    nodes["46"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 780, "y": 450},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 2.0}, "input1": {"type": "float", "value": 0.4}},
        "name": "Travel Span Calc",
        "thumbnail_visible": False
    }
    conn(40, "output0", 46, "input1")

    # Continuous Move = Phase * Travel Span
    nodes["47"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 920, "y": 450},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 1.6}},
        "name": "Cont Move Calc",
        "thumbnail_visible": False
    }
    conn(36, "output", 47, "input0")
    conn(46, "output0", 47, "input1")

    # Continuous X Position = Left Edge + Cont Move
    nodes["48"] = {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 1060, "y": 450},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": -0.8}, "input1": {"type": "float", "value": 0.0}},
        "name": "Continuous X Pos",
        "thumbnail_visible": True
    }
    conn(42, "output0", 48, "input0")
    conn(47, "output0", 48, "input1")

    # Switch Snap X: 0 = Continuous (48), 1 = Snapped (45)
    nodes["49"] = {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 100, "width": 195, "x": 1220, "y": 250},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "selection": {"type": "integer", "value": 1}},
        "name": "Switch Snap Mode",
        "thumbnail_visible": True
    }
    conn(15, "output", 49, "selection")
    conn(48, "output0", 49, "input0")
    conn(45, "output0", 49, "input1")

    # Translation Vec2: [49, 0.0]
    nodes["50"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 1440, "y": 250},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Translation Vec2",
        "thumbnail_visible": True
    }
    conn(49, "output", 50, "input0")

    # Procedural Rectangle Bar
    nodes["51"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": 1440, "y": 450},
        "class": {"id": "77697265-4db6-4573-8aa7-42362bc44931", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"height": {"type": "float", "value": 2.0}, "round": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]}, "width": {"type": "float", "value": 0.4}},
        "name": "Chase Bar Shape",
        "thumbnail_visible": True
    }
    conn(40, "output0", 51, "width")

    # Move Shape
    nodes["52"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "procedural"},
            "instances": {"type": "integer", "value": 1},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 58, "width": 195, "x": 1660, "y": 350},
        "class": {"id": "77697265-0e5a-4bfd-b136-e4f68P3cc463", "version": 3},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {"input": {"type": "procedural", "value": None}, "translation": {"type": "float2", "value": [0.0, 0.0]}},
        "name": "Move Beam",
        "thumbnail_visible": True
    }
    conn(51, "output", 52, "input")
    conn(50, "output", 52, "translation")

    # Render Beam Texture
    nodes["53"] = {
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
        "bounds": {"height": 82, "width": 195, "x": 1660, "y": 500},
        "class": {"id": "77697265-EA26-47D6-985A-B4D5DC314BF7", "version": 2},
        "clock": "video",
        "color": "ff2dc18a",
        "constants": {"material": {"type": "color", "value": [1.0, 0.75, 0.2, 1.0]}, "shape": {"type": "procedural", "value": None}},
        "name": "Render Beam",
        "thumbnail_visible": True
    }
    conn(52, "output", 53, "shape")
    conn(17, "output", 53, "material")

    # Gate: Chase (Hold) * Intensity
    nodes["54"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 1660, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Chase Gate",
        "thumbnail_visible": True
    }
    conn(10, "output", 54, "input0")
    conn(18, "output", 54, "input1")

    # Video Mixer for Beam (Add mode 11)
    nodes["55"] = node_video_mixer(55, 11, 1900, 0)
    conn(0, "output", 55, "input1")
    conn(53, "output0", 55, "input2")
    conn(54, "output0", 55, "opacity2")

    # Video Mixer for Bypass Switch
    nodes["56"] = node_video_mixer(56, 0, 2150, 0)
    conn(55, "output", 56, "input1")
    conn(0, "output", 56, "input2")
    conn(19, "output", 56, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 2400, 0)
    conn(56, "output", 1, "input")

    return patch

# =============================================================================
# 3. BUILD ZZ-WIPER (Real Radiant Gradient Curtain Wipe - "Gradient tapi digeser")
# =============================================================================
def build_zz_wiper():
    patch = base_patch(
        "zz-wiper",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e250",
        "IP26 Modular Suite: Real Smooth Gradient Curtain Wipe (Moving Gradient Light Beam).",
        ["ip26", "wiper", "curtain", "scanner", "beam", "gradient", "worship"],
        [0, 10, 11, 12, 13, 14, 15, 16, 17]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Wiper (Hold)", True, -600, 150)
    nodes["11"] = node_int_in(11, "Direction", 0, 5, 0, -600, 250) # 0: L->R, 1: R->L, 2: U->D, 3: D->U, 4: Center->Out, 5: Out->Center
    nodes["12"] = node_bool_in(12, "Bounce", False, -600, 350)
    nodes["13"] = node_float_in(13, "Wipe Speed", 0.1, 6.0, 1.2, -600, 450)
    nodes["14"] = node_float_in(14, "Gradient Width", 0.2, 3.0, 1.0, -600, 550)
    nodes["15"] = node_color_in(15, "Wipe Color", [1.0, 1.0, 1.0, 1.0], -600, 650)
    nodes["16"] = node_float_in(16, "Wipe Intensity", 0.0, 1.0, 1.0, -600, 750)
    nodes["17"] = node_bool_in(17, "Bypass", False, -600, 850)

    # Oscillators
    # Saw Osc (0..1)
    nodes["20"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": -350, "y": 200},
        "class": {"id": "77697265-F95F-41D8-8FC4-DF0DC56E1051", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.5}, "frequency": {"type": "float", "value": 1.2}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Saw Osc",
        "thumbnail_visible": True
    }
    conn(13, "output", 20, "frequency")

    # Bounce Osc (Triangle -1.5 .. +1.5)
    nodes["21"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": -350, "y": 350},
        "class": {"id": "77697265-9890-41DC-A93D-9F3913A78FEB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.5}, "frequency": {"type": "float", "value": 1.2}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
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
        "name": "Invert Movement",
        "thumbnail_visible": True
    }
    conn(22, "output", 23, "input0")

    # Switch Translation X (0: L->R = 22, 1: R->L = 23, 2: 0, 3: 0, 4: 0, 5: 0)
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

    # Switch Translation Y (0: 0, 1: 0, 2: U->D = 23, 3: D->U = 22, 4: 0, 5: 0)
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

    # Radial Gradient Generator (Center peak with smooth falloff to transparent edges)
    nodes["27"] = {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "instances": {"type": "integer", "value": 1},
            "method": {"type": "integer", "value": 0},
            "mode": {"type": "integer", "value": 0},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]},
            "type": {"type": "integer", "value": 1} # Radial Gradient
        },
        "bounds": {"height": 106, "width": 195, "x": 350, "y": 600},
        "class": {"id": "77697265-FCE2-4EBE-8C81-99C578524A24", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "bypass": {"type": "bool", "value": False},
            "color1": {"type": "float4", "value": [1.0, 1.0, 1.0, 1.0]},
            "color2": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]},
            "dither": {"type": "float", "value": 0.0}
        },
        "name": "Radiant Gradient",
        "thumbnail_visible": True
    }
    conn(15, "output", 27, "color1")

    # Scale Vec2: For H directions (0, 1), scale X = Gradient Width, scale Y = 4.0 (tall vertical radiant curtain)
    # For V directions (2, 3), scale X = 4.0, scale Y = Gradient Width (wide horizontal radiant curtain)
    nodes["28"] = {
        "attributes": make_attr_float_switch(6),
        "bounds": {"height": 150, "width": 195, "x": 580, "y": 450},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 1.0}, "input2": {"type": "float", "value": 4.0}, "input3": {"type": "float", "value": 4.0}, "input4": {"type": "float", "value": 2.0}, "input5": {"type": "float", "value": 2.0}},
        "name": "Switch Scale X",
        "thumbnail_visible": False
    }
    conn(11, "output", 28, "selection")
    conn(14, "output", 28, "input0")
    conn(14, "output", 28, "input1")

    nodes["29"] = {
        "attributes": make_attr_float_switch(6),
        "bounds": {"height": 150, "width": 195, "x": 580, "y": 650},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 4.0}, "input1": {"type": "float", "value": 4.0}, "input2": {"type": "float", "value": 1.0}, "input3": {"type": "float", "value": 1.0}, "input4": {"type": "float", "value": 2.0}, "input5": {"type": "float", "value": 2.0}},
        "name": "Switch Scale Y",
        "thumbnail_visible": False
    }
    conn(11, "output", 29, "selection")
    conn(14, "output", 29, "input2")
    conn(14, "output", 29, "input3")

    nodes["30"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 800, "y": 550},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 4.0}},
        "name": "Scale Vec2",
        "thumbnail_visible": False
    }
    conn(28, "output", 30, "input0")
    conn(29, "output", 30, "input1")

    # Transform Node: Shifts the radiant gradient across the screen!
    nodes["31"] = {
        "attributes": {
            "anchor-type": {"type": "type", "value": "float2"},
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "texture2d"},
            "instances": {"type": "integer", "value": 1},
            "rotation-type": {"type": "type", "value": "float"},
            "scale-type": {"type": "type", "value": "float2"},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 130, "width": 195, "x": 1050, "y": 450},
        "class": {"id": "77697265-9225-4009-9D2D-5F898E94CC33", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "anchor": {"type": "float2", "value": [0.0, 0.0]},
            "input": {"type": "texture2d", "value": None},
            "rotation": {"type": "float", "value": 0.0},
            "scale": {"type": "float2", "value": [1.0, 4.0]},
            "translation": {"type": "float2", "value": [0.0, 0.0]}
        },
        "name": "Shift Gradient",
        "thumbnail_visible": True
    }
    conn(27, "output", 31, "input")
    conn(26, "output", 31, "translation")
    conn(30, "output", 31, "scale")

    # Wiper Gate: Wiper (Hold) * Intensity
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
# 4. BUILD ZZ-STROBE (Stock Strobe with Piano Hold)
# =============================================================================
def build_zz_strobe():
    patch = base_patch(
        "zz-strobe",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e230",
        "IP26 Modular Suite: High-Speed Multi-Rate Flash Strobe (Piano Hold & Clean).",
        ["ip26", "strobe", "flash", "speed", "pulse", "worship"],
        [0, 10, 11, 12, 13, 14]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Strobe (Hold)", False, -600, 150)
    nodes["11"] = node_float_in(11, "Strobe Rate", 2.0, 30.0, 14.0, -600, 250)
    nodes["12"] = node_color_in(12, "Strobe Color", [1.0, 1.0, 1.0, 1.0], -600, 350)
    nodes["13"] = node_float_in(13, "Strobe Intensity", 0.0, 1.0, 1.0, -600, 450)
    nodes["14"] = node_bool_in(14, "Bypass", False, -600, 550)

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

    # Strobe Active Gate: Strobe (Hold) * Pulse Clock
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
    conn(13, "output", 22, "input1")

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
    conn(12, "output", 23, "color")

    # Video Mixer (Add mode 11)
    nodes["24"] = node_video_mixer(24, 11, 350, 0)
    conn(0, "output", 24, "input1")
    conn(23, "output", 24, "input2")
    conn(22, "output0", 24, "opacity2")

    # Video Mixer for Bypass Switch
    nodes["25"] = node_video_mixer(25, 0, 600, 0)
    conn(24, "output", 25, "input1")
    conn(0, "output", 25, "input2")
    conn(14, "output", 25, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 850, 0)
    conn(25, "output", 1, "input")

    return patch

# =============================================================================
# 5. BUILD ZZ-STROKE (Animated Snake Running Along Perimeter with Fading Tail & Flexibility)
# =============================================================================
def build_zz_stroke():
    patch = base_patch(
        "zz-stroke",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e260",
        "IP26 Modular Suite: Animated Snake Border Running Around Screen Perimeter with Fading Tail & Full Flexibility.",
        ["ip26", "stroke", "snake", "border", "inline", "perimeter", "glow", "worship"],
        [0, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Stroke (Hold)", True, -600, 100)
    nodes["11"] = node_float_in(11, "Stroke Width", 0.005, 0.08, 0.025, -600, 200)
    nodes["12"] = node_float_in(12, "Corner Radius", 0.0, 0.5, 0.0, -600, 300)
    nodes["13"] = node_float_in(13, "Border Inset", 0.0, 0.2, 0.0, -600, 400)
    nodes["14"] = node_float_in(14, "Snake Speed", 0.1, 4.0, 1.2, -600, 500)
    nodes["15"] = node_int_in(15, "Direction", 0, 1, 0, -600, 600) # 0: Clockwise, 1: Counter-Clockwise
    nodes["16"] = node_color_in(16, "Stroke Color", [0.0, 0.9, 1.0, 1.0], -600, 700)
    nodes["17"] = node_float_in(17, "Stroke Intensity", 0.0, 1.0, 1.0, -600, 800)
    nodes["18"] = node_bool_in(18, "Bypass", False, -600, 900)

    # Inset Math: Rect Size = 2.0 - (Border Inset * 2.0)
    nodes["19"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": -400, "y": 400},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 2.0}},
        "name": "Inset Mult 2",
        "thumbnail_visible": False
    }
    conn(13, "output", 19, "input0")

    nodes["20"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": -260, "y": 400},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 2.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Rect Size Calc",
        "thumbnail_visible": False
    }
    conn(19, "output0", 20, "input1")

    # Corner Radius Float4 (for 4 corners of rectangle)
    nodes["21"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-type": {"type": "type", "value": "float"},
            "input1-type": {"type": "type", "value": "float"},
            "input2-type": {"type": "type", "value": "float"},
            "input3-type": {"type": "type", "value": "float"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 130, "width": 195, "x": -260, "y": 250},
        "class": {"id": "77697265-19E0-4717-BD17-6C7D4A9252C4", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "input2": {"type": "float", "value": 0.0}, "input3": {"type": "float", "value": 0.0}},
        "name": "Corner Radius Float4",
        "thumbnail_visible": False
    }
    conn(12, "output", 21, "input0")
    conn(12, "output", 21, "input1")
    conn(12, "output", 21, "input2")
    conn(12, "output", 21, "input3")

    # Outer Screen Rectangle (Normalized Canvas with dynamic Inset & Radius)
    nodes["22"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": -50, "y": 250},
        "class": {"id": "77697265-4db6-4573-8aa7-42362bc44931", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"height": {"type": "float", "value": 2.0}, "round": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]}, "width": {"type": "float", "value": 2.0}},
        "name": "Screen Rect",
        "thumbnail_visible": True
    }
    conn(20, "output0", 22, "width")
    conn(20, "output0", 22, "height")
    conn(21, "output", 22, "round")

    # Edge Node: Converts full rectangle into perimeter border stroke frame
    nodes["23"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}, "mode": {"type": "integer", "value": 0}},
        "bounds": {"height": 58, "width": 195, "x": 160, "y": 250},
        "class": {"id": "77697265-ab950887-37ee-4fd2-9487-c856b6b75c83", "version": 2},
        "clock": "video",
        "color": "fff26eb5",
        "constants": {"input": {"type": "procedural", "value": None}, "thickness": {"type": "float", "value": 0.025}},
        "name": "Border Stroke",
        "thumbnail_visible": True
    }
    conn(22, "output", 23, "input")
    conn(11, "output", 23, "thickness")

    # Shape Render: Renders the border frame texture (relative resolution mode 0)
    nodes["24"] = {
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
        "bounds": {"height": 82, "width": 195, "x": 380, "y": 250},
        "class": {"id": "77697265-EA26-47D6-985A-B4D5DC314BF7", "version": 2},
        "clock": "video",
        "color": "ff2dc18a",
        "constants": {"material": {"type": "float4", "value": [1.0, 1.0, 1.0, 1.0]}, "shape": {"type": "procedural", "value": None}},
        "name": "Render Frame",
        "thumbnail_visible": True
    }
    conn(23, "output", 24, "shape")

    # Sweep / Conical Gradient: Head=White [1,1,1,1], Tail=Transparent/Black [0,0,0,0]
    nodes["25"] = {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "method": {"type": "integer", "value": 0},
            "mode": {"type": "integer", "value": 0},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]},
            "type": {"type": "integer", "value": 2}
        },
        "bounds": {"height": 82, "width": 195, "x": 160, "y": 450},
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

    # Rotation Oscillator (Saw)
    nodes["26"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": -100, "y": 600},
        "class": {"id": "77697265-F95F-41D8-8FC4-DF0DC56E1051", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.0}, "frequency": {"type": "float", "value": 1.2}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Rotation Osc",
        "thumbnail_visible": True
    }
    conn(14, "output", 26, "frequency")

    # Inverted Saw (* -1.0) for Counter-Clockwise
    nodes["27"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 160, "y": 650},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": -1.0}},
        "name": "Invert Rotation",
        "thumbnail_visible": True
    }
    conn(26, "output", 27, "input0")

    # Switch Direction (0=CW, 1=CCW)
    nodes["28"] = {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 100, "width": 195, "x": 380, "y": 600},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "selection": {"type": "integer", "value": 0}},
        "name": "Direction Switch",
        "thumbnail_visible": True
    }
    conn(15, "output", 28, "selection")
    conn(26, "output", 28, "input0")
    conn(27, "output0", 28, "input1")

    # Transform: Rotate the Sweep Gradient around center
    nodes["29"] = {
        "attributes": {
            "anchor-type": {"type": "type", "value": "float2"},
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "texture2d"},
            "instances": {"type": "integer", "value": 1},
            "rotation-type": {"type": "type", "value": "float"},
            "scale-type": {"type": "type", "value": "float2"},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 130, "width": 195, "x": 380, "y": 450},
        "class": {"id": "77697265-9225-4009-9D2D-5F898E94CC33", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"anchor": {"type": "float2", "value": [0.0, 0.0]}, "input": {"type": "texture2d", "value": None}, "rotation": {"type": "float", "value": 0.0}, "scale": {"type": "float2", "value": [1.0, 1.0]}, "translation": {"type": "float2", "value": [0.0, 0.0]}},
        "name": "Rotate Sweep",
        "thumbnail_visible": True
    }
    conn(25, "output", 29, "input")
    conn(28, "output", 29, "rotation")

    # Mask Mixer: Border Frame * Rotating Gradient (Multiply mode 0, opacity2: 1.0!)
    nodes["30"] = node_video_mixer(30, 0, 640, 300, op2=1.0)
    conn(24, "output0", 30, "input1")
    conn(29, "output0", 30, "input2")

    # Neon Color Source
    nodes["31"] = {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [1920, 1080]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 58, "width": 195, "x": 640, "y": 550},
        "class": {"id": "77697265-E8EC-4F1B-901A-CFFC104D3B07", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"bypass": {"type": "bool", "value": False}, "color": {"type": "color", "value": [0.0, 0.9, 1.0, 1.0]}},
        "name": "Neon Color Source",
        "thumbnail_visible": True
    }
    conn(16, "output", 31, "color")

    # Colorize the Snake: Masked Snake * Color (Multiply mode 0, opacity2: 1.0)
    nodes["32"] = node_video_mixer(32, 0, 880, 300, op2=1.0)
    conn(30, "output", 32, "input1")
    conn(31, "output", 32, "input2")

    # Gate: Stroke (Hold) * Stroke Intensity
    nodes["33"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 880, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Stroke Gate",
        "thumbnail_visible": True
    }
    conn(10, "output", 33, "input0")
    conn(17, "output", 33, "input1")

    # Blend Snake over Texture In (Add mode 11)
    nodes["34"] = node_video_mixer(34, 11, 1120, 0)
    conn(0, "output", 34, "input1")
    conn(32, "output", 34, "input2")
    conn(33, "output0", 34, "opacity2")

    # Bypass Switch
    nodes["35"] = node_video_mixer(35, 0, 1360, 0)
    conn(34, "output", 35, "input1")
    conn(0, "output", 35, "input2")
    conn(18, "output", 35, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 1600, 0)
    conn(35, "output", 1, "input")

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
        ('77697265-D235-4A6A-B661-02ABE55C72FF', 3): ['input', 'instances', 'flow', 'has-min', 'min', 'has-max', 'max', 'options-count', 'widget', 'unit'],
        ('77697265-86ce-4e85-a02d-34f915fca74e', 1): ['input0-type', 'flow', 'instances'],
        ('77697265-A9AF-4CB4-B10F-3968B36BB63B', 1): ['flow', 'size', 'type0', 'input0-dimensions', 'type1', 'input1-dimensions'],
        ('77697265-7557-4053-ABEC-73E2A9786804', 2): ['flow', 'value-type', 'value-dimensions', 'min-type', 'min-dimensions', 'max-type', 'max-dimensions'],
        ('77697265-A0D8-429A-A558-69BC58D0D425', 1): ['flow', 'size', 'type0', 'input0-dimensions', 'type1', 'input1-dimensions'],
        ('77697265-E7EF-4944-8FC2-D808EE0433CB', 1): ['flow', 'instances'],
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
        ('77697265-e61f-42c0-862a-0dca04e14569', 1): ['input', 'instances', 'flow'],
        ('77697265-19E0-4717-BD17-6C7D4A9252C4', 1): ['input0-type', 'input1-type', 'input2-type', 'input3-type', 'flow', 'instances']
    }

    wire_dir = os.path.join(target_dir, "wire")
    cwired_dir = os.path.join(target_dir, "cwired")
    os.makedirs(wire_dir, exist_ok=True)
    os.makedirs(cwired_dir, exist_ok=True)

    # Clean up any leftover test files
    for old_f in ["zz_outliner.wire", "zz_outliner.cwired"]:
        p1 = os.path.join(wire_dir, old_f)
        p2 = os.path.join(cwired_dir, old_f)
        if os.path.exists(p1): os.remove(p1)
        if os.path.exists(p2): os.remove(p2)

    print("=== BUILDING ZZ-SUITE V2 PURE MODULAR PLUGINS ===")
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
