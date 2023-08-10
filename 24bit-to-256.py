#!/usr/bin/env python3

import json
import sys


def load_colors():
    with open('256-colors.json') as f:
        return json.load(f)

def parse_hex(hex):
    return {"r":int(hex[0:2], 16), "g":int(hex[2:4], 16), "b":int(hex[4:6], 16)}

def squared_distance(color1, color2):
    r = (color1["r"] - color2["r"]) ** 2
    g = (color1["g"] - color2["g"]) ** 2
    b = (color1["b"] - color2["b"]) ** 2
    return r + g + b

def auto_color(rgb):
    brightness = 0.2126 * rgb['r'] + 0.7152 * rgb['g'] + 0.0722 * rgb['b']
    if brightness > 144:
        return '\033[38;5;232m'
    return '\033[38;5;231m'

def print_color(name, rgb):
    color = auto_color(rgb)
    background = f"{rgb['r']};{rgb['g']};{rgb['b']}"
    print(f"{name:>6} \033[48;2;{background}m{color} {background:11} \033[0m")

if __name__ == "__main__":
    colors = load_colors()
    target = parse_hex(sys.argv[1])

    n = 5
    top_n: list = [None] * n
    for c in colors:
        distance = squared_distance(target, c["rgb"])
        for i in range(n):
            if top_n[i] is None or distance < top_n[i]["distance"]:
                top_n[i] = {"distance":distance, "id":c["colorId"], "rgb":c["rgb"]}
                break

    print_color(sys.argv[1], target)
    for color in top_n:
        if color is not None:
            print_color(color["id"], color["rgb"])
