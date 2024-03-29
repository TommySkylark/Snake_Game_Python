#Snake object
import pygame
from pygame.locals import *
class Snake():

    def __init__(self, color, start_direction, screen, box_size, difficulty):
        self.x = 105
        self.y = 245

        self.positions = [[self.x, self.y], [self.x - box_size, self.y], [self.x - box_size * 2, self.y]]
        self.direction = start_direction
        self.color = color
        self.head_coords = self.positions[0]
        self.tail_coords = self.positions[-1]
        self.screen = screen
        self.box_size = box_size
        self.difficulty = difficulty
        

        #Graphics
        #load based on color setting
        
        self.head_up = self.head_down = pygame.image.load("graphics/" + self.color + "_snake/snake_head_up.png").convert_alpha()
        self.head_down = pygame.image.load("graphics/" + self.color + "_snake/snake_head_down.png").convert_alpha()
        self.head_left = pygame.image.load("graphics/" + self.color + "_snake/snake_head_left.png").convert_alpha()
        self.head_right = pygame.image.load("graphics/" + self.color + "_snake/snake_head_right.png").convert_alpha()
        self.snake_end_left = pygame.image.load("graphics/" + self.color + "_snake/snake_end_left.png").convert_alpha()
        self.snake_end_right = pygame.image.load("graphics/" + self.color + "_snake/snake_end_right.png").convert_alpha()
        self.snake_end_up = pygame.image.load("graphics/" + self.color + "_snake/snake_end_up.png").convert_alpha()
        self.snake_end_down = pygame.image.load("graphics/" + self.color + "_snake/snake_end_down.png").convert_alpha()
        self.snake_segment_horizontal = pygame.image.load("graphics/" + self.color + "_snake/snake_segment_horizontal.png").convert_alpha()
        self.snake_segment_vertical = pygame.image.load("graphics/" + self.color + "_snake/snake_segment_vertical.png").convert_alpha()
        self.corner_1 = pygame.image.load("graphics/" + self.color + "_snake/snake_corner_1.png").convert_alpha()
        self.corner_2 = pygame.image.load("graphics/" + self.color + "_snake/snake_corner_2.png").convert_alpha()
        self.corner_3 = pygame.image.load("graphics/" + self.color + "_snake/snake_corner_3.png").convert_alpha()
        self.corner_4 = pygame.image.load("graphics/" + self.color + "_snake/snake_corner_4.png").convert_alpha()


    def move(self, direction, speed):


        
        if direction == 'UP':
            self.head_coords = [self.head_coords[0], self.head_coords[1] - self.box_size ]
        elif direction == "DOWN":
            self.head_coords = [self.head_coords[0], self.head_coords[1] + self.box_size ]
        elif direction == "RIGHT":
            self.head_coords = [self.head_coords[0] + self.box_size , self.head_coords[1]]
        elif direction == "LEFT": 
            self.head_coords = [self.head_coords[0] - self.box_size , self.head_coords[1]]


       
        self.positions.insert(0, self.head_coords)

    
        
    

    def draw(self):
        '''draws the snake based on its positions'''
    
        

        #Draw the head
        if self.direction == 'UP':
            self.screen.blit(self.head_up, (self.head_coords[0], self.head_coords[1]))
        elif self.direction == 'DOWN':
            self.screen.blit(self.head_down, (self.head_coords[0], self.head_coords[1]))
        elif self.direction == "RIGHT":
            self.screen.blit(self.head_right, (self.head_coords[0], self.head_coords[1]))
        elif self.direction == "LEFT":
            self.screen.blit(self.head_left, (self.head_coords[0], self.head_coords[1]))

        #Body
        for i in range(len(self.positions)):
            if i != 0 and i != len(self.positions) - 1:

                #look at previous AND next coordinates to determine if this is a 'corner' piece
                #Corner Piece #1 First Case
                if self.positions[i][0] == self.positions[i-1][0] and self.positions[i][1] > self.positions[i-1][1]:
                    if self.positions[i][0] > self.positions[i + 1][0]:
                        self.screen.blit(self.corner_1, (self.positions[i]))
                
                    #Corner Piece #2 First Case
                    elif self.positions[i][0] < self.positions[i+1][0]:
                        self.screen.blit(self.corner_2, (self.positions[i]))

                #Corner Piece #1 second case
                elif self.positions[i][1] == self.positions[i-1][1] and self.positions[i][0] > self.positions[i-1][0] :
                    if self.positions[i+1][0] == self.positions[i][0] and self.positions[i+1][1] < self.positions[i][1]:
                        self.screen.blit(self.corner_1, (self.positions[i]))
                    #Corner Piece #3 First Case
                    elif self.positions[i+1][0] == self.positions[i][0] and self.positions[i+1][1] > self.positions[i][1]:
                        self.screen.blit(self.corner_3, (self.positions[i]))                    

                #Corner Piece #2 second case
                elif self.positions[i][1] == self.positions[i-1][1] and self.positions[i][0] < self.positions[i-1][0]:
                    if self.positions[i][0] == self.positions[i+1][0] and self.positions[i][1] > self.positions[i+1][1]:
                        self.screen.blit(self.corner_2, (self.positions[i]))
                    #Corner Piece #4 First Case
                    elif self.positions[i][0] == self.positions[i+1][0] and self.positions[i][1] < self.positions[i+1][1]:
                        self.screen.blit(self.corner_4, (self.positions[i]))
                #Corner Piece #3 Second Case
                elif self.positions[i][0] == self.positions[i-1][0] and self.positions[i][1] < self.positions[i-1][1]:
                    if self.positions[i][1] == self.positions[i+1][1] and self.positions[i+1][0] < self.positions[i][0]:
                        self.screen.blit(self.corner_3, (self.positions[i])) 
                    #Corner Piece #4 Second Case
                    elif self.positions[i][1] == self.positions[i+1][1] and self.positions[i+1][0] > self.positions[i][0]:
                        self.screen.blit(self.corner_4, (self.positions[i]))
                #No corner piece
            
                if self.positions[i][0] == self.positions[i-1][0] and self.positions[i][0] == self.positions[i+1][0]:
                    self.screen.blit(self.snake_segment_vertical, (self.positions[i]))
                    
                elif self.positions[i][1] == self.positions[i-1][1] and self.positions[i][1] == self.positions[i+1][1]:
                        self.screen.blit(self.snake_segment_horizontal, (self.positions[i]))
            elif i == len(self.positions) - 1:
                if self.positions[i][0] < self.positions[i-1][0]:
                    self.screen.blit(self.snake_end_left, (self.positions[i]))
                elif self.positions[i][0] > self.positions[i-1][0]:
                    self.screen.blit(self.snake_end_right, (self.positions[i]))
                elif self.positions[i][1] < self.positions[i-1][1]:
                    self.screen.blit(self.snake_end_up, (self.positions[i]))
                elif self.positions[i][1] > self.positions[i-1][1]:
                    self.screen.blit(self.snake_end_down, (self.positions[i]))
       
    def eat_apple(self, apple):

        if self.head_coords == apple.position:
            return True
        else:
            return False

    def pieces_in_box(self):
        
        if self.head_coords[0] % self.box_size == 0 and self.head_coords[1] % self.box_size == 0:
            return True
        else:
        
            return False