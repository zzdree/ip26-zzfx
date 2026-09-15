import json
import os
import subprocess
import sys

def build_patch():
    patch = {
        "formatVersion": {
            "major": 1,
            "minor": 1,
            "patch": 0
        },
        "patch": {
            "connections": [],
            "inputOrder": [
                0,    # Texture In
                90,   # Master Punch (Trigger In)
                97,   # Master Mix (Float In)
                10,   # Push Enable (Bool In)
                11,   # Push Trigger (Trigger In)
                12,   # Push Amount (Float In)
                13,   # Push Decay (Float In)
                20,   # Outline Enable (Bool In)
                21,   # Outline Strength (Float In)
                22,   # Outline Color (Color In)
                23,   # Outline Mix (Float In)
                30,   # Chase Enable (Bool In)
                37,   # Chase Trigger (Trigger In - Momentary Sweep / Burst)
                31,   # Grid Slices (Int In - default 5)
                32,   # Snap to Grid (Bool In - discrete vs smooth)
                33,   # Chase Direction (Int In Dropdown: 7 directions!)
                34,   # Chase Speed (Float In)
                35,   # Chase Color (Color In)
                36,   # Chase Intensity (Float In)
                50,   # Strobe Enable (Bool In)
                51,   # Strobe Trigger (Trigger In)
                52,   # Strobe Rate (Float In)
                53    # Strobe Intensity (Float In)
            ],
            "meta": {
                "author": "Andreas - IP26 Production",
                "category": "Effect",
                "description": "IP26 Multi-Performance Rack: Push, Multi-Direction Grid Chaser (7 Patterns / 1-10 Slices / H&V), Strobe, Outline, and Master Punch for Ibadah Perdana UKK UNNES 2026 (Universal Resolution / 2400x720 / 16:9).",
                "displayName": "zzfx",
                "identifier": "ip26.andreas.zzfx",
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
                "version": "1.1.0"
            },
            "nextNodeId": 180,
            "nodes": {},
            "ui": {
                "pan": {"x": 0.0, "y": 0.0},
                "zoom": 1.0
            }
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

    def float_multiply_attr():
        return {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        }

    def float_add_attr():
        return {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        }

    def float_switch_attr(cases_count):
        return {
            "case-type": {"type": "type", "value": "float"},
            "flow": {"type": "flow", "value": "signal"},
            "instances": {"type": "integer", "value": 1},
            "selection-type": {"type": "type", "value": "integer"},
            "size": {"type": "integer", "value": cases_count}
        }

    # =========================================================================
    # 0. INPUT & MASTER SECTION
    # =========================================================================
    # Texture In (Node 0)
    add_node(0, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 195, "x": -600, "y": 0},
        "class": {"id": "77697265-B2A2-4C1C-8C4C-2915D78CC8E9", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "texture2d", "value": None}},
        "name": "Texture In",
        "thumbnail_visible": True
    })

    # Master Punch Trigger In (Node 90) - Combo button for drops
    add_node(90, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 140, "x": -600, "y": 200},
        "class": {"id": "77697265-e61f-42c0-862a-0dca04e14569", "version": 1},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {"input": {"type": "trigger", "value": None}},
        "hidden": ["instances", "flow"],
        "name": "Master Punch",
        "thumbnail_visible": True
    })

    # Master Mix Float In (Node 97) - Global Dry/Wet
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
        "bounds": {"height": 82, "width": 140, "x": 1900, "y": 200},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 1.0}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Master Mix",
        "thumbnail_visible": True
    })

    # Master Dry/Wet Video Mixer (Node 98)
    add_node(98, {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "input-count": {"type": "integer", "value": 2},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0}, # Auto from input
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
            "mode": {"type": "integer", "value": 0}, # Normal alpha blend
            "opacity1": {"type": "float", "value": 1.0},
            "opacity2": {"type": "float", "value": 1.0}
        },
        "hidden": ["bypass", "input-count", "bitdepth", "resolution-absolute", "resolution-relative", "resolution-mode", "instances"],
        "name": "Dry/Wet Mixer",
        "thumbnail_visible": True
    })

    # Texture Out (Node 99)
    add_node(99, {
        "attributes": {
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 195, "x": 2350, "y": 0},
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
    # 1. PUSH MODULE (Zoom / Kick Punch)
    # =========================================================================
    add_node(10, {
        "attributes": {
            "bool-view": {"type": "integer", "value": 0},
            "flow": {"type": "flow", "value": "signal"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 140, "x": -400, "y": -400},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": True}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": "Push Enable",
        "thumbnail_visible": True
    })

    add_node(11, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 140, "x": -400, "y": -300},
        "class": {"id": "77697265-e61f-42c0-862a-0dca04e14569", "version": 1},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {"input": {"type": "trigger", "value": None}},
        "hidden": ["instances", "flow"],
        "name": "Push Trigger",
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
        "bounds": {"height": 82, "width": 140, "x": -400, "y": -200},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 0.4}},
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
            "min": {"type": "float", "value": 0.05},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": -400, "y": -100},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 0.25}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Push Decay",
        "thumbnail_visible": True
    })

    add_node(14, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 130, "width": 195, "x": -200, "y": -250},
        "class": {"id": "77697265-D980-43B3-9237-6683B154A5B0", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "attack-time": {"type": "float", "value": 0.01},
            "linear": {"type": "bool", "value": False},
            "release": {"type": "trigger", "value": None},
            "release-time": {"type": "float", "value": 0.25},
            "reset": {"type": "trigger", "value": None},
            "restart-at-zero": {"type": "bool", "value": False},
            "trigger": {"type": "trigger", "value": None}
        },
        "hidden": ["instances", "flow", "attack-time", "linear", "restart-at-zero", "reset", "release"],
        "name": "Push Envelope",
        "thumbnail_visible": True
    })
    connect(11, "output", 14, "trigger")
    connect(90, "output", 14, "trigger")
    connect(13, "output", 14, "release-time")

    add_node(15, {
        "attributes": float_multiply_attr(),
        "bounds": {"height": 82, "width": 130, "x": 30, "y": -250},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Push Gain",
        "thumbnail_visible": True
    })
    connect(14, "output", 15, "input0")
    connect(12, "output", 15, "input1")

    add_node(16, {
        "attributes": float_multiply_attr(),
        "bounds": {"height": 82, "width": 130, "x": 190, "y": -250},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Push Gate",
        "thumbnail_visible": True
    })
    connect(15, "output0", 16, "input0")
    connect(10, "output", 16, "input1")

    add_node(17, {
        "attributes": float_add_attr(),
        "bounds": {"height": 82, "width": 130, "x": 350, "y": -250},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Add Base Scale",
        "thumbnail_visible": True
    })
    connect(16, "output0", 17, "input1")

    add_node(19, {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 350, "y": -120},
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
    # 2. OUTLINE MODULE (Sobel Edge + Neon Tint + Add Blend)
    # =========================================================================
    add_node(20, {
        "attributes": {
            "bool-view": {"type": "integer", "value": 0},
            "flow": {"type": "flow", "value": "signal"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 140, "x": 100, "y": 400},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": False}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": "Outline Enable",
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
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "instances": {"type": "integer", "value": 1},
            "options-count": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 100, "y": 600},
        "class": {"id": "77697265-4C9E-4F75-B4F0-5415B713EA1B", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "color", "value": [0.0, 0.85, 1.0, 1.0]}},
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
        "constants": {"input": {"type": "float", "value": 0.8}},
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
        "attributes": float_multiply_attr(),
        "bounds": {"height": 82, "width": 130, "x": 320, "y": 400},
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

    # Outline Mixer
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
    # 3. CHASE MODULE (7 Directions, Grid Slices, Snap-to-Grid, Momentary Trigger)
    # =========================================================================
    # Chase Enable Bool In (Node 30) - Continuous toggle
    add_node(30, {
        "attributes": {
            "bool-view": {"type": "integer", "value": 0},
            "flow": {"type": "flow", "value": "signal"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 250},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": False}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": "Chase Enable",
        "thumbnail_visible": True
    })

    # Chase Trigger In (Node 37) - Shortcut momentary sweep button
    add_node(37, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 350},
        "class": {"id": "77697265-e61f-42c0-862a-0dca04e14569", "version": 1},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {"input": {"type": "trigger", "value": None}},
        "hidden": ["instances", "flow"],
        "name": "Chase Trigger",
        "thumbnail_visible": True
    })

    # Chase Momentary Burst Envelope (Node 38)
    add_node(38, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 130, "width": 195, "x": 760, "y": 350},
        "class": {"id": "77697265-D980-43B3-9237-6683B154A5B0", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "attack-time": {"type": "float", "value": 0.01},
            "linear": {"type": "bool", "value": False},
            "release": {"type": "trigger", "value": None},
            "release-time": {"type": "float", "value": 0.45},
            "reset": {"type": "trigger", "value": None},
            "restart-at-zero": {"type": "bool", "value": False},
            "trigger": {"type": "trigger", "value": None}
        },
        "hidden": ["instances", "flow", "attack-time", "linear", "restart-at-zero", "reset", "release", "release-time"],
        "name": "Chase Envelope",
        "thumbnail_visible": True
    })
    connect(37, "output", 38, "trigger")

    # Combine Chase Enable + Chase Burst Envelope (Node 39)
    add_node(39, {
        "attributes": float_add_attr(),
        "bounds": {"height": 82, "width": 130, "x": 980, "y": 280},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Chase Gate Add",
        "thumbnail_visible": True
    })
    connect(30, "output", 39, "input0")
    connect(38, "output", 39, "input1")

    # Grid Slices Int In (Node 31) - default 5 slices
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
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 450},
        "class": {"id": "77697265-2649-4abb-b38f-4e1005183415", "version": 2},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "integer", "value": 5}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Grid Slices",
        "thumbnail_visible": True
    })

    # Snap to Grid Bool In (Node 32)
    add_node(32, {
        "attributes": {
            "bool-view": {"type": "integer", "value": 0},
            "flow": {"type": "flow", "value": "signal"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 550},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": True}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": "Snap to Grid",
        "thumbnail_visible": True
    })

    # Chase Direction Int In Dropdown (Node 33) - 7 Animation Patterns!
    add_node(33, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "integer", "value": 6},
            "min": {"type": "integer", "value": 0},
            "option0-label": {"type": "string", "value": "Left to Right"},
            "option0-value": {"type": "integer", "value": 0},
            "option1-label": {"type": "string", "value": "Right to Left"},
            "option1-value": {"type": "integer", "value": 1},
            "option2-label": {"type": "string", "value": "Center to Out"},
            "option2-value": {"type": "integer", "value": 2},
            "option3-label": {"type": "string", "value": "Out to Center"},
            "option3-value": {"type": "integer", "value": 3},
            "option4-label": {"type": "string", "value": "Up to Down"},
            "option4-value": {"type": "integer", "value": 4},
            "option5-label": {"type": "string", "value": "Down to Up"},
            "option5-value": {"type": "integer", "value": 5},
            "option6-label": {"type": "string", "value": "Bounce / Ping-Pong"},
            "option6-value": {"type": "integer", "value": 6},
            "options-count": {"type": "integer", "value": 7},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 1} # Dropdown
        },
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 650},
        "class": {"id": "77697265-2649-4abb-b38f-4e1005183415", "version": 2},
        "clock": "video",
        "color": "ffd0c117",
        "constants": {"input": {"type": "integer", "value": 0}},
        "hidden": [
            "flow", "has-max", "has-min", "input", "instances", "max", "min",
            "option0-label", "option0-value", "option1-label", "option1-value",
            "option2-label", "option2-value", "option3-label", "option3-value",
            "option4-label", "option4-value", "option5-label", "option5-value",
            "option6-label", "option6-value",
            "options-count", "widget", "unit"
        ],
        "name": "Chase Direction",
        "thumbnail_visible": True
    })

    # Chase Speed Float In (Node 34)
    add_node(34, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "has-max": {"type": "bool", "value": True},
            "has-min": {"type": "bool", "value": True},
            "instances": {"type": "integer", "value": 1},
            "max": {"type": "float", "value": 8.0},
            "min": {"type": "float", "value": 0.2},
            "options-count": {"type": "integer", "value": 0},
            "unit": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 750},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 1.2}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Chase Speed",
        "thumbnail_visible": True
    })

    # Chase Color Color In (Node 35)
    add_node(35, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "instances": {"type": "integer", "value": 1},
            "options-count": {"type": "integer", "value": 0},
            "widget": {"type": "integer", "value": 0}
        },
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 850},
        "class": {"id": "77697265-4C9E-4F75-B4F0-5415B713EA1B", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "color", "value": [1.0, 0.85, 0.3, 1.0]}},
        "hidden": ["input", "instances", "flow", "options-count", "widget"],
        "name": "Chase Color",
        "thumbnail_visible": True
    })

    # Chase Intensity Float In (Node 36)
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
        "bounds": {"height": 82, "width": 140, "x": 600, "y": 950},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 0.8}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Chase Intensity",
        "thumbnail_visible": True
    })

    # Divide 2.0 by Grid Slices to get Slice Width (Node 61)
    add_node(61, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input1-dimensions": {"type": "integer", "value": 1},
            "size": {"type": "integer", "value": 2},
            "type0": {"type": "type", "value": "float"},
            "type1": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 82, "width": 130, "x": 800, "y": 450},
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
        "attributes": {
            "anti-alias": {"type": "bool", "value": False},
            "instances": {"type": "integer", "value": 1},
            "unipolar": {"type": "bool", "value": False}
        },
        "bounds": {"height": 130, "width": 195, "x": 800, "y": 580},
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
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input0-type": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 30, "width": 130, "x": 1020, "y": 580},
        "class": {"id": "77697265-1296-4264-A646-5CE3BE529286", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}},
        "hidden": ["input0-type", "flow", "input0-dimensions"],
        "name": "Negate Saw",
        "thumbnail_visible": True
    })
    connect(62, "output", 63, "input0")

    # Triangle Oscillator (Node 64) - Center to Out (Unipolar: 0.0 center to 1.0 edges)
    add_node(64, {
        "attributes": {
            "anti-alias": {"type": "bool", "value": False},
            "instances": {"type": "integer", "value": 1},
            "unipolar": {"type": "bool", "value": True}
        },
        "bounds": {"height": 130, "width": 195, "x": 800, "y": 740},
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

    # Negate Triangle (Node 80) for Out to Center
    add_node(80, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input0-type": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 30, "width": 130, "x": 1020, "y": 740},
        "class": {"id": "77697265-1296-4264-A646-5CE3BE529286", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}},
        "hidden": ["input0-type", "flow", "input0-dimensions"],
        "name": "Negate Triangle",
        "thumbnail_visible": True
    })
    connect(64, "output", 80, "input0")

    # Add 1.0 to Negate Triangle (Node 81) -> 1.0 - Triangle (Out to Center)
    add_node(81, {
        "attributes": float_add_attr(),
        "bounds": {"height": 82, "width": 130, "x": 1170, "y": 740},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 1.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Out to Center Calc",
        "thumbnail_visible": True
    })
    connect(80, "output0", 81, "input1")

    # Triangle Oscillator (Node 79) - Bounce / Ping-Pong (Bipolar: -1.0 left to +1.0 right and back)
    add_node(79, {
        "attributes": {
            "anti-alias": {"type": "bool", "value": False},
            "instances": {"type": "integer", "value": 1},
            "unipolar": {"type": "bool", "value": False}
        },
        "bounds": {"height": 130, "width": 195, "x": 800, "y": 900},
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

    # Switch Raw Pos X (Node 65) - 7 Directions
    add_node(65, {
        "attributes": float_switch_attr(7),
        "bounds": {"height": 160, "width": 195, "x": 1350, "y": 550},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "input0": {"type": "float", "value": 0.0},
            "input1": {"type": "float", "value": 0.0},
            "input2": {"type": "float", "value": 0.0},
            "input3": {"type": "float", "value": 0.0},
            "input4": {"type": "float", "value": 0.0},
            "input5": {"type": "float", "value": 0.0},
            "input6": {"type": "float", "value": 0.0},
            "selection": {"type": "integer", "value": 0}
        },
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Switch Raw X",
        "thumbnail_visible": True
    })
    connect(33, "output", 65, "selection")
    connect(62, "output", 65, "input0")   # 0: Left to Right
    connect(63, "output0", 65, "input1")  # 1: Right to Left
    connect(64, "output", 65, "input2")   # 2: Center to Out
    connect(81, "output0", 65, "input3")  # 3: Out to Center
    # input4 (Up to Down) stays 0.0
    # input5 (Down to Up) stays 0.0
    connect(79, "output", 65, "input6")   # 6: Bounce / Ping-Pong

    # Switch Raw Pos Y (Node 66) - 7 Directions
    add_node(66, {
        "attributes": float_switch_attr(7),
        "bounds": {"height": 160, "width": 195, "x": 1350, "y": 740},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "input0": {"type": "float", "value": 0.0},
            "input1": {"type": "float", "value": 0.0},
            "input2": {"type": "float", "value": 0.0},
            "input3": {"type": "float", "value": 0.0},
            "input4": {"type": "float", "value": 0.0},
            "input5": {"type": "float", "value": 0.0},
            "input6": {"type": "float", "value": 0.0},
            "selection": {"type": "integer", "value": 0}
        },
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Switch Raw Y",
        "thumbnail_visible": True
    })
    connect(33, "output", 66, "selection")
    # input0, input1, input2, input3 stay 0.0
    connect(63, "output0", 66, "input4")  # 4: Up to Down (moves downwards)
    connect(62, "output", 66, "input5")   # 5: Down to Up (moves upwards)
    # input6 (Bounce) stays 0.0

    # Quantize Pos X (Node 67)
    add_node(67, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "input0-dimensions": {"type": "integer", "value": 1},
            "input0-type": {"type": "type", "value": "float"},
            "input1-dimensions": {"type": "integer", "value": 1},
            "input1-type": {"type": "type", "value": "float"}
        },
        "bounds": {"height": 58, "width": 130, "x": 1580, "y": 550},
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
        "bounds": {"height": 58, "width": 130, "x": 1580, "y": 740},
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

    # Switch Snap X (Node 69) - Case 0: Smooth Raw, Case 1: Quantized Slice
    add_node(69, {
        "attributes": float_switch_attr(2),
        "bounds": {"height": 106, "width": 130, "x": 1750, "y": 550},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "input0": {"type": "float", "value": 0.0},
            "input1": {"type": "float", "value": 0.0},
            "selection": {"type": "integer", "value": 1}
        },
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Snap Select X",
        "thumbnail_visible": True
    })
    connect(32, "output", 69, "selection")
    connect(65, "output", 69, "input0")
    connect(67, "output", 69, "input1")

    # Switch Snap Y (Node 70)
    add_node(70, {
        "attributes": float_switch_attr(2),
        "bounds": {"height": 106, "width": 130, "x": 1750, "y": 740},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "input0": {"type": "float", "value": 0.0},
            "input1": {"type": "float", "value": 0.0},
            "selection": {"type": "integer", "value": 1}
        },
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Snap Select Y",
        "thumbnail_visible": True
    })
    connect(32, "output", 70, "selection")
    connect(66, "output", 70, "input0")
    connect(68, "output", 70, "input1")

    # Beam Pos Vec2 (Node 71)
    add_node(71, {
        "attributes": {"flow": {"type": "flow", "value": "signal"}, "instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 82, "width": 130, "x": 1920, "y": 640},
        "class": {"id": "77697265-E7EF-4944-8FC2-D808EE0433CB", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "name": "Beam Position",
        "thumbnail_visible": True
    })
    connect(69, "output", 71, "input0")
    connect(70, "output", 71, "input1")

    # Switch Bar Width (Node 72) - 7 Directions
    add_node(72, {
        "attributes": float_switch_attr(7),
        "bounds": {"height": 160, "width": 130, "x": 1580, "y": 300},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "input0": {"type": "float", "value": 0.4},
            "input1": {"type": "float", "value": 0.4},
            "input2": {"type": "float", "value": 0.4},
            "input3": {"type": "float", "value": 0.4},
            "input4": {"type": "float", "value": 2.0}, # Full width when sweeping Up-Down
            "input5": {"type": "float", "value": 2.0}, # Full width when sweeping Down-Up
            "input6": {"type": "float", "value": 0.4}, # Ping-Pong
            "selection": {"type": "integer", "value": 0}
        },
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Switch Bar Width",
        "thumbnail_visible": True
    })
    connect(33, "output", 72, "selection")
    connect(61, "output0", 72, "input0") # 0: Left to Right
    connect(61, "output0", 72, "input1") # 1: Right to Left
    connect(61, "output0", 72, "input2") # 2: Center to Out
    connect(61, "output0", 72, "input3") # 3: Out to Center
    # input4 & input5 are constant 2.0 (horizontal bar sweeping vertically)
    connect(61, "output0", 72, "input6") # 6: Bounce / Ping-Pong

    # Switch Bar Height (Node 73) - 7 Directions
    add_node(73, {
        "attributes": float_switch_attr(7),
        "bounds": {"height": 160, "width": 130, "x": 1750, "y": 300},
        "class": {"id": "77697265-6899-4A9C-82AB-949346033440", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "input0": {"type": "float", "value": 2.0}, # Full height for horizontal sweeps
            "input1": {"type": "float", "value": 2.0},
            "input2": {"type": "float", "value": 2.0},
            "input3": {"type": "float", "value": 2.0},
            "input4": {"type": "float", "value": 0.4}, # Slice height for Up-Down
            "input5": {"type": "float", "value": 0.4}, # Slice height for Down-Up
            "input6": {"type": "float", "value": 2.0},
            "selection": {"type": "integer", "value": 0}
        },
        "hidden": ["selection-type", "case-type", "flow", "size", "instances"],
        "name": "Switch Bar Height",
        "thumbnail_visible": True
    })
    connect(33, "output", 73, "selection")
    # input0, 1, 2, 3 are constant 2.0 (vertical bar sweeping horizontally)
    connect(61, "output0", 73, "input4") # 4: Up to Down
    connect(61, "output0", 73, "input5") # 5: Down to Up
    # input6 is constant 2.0

    # Rectangle for Chase Bar (Node 74)
    add_node(74, {
        "attributes": {"instances": {"type": "integer", "value": 1}},
        "bounds": {"height": 106, "width": 195, "x": 1920, "y": 300},
        "class": {"id": "77697265-4db6-4573-8aa7-42362bc44931", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "height": {"type": "float", "value": 2.0},
            "round": {"type": "float4", "value": [0.0, 0.0, 0.0, 0.0]},
            "width": {"type": "float", "value": 0.4}
        },
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
        "bounds": {"height": 58, "width": 195, "x": 2150, "y": 450},
        "class": {"id": "77697265-0e5a-4bfd-b136-e4f68P3cc463", "version": 3},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {
            "input": {"type": "procedural", "value": None},
            "translation": {"type": "float2", "value": [0.0, 0.0]}
        },
        "hidden": ["input-type", "translation-type", "flow", "instances"],
        "name": "Move Beam",
        "thumbnail_visible": True
    })
    connect(74, "output", 75, "input")
    connect(71, "output", 75, "translation")

    # Shape Render for Chase Bar (Node 76)
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
        "bounds": {"height": 82, "width": 195, "x": 2150, "y": 600},
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

    # Multiply Chase Intensity with (Chase Enable + Chase Burst Envelope) (Node 77)
    add_node(77, {
        "attributes": float_multiply_attr(),
        "bounds": {"height": 82, "width": 130, "x": 1170, "y": 380},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Chase Gate",
        "thumbnail_visible": True
    })
    connect(36, "output", 77, "input0")
    connect(39, "output0", 77, "input1")

    # Video Mixer for Chase (Node 78)
    add_node(78, {
        "attributes": {
            "bitdepth": {"type": "integer", "value": 0},
            "input-count": {"type": "integer", "value": 2},
            "instances": {"type": "integer", "value": 1},
            "resolution-absolute": {"type": "float2", "value": [2400, 720]},
            "resolution-mode": {"type": "integer", "value": 0},
            "resolution-relative": {"type": "float2", "value": [1, 1]}
        },
        "bounds": {"height": 154, "width": 195, "x": 1050, "y": 0},
        "class": {"id": "77697265-A270-4D60-911C-A88B1BE6369A", "version": 3},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "bypass": {"type": "bool", "value": False},
            "input1": {"type": "texture2d", "value": None},
            "input2": {"type": "texture2d", "value": None},
            "mode": {"type": "integer", "value": 11}, # Add blend
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
    # 4. STROBE MODULE
    # =========================================================================
    add_node(50, {
        "attributes": {
            "bool-view": {"type": "integer", "value": 0},
            "flow": {"type": "flow", "value": "signal"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 140, "x": 1300, "y": -400},
        "class": {"id": "77697265-999C-4F8B-8B9D-3646DC68AA69", "version": 2},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input": {"type": "bool", "value": False}},
        "hidden": ["input", "instances", "flow", "bool-view"],
        "name": "Strobe Enable",
        "thumbnail_visible": True
    })

    add_node(51, {
        "attributes": {
            "flow": {"type": "flow", "value": "event"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 82, "width": 140, "x": 1300, "y": -300},
        "class": {"id": "77697265-e61f-42c0-862a-0dca04e14569", "version": 1},
        "clock": "video",
        "color": "ff02bbff",
        "constants": {"input": {"type": "trigger", "value": None}},
        "hidden": ["instances", "flow"],
        "name": "Strobe Trigger",
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
        "bounds": {"height": 82, "width": 140, "x": 1300, "y": -200},
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
        "bounds": {"height": 82, "width": 140, "x": 1300, "y": -100},
        "class": {"id": "77697265-D235-4A6A-B661-02ABE55C72FF", "version": 3},
        "clock": "video",
        "color": "ff20c7bb",
        "constants": {"input": {"type": "float", "value": 0.9}},
        "hidden": ["input", "instances", "flow", "has-min", "min", "has-max", "max", "options-count", "widget", "unit"],
        "name": "Strobe Intensity",
        "thumbnail_visible": True
    })

    add_node(54, {
        "attributes": {
            "anti-alias": {"type": "bool", "value": False},
            "instances": {"type": "integer", "value": 1},
            "unipolar": {"type": "bool", "value": True}
        },
        "bounds": {"height": 130, "width": 195, "x": 1480, "y": -200},
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

    add_node(55, {
        "attributes": {
            "flow": {"type": "flow", "value": "signal"},
            "instances": {"type": "integer", "value": 1}
        },
        "bounds": {"height": 130, "width": 195, "x": 1480, "y": -350},
        "class": {"id": "77697265-D980-43B3-9237-6683B154A5B0", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "attack-time": {"type": "float", "value": 0.01},
            "linear": {"type": "bool", "value": False},
            "release": {"type": "trigger", "value": None},
            "release-time": {"type": "float", "value": 0.35},
            "reset": {"type": "trigger", "value": None},
            "restart-at-zero": {"type": "bool", "value": False},
            "trigger": {"type": "trigger", "value": None}
        },
        "hidden": ["instances", "flow", "attack-time", "linear", "restart-at-zero", "reset", "release", "release-time"],
        "name": "Strobe Burst",
        "thumbnail_visible": True
    })
    connect(51, "output", 55, "trigger")
    connect(90, "output", 55, "trigger")

    add_node(56, {
        "attributes": float_add_attr(),
        "bounds": {"height": 82, "width": 130, "x": 1690, "y": -350},
        "class": {"id": "77697265-A9AF-4CB4-B10F-3968B36BB63B", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Strobe Gate",
        "thumbnail_visible": True
    })
    connect(50, "output", 56, "input0")
    connect(55, "output", 56, "input1")

    add_node(57, {
        "attributes": float_multiply_attr(),
        "bounds": {"height": 82, "width": 130, "x": 1690, "y": -200},
        "class": {"id": "77697265-A0D8-429A-A558-69BC58D0D425", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {"input0": {"type": "float", "value": 0.0}, "input1": {"type": "float", "value": 0.0}},
        "hidden": ["size", "input0-dimensions", "input1-dimensions", "type0", "type1", "flow"],
        "name": "Strobe Pulse",
        "thumbnail_visible": True
    })
    connect(54, "output", 57, "input0")
    connect(56, "output0", 57, "input1")

    add_node(58, {
        "attributes": float_multiply_attr(),
        "bounds": {"height": 82, "width": 130, "x": 1690, "y": -80},
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
        "bounds": {"height": 58, "width": 195, "x": 1600, "y": 200},
        "class": {"id": "77697265-E8EC-4F1B-901A-CFFC104D3B07", "version": 1},
        "clock": "video",
        "color": "ffff6a00",
        "constants": {
            "bypass": {"type": "bool", "value": False},
            "color": {"type": "color", "value": [1.0, 1.0, 1.0, 1.0]}
        },
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
        "bounds": {"height": 154, "width": 195, "x": 1800, "y": 0},
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
