import pygame as pg
from math import *
from random import randint


pg.init()
clock = pg.time.Clock()
WINDOW_SETTINGS = (1000, 700)
HORIZONT = 300
window = pg.display.set_mode(WINDOW_SETTINGS)
pg.display.set_caption("Дикий тир")
run = True
backg = pg.image.load("Саванна.jpg")
backg = pg.transform.scale(backg, WINDOW_SETTINGS)

BULLET_WIDTH = 25
BULLET_HEIGHT = 40

GUN_WIDTH = 130
GUN_HEIGHT = 50

SPEED = 1
BULLET_SPEED = 100

class Object:
    def __init__(self, x, y, img, w, h, speed):
        self.image = pg.image.load(img)
        self.image = pg.transform.scale(self.image, (w, h))
        # Rect создается с картинки, считая переданные x,y координатами центра
        self.rect = self.image.get_rect(center=[x, y])
        self.speed = speed

    def draw(self, canvas):
        canvas.blit(self.image, self.rect)


class ObjectRotatable(Object):
    def __init__(self, x, y, img, w, h, speed):
        super().__init__(x, y, img, w, h, speed)
        self.img_rotated = self.image
        # Rect создается с картинки, считая переданные x,y координатами центра
        self.rect = self.img_rotated.get_rect(center=[x, y])
        self.angle_radians = 0
        self.angle_degrees = 0
        self.speed = speed

    def getAngleDegrees(angle_radians):
        return angle_radians * 180 / pi

    def getAngleRadians(object1X, object1Y, object2X, object2Y):
        katetX = object2X - object1X;
        katetY = object2Y - object1Y;

        angle_radians = atan2(katetY, katetX);

        return angle_radians

    def getDirection(angle_radians, vector_len):
        return cos(angle_radians) * vector_len, sin(angle_radians) * vector_len

    def draw(self, canvas):
        canvas.blit(self.img_rotated, self.rect)


class Gun(ObjectRotatable):
    def __init__(self, x, y, img, w, h):
        super().__init__(x, y, img, w, h, SPEED)
        self.x = x
        self.y = y

    def update(self, mouseX, mouseY):
        angle_radians = ObjectRotatable.getAngleRadians(self.x, self.y, mouseX, mouseY)
        if -pi < angle_radians < 0:
            self.angle_radians = angle_radians
        self.angle_degrees = ObjectRotatable.getAngleDegrees(self.angle_radians)
        #
        self.img_rotated = pg.transform.rotate(self.image, 180 - self.angle_degrees)
        # Rect создается с картинки, считая переданные x,y координатами центра
        self.rect = self.img_rotated.get_rect(center=[self.x, self.y])


class Bullet(ObjectRotatable):
    def __init__(self, x, y, img, w, h, angle_radians):
        super().__init__(x, y, img, w, h, BULLET_SPEED)

        self.angle_radians = angle_radians
        self.angle_degrees = ObjectRotatable.getAngleDegrees(self.angle_radians)

        self.vX, self.vY = ObjectRotatable.getDirection(self.angle_radians, self.speed)

        self.img_rotated = pg.transform.rotate(self.image, -90 - self.angle_degrees)
        # Rect создается с картинки, считая переданные x, y координатами центра
        self.rect = self.img_rotated.get_rect(center=[x, y])

    def update(self):
        self.rect.x += self.vX
        self.rect.y += self.vY


class Animal:
    def __init__(self, x, y, image, w, h, speed, points):
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (w, h))
        self.speed = speed
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.points = points

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right >= WINDOW_SETTINGS[0]:
            self.rect.x = self.x
            self.rect.y = randint(HORIZONT, WINDOW_SETTINGS[1])
        if self.rect.left <= 0:
            self.rect.x = self.x
            self.rect.y = randint(HORIZONT, WINDOW_SETTINGS[1])


gun = Gun(WINDOW_SETTINGS[0] / 2, WINDOW_SETTINGS[1] - GUN_HEIGHT, 'Пулемёт.png', GUN_WIDTH, GUN_HEIGHT)
bullets = []

