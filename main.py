import pygame as pg


pg.init()
clock = pg.time.Clock()
WINDOW_SETTINGS = (1000, 700)
window = pg.display.set_mode(WINDOW_SETTINGS)
pg.display.set_caption("Дикий тир")
run = True
backg = pg.image.load("Саванна.jpg")
backg = pg.transform.scale(backg, WINDOW_SETTINGS)


class Animal:
    def __init__(self, x, y, image, w, h, speed):
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (w, h))
        self.speed = speed
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right >= WINDOW_SETTINGS[0]:
            self.rect.x = self.x
            self.rect.y = self.y
        if self.rect.left <= 0:
            self.rect.x = self.x
            self.rect.y = self.y


el1 = Animal(700, 400, "Слон.png", 300, 300, 1)

while run:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT: # QUIT- нажатие на крестик
            run = False
    el1.update()
    window.blit(backg, (0, 0))
    window.blit(el1.image, el1.rect)
    pg.display.update()

pg.quit()