from PIL import Image,ImageOps,ImageFont,ImageDraw
import barcode
from barcode.writer import ImageWriter
from io import BytesIO



CLASSDICT = {
    "VANGUARD":"classicon/class_先锋.png",
    "DEFENDER":"classicon/class_近卫.png",
    "SNIPER":"classicon/class_狙击.png",
    "TANK":"classicon/class_重装.png",
    "MEDIC":"classicon/class_医疗.png",
    "SUPPORTER":"classicon/class_支援.png",
    "CASTER":"classicon/class_术师.png",
    "SPECIALIST":"classicon/class_特种.png",
}

OPERATOR_CLASS = "SNIPER"
OPERATOR_NAME = "FIAMETTA"
OPERATOR_CODE = "ARKNIGHTS - LT77"
CLASS_TEXT = CLASSDICT[OPERATOR_CLASS] + "/RHODES ISLAND"

bg = Image.open("template.png")
classicon = Image.open(CLASSDICT[OPERATOR_CLASS])
classicon = classicon.resize((50, 50))
classicon = classicon.convert("RGB")
inv_classicon = ImageOps.invert(classicon)

operator_name = Image.new("RGBA", (200, 50), (0, 0, 0, 0))
operator_name_draw = ImageDraw.Draw(operator_name)
operator_name_draw.text((0, 0), OPERATOR_NAME, fill=(255, 255, 255,255), 
    font=ImageFont.truetype("font/BebasNeue-1.otf", 40))

operator_code = Image.new("RGBA", (200, 50), (0, 0, 0, 0))
operator_code_draw = ImageDraw.Draw(operator_code)
operator_code_draw.text((0, 0), OPERATOR_CODE, fill=(255, 255, 255,255), 
    font=ImageFont.truetype("font/NotoSans-Bold-5.ttf", 10))

operator_code_2 = Image.new("RGBA", (200, 30), (0, 0, 0, 0))
operator_code_2_draw = ImageDraw.Draw(operator_code_2)
operator_code_2_draw.text((0, 0), OPERATOR_CODE, fill=(0, 0, 0,255), 
    font=ImageFont.truetype("font/NotoSans-Bold-5.ttf", 10))
operator_code_2 = operator_code_2.rotate(270,expand=True,fillcolor=(0, 0, 0, 0))

EAN = barcode.get_barcode_class('code128')
my_ean = EAN(OPERATOR_NAME, writer=ImageWriter())
fp = BytesIO()
my_ean.write(fp)
barcode_img = Image.open(fp)
barcode_img = barcode_img.crop((50,15,300,50))
barcode_img = barcode_img.resize((150, 35))
barcode_img = barcode_img.rotate(270,expand=True,fillcolor=(0, 0, 0, 0))

class_text = Image.new("RGBA", (150, 30), (0, 0, 0, 0))
class_text_draw = ImageDraw.Draw(class_text)
class_text_draw.text((0, 0), "SNIPER/RHODES ISLAND", fill=(255, 255, 255,255), 
    font=ImageFont.truetype("font/NotoSans-Regular-2.ttf", 10))

bg.alpha_composite(operator_name, (70, 415))
bg.alpha_composite(operator_code, (70, 461))
bg.alpha_composite(operator_code_2, (21, 530))
bg.alpha_composite(class_text, (68,602))

bg.paste(inv_classicon, (70, 520))
bg.paste(barcode_img, (0,480))

bg.show()


