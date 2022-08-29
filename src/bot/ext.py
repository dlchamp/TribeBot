"""
MIT License

Copyright (c) 2022 DLCHAMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
from typing import Optional


def load_config():
    with open("./bot/data/config.json") as f:
        return json.load(f)


def dump_config(data):
    with open("./bot/data/config.json", "w") as f:
        json.dump(data, f)


def get_welcome_message_id() -> bool:
    data = load_config()
    return data["welcome_message_id"]


def update_message_sent(message_id: Optional[int] = None) -> None:
    data = load_config()
    data["welcome_message_id"] = message_id
    dump_config(data)


def get_welcome_embed():
    with open("./bot/data/welcome_embed.json") as f:
        return json.load(f)


def get_quizzed_members():
    data = load_config()
    return data["quizzed"]


def add_quizzed_member(member_id: int) -> None:
    data = load_config()
    data["quizzed"].append(member_id)
    dump_config(data)
