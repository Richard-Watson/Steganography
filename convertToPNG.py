from PIL import Image, ImageDraw

image = Image.open("google.jpg") #Открываем изображение.
image.save("google.png", "PNG")