SPEED_ELEPHANT, POINTS_ELEPHANT = 1, 2
SPEED_LION, POINTS_LION = 4, 10
SPEED_TIGER, POINTS_TIGER = 5, 15
SPEED_JERBOA, POINTS_JERBOA = 2, 20  # ТУШКАНЧИК
SPEED_OSTRICH, POINTS_OSTRICH = 3, 7 # СТРАУС
SPEED_HYENA, POINTS_HYENA = 3, 8
SPEED_HAWK, POINTS_HAWK = 1, 2 # ЯСТРЕБ
SPEED_ZEBRA, POINTS_ZEBRA = 2, 3
SPEED_IRONCLAD, POINTS_IRONCLAD = 2, 1 # БРОНЕНОСЕЦ !!!!!!!!!!!!
SPEED_ECHIDNA, POINTS_ECHIDNA = 3, 16 # МЕЛКИЙ АФРИКАНСКИЙ ЕЖ !!!!!!!
SPEED_CHAMELEON, POINTS_CHAMELEON = 1, 20

animals = [Animal(700, randint(HORIZONT, WINDOW_SETTINGS[1]), "Слон.png", 300, 300, SPEED_ELEPHANT, POINTS_ELEPHANT),
           Animal(700, randint(HORIZONT, WINDOW_SETTINGS[1]), "Слон.png", 300, 150, SPEED_LION, POINTS_LION),
           Animal(700, randint(HORIZONT, WINDOW_SETTINGS[1]), "Слон.png", 300, 150, SPEED_TIGER, POINTS_TIGER),
           Animal(700, randint(HORIZONT, WINDOW_SETTINGS[1]), "Слон.png", 50, 50, SPEED_JERBOA, POINTS_JERBOA),
           Animal(700, randint(HORIZONT, WINDOW_SETTINGS[1]), "Слон.png", 100, 300, SPEED_OSTRICH, POINTS_OSTRICH),
           Animal(700, randint(HORIZONT, WINDOW_SETTINGS[1]), "Слон.png", 250, 100, SPEED_HYENA, POINTS_HYENA),
           Animal(700, randint(0, HORIZONT), "Слон.png", 80, 100, SPEED_HAWK, POINTS_HAWK),
           Animal(700, randint(HORIZONT, WINDOW_SETTINGS[1]), "Слон.png", 290, 140, SPEED_ZEBRA, POINTS_ZEBRA),
           Animal(700, randint(HORIZONT, WINDOW_SETTINGS[1]), "Слон.png", 80, 80, SPEED_IRONCLAD, POINTS_IRONCLAD),
           Animal(700, randint(HORIZONT, WINDOW_SETTINGS[1]), "Слон.png", 90, 90, SPEED_ECHIDNA, POINTS_ECHIDNA),
           Animal(700, randint(HORIZONT, WINDOW_SETTINGS[1]), "Слон.png", 30, 30, SPEED_CHAMELEON, POINTS_CHAMELEON)]

spisok_animals_on_the_screen = []
for i in range(10):
    spisok_animals_on_the_screen.append(animals[randint(0, len(animals) - 1)])

while run:
    clock.tick(60)
    mouseX = pg.mouse.get_pos()[0]
    mouseY = pg.mouse.get_pos()[1]
    for event in pg.event.get():
        if event.type == pg.QUIT: # QUIT- нажатие на крестик
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullets.append(Bullet(gun.x, gun.y, 'Пуля.png', BULLET_WIDTH, BULLET_HEIGHT, gun.angle_radians))
    keys = pg.key.get_pressed()
    gun.update(mouseX, mouseY)
    for bullet in bullets:
        bullet.update()
    for animal in spisok_animals_on_the_screen: # обновление данных
        animal.update()
    window.blit(backg, (0, 0)) # прорисовка заднего фона
    for animal in spisok_animals_on_the_screen:  # прорисовка
        window.blit(animal.image, animal.rect)
    gun.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    pg.display.update()

pg.quit()