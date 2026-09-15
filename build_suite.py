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

def make_attr_clamp():
    return {
        "flow": {"type": "flow", "value": "signal"},
        "max-dimensions": {"type": "integer", "value": 1},
        "max-type": {"type": "type", "value": "float"},
        "min-dimensions": {"type": "integer", "value": 1},
        "min-type": {"type": "type", "value": "float"},
        "value-dimensions": {"type": "integer", "value": 1},
        "value-type": {"type": "type", "value": "float"}
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
            "nextNodeId": 200,
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

def node_color_in(nid, name, rgba, x=-600, y=400):
    return {
        "attributes": {"flow": {"type": "flow", "value": "event"}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
        "bounds": {"height": 82, "width": 140, "x": x, "y": y},
        "class": {"id": "77697265-4C9E-4F75-B4F0-5415B713EA1B", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "color", "value": rgba}},
        "hidden": ["input", "instances", "flow", "options-count", "widget"],
        "name": name,
        "thumbnail_visible": True
    }

def node_video_mixer(nid, mode=11, x=1000, y=0):
    return {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "input-count": {"type": "integer", "value": 2},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
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
        "hidden": ["instances", "bypass", "bitdepth", "resolution-absolute", "resolution-relative", "resolution-mode"],
        "name": "Video Mixer",
        "thumbnail_visible": True
    }

# =============================================================================
# 1. BUILD ZZ-PUSHER
# =============================================================================
def build_zz_pusher():
    patch = base_patch(
        "zz-pusher",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e210",
        "IP26 Modular Suite: Elastic Zoom Kick & Beat Punch Rack (Piano Mode).",
        ["ip26", "pusher", "bumper", "zoom", "punch", "worship"],
        [0, 10, 12, 13]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Push", False, -600, 150)
    nodes["12"] = node_float_in(12, "Push Amount", 0.0, 1.0, 0.35, -600, 250)
    nodes["13"] = node_float_in(13, "Push Decay", 0.0, 1.0, 0.12, -600, 350)

    # Target Zoom Gain = Push (10) * Amount (12)
    nodes["15"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": -350, "y": 200},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Target Zoom",
        "thumbnail_visible": True
    }
    conn(10, "output", 15, "input0")
    conn(12, "output", 15, "input1")

    # Push Smooth (Node 14) - duration = Decay
    nodes["14"] = {
        "attributes": {"input0-type": {"type": "type", "value": "float"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 58, "width": 195, "x": -150, "y": 200},
        "class": {"id": "77697265-86ce-4e85-a02d-34f915fca74e", "version": 1},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"duration": {"type": "float", "value": 0.12}, "input0": {"type": "float", "value": 0.0}},
        "name": "Push Smooth",
        "thumbnail_visible": True
    }
    conn(15, "output0", 14, "input0")
    conn(13, "output", 14, "duration")

    # Constant 1.0
    nodes["16"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "has-max": {"type": "bool", "value": False}, "has-min": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "unit": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
        "bounds": {"height": 58, "width": 100, "x": -150, "y": 350},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 1.0}},
        "name": "Base Scale 1.0",
        "thumbnail_visible": False
    }

    # Total Scale Add: 1.0 + Smooth
    nodes["17"] = {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 100, "y": 250},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Total Scale",
        "thumbnail_visible": True
    }
    conn(16, "output", 17, "input0")
    conn(14, "output0", 17, "input1")

    # Float2 for Scale (X, Y)
    nodes["19"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 280, "y": 250},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 1.0}},
        "name": "Scale Vec2",
        "thumbnail_visible": True
    }
    conn(17, "output0", 19, "input0")
    conn(17, "output0", 19, "input1")

    # Transform (Zoom Center)
    nodes["18"] = {
        "attributes": {
            "anchor-type": {"type": "type", "value": "float2"},
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "texture2d"},
            "instances": {"type": "integer", "value": 1},
            "rotation-type": {"type": "type", "value": "float"},
            "scale-type": {"type": "type", "value": "float2"},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 130, "width": 195, "x": 450, "y": 0},
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
        "hidden": ["flow", "input-type", "translation-type", "rotation-type", "scale-type", "anchor-type", "instances"],
        "name": "Push Zoom",
        "thumbnail_visible": True
    }
    conn(0, "output", 18, "input")
    conn(19, "output", 18, "scale")

    # Texture Out
    nodes["1"] = node_texture_out(1, 750, 0)
    conn(18, "output0", 1, "input")

    return patch

