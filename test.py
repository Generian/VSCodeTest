"""This is supposed to be a game"""

import sys
import pygame

pygame.init()

FPS = 120

WIDTH = 800
HEIGHT = 600

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define block specific variables
BLOCK_HEIGHT = 25
BLOCK_WIDTH = 200

# Define game specifics
SPEED_NORMAL = (2, 0)
SPEED_FALLING = (2, 2)
MARGIN = 3


def add_block(gameover, block_list, block_number, width, speed, pos_x):
    """Adds a block to the list"""
    if len(block_list) > 1:
        pos_y = block_list[len(block_list)-1].pos_y - BLOCK_HEIGHT
    else:
        pos_y = HEIGHT - (block_number * BLOCK_HEIGHT)
    if not gameover:
        block_list.append(Rectangle(pos_x,
                                    pos_y,
                                    width, BLOCK_HEIGHT, speed))


def add_falling_block(list_parts, pos_x, pos_y, width, speed):
    """Adds a block to the list"""
    list_parts.append(Rectangle(pos_x, pos_y, width, BLOCK_HEIGHT, speed))

def move_down(block_list):
    """Moves everything down"""
    blocknumber_medium = 0.5 * HEIGHT/BLOCK_HEIGHT
    if len(block_list) > blocknumber_medium:
        print "Move down"
        for block in block_list:
            block.pos_y += BLOCK_HEIGHT


class Rectangle(object):
    """This class defines a moving rectangle"""
    def __init__(self, pos_x, pos_y, width, height, speed):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.height = height
        self.width = width
        self.right = self.pos_x + self.width
        self.speed_x = speed[0]
        self.speed_y = speed[1]

    def speed(self, speed):
        """Defines the speed of the rectangles"""
        self.speed_x = speed[0]
        self.speed_y = speed[1]

    #def accelerate(self, acceleration):

    def draw(self, display):
        """Draws the rectangle on the screen"""
        pygame.draw.rect(display, BLACK,
                         [self.pos_x, self.pos_y, self.width, self.height])

    def move(self):
        """Moves the rectangle"""
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.right = self.pos_x + self.width
        if self.pos_x >= WIDTH - self.width or self.pos_x <= 0:
            self.speed_x = -self.speed_x
        # if self.pos_y > 250 or self.pos_y < 0:
        #     self.speed_y = -self.speed_y

    def check_pos(self, block_list):
        """Checks if the block was stopped within a limit margin"""
        if abs(self.pos_x - block_list[len(block_list)-2].pos_x) <= MARGIN:
            self.pos_x = block_list[len(block_list)-2].pos_x

    def check_gameover(self, block_list):
        """Checks if game is over"""
        last_block = block_list[len(block_list)-2]
        if self.speed_x == 0 and self.speed_y == 0:
            if self.right <= last_block.pos_x or self.pos_x >= last_block.right:
                print "Game Over!"
                return True

    def break_up(self, block_list, list_parts, gameover):
        """Breaks up the part"""
        last_block = block_list[len(block_list)-2]
        if self.speed_x == 0 and self.speed_y == 0:
            if gameover:
                self.speed_y = 2
            if self.pos_x < last_block.pos_x:
                lost_left = last_block.pos_x - self.pos_x
                add_falling_block(list_parts, self.pos_x, self.pos_y, lost_left, (-2, 2))
                self.width -= last_block.pos_x - self.pos_x
                self.pos_x = last_block.pos_x
            if self.right > last_block.right:
                lost_right = self.width - last_block.right + self.pos_x
                add_falling_block(list_parts, last_block.right, self.pos_y, lost_right, (2, 2))
                self.width = last_block.right - self.pos_x


def main():
    """Main method"""
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((WIDTH, HEIGHT))

    gameover = False

    block_list = []
    list_parts = []

    pos_new_block = 0
    speed_new_block = 0

    block_list.append(Rectangle((WIDTH - BLOCK_WIDTH)/2,
                                HEIGHT - BLOCK_HEIGHT,
                                BLOCK_WIDTH, BLOCK_HEIGHT, (0, 0)))

    add_block(gameover, block_list, 2, BLOCK_WIDTH, SPEED_NORMAL, (WIDTH - BLOCK_WIDTH)/2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    move_down(block_list)
                    current_block = block_list[len(block_list)-1]
                    last_block = block_list[len(block_list)-2]
                    if current_block.speed_x < 0:
                        pos_new_block = 1 #- last_block.width
                        speed_new_block = SPEED_NORMAL
                    else:
                        pos_new_block = WIDTH - current_block.width
                        speed_new_block = (-2, 0)
                    current_block.speed((0, 0))
                    current_block.check_pos(block_list)
                    gameover = current_block.check_gameover(block_list)
                    current_block.break_up(block_list, list_parts, gameover)
                    add_block(gameover, block_list, len(block_list) + 1, 
                              current_block.width, speed_new_block, pos_new_block)


        display.fill(WHITE)

        for block in block_list:
            block.draw(display)
            block.move()
            block.draw(display)

        for block in list_parts:
            block.draw(display)
            block.move()
            block.draw(display)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()


