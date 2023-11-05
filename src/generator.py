import random
from src.objects import GameObject, Pet, Shade, Butterfly, SmthOnTheFloor, SmthInTheAir
from collections import deque
import pygame
import src.consts as cst

class Chunk:
    def __init__(self, objects, pos):
        """Initializes chunk variables.
        Args:
            self (Chunk): an instance of the class.
            objects (list): chunk objects.
            pos (int): chunk position.
        Returns:
            None.
        """
        self.objects = objects
        self.pos = pos
    def is_visible(self):
        """Checks if a chunk is available on the screen.
        Args:
            self (Chunk): an instance of the class.
        Returns:
            bool: True if chunk still on the screen.
        """
        return self.pos < 0
    def draw(self, screen):
        """Displaying objects on the screen.
        Args:
            self (Chunk): an instance of the class.
            screen (pygame.surface.Surface): output screen.
        Returns:
            None.
        """
        for obj in self.objects:
            cords = (obj.cords[0], obj.cords[1])
            screen.blit(obj.sprites[0], cords)
            #pygame.draw.circle(screen, 'Blue', obj.r)
    def update(self, n):
        """Updates the coordinates of a chunk.
        Args:
            self (Chunk): an instance of the class.
            n (int): new coordinates.
        Returns:
            None.
        """
        self.pos -= n
        for obj in self.objects:
            obj.upd((obj.cords[0] - n, obj.cords[1]))
    def is_colliding(self, shiba):
        """Collision check.
        Args:
            self (Chunk): an instance of the class.
            shiba (src.objects.Pet): collision object.
        Returns:
            bool: True if a collision occurs.
        """
        for obj in self.objects:
            if pygame.sprite.collide_circle(shiba, obj):
                return True
        return False

class Generator:
    def __init__(self):
        """Initializes the chunk queue.
        Args:
            self (Generator): an instance of the class.
        Returns:
            None.
        """
        self.chunks = deque()

    def update(self, n, screen):
        """Initializes the chunk queue.
        Args:
            n (int): number of chunks.
            screen (pygame.surface.Surface): output screen.
            self (Generator): an instance of the class.
        Returns:
            None.
        """
        if len(self.chunks) == 0:
            return
        if self.chunks[0].is_visible():
            self.chunks.popleft()
        for chunk in self.chunks:
            chunk.update(n)
            chunk.draw(screen)

    def is_colliding(self, shiba):
        """Collision check.
        Args:
            self (Generator): an instance of the class.
            shiba (src.objects.Pet): collision object.
        Returns:
            bool: True if a collision occurs.
        """
        if len(self.chunks) == 0:
            return False
        for chunk in self.chunks:
            if chunk.is_colliding(shiba):
                return True
        return False

    def create_chunk(self, name):
        """Chunk creation.
        Args:
            name (str): chunk name.
            self (Generator): an instance of the class.
        Returns:
            None.
        """
        if name == 'mnogo_muhamorov':
            if len(self.chunks) > 0:
                initial = max([chunk.pos + cst.chunk_gap for chunk in self.chunks])
            else:
                initial = cst.chunk_initial_cord
            pos_x = initial
            m = random.randint(cst.mash_groups_min, cst.mash_groups_max)
            objects = []
            for j in range(m):
                n = random.randint(cst.mash_in_group_min, cst.mash_in_group_max)
                for i in range(n):
                    pos_x += cst.mash_diff
                    mash = SmthOnTheFloor((pos_x, 605), [pygame.image.load('src/images/sprites/muhamor.png')])
                    objects.append(mash)
                pos_x += cst.mash_gap
            chunk = Chunk(objects, pos_x)
            self.chunks.append(chunk)
        if name == "zhal_tvoyu_mat":
            if len(self.chunks) > 0:
                initial = max([chunk.pos + cst.chunk_gap for chunk in self.chunks])
            else:
                initial = cst.chunk_initial_cord
            pos_y = 580
            objects = []
            crd_x = [random.randint(-cst.have_dif_x, cst.have_dif_x) for i in range(4)]
            crd = [random.randint(210, 250), random.randint(80, 100), random.randint(80, 250)]
            random.shuffle(crd)
            crd = [random.randint(30, 50)] + crd
            for i in range(4):
                pos_y -= crd[i]
                hive = SmthInTheAir((initial + crd_x[i], pos_y), [pygame.image.load('src/images/sprites/hive.png')])
                objects.append(hive)
            chunk = Chunk(objects, initial + cst.have_gap)
            self.chunks.append(chunk)