# =============================================================================
# 2. BUILD ZZ-CHASER
# =============================================================================
def build_zz_chaser():
    patch = base_patch(
        "zz-chaser",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e220",
        "IP26 Modular Suite: 7-Direction Dedicated Piano Chaser with Grid Quantization.",
        ["ip26", "chaser", "slices", "grid", "runner", "worship"],
        [0, 301, 302, 303, 304, 305, 306, 307, 31, 32, 34, 35, 36]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)

    # 7 Triggers
    chase_names = [
        (301, "Chase 1: Left -> Right"),
        (302, "Chase 2: Right -> Left"),
        (303, "Chase 3: Center -> Out"),
        (304, "Chase 4: Out -> Center"),
        (305, "Chase 5: Up -> Down"),
        (306, "Chase 6: Down -> Up"),
        (307, "Chase 7: Bounce")
    ]
    for idx, (cid, cname) in enumerate(chase_names):
        nodes[str(cid)] = node_bool_in(cid, cname, False, -600, 100 + idx*70)

    # Chase Settings
    nodes["31"] = node_int_in(31, "Grid Slices", 1, 10, 5, -600, 620)
    nodes["32"] = node_bool_in(32, "Snap to Grid", True, -600, 710)
    nodes["34"] = node_float_in(34, "Chase Speed", 0.1, 8.0, 1.2, -600, 800)
    nodes["35"] = node_color_in(35, "Chase Color", [1.0, 0.75, 0.2, 1.0], -600, 890)
    nodes["36"] = node_float_in(36, "Chase Intensity", 0.0, 1.0, 1.0, -600, 980)

    # Direction Weights & Mults
    for i in range(2, 7):
        nodes[str(310 + i)] = {
            "attributes": {"flow": {"type": "flow", "value": "event"}, "has-max": {"type": "bool", "value": False}, "has-min": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "unit": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
            "bounds": {"height": 50, "width": 80, "x": -350, "y": 100 + (i-1)*70},
            "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
            "clock": "video",
            "color": "ff20c7bb",
            "constants": {"input": {"type": "float", "value": float(i-1)}},
            "name": f"Weight {i-1}",
            "thumbnail_visible": False
        }
        nodes[str(320 + i)] = {
            "attributes": make_attr_float_mult(),
            "bounds": {"height": 60, "width": 100, "x": -220, "y": 100 + (i-1)*70},
            "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
            "clock": "video",
            "color": "ffff6a00",
            "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
            "name": f"WMult {i}",
            "thumbnail_visible": False
        }
        conn(300 + i, "output", 320 + i, "input0")
        conn(310 + i, "output", 320 + i, "input1")

    # Encoded Direction Sum
    nodes["330"] = {
        "attributes": make_attr_float_add(6),
        "bounds": {"height": 140, "width": 130, "x": -80, "y": 200},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{k}": {"type": "float", "value": 0.0} for k in range(6)},
        "name": "Encoded Direction",
        "thumbnail_visible": True
    }
    conn(302, "output", 330, "input0")
    for i in range(2, 7):
        conn(320 + i, "output0", 330, f"input{i-1}")

    # Sum 7 Triggers for Active Gate
    nodes["340"] = {
        "attributes": make_attr_float_add(7),
        "bounds": {"height": 160, "width": 130, "x": -80, "y": 450},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{k}": {"type": "float", "value": 0.0} for k in range(7)},
        "name": "Sum 7 Triggers",
        "thumbnail_visible": True
    }
    for i in range(1, 8):
        conn(300 + i, "output", 340, f"input{i-1}")

    nodes["341"] = {
        "attributes": make_attr_clamp(),
        "bounds": {"height": 82, "width": 130, "x": 80, "y": 450},
        "class": {"id": "77697265-7557-4053-ABEC-73E2A9786804", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"max": {"type": "float", "value": 1.0}, "min": {"type": "float", "value": 0.0}, "value": {"type": "float", "value": 0.0}},
        "name": "Chase Active Gate",
        "thumbnail_visible": True
    }
    conn(340, "output0", 341, "value")

    # Grid Slice Width (2.0 / Slices)
    nodes["60"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "has-max": {"type": "bool", "value": False}, "has-min": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "unit": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
        "bounds": {"height": 58, "width": 100, "x": 80, "y": 620},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 2.0}},
        "name": "Total Screen Width 2.0",
        "thumbnail_visible": False
    }
    nodes["61"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 220, "y": 620},
        "class": {"id": "77697265-0D55-485E-813D-706DD5DFE88D", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 2.0}, "input1": {"type": "float", "value": 5.0}},
        "hidden": ["flow", "size", "type0", "input0-dimensions", "type1", "input1-dimensions"],
        "name": "Slice Width Calc",
        "thumbnail_visible": True
    }
    conn(60, "output", 61, "input0")
    conn(31, "output", 61, "input1")

    # Oscillators
    nodes["62"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": 220, "y": 150},
        "class": {"id": "77697265-F95F-41D8-8FC4-DF0DC56E1051", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.0}, "frequency": {"type": "float", "value": 1.2}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Saw LFO Forward",
        "thumbnail_visible": True
    }
    conn(34, "output", 62, "frequency")

    # Inverted Saw (Right to Left / Down to Up)
    nodes["63"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 450, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": -1.0}},
        "name": "Invert Direction",
        "thumbnail_visible": True
    }
    conn(62, "output", 63, "input0")

    # Triangle Osc (Center to Out)
    nodes["64"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": 220, "y": 300},
        "class": {"id": "77697265-9890-41DC-A93D-9F3913A78FEB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.0}, "frequency": {"type": "float", "value": 1.2}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Center-Out Osc",
        "thumbnail_visible": True
    }
    conn(34, "output", 64, "frequency")

    # Bounce Osc
    nodes["79"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": 220, "y": 450},
        "class": {"id": "77697265-9890-41DC-A93D-9F3913A78FEB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.0}, "frequency": {"type": "float", "value": 1.2}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Ping-Pong Osc",
        "thumbnail_visible": True
    }
    conn(34, "output", 79, "frequency")

    # Out to Center Calc: 1.0 - Triangle
    nodes["80"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "has-max": {"type": "bool", "value": False}, "has-min": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "unit": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
        "bounds": {"height": 50, "width": 80, "x": 450, "y": 300},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 1.0}},
        "name": "Const 1.0",
        "thumbnail_visible": False
    }
    nodes["81"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 580, "y": 300},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Out to Center Calc",
        "thumbnail_visible": True
    }
    conn(80, "output", 81, "input0")
    conn(64, "output", 81, "input1")

    # Switch Raw X & Y
    nodes["65"] = {
        "attributes": make_attr_float_switch(7),
        "bounds": {"height": 160, "width": 195, "x": 750, "y": 150},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(7)},
        "name": "Switch Raw X",
        "thumbnail_visible": True
    }
    conn(330, "output0", 65, "selection")
    conn(62, "output", 65, "input0")
    conn(63, "output0", 65, "input1")
    conn(64, "output", 65, "input2")
    conn(81, "output0", 65, "input3")
    conn(79, "output", 65, "input6")

    nodes["66"] = {
        "attributes": make_attr_float_switch(7),
        "bounds": {"height": 160, "width": 195, "x": 750, "y": 350},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(7)},
        "name": "Switch Raw Y",
        "thumbnail_visible": True
    }
    conn(330, "output0", 66, "selection")
    conn(63, "output0", 66, "input4")
    conn(62, "output", 66, "input5")

    # Quantize X & Y
    nodes["67"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input0-type": {"type": "type", "value": "float"},
            "input1-dimensions": {"type": "integer", "value": 1},
            "input1-type": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 58, "width": 130, "x": 980, "y": 150},
        "class": {"id": "77697265-548F-4EF6-9B00-F3005FEC8687", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.4}},
        "name": "Quantize X",
        "thumbnail_visible": True
    }
    conn(65, "output", 67, "input0")
    conn(61, "output0", 67, "input1")

    nodes["68"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input0-type": {"type": "type", "value": "float"},
            "input1-dimensions": {"type": "integer", "value": 1},
            "input1-type": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 58, "width": 130, "x": 980, "y": 350},
        "class": {"id": "77697265-548F-4EF6-9B00-F3005FEC8687", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.4}},
        "name": "Quantize Y",
        "thumbnail_visible": True
    }
    conn(66, "output", 68, "input0")
    conn(61, "output0", 68, "input1")

    # Switch Snap X & Y
    nodes["69"] = {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 100, "width": 195, "x": 1150, "y": 150},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "selection": {"type": "integer", "value": 1}},
        "name": "Switch Snap X",
        "thumbnail_visible": True
    }
    conn(32, "output", 69, "selection")
    conn(65, "output", 69, "input0")
    conn(67, "output0", 69, "input1")

    nodes["70"] = {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 100, "width": 195, "x": 1150, "y": 350},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "selection": {"type": "integer", "value": 1}},
        "name": "Switch Snap Y",
        "thumbnail_visible": True
    }
    conn(32, "output", 70, "selection")
    conn(66, "output", 70, "input0")
    conn(68, "output0", 70, "input1")

    # Translation Float2
    nodes["71"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 1380, "y": 250},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Final Translation",
        "thumbnail_visible": True
    }
    conn(69, "output", 71, "input0")
    conn(70, "output", 71, "input1")

    # Switch Bar Width & Height
    nodes["72"] = {
        "attributes": make_attr_float_switch(7),
        "bounds": {"height": 160, "width": 195, "x": 980, "y": 550},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "input0": {"type": "float", "value": 0.4}, "input1": {"type": "float", "value": 0.4}, "input2": {"type": "float", "value": 0.4},
            "input3": {"type": "float", "value": 0.4}, "input4": {"type": "float", "value": 2.0}, "input5": {"type": "float", "value": 2.0},
            "input6": {"type": "float", "value": 0.4}, "selection": {"type": "integer", "value": 0}
        },
        "name": "Switch Bar Width",
        "thumbnail_visible": True
    }
    conn(330, "output0", 72, "selection")
    conn(61, "output0", 72, "input0")
    conn(61, "output0", 72, "input1")
    conn(61, "output0", 72, "input2")
    conn(61, "output0", 72, "input3")
    conn(61, "output0", 72, "input6")

    nodes["73"] = {
        "attributes": make_attr_float_switch(7),
        "bounds": {"height": 160, "width": 195, "x": 980, "y": 750},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "input0": {"type": "float", "value": 2.0}, "input1": {"type": "float", "value": 2.0}, "input2": {"type": "float", "value": 2.0},
            "input3": {"type": "float", "value": 2.0}, "input4": {"type": "float", "value": 0.4}, "input5": {"type": "float", "value": 0.4},
            "input6": {"type": "float", "value": 2.0}, "selection": {"type": "integer", "value": 0}
        },
        "name": "Switch Bar Height",
        "thumbnail_visible": True
    }
    conn(330, "output0", 73, "selection")
    conn(61, "output0", 73, "input4")
    conn(61, "output0", 73, "input5")

    # Procedural Rectangle
    nodes["74"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": 1250, "y": 650},
        "class": {"id": "77697265-4db6-4573-8aa7-42362bc44931", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"height": {"type": "float", "value": 2.0}, "round": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]}, "width": {"type": "float", "value": 0.4}},
        "name": "Chase Bar",
        "thumbnail_visible": True
    }
    conn(72, "output", 74, "width")
    conn(73, "output", 74, "height")

    # Move Shape
    nodes["75"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "procedural"},
            "instances": {"type": "integer", "value": 1},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 58, "width": 195, "x": 1550, "y": 450},
        "class": {"id": "77697265-0e5a-4bfd-b136-e4f68P3cc463", "version": 3},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {"input": {"type": "procedural", "value": None}, "translation": {"type": "float2", "value": [0.0, 0.0]}},
        "name": "Move Beam",
        "thumbnail_visible": True
    }
    conn(74, "shape", 75, "input")
    conn(71, "output", 75, "translation")

    # Render Shape
    nodes["76"] = {
        "attributes": {
            "aa-blend": {"type": "bool", "value": False},
            "bitdepth": {"type": "integer", "value": 0},
            "camera-type": {"type": "type", "value": "float"},
            "instances": {"type": "integer", "value": 1},
            "material-dimensions": {"type": "integer", "value": 1},
            "material-type": {"type": "type", "value": "color"},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]},
            "shape-dimensions": {"type": "integer", "value": 1},
            "shape-type": {"type": "type", "value": "procedural"}
        },
        "bounds": {"height": 82, "width": 195, "x": 1550, "y": 600},
        "class": {"id": "77697265-EA26-47D6-985A-B4D5DC314BF7", "version": 2},
        "clock": "video",
        "color": "ff2dc18a",
        "constants": {"material": {"type": "color", "value": [1.0, 0.75, 0.2, 1.0]}, "shape": {"type": "procedural", "value": None}},
        "name": "Render Beam",
        "thumbnail_visible": True
    }
    conn(75, "output", 76, "shape")
    conn(35, "output", 76, "material")

    # Gate: Multiply Chase Intensity * chase_active
    nodes["77"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 1550, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Chase Gate",
        "thumbnail_visible": True
    }
    conn(36, "output", 77, "input0")
    conn(341, "output0", 77, "input1")

    # Video Mixer
    nodes["78"] = node_video_mixer(78, 11, 1800, 0)
    conn(0, "output", 78, "input1")
    conn(76, "output", 78, "input2")
    conn(77, "output0", 78, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 2050, 0)
    conn(78, "output", 1, "input")

    return patch

