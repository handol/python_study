# creates a 50x50 pixel black box with hello world written in white, 8 point Arial text
import Image, ImageDraw, ImageFont

i = Image.new("RGB", (50,50))
d = ImageDraw.Draw(i)
#f = ImageFont.truetype("", 8)
#d.text((0,0), "hello world", font=f)
d.text((0,0), "hello world")
i.save(open("helloworld.png", "wb"), "PNG")

