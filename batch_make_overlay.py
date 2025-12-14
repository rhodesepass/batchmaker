from PIL import Image,ImageOps,ImageFont,ImageDraw
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
FONT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "font"))
CLASSICON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "classicon"))

CLASSDICT = {
    "VANGUARD":os.path.join(CLASSICON_PATH, "class_先锋.png"),
    "DEFENDER":os.path.join(CLASSICON_PATH, "class_近卫.png"),
    "SNIPER":os.path.join(CLASSICON_PATH, "class_狙击.png"),
    "GUARD":os.path.join(CLASSICON_PATH, "class_重装.png"),
    "MEDIC":os.path.join(CLASSICON_PATH, "class_医疗.png"),
    "SUPPORTER":os.path.join(CLASSICON_PATH, "class_辅助.png"),
    "CASTER":os.path.join(CLASSICON_PATH, "class_术师.png"),
    "SPECIALIST":os.path.join(CLASSICON_PATH, "class_特种.png"),
}

def make_overlay(opname, opcode, opclass):
    bg = Image.open(os.path.join(BASE_DIR, "template.png")) 
    classicon = Image.open(CLASSDICT[opclass])
    classicon = classicon.resize((50, 50))
    classicon = classicon.convert("RGB")
    inv_classicon = ImageOps.invert(classicon)

    operator_name = Image.new("RGBA", (200, 50), (0, 0, 0, 0))
    operator_name_draw = ImageDraw.Draw(operator_name)
    operator_name_draw.text((0, 0), opname, fill=(255, 255, 255,255), 
        font=ImageFont.truetype(os.path.join(FONT_PATH, "BebasNeue-1.otf"), 40))

    operator_code = Image.new("RGBA", (200, 50), (0, 0, 0, 0))
    operator_code_draw = ImageDraw.Draw(operator_code)
    operator_code_draw.text((0, 0), opcode, fill=(255, 255, 255,255), 
        font=ImageFont.truetype(os.path.join(FONT_PATH, "NotoSans-Bold-5.ttf"), 10))

    operator_code_2 = Image.new("RGBA", (200, 30), (0, 0, 0, 0))
    operator_code_2_draw = ImageDraw.Draw(operator_code_2)
    operator_code_2_draw.text((0, 0), opcode, fill=(0, 0, 0,255), 
        font=ImageFont.truetype(os.path.join(FONT_PATH, "NotoSans-Bold-5.ttf"), 10))
    operator_code_2 = operator_code_2.rotate(270,expand=True,fillcolor=(0, 0, 0, 0))

    EAN = barcode.get_barcode_class('code128')
    writ = ImageWriter()
    writ.font_path = os.path.join(FONT_PATH, "NotoSans-Bold-5.ttf")
    my_ean = EAN(opname+"-"+opcode, writer=writ)
    fp = BytesIO()
    my_ean.write(fp)
    barcode_img = Image.open(fp)
    barcode_img = barcode_img.crop((50,15,300,50))
    barcode_img = barcode_img.resize((150, 35))
    barcode_img = barcode_img.rotate(270,expand=True,fillcolor=(0, 0, 0, 0))

    class_text = Image.new("RGBA", (150, 30), (0, 0, 0, 0))
    class_text_draw = ImageDraw.Draw(class_text)
    class_text_draw.text((0, 0), opclass + "/RHODES ISLAND", fill=(255, 255, 255,255), 
        font=ImageFont.truetype(os.path.join(FONT_PATH, "NotoSans-Regular-2.ttf"), 10))

    bg.alpha_composite(operator_name, (70, 415))
    bg.alpha_composite(operator_code, (70, 461))
    bg.alpha_composite(operator_code_2, (21, 530))
    bg.alpha_composite(class_text, (68,602))

    bg.paste(inv_classicon, (70, 520))
    bg.paste(barcode_img, (0,480))

    return bg

if __name__ == "__main__":
    opname = "FIAMETTA"
    opcode = "ARKNIGHTS - LT77"
    opclass = "SNIPER"
    bg = make_overlay(opname, opcode, opclass)
    bg.show()