# =============================================================================
# 3. BUILD ZZ-STROBE
# =============================================================================
def build_zz_strobe():
    patch = base_patch(
        "zz-strobe",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e230",
        "IP26 Modular Suite: High-Speed Multi-Rate Flash Strobe (Piano Mode).",
        ["ip26", "strobe", "flash", "speed", "pulse", "worship"],
        [0, 10, 11, 12, 13]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Strobe", False, -600, 150)
    nodes["11"] = node_float_in(11, "Strobe Rate", 2.0, 30.0, 14.0, -600, 250)
    nodes["12"] = node_float_in(12, "Strobe Intensity", 0.0, 1.0, 1.0, -600, 350)
    nodes["13"] = node_color_in(13, "Strobe Color", [1.0, 1.0, 1.0, 1.0], -600, 450)

    # Pulse Oscillator
    nodes["15"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": True}},
        "bounds": {"height": 130, "width": 195, "x": -250, "y": 200},
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
        "name": "Strobe Pulse Clock",
        "thumbnail_visible": True
    }
    conn(11, "output", 15, "frequency")

    # Strobe Active Gate: Strobe (10) * Pulse (15)
    nodes["16"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 0, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Gate Flash",
        "thumbnail_visible": True
    }
    conn(10, "output", 16, "input0")
    conn(15, "output", 16, "input1")

    # Multiply with Strobe Intensity
    nodes["17"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 180, "y": 250},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Final Flash Opacity",
        "thumbnail_visible": True
    }
    conn(16, "output0", 17, "input0")
    conn(12, "output", 17, "input1")

    # Solid Color Source
    nodes["18"] = {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 58, "width": 195, "x": 180, "y": 400},
        "class": {"id": "77697265-E8EC-4F1B-901A-CFFC104D3B07", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"bypass": {"type": "bool", "value": False}, "color": {"type": "color", "value": [1.0, 1.0, 1.0, 1.0]}},
        "name": "White Flash Source",
        "thumbnail_visible": True
    }
    conn(13, "output", 18, "color")

    # Video Mixer (Add Mode 11)
    nodes["20"] = node_video_mixer(20, 11, 450, 0)
    conn(0, "output", 20, "input1")
    conn(18, "output", 20, "input2")
    conn(17, "output0", 20, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 700, 0)
    conn(20, "output", 1, "input")

    return patch

