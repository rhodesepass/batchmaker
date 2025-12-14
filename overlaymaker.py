from InquirerPy import prompt
import json
from batch_make_overlay import make_overlay
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

CLASSID_DICT = {
    512:"VANGUARD",
    1:"GUARD",
    4:"DEFENDER",
    32:"CASTER",
    2:"SNIPER",
    8:"MEDIC",
    16:"SUPPORTER",
    64:"SPECIALIST",
    128:"UNKNOWN",
    256:"UNKNOWN",
}

operator_data = {}
choices = []
with open(os.path.join(BASE_DIR, "character_table.json"),"r",encoding="utf-8") as f:
    chardata = json.loads(f.read())


for k,char in chardata["Characters"].items():
    opname = char["Appellation"]
    opnamezh = char["Name"]
    opcode = char["DisplayNumber"]
    opnation = char["NationId"]
    opclass = CLASSID_DICT[char["Profession"]]
    operator_data[k] = {
        "name":opname,
        "namezh":opnamezh,
        "opcode":opcode,
        "opnation":opnation,
        "opclass":opclass,
    }
    choices.append(k + ":" + opnamezh)

while True:
    questions = [
        {
            "type":"fuzzy",
            "name":"operator",
            "message":"请选择要制作的干员",
            "choices":choices,
        }
    ]
    answers = prompt(questions)
    operator_id = answers["operator"].split(":")[0]
    opdata = operator_data[operator_id]
    overlayimg = make_overlay(opdata["name"], "ARKNIGHTS - " + opdata["opcode"], opdata["opclass"])
    overlayimg.save(f"{opdata['name']}.png")
    overlayimg.show()
    print("制作完成: " + opdata["name"] + " " + opdata["namezh"] + " " + opdata["opcode"] + " " + opdata["opclass"])