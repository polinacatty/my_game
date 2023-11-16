#While True File
import random
import pygame
import time
import math
from src.objects import Pet, Shade, Butterfly, SmthOnTheFloor
from src.generator import Generator
import src.consts as cst


class Run():
    def __init__(self, screen, pt):
        """The function initializes all variables to start a new round and sets them to the standard state.
        Args:
            self(Run): an instance of the class.
            pt (str): filename with pet sprites.
            screen (pygame.surface.Surface): output screen.
        Returns:
            None.
        """
        self.gen = Generator()
        self.screen = screen
        self.wr = True
        self.myfont = pygame.font.Font('src/fonts/18VAG Rounded M Bold.ttf', 60)
        self.in_game_time_ = 0.0
        self.cnt = 0
        self.bgx = 0
        self.start_time = time.time()
        self.bg = pygame.image.load('src/images/Unknown.jpg').convert()
        self.names = ['zhal_tvoyu_mat', 'mnogo_muhamorov']
        self.lose_screen = pygame.Surface((1320, 800))
        self.lose_screen.fill(cst.background_color)
        self.l_x = 1280
        self.shiba = Pet((400, 560), [pygame.image.load('src/images/sprites/' + pt + '/m_right_0.png').convert_alpha(),
                                      pygame.image.load('src/images/sprites/' + pt + '/m_right_1.png').convert_alpha(),
                                      pygame.image.load('src/images/sprites/' + pt + '/m_right_2.png').convert_alpha(),
                                      pygame.image.load('src/images/sprites/' + pt + '/m_right_3.png').convert_alpha(),
                                      pygame.image.load('src/images/sprites/' + pt + '/run_0.png').convert_alpha(),
                                      pygame.image.load('src/images/sprites/' + pt + '/run_1.png').convert_alpha(),
                                      pygame.image.load('src/images/sprites/' + pt + '/run_2.png').convert_alpha()])

        self.shade = Shade((self.shiba.cords[0], self.shiba.initial_cords[1] - 10),
                           [pygame.image.load('src/images/sprites/shade_rare.png').convert_alpha(),
                            pygame.image.load('src/images/sprites/shade_medium.png').convert_alpha(),
                            pygame.image.load('src/images/sprites/shade_smol.png').convert_alpha()])

        self.butterfly = Butterfly((900, 400), [pygame.image.load('src/images/sprites/bt_ 0.png'),
                                                pygame.image.load('src/images/sprites/bt_1.png')])
        self.time_ = 0
        self.time_deth = 0
    def update_file(self, num):
        """High score table update.
        Args:
            self(Run): an instance of the class.
            num (float): new result.
        Returns:
            None.
        """
        filename = 'src/numbers.txt'
        numbers = []
        with open(filename, 'r') as f:
            for line in f:
                numbers.append(float(line.strip()))
        numbers.sort()
        if len(numbers) < 10 or num > numbers[0]:
            if len(numbers) == 10:
                numbers.pop(0)
            numbers.append(num)
            numbers.sort()
        numbers.reverse()
        with open(filename, 'w') as f:
            for n in numbers:
                f.write(str(n) + '\n')


    def get_speed(self, time_):
        """High score table update.
        Args:
            self(Run): an instance of the class.
            time_ (float): game time.
        Returns:
            int: current speed.
        """
        return 6 + (min(time_, 30) / 30) * 4

    def run(self):
        """starts the round and maintains its correct state.
        Args:
            self(Run): an instance of the class.
        Returns:
            bool: True if the game ended and the screen shifted by 20 pixels.
        """
        dt = time.time() - self.time_
        self.time_ = time.time()
        if not self.shiba.is_dead:
            self.in_game_time_ = self.time_ - self.start_time
        elif self.wr:
            self.update_file(self.in_game_time_)
            self.wr = False
        tx = self.myfont.render('{0:.1f}'.format(self.in_game_time_), True, cst.font_color)
        if len(self.gen.chunks) < 3:
            self.gen.create_chunk(self.names[random.randint(0, 1)])
        key = pygame.key.get_pressed()
        self.screen.blit(self.bg, (self.bgx, 0))
        self.screen.blit(self.bg, (self.bgx + 1279, 0))
        self.screen.blit(tx, (10, 10))
        self.screen.blit(self.butterfly.sprites[(self.cnt // 4) % 2], (
        self.butterfly.cords[0] + 40 * math.cos(self.time_ / 2), self.butterfly.cords[1] + 100 * math.sin(self.time_ / 3) - 50))
        self.shiba.jump(dt, key)
        if (self.shiba.is_dead):
            self.screen.blit(self.shiba.sprites[self.cnt // 4], self.shiba.cords)
        elif self.shiba.pl_y >= self.shiba.floor_level:
            self.screen.blit(self.shade.sprites[0], self.shade.cords)
            self.screen.blit(self.shiba.sprites[self.cnt // 4], self.shiba.cords)
        elif self.shiba.floor_level - self.shiba.pl_y < 50:
            self.screen.blit(self.shade.sprites[0], self.shade.cords)
            self.screen.blit(self.shiba.sprites[4], self.shiba.cords)
        elif self.shiba.floor_level - self.shiba.pl_y < 100:
            self.screen.blit(self.shade.sprites[1], self.shade.cords)
            self.screen.blit(self.shiba.sprites[5], self.shiba.cords)
        else:
            self.screen.blit(self.shade.sprites[2], self.shade.cords)
            self.screen.blit(self.shiba.sprites[6], self.shiba.cords)
        self.gen.update(self.get_speed(self.time_ - self.start_time), self.screen)
        if self.gen.is_colliding(self.shiba) and not self.shiba.is_dead:
            self.shiba.die()
            self.time_deth = time.time()
        self.bgx -= self.get_speed(self.time_ - self.start_time)
        if (self.shiba.is_dead):
            self.screen.blit(self.lose_screen, (self.l_x, 0))
        if (self.bgx < -1280):
            self.bgx = 0
        self.cnt = (self.cnt + 1) % 16
        if (self.shiba.is_dead):
            self.l_x -= 2 * self.get_speed(self.time_ - self.start_time)
        return (self.l_x > -20)

class Icons():
    def __init__(self, screen):
        """The Initializing objects for the character selection menu.
        Args:
            self(Icons): an instance of the class.
            screen (pygame.surface.Surface): output screen.
        Returns:
            None.
        """
        self.screen = screen
        self.p1 = (Pet((0, 0), [pygame.image.load('src/images/sprites/shiba_white/m_frvrd_0.png').convert_alpha(),
                           pygame.image.load('src/images/sprites/shiba_white/m_frvrd_1.png').convert_alpha(),
                           pygame.image.load('src/images/sprites/shiba_white/m_frvrd_2.png').convert_alpha()]))
        self.r1 = self.p1.sprites[0].get_rect(topleft = cst.pet1_cords)
        self.p2 = (Pet((0, 0), [pygame.image.load('src/images/sprites/shiba_classic/m_frdrv_0.png').convert_alpha(),
                           pygame.image.load('src/images/sprites/shiba_classic/m_frdrv_1.png').convert_alpha(),
                           pygame.image.load('src/images/sprites/shiba_classic/m_frdrv_2.png').convert_alpha()]))
        self.r2 = self.p1.sprites[0].get_rect(topleft=cst.pet2_cords)
        self.p4 = (Pet((0, 0), [pygame.image.load('src/images/sprites/cat_black/m_frdrv_0.png').convert_alpha(),
                           pygame.image.load('src/images/sprites/cat_black/m_frdrv_1.png').convert_alpha(),
                           pygame.image.load('src/images/sprites/cat_black/m_frdrv_2.png').convert_alpha()]))
        self.r4 = self.p1.sprites[0].get_rect(topleft=cst.pet4_cords)
        self.p5 = (Pet((0, 0), [pygame.image.load('src/images/sprites/cat_red/m_frvrd_0.png').convert_alpha(),
                           pygame.image.load('src/images/sprites/cat_red/m_frvrd_1.png').convert_alpha(),
                           pygame.image.load('src/images/sprites/cat_red/m_frvrd_2.png').convert_alpha()]))
        self.r5 = self.p1.sprites[0].get_rect(topleft=cst.pet5_cords)
        self.p6 = (Pet((0, 0), [pygame.image.load('src/images/sprites/cat_gray/m_frvrd_0.png').convert_alpha(),
                           pygame.image.load('src/images/sprites/cat_gray/m_frvrd_1.png').convert_alpha(),
                           pygame.image.load('src/images/sprites/cat_gray/m_frvrd_2.png').convert_alpha()]))
        self.r6 = self.p1.sprites[0].get_rect(topleft=cst.pet6_cords)

        self.shade = Shade((0, 0), [pygame.image.load('src/images/sprites/shade_rare.png').convert_alpha()])

    def draw(self, cnt):
        """The Initializing objects for the character selection menu.
        Args:
            self(Icons): an instance of the class.
            cnt (int): character number.
        Returns:
            None.
        """
        self.screen.blit(self.shade.sprites[0], cst.shade_cords1)
        self.screen.blit(self.shade.sprites[0], cst.shade_cords2)
        self.screen.blit(self.shade.sprites[0], cst.shade_cords3)
        self.screen.blit(self.shade.sprites[0], cst.shade_cords4)
        self.screen.blit(self.shade.sprites[0], cst.shade_cords5)
        self.screen.blit(self.p1.sprites[cnt], cst.pet1_cords)
        self.screen.blit(self.p2.sprites[cnt], cst.pet2_cords)
        self.screen.blit(self.p4.sprites[cnt], cst.pet4_cords)
        self.screen.blit(self.p5.sprites[cnt], cst.pet5_cords)
        self.screen.blit(self.p6.sprites[cnt], cst.pet6_cords)