# =============================================================================
# 4. BUILD ZZ-OUTLINER
# =============================================================================
def build_zz_outliner():
    patch = base_patch(
        "zz-outliner",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e240",
        "IP26 Modular Suite: Neon Sobel Edge Detection & Glow Overlay.",
        ["ip26", "outline", "edge", "neon", "glow", "worship"],
        [0, 10, 11, 12, 13]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Outline", True, -600, 150)
    nodes["11"] = node_float_in(11, "Outline Strength", 0.5, 8.0, 2.5, -600, 250)
    nodes["12"] = node_color_in(12, "Outline Color", [0.0, 1.0, 0.9, 1.0], -600, 350)
    nodes["13"] = node_float_in(13, "Outline Mix", 0.0, 1.0, 1.0, -600, 450)

    # Edge Detection
    nodes["14"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}, "pretty": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": -250, "y": 200},
        "class": {"id": "77697265-9DF3-4B94-A36D-42F1C6FBE997", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "algorithm": {"type": "integer", "value": 3},
            "bypass": {"type": "bool", "value": False},
            "color-select": {"type": "integer", "value": 0},
            "input": {"type": "texture2d", "value": None},
            "preserve-alpha": {"type": "bool", "value": False},
            "sample-offset": {"type": "float2", "value": [1.0, 1.0]},
            "strength": {"type": "float", "value": 2.5}
        },
        "name": "Edge Detection",
        "thumbnail_visible": True
    }
    conn(0, "output", 14, "input")
    conn(11, "output", 14, "strength")

    # Neon Tint (Gradient Palette)
    nodes["15"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": 0, "y": 200},
        "class": {"id": "77697265-974B-4C09-A806-EA8D80FCF53F", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "blackTo": {"type": "color", "value": [0.0, 0.0, 0.0, 1.0]},
            "bypass": {"type": "bool", "value": False},
            "input": {"type": "texture2d", "value": None},
            "whiteTo": {"type": "color", "value": [0.0, 0.85, 1.0, 1.0]}
        },
        "name": "Neon Tint",
        "thumbnail_visible": True
    }
    conn(14, "output", 15, "input")
    conn(12, "output", 15, "whiteTo")

    # Outline Gate: Outline (10) * Mix (13)
    nodes["16"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 0, "y": 380},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Outline Gate",
        "thumbnail_visible": True
    }
    conn(10, "output", 16, "input0")
    conn(13, "output", 16, "input1")

    # Video Mixer (Add Mode 11)
    nodes["17"] = node_video_mixer(17, 11, 280, 0)
    conn(0, "output", 17, "input1")
    conn(15, "output", 17, "input2")
    conn(16, "output0", 17, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 550, 0)
    conn(17, "output", 1, "input")

    return patch

