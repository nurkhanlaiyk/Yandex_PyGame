import pygame
import pygame_menu
import random
import time
import os
import csv
from pygame import mixer


def collide(obj1, obj2):
    return obj1.mask.overlap(obj2.mask, (obj2.x_coord - obj1.x_coord, obj2.y_coord - obj1.y_coord)) != None


class Raketa:
    def __init__(self, x_coord, y_coord, image):
        self.img = image
        self.mask = pygame.mask.from_surface(self.img)
        self.x_coord = x_coord
        self.y_coord = y_coord

    def draw(self, window):
        window.blit(self.img, (self.x_coord, self.y_coord))

    def move(self, vel):
        self.x_coord += vel

    def off_screen(self, breadth):
        if self.x_coord >= 0:
            if breadth >= self.x_coord:
                return False
            else:
                return True
        else:
            return True

    def collision(self, obj):
        return collide(self, obj)
