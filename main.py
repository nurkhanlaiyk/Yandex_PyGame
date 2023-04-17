import pygame
import pygame_menu
import random
import time
import os #надо написать, что юзер должен нажимать на keyboard space
import csv
from pygame import mixer
from helper_classes import Raketa


pygame.init()
pygame.font.init()
width, height = 1200, 600
tank_width, tank_height = 300, 200
raketa_width, raketa_height = 100, 50
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Voina tankov")



if not os.path.isfile('Posescheniye.csv'):
    with open('Posescheniye.csv', 'w', newline='') as file:
        # set_player_name(player_name)
        head_list = ["Player's name", "Level of the player", "Lost", "Win"]
        writer = csv.writer(file)
        writer.writerow(head_list)

# main_tank
main_tank = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tank1.png")), (tank_width, tank_height))

# vrag
vrag_tank_1 = pygame.transform.scale(pygame.image.load("assets/tank1.png"), (tank_width, tank_height))
vrag_tank_2 = pygame.transform.scale(pygame.image.load("assets/tank1.png"), (tank_width, tank_height))
vrag_tank_3 = pygame.transform.scale(pygame.image.load("assets/tank1.png"), (tank_width, tank_height))

# tank_raketa
main_raketa = pygame.transform.scale(pygame.image.load("assets/raketa.png"),
                                      (raketa_width, raketa_height))
vrag_raketa_1 = pygame.transform.scale(pygame.image.load("assets/raketa2.png"),
                                         (raketa_width, raketa_height))
vrag_raketa_2 = pygame.transform.scale(pygame.image.load("assets/raketa3.png"),
                                         (raketa_width, raketa_height))

# background_image
bg = pygame.transform.scale(pygame.image.load("assets/background.jpg"), (width, height))

# raketa_sound
raketa_sound = pygame.mixer.Sound("sound\mraketa.wav")

# tank moving sound
tank_moving_sound = pygame.mixer.Sound("sound\Tank.wav")


class Tank:
    cooling_down = 200

    def __init__(self, x_coord, y_coord, health=100):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.health = health
        self.tank_img = None
        self.raketa_img = None
        self.raketas = []
        self.cool_down_counter = 0

    def draw(self, window):
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50) )
        window.blit(self.tank_img, (self.x_coord, self.y_coord))
        for raketa in self.raketas:
            raketa.draw(window)

    def move_raketa(self, vel, obj):
        self.cooldown()
        for raketa in self.raketas:

            raketa.move(vel)
            if raketa.off_screen(width):
                self.raketas.remove(raketa)
            elif raketa.collision(obj):
                if value_mode == 1:
                    obj.health -= 10
                elif value_mode == 2:
                    obj.health -= 20
                elif value_mode == 3:
                    obj.health -= 100

                self.raketas.remove(raketa)

    def cooldown(self):
        if self.cool_down_counter >= self.cooling_down: self.cool_down_counter = 0
        elif self.cool_down_counter > 0: self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            raketa = Raketa(self.x_coord + self.get_width(), self.y_coord + 50, self.raketa_img)
            self.raketas.append(raketa)
            self.cool_down_counter = 1

    def get_width(self):
        return self.tank_img.get_width()

    def get_height(self):
        return self.tank_img.get_height()


class Player(Tank):
    score = 0

    def __init__(self, x_coord, y_coord, health=100):
        super().__init__(x_coord, y_coord, health)
        self.tank_img = main_tank
        self.raketa_img = main_raketa
        self.mask = pygame.mask.from_surface(self.tank_img)
        self.max_health = health

    def draw(self, window):
        super().draw(window)

    def move_raketa(self, vel, objs):
        self.cooldown()
        for raketa in self.raketas:
            raketa.move(vel)
            if raketa.off_screen(width):
                self.raketas.remove(raketa)
            else:
                for obj in objs:
                    if raketa.collision(obj):
                        self.score += 1
                        objs.remove(obj)
                        if raketa in self.raketas:
                            self.raketas.remove(raketa)

    def raketa_collision(self, mobjs):
        for raketa in self.raketas:
            for obj in mobjs:
                if raketa.collision(obj):
                    mobjs.remove(obj)
                    if raketa in self.raketas:
                        self.raketas.remove(raketa)

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        color_for_window = (255, 0, 0)
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x_coord, self.y_coord + self.tank_img.get_height() + 10, self.tank_img.get_width(), 10))
        color_for_window_2 = (0, 255, 0)
        pygame.draw.rect(window, (0, 255, 0), (
            self.x_coord, self.y_coord + self.tank_img.get_height() + 10,
            self.tank_img.get_width() * (self.health / self.max_health),
            10))


class Vrag(Tank):
    COLOR_MAP = {
        "grey": (vrag_tank_1, vrag_raketa_1),
        "camo": (vrag_tank_2, vrag_raketa_2),
        "yellow": (vrag_tank_3, vrag_raketa_1),
    }

    def __init__(self, x_coord, y_coord, color, health=100):
        super().__init__(x_coord, y_coord, health)
        self.tank_img, self.raketa_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.tank_img)

    def move(self, vel):
        self.x_coord -= vel

    def shoot(self):
        if self.cool_down_counter == 0:
            raketa = Raketa(self.x_coord, self.y_coord + 35, self.raketa_img)
            self.raketas.append(raketa)
            self.cool_down_counter = 1




def collide(obj1, obj2):
    return obj1.mask.overlap(obj2.mask, (obj2.x_coord - obj1.x_coord, obj2.y_coord - obj1.y_coord)) != None