# =============================================================================
# 5. BUILD ZZ-WIPER
# =============================================================================
def build_zz_wiper():
    patch = base_patch(
        "zz-wiper",
        "b8f047e1-884c-47bc-9fb5-6eb7f2d5e250",
        "IP26 Modular Suite: Linear Scanner Light Beam & Curtain Wipe (Piano Mode).",
        ["ip26", "wiper", "curtain", "scanner", "beam", "worship"],
        [0, 10, 11, 12, 13, 14, 15]
    )
    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]
    def conn(f_id, f_port, t_id, t_port):
        connections.append({"from": [int(f_id), str(f_port)], "to": [int(t_id), str(t_port)]})

    nodes["0"] = node_texture_in(0)
    nodes["10"] = node_bool_in(10, "Wiper", False, -600, 150)
    nodes["11"] = node_int_in(11, "Wipe Direction", 0, 3, 0, -600, 250) # 0: L->R, 1: R->L, 2: Up->Down, 3: Down->Up
    nodes["12"] = node_float_in(12, "Wipe Speed", 0.1, 6.0, 1.2, -600, 350)
    nodes["13"] = node_float_in(13, "Bar Width", 0.05, 1.0, 0.35, -600, 450)
    nodes["14"] = node_color_in(14, "Bar Color", [1.0, 1.0, 1.0, 1.0], -600, 550)
    nodes["15"] = node_float_in(15, "Wipe Intensity", 0.0, 1.0, 1.0, -600, 650)

    # Constant -1.0 for direction inversion
    nodes["210"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "has-max": {"type": "bool", "value": False}, "has-min": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "unit": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
        "bounds": {"height": 50, "width": 80, "x": -250, "y": 380},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": -1.0}},
        "name": "Const -1.0",
        "thumbnail_visible": False
    }

    # Saw Oscillator
    nodes["20"] = {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": -250, "y": 200},
        "class": {"id": "77697265-F95F-41D8-8FC4-DF0DC56E1051", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"amplitude": {"type": "float", "value": 1.0}, "frequency": {"type": "float", "value": 1.2}, "offset": {"type": "float", "value": 0.0}, "phase-offset": {"type": "float", "value": 0.0}, "reset-phase": {"type": "trigger", "value": None}},
        "name": "Saw Forward",
        "thumbnail_visible": True
    }
    conn(12, "output", 20, "frequency")

    # Inverted Saw: Saw * -1.0
    nodes["21"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": -30, "y": 200},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": -1.0}},
        "name": "Saw Reverse",
        "thumbnail_visible": True
    }
    conn(20, "output", 21, "input0")
    conn(210, "output", 21, "input1")

    # Switch Pos X (0: Fwd, 1: Rev, 2: 0, 3: 0)
    nodes["22"] = {
        "attributes": make_attr_float_switch(4),
        "bounds": {"height": 130, "width": 195, "x": 160, "y": 150},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(4)},
        "name": "Switch Wipe X",
        "thumbnail_visible": True
    }
    conn(11, "output", 22, "selection")
    conn(20, "output", 22, "input0")
    conn(21, "output0", 22, "input1")

    # Switch Pos Y (0: 0, 1: 0, 2: Rev, 3: Fwd)
    nodes["23"] = {
        "attributes": make_attr_float_switch(4),
        "bounds": {"height": 130, "width": 195, "x": 160, "y": 320},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(4)},
        "name": "Switch Wipe Y",
        "thumbnail_visible": True
    }
    conn(11, "output", 23, "selection")
    conn(21, "output0", 23, "input2")
    conn(20, "output", 23, "input3")

    # Float2 Translation (X, Y)
    nodes["24"] = {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 400, "y": 250},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Translation Vec2",
        "thumbnail_visible": True
    }
    conn(22, "output", 24, "input0")
    conn(23, "output", 24, "input1")

    # Switch Bar Width (Modes 0, 1: Bar Width; Modes 2, 3: 2.0 full)
    nodes["25"] = {
        "attributes": make_attr_float_switch(4),
        "bounds": {"height": 130, "width": 195, "x": 160, "y": 500},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.35}, "input1": {"type": "float", "value": 0.35}, "input2": {"type": "float", "value": 2.0}, "input3": {"type": "float", "value": 2.0}},
        "name": "Switch Bar Width",
        "thumbnail_visible": True
    }
    conn(11, "output", 25, "selection")
    conn(13, "output", 25, "input0")
    conn(13, "output", 25, "input1")

    # Switch Bar Height (Modes 0, 1: 2.0 full; Modes 2, 3: Bar Width)
    nodes["26"] = {
        "attributes": make_attr_float_switch(4),
        "bounds": {"height": 130, "width": 195, "x": 160, "y": 660},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 2.0}, "input1": {"type": "float", "value": 2.0}, "input2": {"type": "float", "value": 0.35}, "input3": {"type": "float", "value": 0.35}},
        "name": "Switch Bar Height",
        "thumbnail_visible": True
    }
    conn(11, "output", 26, "selection")
    conn(13, "output", 26, "input2")
    conn(13, "output", 26, "input3")

    # Procedural Rectangle
    nodes["27"] = {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": 400, "y": 550},
        "class": {"id": "77697265-4db6-4573-8aa7-42362bc44931", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"height": {"type": "float", "value": 2.0}, "round": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]}, "width": {"type": "float", "value": 0.35}},
        "name": "Wiper Bar Shape",
        "thumbnail_visible": True
    }
    conn(25, "output", 27, "width")
    conn(26, "output", 27, "height")

    # Move Shape
    nodes["28"] = {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "procedural"},
            "instances": {"type": "integer", "value": 1},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 58, "width": 195, "x": 600, "y": 450},
        "class": {"id": "77697265-0e5a-4bfd-b136-e4f68P3cc463", "version": 3},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {"input": {"type": "procedural", "value": None}, "translation": {"type": "float2", "value": [0.0, 0.0]}},
        "name": "Move Beam",
        "thumbnail_visible": True
    }
    conn(27, "shape", 28, "input")
    conn(24, "output", 28, "translation")

    # Render Beam
    nodes["29"] = {
        "attributes": {
            "aa-blend": {"type": "bool", "value": False},
            "bitdepth": {"type": "integer", "value": 0},
            "camera-type": {"type": "type", "value": "float"},
            "instances": {"type": "integer", "value": 1},
            "material-dimensions": {"type": "integer", "value": 1},
            "material-type": {"type": "type", "value": "color"},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]},
            "shape-dimensions": {"type": "integer", "value": 1},
            "shape-type": {"type": "type", "value": "procedural"}
        },
        "bounds": {"height": 82, "width": 195, "x": 830, "y": 450},
        "class": {"id": "77697265-EA26-47D6-985A-B4D5DC314BF7", "version": 2},
        "clock": "video",
        "color": "ff2dc18a",
        "constants": {"material": {"type": "color", "value": [1.0, 1.0, 1.0, 1.0]}, "shape": {"type": "procedural", "value": None}},
        "name": "Render Beam",
        "thumbnail_visible": True
    }
    conn(28, "output", 29, "shape")
    conn(14, "output", 29, "material")

    # Wiper Gate: Wiper (10) * Intensity (15)
    nodes["30"] = {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 600, "y": 150},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Wiper Gate",
        "thumbnail_visible": True
    }
    conn(10, "output", 30, "input0")
    conn(15, "output", 30, "input1")

    # Video Mixer (Add Mode 11)
    nodes["31"] = node_video_mixer(31, 11, 830, 0)
    conn(0, "output", 31, "input1")
    conn(29, "output", 31, "input2")
    conn(30, "output0", 31, "opacity2")

    # Texture Out
    nodes["1"] = node_texture_out(1, 1080, 0)
    conn(31, "output", 1, "input")

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
        ("zz-outliner", "zz_outliner.wire", "zz_outliner.cwired", build_zz_outliner),
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
        ('77697265-9DF3-4B94-A36D-42F1C6FBE997', 2): ['instances', 'bypass', 'pretty', 'algorithm', 'color-select', 'preserve-alpha', 'sample-offset'],
        ('77697265-974B-4C09-A806-EA8D80FCF53F', 2): ['instances', 'bypass', 'blackTo'],
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
        ('77697265-E8EC-4F1B-901A-CFFC104D3B07', 1): ['instances', 'bypass', 'bitdepth', 'resolution-absolute', 'resolution-relative', 'resolution-mode']
    }

    print("=== BUILDING ZZ-SUITE MODULAR PLUGINS ===")
    for name, wire_file, cwired_file, builder in modules:
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
        with open(wire_file, "w", encoding="utf-8") as f:
            json.dump(patch_data, f, indent=2)
        print(f"  -> Generated {wire_file} ({len(patch_data['patch']['nodes'])} nodes, {len(patch_data['patch']['connections'])} connections)")

    print("\n=== COMPILING WITH WIRE CLI ===")
    wire_exe = r"C:\Program Files\Resolume Wire\Wire.exe"
    for name, wire_file, cwired_file, builder in modules:
        if os.path.exists(cwired_file):
            try:
                os.remove(cwired_file)
            except:
                pass
        print(f"Compiling {wire_file} -> {cwired_file}...")
        try:
            res = subprocess.run([wire_exe, "compile", wire_file, "-o", cwired_file], capture_output=True, text=True, timeout=30)
            if os.path.exists(cwired_file):
                size = os.path.getsize(cwired_file)
                print(f"  [SUCCESS] {cwired_file} compiled successfully! ({size} bytes)")
            else:
                print(f"  [FAILED] {cwired_file} was not created!")
                # print last 5 lines of stdout/stderr
                lines = (res.stdout + res.stderr).splitlines()
                for l in lines[-10:]:
                    print("   ", l)
        except Exception as e:
            print(f"  [ERROR] {e}")

if __name__ == "__main__":
    main()
