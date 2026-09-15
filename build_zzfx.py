import json
import os
import subprocess

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

def build_patch():
    patch = {
        "formatVersion": {"major": 1, "minor": 1, "patch": 0},
        "patch": {
            "connections": [],
            "inputOrder": [
                0,    # Texture In
                90,   # Master Punch
                97,   # Master Mix
                # --- PUSH MODULE ---
                10,   # Push
                12,   # Push Amount
                13,   # Push Decay
                # --- STROBE MODULE ---
                50,   # Strobe
                52,   # Strobe Rate
                53,   # Strobe Intensity
                # --- OUTLINE MODULE ---
                20,   # Outline
                21,   # Outline Strength
                22,   # Outline Color
                23,   # Outline Mix
                # --- 7 CHASE TRIGGER BUTTONS (PIANO MODE) ---
                301,  # Chase 1: Left -> Right
                302,  # Chase 2: Right -> Left
                303,  # Chase 3: Center -> Out
                304,  # Chase 4: Out -> Center
                305,  # Chase 5: Up -> Down
                306,  # Chase 6: Down -> Up
                307,  # Chase 7: Bounce / Ping-Pong
                # --- CHASE SETTINGS ---
                31,   # Grid Slices
                32,   # Snap to Grid
                34,   # Chase Speed
                35,   # Chase Color
                36    # Chase Intensity
            ],
            "meta": {
                "author": "Andreas - IP26 Production",
                "category": "effect",
                "description": "IP26 7-Trigger Piano Performance Rack v3.0: Direct Keys 1-7 Chaser, Piano Push, Strobe, Outline, and Master Punch for Ibadah Perdana UKK UNNES 2026.",
                "displayName": "zzfx",
                "identifier": "b8f047e1-884c-47bc-9fb5-6eb7f2d5e206",
                "license": "MIT",
                "mail": "",
                "name": "zzfx",
                "tags": [
                    "ip26",
                    "push",
                    "chase",
                    "grid",
                    "strobe",
                    "outline",
                    "worship",
                    "unnes",
                    "resolume"
                ],
                "type": "effect",
                "url": "https://github.com/zzdree/ip26-zzfx",
                "vendor": "IP26 Production",
                "version": "3.0.0"
            },
            "nextNodeId": 400,
            "nodes": {},
            "ui": {"pan": {"x": 0.0, "y": 0.0}, "zoom": 1.0}
        },
        "resources": {},
        "ui": {}
    }

    nodes = patch["patch"]["nodes"]
    connections = patch["patch"]["connections"]

    def add_node(nid, node_data):
        nodes[str(nid)] = node_data

    def connect(from_id, from_port, to_id, to_port):
        connections.append({
            "from": [int(from_id), str(from_port)],
            "to": [int(to_id), str(to_port)]
        })

    # =========================================================================
    # 0. MASTER INPUT & OUTPUT
    # =========================================================================
    add_node(0, {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": -600, "y": 0},
        "class": {"id": "77697265-B2A2-4C1C-8C4C-2915D78CC8E9", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "texture2d", "value": None}},
        "name": "Texture In",
        "thumbnail_visible": True
    })

    add_node(90, {
        "attributes": {"bool-view": {"type": "integer", "value": 0}, "flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 140, "x": -600, "y": 200},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": False}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": "Master Punch",
        "thumbnail_visible": True
    })

    add_node(97, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": 1.0},
            "min": {"type": "float", "value": 0.0},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 2300, "y": 200},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 1.0}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Master Mix",
        "thumbnail_visible": True
    })

    add_node(98, {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "input-count": {"type": "integer", "value": 2},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 154, "width": 195, "x": 2500, "y": 0},
        "class": {"id": "77697265-A270-4D60-911C-A88B1BE6369A", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "bypass": {"type": "bool", "value": False},
            "input1": {"type": "texture2d", "value": None},
            "input2": {"type": "texture2d", "value": None},
            "mode": {"type": "integer", "value": 0},
            "opacity1": {"type": "float", "value": 1.0},
            "opacity2": {"type": "float", "value": 1.0}
        },
        "hidden": ["bypass", "input-count", "bitdepth", "resolution-absolute", "resolution-relative", "resolution-mode", "instances"],
        "name": "Dry/Wet Mixer",
        "thumbnail_visible": True
    })

    add_node(99, {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": 2750, "y": 0},
        "class": {"id": "77697265-BEEA-4D38-8EE5-0EBA4CBD0AEE", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "texture2d", "value": None}},
        "name": "Texture Out",
        "thumbnail_visible": True
    })
    connect(0, "output", 98, "input1")
    connect(97, "output", 98, "opacity2")
    connect(98, "output", 99, "input")

    # =========================================================================
    # 1. PUSH MODULE (Responsive Zoom Punch)
    # =========================================================================
    add_node(10, {
        "attributes": {"bool-view": {"type": "integer", "value": 0}, "flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 140, "x": -400, "y": -400},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": False}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": "Push",
        "thumbnail_visible": True
    })

    add_node(12, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": 1.0},
            "min": {"type": "float", "value": 0.0},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": -400, "y": -250},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 0.35}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Push Amount",
        "thumbnail_visible": True
    })

    add_node(13, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": 1.0},
            "min": {"type": "float", "value": 0.0},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": -400, "y": -120},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 0.12}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Push Decay",
        "thumbnail_visible": True
    })

    # Combine Push + Master Punch (Node 101)
    add_node(101, {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": -200, "y": -350},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Push+Punch Add",
        "thumbnail_visible": True
    })
    connect(10, "output", 101, "input0")
    connect(90, "output", 101, "input1")

    # Clamp Push Active (Node 102)
    add_node(102, {
        "attributes": make_attr_clamp(),
        "bounds": {"height": 82, "width": 130, "x": -40, "y": -350},
        "class": {"id": "77697265-7557-4053-ABEC-73E2A9786804", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"max": {"type": "float", "value": 1.0}, "min": {"type": "float", "value": 0.0}, "value": {"type": "float", "value": 0.0}},
        "hidden": ["value-type", "min-type", "max-type", "flow", "value-dimensions", "min-dimensions", "max-dimensions"],
        "name": "Push Clamp",
        "thumbnail_visible": True
    })
    connect(101, "output0", 102, "value")

    # Target Zoom Gain (Node 15)
    add_node(15, {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 120, "y": -350},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Target Zoom",
        "thumbnail_visible": True
    })
    connect(102, "output0", 15, "input0")
    connect(12, "output", 15, "input1")

    # Smooth Transition (Node 14)
    add_node(14, {
        "attributes": {"input0-type": {"type": "type", "value": "float"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 58, "width": 195, "x": 280, "y": -350},
        "class": {"id": "77697265-86ce-4e85-a02d-34f915fca74e", "version": 1},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"duration": {"type": "float", "value": 0.12}, "input0": {"type": "float", "value": 0.0}},
        "hidden": ["input0-type", "instances"],
        "name": "Push Smooth",
        "thumbnail_visible": True
    })
    connect(15, "output0", 14, "input0")
    connect(13, "output", 14, "duration")

    # Add Base Scale 1.0 (Node 17)
    add_node(17, {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 500, "y": -350},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Add Base Scale",
        "thumbnail_visible": True
    })
    connect(14, "output0", 17, "input1")

    add_node(19, {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 500, "y": -200},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 1.0}},
        "name": "Scale Vec2",
        "thumbnail_visible": True
    })
    connect(17, "output0", 19, "input0")
    connect(17, "output0", 19, "input1")

    add_node(18, {
        "attributes": {
            "anchor-type": {"type": "type", "value": "float2"},
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "texture2d"},
            "instances": {"type": "integer", "value": 1},
            "rotation-type": {"type": "type", "value": "float"},
            "scale-type": {"type": "type", "value": "float2"},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 130, "width": 195, "x": -200, "y": 0},
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
        "name": "Push Transform",
        "thumbnail_visible": True
    })
    connect(0, "output", 18, "input")
    connect(19, "output", 18, "scale")

    # =========================================================================
    # 2. OUTLINE MODULE (Sobel Edge + Neon Tint)
    # =========================================================================
    add_node(20, {
        "attributes": {"bool-view": {"type": "integer", "value": 0}, "flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 140, "x": 100, "y": 400},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": False}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": "Outline",
        "thumbnail_visible": True
    })

    add_node(21, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": 8.0},
            "min": {"type": "float", "value": 0.5},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 100, "y": 500},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 2.5}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Outline Strength",
        "thumbnail_visible": True
    })

    add_node(22, {
        "attributes": {"flow": {"type": "flow", "value": "event"}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
        "bounds": {"height": 82, "width": 140, "x": 100, "y": 600},
        "class": {"id": "77697265-4C9E-4F75-B4F0-5415B713EA1B", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "color", "value": [0.0, 1.0, 0.9, 1.0]}},
        "hidden": ["input", "instances", "flow", "options-count", "widget"],
        "name": "Outline Color",
        "thumbnail_visible": True
    })

    add_node(23, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": 1.0},
            "min": {"type": "float", "value": 0.0},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 100, "y": 700},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 1.0}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Outline Mix",
        "thumbnail_visible": True
    })

    add_node(24, {
        "attributes": {"instances": {"type": "integer", "value": 1}, "pretty": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": 100, "y": 200},
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
        "hidden": ["instances", "bypass", "pretty", "algorithm", "color-select", "preserve-alpha", "sample-offset"],
        "name": "Edge Detection",
        "thumbnail_visible": True
    })
    connect(18, "output0", 24, "input")
    connect(21, "output", 24, "strength")

    add_node(25, {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": 320, "y": 200},
        "class": {"id": "77697265-974B-4C09-A806-EA8D80FCF53F", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "blackTo": {"type": "color", "value": [0.0, 0.0, 0.0, 1.0]},
            "bypass": {"type": "bool", "value": False},
            "input": {"type": "texture2d", "value": None},
            "whiteTo": {"type": "color", "value": [0.0, 0.85, 1.0, 1.0]}
        },
        "hidden": ["instances", "bypass", "blackTo"],
        "name": "Neon Tint",
        "thumbnail_visible": True
    })
    connect(24, "output", 25, "input")
    connect(22, "output", 25, "whiteTo")

    add_node(26, {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 320, "y": 650},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Outline Gate",
        "thumbnail_visible": True
    })
    connect(23, "output", 26, "input0")
    connect(20, "output", 26, "input1")

    add_node(27, {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "input-count": {"type": "integer", "value": 2},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 154, "width": 195, "x": 550, "y": 0},
        "class": {"id": "77697265-A270-4D60-911C-A88B1BE6369A", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "bypass": {"type": "bool", "value": False},
            "input1": {"type": "texture2d", "value": None},
            "input2": {"type": "texture2d", "value": None},
            "mode": {"type": "integer", "value": 11},
            "opacity1": {"type": "float", "value": 1.0},
            "opacity2": {"type": "float", "value": 0.0}
        },
        "hidden": ["bypass", "input-count", "bitdepth", "resolution-absolute", "resolution-relative", "resolution-mode", "instances"],
        "name": "Outline Mixer",
        "thumbnail_visible": True
    })
    connect(18, "output0", 27, "input1")
    connect(25, "output", 27, "input2")
    connect(26, "output0", 27, "opacity2")

    # =========================================================================
    # 3. CHASE MODULE — 7 DIRECT PIANO TRIGGER BUTTONS
    # =========================================================================
    # 7 Direct Trigger Buttons (Bool In)
    chase_buttons = [
        (301, "Chase 1: Left -> Right", -100),
        (302, "Chase 2: Right -> Left", 0),
        (303, "Chase 3: Center -> Out", 100),
        (304, "Chase 4: Out -> Center", 200),
        (305, "Chase 5: Up -> Down", 300),
        (306, "Chase 6: Down -> Up", 400),
        (307, "Chase 7: Bounce", 500),
    ]

    for cid, cname, ypos in chase_buttons:
        add_node(cid, {
            "attributes": {"bool-view": {"type": "integer", "value": 0}, "flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
            "bounds": {"height": 82, "width": 160, "x": 600, "y": ypos},
            "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
            "clock": "video",
            "color": "ffff6a00",
            "constants": {"input": {"type": "bool", "value": False}},
            "hidden": ["input", "instances", "flow", "bool-view"],
            "name": cname,
            "thumbnail_visible": True
        })

    # Chase Settings
    add_node(31, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "integer", "value": 10},
            "min": {"type": "integer", "value": 1},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 620},
        "class": {"id": "77697265-2649-4abb-b38f-4e1005183415", "version": 2},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "integer", "value": 5}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Grid Slices",
        "thumbnail_visible": True
    })

    add_node(32, {
        "attributes": {"bool-view": {"type": "integer", "value": 0}, "flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 720},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": True}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": "Snap to Grid",
        "thumbnail_visible": True
    })

    add_node(34, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": 8.0},
            "min": {"type": "float", "value": 0.1},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 820},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 1.2}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Chase Speed",
        "thumbnail_visible": True
    })

    add_node(35, {
        "attributes": {"flow": {"type": "flow", "value": "event"}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 920},
        "class": {"id": "77697265-4C9E-4F75-B4F0-5415B713EA1B", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "color", "value": [1.0, 0.85, 0.3, 1.0]}},
        "hidden": ["input", "instances", "flow", "options-count", "widget"],
        "name": "Chase Color",
        "thumbnail_visible": True
    })

    add_node(36, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": 1.0},
            "min": {"type": "float", "value": 0.0},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 1020},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 1.0}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Chase Intensity",
        "thumbnail_visible": True
    })

    # -------------------------------------------------------------------------
    # Direction Encoding & Active Detection Math
    # -------------------------------------------------------------------------
    # Direction Weight Multipliers (Nodes 312..316 for weights 2..6)
    weights = [(312, 2.0), (313, 3.0), (314, 4.0), (315, 5.0), (316, 6.0)]
    for wid, wval in weights:
        add_node(wid, {
            "attributes": {"flow": {"type": "flow", "value": "event"}, "has-max": {"type": "bool", "value": False}, "has-min": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "options-count": {"type": "integer", "value": 0}, "unit": {"type": "integer", "value": 0}, "widget": {"type": "integer", "value": 0}},
            "bounds": {"height": 30, "width": 80, "x": 780, "y": int(wid)*30 - 9200},
            "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
            "clock": "video",
            "color": "ff20c7bb",
            "constants": {"input": {"type": "float", "value": wval}},
            "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
            "name": f"Weight {int(wval)}",
            "thumbnail_visible": False
        })

    mult_pairs = [
        (322, 303, 312), # B2 * 2.0
        (323, 304, 313), # B3 * 3.0
        (324, 305, 314), # B4 * 4.0
        (325, 306, 315), # B5 * 5.0
        (326, 307, 316), # B6 * 6.0
    ]
    for mid, bid, wid in mult_pairs:
        add_node(mid, {
            "attributes": make_attr_float_mult(),
            "bounds": {"height": 50, "width": 100, "x": 880, "y": mid*10 - 3100},
            "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
            "clock": "video",
            "color": "ffff6a00",
            "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
            "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
            "name": f"Weight Mult {mid}",
            "thumbnail_visible": False
        })
        connect(bid, "output", mid, "input0")
        connect(wid, "output", mid, "input1")

    # Add 6 terms for dir: B1(302) + 2*B2(322) + 3*B3(323) + 4*B4(324) + 5*B5(325) + 6*B6(326) (Node 330)
    add_node(330, {
        "attributes": make_attr_float_add(6),
        "bounds": {"height": 140, "width": 130, "x": 1020, "y": 200},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(6)},
        "hidden": ["size", "flow"] + [f"type{i}" for i in range(6)] + [f"input{i}-dimensions" for i in range(6)],
        "name": "Encoded Direction",
        "thumbnail_visible": True
    })
    connect(302, "output", 330, "input0")
    connect(322, "output0", 330, "input1")
    connect(323, "output0", 330, "input2")
    connect(324, "output0", 330, "input3")
    connect(325, "output0", 330, "input4")
    connect(326, "output0", 330, "input5")

    # Active Detection: Sum all 7 buttons (Node 340)
    add_node(340, {
        "attributes": make_attr_float_add(7),
        "bounds": {"height": 160, "width": 130, "x": 820, "y": -100},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(7)},
        "hidden": ["size", "flow"] + [f"type{i}" for i in range(7)] + [f"input{i}-dimensions" for i in range(7)],
        "name": "Sum 7 Triggers",
        "thumbnail_visible": True
    })
    for idx, (cid, _, _) in enumerate(chase_buttons):
        connect(cid, "output", 340, f"input{idx}")

    # Clamp Active State (Node 341)
    add_node(341, {
        "attributes": make_attr_clamp(),
        "bounds": {"height": 82, "width": 130, "x": 980, "y": -100},
        "class": {"id": "77697265-7557-4053-ABEC-73E2A9786804", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"max": {"type": "float", "value": 1.0}, "min": {"type": "float", "value": 0.0}, "value": {"type": "float", "value": 0.0}},
        "hidden": ["value-type", "min-type", "max-type", "flow", "value-dimensions", "min-dimensions", "max-dimensions"],
        "name": "Chase Active Gate",
        "thumbnail_visible": True
    })
    connect(340, "output0", 341, "value")

    # -------------------------------------------------------------------------
    # Slice Math & Oscillators
    # -------------------------------------------------------------------------
    add_node(61, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 800, "y": 620},
        "class": {"id": "77697265-0D55-485E-813D-706DD5DFE88D", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 2.0}, "input1": {"type": "float", "value": 5.0}},
        "hidden": ["flow", "size", "type0", "input0-dimensions", "type1", "input1-dimensions"],
        "name": "Calc Slice Width",
        "thumbnail_visible": True
    })
    connect(31, "output", 61, "input1")

    # Saw Oscillator (Node 62) - Left-Right & Down-Up
    add_node(62, {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": 1200, "y": 420},
        "class": {"id": "77697265-F95F-41D8-8FC4-DF0DC56E1051", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "amplitude": {"type": "float", "value": 1.0},
            "frequency": {"type": "float", "value": 1.2},
            "offset": {"type": "float", "value": 0.0},
            "phase-offset": {"type": "float", "value": 0.0},
            "reset-phase": {"type": "trigger", "value": None}
        },
        "hidden": ["instances", "reset-phase", "unipolar", "anti-alias", "amplitude", "offset", "phase-offset"],
        "name": "Saw Sweep",
        "thumbnail_visible": True
    })
    connect(34, "output", 62, "frequency")

    # Negate Saw (Node 63) - Right-Left & Up-Down
    add_node(63, {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "input0-dimensions": {"type": "integer", "value": 1}, "input0-type": {"type": "type", "value": "float"}},
        "bounds": {"height": 30, "width": 130, "x": 1420, "y": 420},
        "class": {"id": "77697265-1296-4264-A646-5CE3BE529286", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}},
        "hidden": ["input0-type", "flow", "input0-dimensions"],
        "name": "Negate Saw",
        "thumbnail_visible": True
    })
    connect(62, "output", 63, "input0")

    # Triangle Oscillator Unipolar (Node 64) - Center to Out
    add_node(64, {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": True}},
        "bounds": {"height": 130, "width": 195, "x": 1200, "y": 580},
        "class": {"id": "77697265-9890-41DC-A93D-9F3913A78FEB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "amplitude": {"type": "float", "value": 1.0},
            "frequency": {"type": "float", "value": 1.2},
            "offset": {"type": "float", "value": 0.0},
            "phase-offset": {"type": "float", "value": 0.0},
            "reset-phase": {"type": "trigger", "value": None}
        },
        "hidden": ["instances", "reset-phase", "unipolar", "anti-alias", "amplitude", "offset", "phase-offset"],
        "name": "Triangle Center",
        "thumbnail_visible": True
    })
    connect(34, "output", 64, "frequency")

    # Negate Triangle (Node 80)
    add_node(80, {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "input0-dimensions": {"type": "integer", "value": 1}, "input0-type": {"type": "type", "value": "float"}},
        "bounds": {"height": 30, "width": 130, "x": 1420, "y": 580},
        "class": {"id": "77697265-1296-4264-A646-5CE3BE529286", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}},
        "hidden": ["input0-type", "flow", "input0-dimensions"],
        "name": "Negate Triangle",
        "thumbnail_visible": True
    })
    connect(64, "output", 80, "input0")

    # Out to Center Calc (Node 81)
    add_node(81, {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 1570, "y": 580},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Out to Center Calc",
        "thumbnail_visible": True
    })
    connect(80, "output0", 81, "input1")

    # Triangle Oscillator Bipolar (Node 79) - Bounce
    add_node(79, {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": False}},
        "bounds": {"height": 130, "width": 195, "x": 1200, "y": 740},
        "class": {"id": "77697265-9890-41DC-A93D-9F3913A78FEB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "amplitude": {"type": "float", "value": 1.0},
            "frequency": {"type": "float", "value": 1.2},
            "offset": {"type": "float", "value": 0.0},
            "phase-offset": {"type": "float", "value": 0.0},
            "reset-phase": {"type": "trigger", "value": None}
        },
        "hidden": ["instances", "reset-phase", "unipolar", "anti-alias", "amplitude", "offset", "phase-offset"],
        "name": "Ping-Pong Osc",
        "thumbnail_visible": True
    })
    connect(34, "output", 79, "frequency")

    # Switch Raw Pos X (Node 65) - Driven by Encoded Direction (Node 330)
    add_node(65, {
        "attributes": make_attr_float_switch(7),
        "bounds": {"height": 160, "width": 195, "x": 1750, "y": 380},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(7)},
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Switch Raw X",
        "thumbnail_visible": True
    })
    connect(330, "output0", 65, "selection")
    connect(62, "output", 65, "input0")   # 0: Left to Right
    connect(63, "output0", 65, "input1")  # 1: Right to Left
    connect(64, "output", 65, "input2")   # 2: Center to Out
    connect(81, "output0", 65, "input3")  # 3: Out to Center
    # input4, input5 stay 0.0
    connect(79, "output", 65, "input6")   # 6: Bounce

    # Switch Raw Pos Y (Node 66) - Driven by Encoded Direction (Node 330)
    add_node(66, {
        "attributes": make_attr_float_switch(7),
        "bounds": {"height": 160, "width": 195, "x": 1750, "y": 570},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {f"input{i}": {"type": "float", "value": 0.0} for i in range(7)},
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Switch Raw Y",
        "thumbnail_visible": True
    })
    connect(330, "output0", 66, "selection")
    connect(63, "output0", 66, "input4")  # 4: Up to Down
    connect(62, "output", 66, "input5")   # 5: Down to Up

    # Quantize Pos X (Node 67)
    add_node(67, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input0-type": {"type": "type", "value": "float"},
            "input1-dimensions": {"type": "integer", "value": 1},
            "input1-type": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 58, "width": 130, "x": 1980, "y": 380},
        "class": {"id": "77697265-548F-4EF6-9B00-F3005FEC8687", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.4}},
        "hidden": ["input0-type", "input1-type", "flow", "input0-dimensions", "input1-dimensions"],
        "name": "Quantize X",
        "thumbnail_visible": True
    })
    connect(65, "output", 67, "input0")
    connect(61, "output0", 67, "input1")

    # Quantize Pos Y (Node 68)
    add_node(68, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input0-type": {"type": "type", "value": "float"},
            "input1-dimensions": {"type": "integer", "value": 1},
            "input1-type": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 58, "width": 130, "x": 1980, "y": 570},
        "class": {"id": "77697265-548F-4EF6-9B00-F3005FEC8687", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.4}},
        "hidden": ["input0-type", "input1-type", "flow", "input0-dimensions", "input1-dimensions"],
        "name": "Quantize Y",
        "thumbnail_visible": True
    })
    connect(66, "output", 68, "input0")
    connect(61, "output0", 68, "input1")

    # Switch Snap X (Node 69)
    add_node(69, {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 100, "width": 195, "x": 2150, "y": 380},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "selection": {"type": "integer", "value": 1}},
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Switch Snap X",
        "thumbnail_visible": True
    })
    connect(32, "output", 69, "selection")
    connect(65, "output", 69, "input0")
    connect(67, "output0", 69, "input1")

    # Switch Snap Y (Node 70)
    add_node(70, {
        "attributes": make_attr_float_switch(2),
        "bounds": {"height": 100, "width": 195, "x": 2150, "y": 570},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}, "selection": {"type": "integer", "value": 1}},
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Switch Snap Y",
        "thumbnail_visible": True
    })
    connect(32, "output", 70, "selection")
    connect(66, "output", 70, "input0")
    connect(68, "output0", 70, "input1")

    # Final Translation Float2 (Node 71)
    add_node(71, {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 2380, "y": 450},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Final Translation",
        "thumbnail_visible": True
    })
    connect(69, "output", 71, "input0")
    connect(70, "output", 71, "input1")

    # Switch Bar Width (Node 72)
    add_node(72, {
        "attributes": make_attr_float_switch(7),
        "bounds": {"height": 160, "width": 195, "x": 1750, "y": 760},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "input0": {"type": "float", "value": 0.4},
            "input1": {"type": "float", "value": 0.4},
            "input2": {"type": "float", "value": 0.4},
            "input3": {"type": "float", "value": 0.4},
            "input4": {"type": "float", "value": 2.0},
            "input5": {"type": "float", "value": 2.0},
            "input6": {"type": "float", "value": 0.4},
            "selection": {"type": "integer", "value": 0}
        },
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Switch Bar Width",
        "thumbnail_visible": True
    })
    connect(330, "output0", 72, "selection")
    connect(61, "output0", 72, "input0")
    connect(61, "output0", 72, "input1")
    connect(61, "output0", 72, "input2")
    connect(61, "output0", 72, "input3")
    connect(61, "output0", 72, "input6")

    # Switch Bar Height (Node 73)
    add_node(73, {
        "attributes": make_attr_float_switch(7),
        "bounds": {"height": 160, "width": 195, "x": 1750, "y": 950},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "input0": {"type": "float", "value": 2.0},
            "input1": {"type": "float", "value": 2.0},
            "input2": {"type": "float", "value": 2.0},
            "input3": {"type": "float", "value": 2.0},
            "input4": {"type": "float", "value": 0.4},
            "input5": {"type": "float", "value": 0.4},
            "input6": {"type": "float", "value": 2.0},
            "selection": {"type": "integer", "value": 0}
        },
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Switch Bar Height",
        "thumbnail_visible": True
    })
    connect(330, "output0", 73, "selection")
    connect(61, "output0", 73, "input4")
    connect(61, "output0", 73, "input5")

    # Procedural Rectangle (Node 74)
    add_node(74, {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 195, "x": 2150, "y": 800},
        "class": {"id": "77697265-4db6-4573-8aa7-42362bc44931", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"height": {"type": "float", "value": 2.0}, "round": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]}, "width": {"type": "float", "value": 0.4}},
        "hidden": ["instances", "round"],
        "name": "Chase Bar",
        "thumbnail_visible": True
    })
    connect(72, "output", 74, "width")
    connect(73, "output", 74, "height")

    # Move Procedural Shape (Node 75)
    add_node(75, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input-type": {"type": "type", "value": "procedural"},
            "instances": {"type": "integer", "value": 1},
            "translation-type": {"type": "type", "value": "float2"}
        },
        "bounds": {"height": 58, "width": 195, "x": 2550, "y": 450},
        "class": {"id": "77697265-0e5a-4bfd-b136-e4f68P3cc463", "version": 3},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {"input": {"type": "procedural", "value": None}, "translation": {"type": "float2", "value": [0.0, 0.0]}},
        "hidden": ["input-type", "translation-type", "flow", "instances"],
        "name": "Move Beam",
        "thumbnail_visible": True
    })
    connect(74, "output", 75, "input")
    connect(71, "output", 75, "translation")

    # Shape Render (Node 76)
    add_node(76, {
        "attributes": {
            "antialising-direction": {"type": "integer", "value": 0},
            "bitdepth": {"type": "integer", "value": 0},
            "material-dimensions": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]},
            "shape-dimensions": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 195, "x": 2550, "y": 600},
        "class": {"id": "77697265-EA26-47D6-985A-B4D5DC314BF7", "version": 2},
        "clock": "video",
        "color": "ff2dc18a",
        "constants": {
            "antialiasing": {"type": "float", "value": 4.0},
            "camera": {"type": "camera2d", "value": {"projection": [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1], "view": [1,0,0,0,0,1,0,0,0,0,-1,0,0,0,0,1]}},
            "material": {"type": "float4", "value": [1.0, 0.85, 0.3, 1.0]},
            "shape": {"type": "procedural", "value": None}
        },
        "hidden": ["antialising-direction", "antialiasing", "shape-dimensions", "material-dimensions", "resolution-mode", "resolution-relative", "resolution-absolute", "bitdepth"],
        "name": "Render Beam",
        "thumbnail_visible": True
    })
    connect(75, "output", 76, "shape")
    connect(35, "output", 76, "material")

    # Chase Gate: Multiply Chase Intensity * chase_active (Node 77)
    add_node(77, {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 1150, "y": -100},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Chase Gate",
        "thumbnail_visible": True
    })
    connect(36, "output", 77, "input0")
    connect(341, "output0", 77, "input1")

    # Chase Mixer (Node 78)
    add_node(78, {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "input-count": {"type": "integer", "value": 2},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 154, "width": 195, "x": 1300, "y": 0},
        "class": {"id": "77697265-A270-4D60-911C-A88B1BE6369A", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "bypass": {"type": "bool", "value": False},
            "input1": {"type": "texture2d", "value": None},
            "input2": {"type": "texture2d", "value": None},
            "mode": {"type": "integer", "value": 11},
            "opacity1": {"type": "float", "value": 1.0},
            "opacity2": {"type": "float", "value": 0.0}
        },
        "hidden": ["bypass", "input-count", "bitdepth", "resolution-absolute", "resolution-relative", "resolution-mode", "instances"],
        "name": "Chase Mixer",
        "thumbnail_visible": True
    })
    connect(27, "output", 78, "input1")
    connect(76, "output0", 78, "input2")
    connect(77, "output0", 78, "opacity2")

    # =========================================================================
    # 4. STROBE MODULE (High-Speed Piano Flash)
    # =========================================================================
    add_node(50, {
        "attributes": {"bool-view": {"type": "integer", "value": 0}, "flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 140, "x": 1500, "y": -400},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": False}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": "Strobe",
        "thumbnail_visible": True
    })

    add_node(52, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": 30.0},
            "min": {"type": "float", "value": 2.0},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 1500, "y": -280},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 14.0}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Strobe Rate",
        "thumbnail_visible": True
    })

    add_node(53, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": 1.0},
            "min": {"type": "float", "value": 0.0},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 1500, "y": -160},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 0.9}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Strobe Intensity",
        "thumbnail_visible": True
    })

    # Combine Strobe + Master Punch (Node 151)
    add_node(151, {
        "attributes": make_attr_float_add(2),
        "bounds": {"height": 82, "width": 130, "x": 1680, "y": -400},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Strobe+Punch Add",
        "thumbnail_visible": True
    })
    connect(50, "output", 151, "input0")
    connect(90, "output", 151, "input1")

    # Clamp Strobe Active (Node 152)
    add_node(152, {
        "attributes": make_attr_clamp(),
        "bounds": {"height": 82, "width": 130, "x": 1840, "y": -400},
        "class": {"id": "77697265-7557-4053-ABEC-73E2A9786804", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"max": {"type": "float", "value": 1.0}, "min": {"type": "float", "value": 0.0}, "value": {"type": "float", "value": 0.0}},
        "hidden": ["value-type", "min-type", "max-type", "flow", "value-dimensions", "min-dimensions", "max-dimensions"],
        "name": "Strobe Clamp",
        "thumbnail_visible": True
    })
    connect(151, "output0", 152, "value")

    # Strobe Pulse Oscillator (Node 54)
    add_node(54, {
        "attributes": {"anti-alias": {"type": "bool", "value": False}, "instances": {"type": "integer", "value": 1}, "unipolar": {"type": "bool", "value": True}},
        "bounds": {"height": 130, "width": 195, "x": 1680, "y": -250},
        "class": {"id": "77697265-6256-4856-911C-5465AE6BF656", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "amplitude": {"type": "float", "value": 1.0},
            "frequency": {"type": "float", "value": 14.0},
            "offset": {"type": "float", "value": 0.0},
            "phase-offset": {"type": "float", "value": 0.0},
            "pulse-width": {"type": "float", "value": 0.3},
            "reset-phase": {"type": "trigger", "value": None}
        },
        "hidden": ["instances", "reset-phase", "unipolar", "anti-alias", "amplitude", "offset", "phase-offset", "pulse-width"],
        "name": "Strobe Clock",
        "thumbnail_visible": True
    })
    connect(52, "output", 54, "frequency")

    # Multiply Strobe Clock with Strobe Clamp (Node 57)
    add_node(57, {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 1920, "y": -250},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Strobe Pulse",
        "thumbnail_visible": True
    })
    connect(54, "output", 57, "input0")
    connect(152, "output0", 57, "input1")

    # Multiply with Strobe Intensity (Node 58)
    add_node(58, {
        "attributes": make_attr_float_mult(),
        "bounds": {"height": 82, "width": 130, "x": 1920, "y": -120},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Flash Opacity",
        "thumbnail_visible": True
    })
    connect(57, "output0", 58, "input0")
    connect(53, "output", 58, "input1")

    # White Flash Solid Color (Node 59)
    add_node(59, {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 58, "width": 195, "x": 1920, "y": 200},
        "class": {"id": "77697265-E8EC-4F1B-901A-CFFC104D3B07", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"bypass": {"type": "bool", "value": False}, "color": {"type": "color", "value": [1.0, 1.0, 1.0, 1.0]}},
        "hidden": ["instances", "bypass", "bitdepth", "resolution-absolute", "resolution-relative", "resolution-mode"],
        "name": "White Flash",
        "thumbnail_visible": True
    })

    # Strobe Video Mixer (Node 60)
    add_node(60, {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "input-count": {"type": "integer", "value": 2},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 154, "width": 195, "x": 2100, "y": 0},
        "class": {"id": "77697265-A270-4D60-911C-A88B1BE6369A", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "bypass": {"type": "bool", "value": False},
            "input1": {"type": "texture2d", "value": None},
            "input2": {"type": "texture2d", "value": None},
            "mode": {"type": "integer", "value": 11},
            "opacity1": {"type": "float", "value": 1.0},
            "opacity2": {"type": "float", "value": 0.0}
        },
        "hidden": ["bypass", "input-count", "bitdepth", "resolution-absolute", "resolution-relative", "resolution-mode", "instances"],
        "name": "Strobe Mixer",
        "thumbnail_visible": True
    })
    connect(78, "output", 60, "input1")
    connect(59, "output", 60, "input2")
    connect(58, "output0", 60, "opacity2")

    # Connect Strobe Output to Master Dry/Wet Mixer (Node 98 input2)
    connect(60, "output", 98, "input2")

    return patch

if __name__ == "__main__":
    patch_data = build_patch()
    target_dir = r"C:\ANDREAS\ip26-zzfx"
    os.makedirs(target_dir, exist_ok=True)
    wire_file = os.path.join(target_dir, "zzfx.wire")
    cwired_file = os.path.join(target_dir, "zzfx.cwired")

    with open(wire_file, "w", encoding="utf-8") as f:
        json.dump(patch_data, f, indent=2)

    print(f"Generated {wire_file} ({len(patch_data['patch']['nodes'])} nodes, {len(patch_data['patch']['connections'])} connections)")