default_player_name = False
player_name = 'Guest'
value_mode = 1
#print(value_mode)
def set_default_player_name():
    global player_name
    player_name = "Guest"


def set_player_name(name):
    global player_name
    global default_player_name
    player_name = name
    default_player_name = False

difficulty = 25
value_mode  = 1
def set_game_difficulty(selected, value):
    global difficulty
    global value_mode
    value_mode = value
    if(value == 1):
        difficulty = 25
    elif(value == 2):
        difficulty = 50
    elif(value == 3):
        difficulty = 100
    else:
        difficulty = 25

def main():
    run = True
    frames_per_seconds = 60
    clock = pygame.time.Clock()
    level = 0
    lives = 10
    player_vel = 2
    vrag_vel = 1
    raketa_vel = 2
    vrags = []
    wave_length = 0
    main_font = pygame.font.SysFont("consolas", 50)
    lost_font = pygame.font.SysFont("consolas", 70)
    score_font = pygame.font.SysFont("consolas", 50)
    win_font = pygame.font.SysFont("consolas", 70)
    player_tank = Player(0, 370)
    global lost
    global win
    lost = False
    win = False
    lost_count = 0
    win_count = 0

    def redraw_window():
        WIN.blit(bg, (0, 0))
        level_label = main_font.render(f"Level: {level}", 1, (255, 0, 0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 0, 0))
        score_label = score_font.render(f"Score: {player_tank.score}", 1, (255, 0, 0))
        WIN.blit(level_label, (10, 10))
        WIN.blit(lives_label, (width - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (width / 2 - score_label.get_width() / 2, 10))
        player_tank.draw(WIN)

        for vrag in vrags:
            vrag.draw(WIN)  # using draw method in tank class

        if win:
            win_label = win_font.render(f"You Win!!!", 1, (255, 0, 0))
            WIN.blit(win_label, (width / 2 - win_label.get_width() / 2, height / 2))

        if lost:
            lost_label = lost_font.render(f"You Lost!!!", 1, (255, 0, 0))
            WIN.blit(lost_label, (width / 2 - lost_label.get_width() / 2, height / 2))

        pygame.display.update()

    while run:
        clock.tick(frames_per_seconds)
        redraw_window()

        if level == 4:
            win = True
            win_count += 1
            print('Check', win_count)

        if win == True:
            run = False
            with open('Posescheniye.csv', 'a', newline='') as file:
                set_player_name(player_name)
                new_row = [player_name, level, lost, win]
                writer = csv.writer(file)

                writer.writerow(new_row)
            game_end_show(win_count)

        if lives <= 0 or player_tank.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > frames_per_seconds * 3:
                run = False
                with open('Posescheniye.csv', 'a', newline='') as file:
                    set_player_name(player_name)
                    new_row = [player_name, level, lost, win]
                    writer = csv.writer(file)

                    writer.writerow(new_row)
                game_end_show(win_count)
            else:
                continue

        if len(vrags) == 0:
            level += 1
            wave_length += 2
            for i in range(wave_length):
                if value_mode == 1:
                    vrag = Vrag(2500, 370, "grey")
                    vrags.append(vrag)
                elif value_mode == 2:
                    vrag = Vrag(2500, 370, "yellow")
                    vrags.append(vrag)
                elif value_mode == 3:
                    vrag = Vrag(2500, 370, "camo")
                    vrags.append(vrag)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player_tank.x_coord + player_vel > 0:
            tank_moving_sound.play()
            player_tank.x_coord -= player_vel

        if keys[pygame.K_d] and player_tank.x_coord + player_vel < width / 2 - player_tank.get_width():  # right
            tank_moving_sound.play()
            player_tank.x_coord += player_vel

        if keys[pygame.K_SPACE]:
            player_tank.shoot()
            raketa_sound.play()

        for vrag in vrags[:]:
            vrag.move(vrag_vel)
            vrag.move_raketa(-raketa_vel, player_tank)
            if random.randrange(0, 4 * frames_per_seconds) == 1:
                vrag.shoot()

            if collide(vrag, player_tank):
                player_tank.health -= 10
                vrags.remove(vrag)

            elif vrag.x_coord + vrag.get_width() < 0:
                lives -= 1
                vrags.remove(vrag)

        player_tank.move_raketa(raketa_vel, vrags)
        player_tank.raketa_collision(vrag.raketas)


def game_start_show():
    game_start = pygame_menu.Menu(width=width, height=height, title='Hello, This is the game called "VOINA TANKOV"',
                                  theme=pygame_menu.themes.THEME_GREEN)
    game_start.add.text_input("Type your name: ", default="Guest", onchange=set_player_name)
    game_start.add.selector("Choose your difficulty: ", [("Novice", 1), ("Standard", 2), ("Expert", 3)],
                            onchange=set_game_difficulty)
    game_start.add.button("Play the Game", main)
    game_start.add.button("Exit the Game", pygame_menu.events.EXIT)
    if default_player_name:
        set_default_player_name()
    game_start.mainloop(WIN)


def game_end_show(game_score):
    end_menu = pygame_menu.Menu(width=width, height=height, title='', theme=pygame_menu.themes.THEME_GREEN)
    if lost:
        end_menu.add.label('Sorry, you lost the game, {} would you like to play again?'.format(player_name))
    else:
        end_menu.add.label('Congratulations {}!'.format(player_name))
    end_menu.add.label("Your Score:" + str(game_score))
    end_menu.add.button("Replay Game", main)
    end_menu.add.button("Exit the Game", pygame_menu.events.EXIT)
    end_menu.mainloop(WIN)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    game_start_show()


main_menu()