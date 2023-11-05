import pygame
import time
import math

pygame.init()

class GameObject():
    def __init__(self, cords, object = []):
        """object initialization.
        Args:
            self (Generator): an instance of the class.
            cords (tuple): initialization coordinates.
            object (list): object sprites.
        Returns:
            None.
        """
        self.sprites = object
        self.size = object[0].get_size()
        self.rect = pygame.Rect((cords[0] + self.size[0] / 2, cords[1] + self.size[1] / 2),
                                (self.size[0] // 2, self.size[1] // 2))
        self.initial_cords = cords
        self.cords = cords
        self.radius = self.size[0]//4
    def upd(self, cords_):
        """object update.
        Args:
            self (Generator): an instance of the class.
            cords_ (tuple): initialization coordinates.
        Returns:
            None.
        """
        self.cords = cords_
        self.rect.center = (cords_[0] + self.size[0] / 2, cords_[1] + self.size[1] / 2)



class Pet(GameObject):
    def __init__(self, cords, object = []):
        """Pet initialization.
        Args:
            self (Pet): an instance of the class.
            cords (tuple): initialization coordinates.
            object (list): object sprites.
        Returns:
            None.
        """
        super().__init__(cords, object)
        self.speed_y = 0
        self.speed_x = 0
        self.angle_speed = 0
        self.angle = 0
        self.pl_y = 0
        self.pl_x = 0
        self.floor_level = 0
        self.spase_down = 0
        self.jump_start = 0
        self.is_space_down = False
        self.jump_count = 0
        self.on_grownd = True

        """ properties """
        self.speed_max = -700
        self.max_jumps = 2
        self.is_dead = False

        self.initial_sprites = object.copy()

    def rotate(self, angle):
        """Pet rotate.
        Args:
            self (Pet): an instance of the class.
            angle (float): rotate angle.
        Returns:
            None.
        """
        for i in range(len(self.initial_sprites)):
            self.sprites[i] = pygame.transform.rotate(self.initial_sprites[i], angle)

    def get_jump_speed(self):
        """Pet current speed.
        Args:
            self (Pet): an instance of the class.
        Returns:
            float: current speed.
        """
        if self.jump_count == 1:
            return 500
        return 400

    def get_jump_time(self):
        """Get time in jump.
        Args:
            self (Pet): an instance of the class.
        Returns:
            float: jump time.
        """
        if self.jump_count == 1:
            return .6
        return .4

    def death(self, dt):
        """Get time in jump.
        Args:
            self (Pet): an instance of the class.
            dt (float): time difference between cycles.
        Returns:
            None.
        """
        a1 = 1500
        a2 = 1500
        if (self.speed_y > 0):
            self.speed_y -= a1 * dt
        elif (self.speed_y > self.speed_max):
            self.speed_y -= a2 * dt
        else:
            self.speed_y = self.speed_max
        self.angle += self.angle_speed * dt
        self.rotate(self.angle)
        self.pl_y -= self.speed_y * dt
        self.pl_x -= self.speed_x * dt
        a = self.size[0]
        correction = (math.sin((45 + (self.angle % 90)) * math.pi / 180) * math.sqrt(2) - 1) * a / 2
        self.cords = (self.initial_cords[0] + self.pl_x - correction, self.initial_cords[1] + self.pl_y - correction)

    def die(self):
        """Maintains the correct state if death occurs.
        Args:
            self (Pet): an instance of the class.
        Returns:
            None.
        """
        self.is_dead = True
        self.speed_y = 700
        self.speed_x = 100
        self.angle_speed = 500

    def jump(self, dt, key):
        """Maintains the correct state if death occurs.
        Args:
            self (Pet): an instance of the class.
            key (pygame.key.ScancodeWrapper): button state.
            dt (float): time difference between cycles.
        Returns:
            None.
        """
        if self.is_dead:
            self.death(dt)
            return

        a1 = 1500
        a2 = 1500

        self.on_grownd = self.pl_y >= self.floor_level
        if self.on_grownd:
            self.jump_count = 0

        space_down = key[pygame.K_SPACE] and not self.is_space_down

        if key[pygame.K_SPACE]:
            self.is_space_down = True
        else:
            self.is_space_down = False

        """ время нажатия пробела """
        if space_down and self.jump_count <= self.max_jumps:
            self.spase_down = time.time()
            self.jump_count += 1

        """ прыжок с учетом зажатого незадолго до падения пробела """
        if (self.is_space_down and self.on_grownd and (time.time() - self.spase_down) < 0.15):
            self.jump_start = time.time()

        """ двойные и т.д. прыжки"""
        if (space_down and self.jump_count <= self.max_jumps):
            self.jump_start = time.time()

        """ применение гравитации """
        if (not self.on_grownd):
            if (self.speed_y > 0):
                self.speed_y -= a1 * dt
            elif (self.speed_y > self.speed_max):
                self.speed_y -= a2 * dt
            else:
                self.speed_y = self.speed_max

        """ прыжок """
        if (self.is_space_down and self.jump_count <= self.max_jumps and (time.time() - self.jump_start) <= self.get_jump_time()):
            self.speed_y = self.get_jump_speed()

        """ обнуление при приземлении """
        if (self.pl_y > self.floor_level or (self.pl_y == 0 and self.speed_y < 0)):
            self.pl_y = self.floor_level
            self.speed_y = 0

        #self.rotate(self.speed_y / 50)
        self.pl_y -= self.speed_y * dt
        self.cords = (self.initial_cords[0], self.initial_cords[1] + self.pl_y)
        self.upd(self.cords)

class Shade(GameObject):
    def __int__(self, cords, object = []):
        """Pet initialization.
        Args:
            self (Shade): an instance of the class.
            cords (tuple): initialization coordinates.
            object (list): object sprites.
        Returns:
            None.
        """
        super().__init__(cords, object)

class Butterfly(GameObject):

    def __int__(self, cords, object = []):
        """Pet initialization.
        Args:
            self (Butterfly): an instance of the class.
            cords (tuple): initialization coordinates.
            object (list): object sprites.
        Returns:
            None.
        """
        super().__init__(cords, object)

class SmthOnTheFloor(GameObject):
    def __int__(self, cords, object = []):
        """Pet initialization.
        Args:
            self (SmthOnTheFloor): an instance of the class.
            cords (tuple): initialization coordinates.
            object (list): object sprites.
        Returns:
            None.
        """
        super().__init__(cords, object)

class SmthInTheAir(GameObject):
    def __int__(self, cords, object = []):
        """Pet initialization.
        Args:
            self (SmthInTheAir): an instance of the class.
            cords (tuple): initialization coordinates.
            object (list): object sprites.
        Returns:
            None.
        """
        super().__init__(cords, object)