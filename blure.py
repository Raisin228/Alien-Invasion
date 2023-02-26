# Импортируем Pillow для работы с изображениями
from PIL import Image, ImageFilter

def blure_bg():
    """Функция которая принимает изображение и размывает его"""
    im = Image.open("images/stop_blure_bg/screenshot.jpg")

    # размываем по гауссу
    im1 = im.filter(ImageFilter.GaussianBlur(3))

    # сохраняем размытое изображение
    im1.save('images/stop_blure_bg/bg.jpg')