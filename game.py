#Main game file

import pygame, sys
from pygame.locals import *
from snake import *
from apple import *
from obstacle import *
#Setup some constants/colors
DARKGREEN = (162, 209, 73)
LIGHTGREEN = (170, 215, 81)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTRED = (240, 120, 120)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHTBLUE = (120, 240, 120)
YELLOW = (255, 255, 0)
TRANSPARENTWHITE = (255, 255, 255, 128)
TEAL = (0, 128, 128)
TURQUOISE = (175, 238, 238)
DARKTURQUOISE = (0, 206, 209)
FONT = "freesansbold.ttf"

FPS = 15
BOX_SIZE = 35
DISPLAYX = 455
DISPLAYY = 455

#DIRECTIONS
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

#Score
SCORE = 0
HIGHSCORE = 0




pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/crunch.wav")
pygame.mixer.music.set_volume(0.7)
button_click_sound = pygame.mixer.Sound("sounds/button_select_short.wav")
game_over_sound = pygame.mixer.Sound("sounds/game_over_sound.wav")
dis=pygame.display.set_mode((DISPLAYX, DISPLAYY))
CLOCK = pygame.time.Clock()
pygame.display.update()
pygame.display.set_caption("ADVANCED SNAKE")

grass = pygame.image.load("graphics/grass/grass.png").convert()




count_font = pygame.font.SysFont("freesansbold.ttf", 35)

def apple_count(count):
    value = count_font.render("Score: " + str(count), True, WHITE)
    high_score_value = count_font.render("Best: " + str(get_high_score()), True, WHITE)
    dis.blit(value, [0, 0])
    dis.blit(high_score_value, [0, BOX_SIZE])

def get_high_score():
    score_file = open("highscore.txt")
    high_score = 0
    for line in score_file:
        high_score = line
    return int(high_score)

def set_high_score(score):
    file_write = open("highscore.txt", "w")
    file_write.write(str(score))
    file_write.close()


def game_loop(difficulty):

    global SCORE
    

    time = 0
    
    #Create new snake
    snake_obj = Snake(get_current_color(), "RIGHT", dis, BOX_SIZE, difficulty)

    #Create new apple
    

    frame = 0
    pressed = False
    
    obstacles = Obstacles(BOX_SIZE, DISPLAYX, DISPLAYY, difficulty, BLACK, snake_obj, [350, 245])
    apple = Apple(RED, dis, BOX_SIZE, snake_obj, obstacles)
    obstacles.create_obstacles()

    
    while True:
        pressed = False
        time_passed = CLOCK.tick(FPS) / 1000
        time += time_passed
        
        if frame == 1:
            frame == 0
        else:
            frame += 1
        
        #count = len(snake_obj.positions) - 1    
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (pressed == False and snake_obj.pieces_in_box()):
                if collision_check(snake_obj, obstacles) == True:
                    SCORE = 0
                    game_over(snake_obj, obstacles, difficulty)
                    return                
                if event.key == K_LEFT:
                    if snake_obj.direction != RIGHT:
                        
                        snake_obj.direction = LEFT
                        pressed = True

                        snake_obj.move(snake_obj.direction, difficulty)

                elif event.key == K_RIGHT:
                    if snake_obj.direction != LEFT:
                        
                        snake_obj.direction = RIGHT
                        pressed = True
                        
                        snake_obj.move(RIGHT, difficulty)

                elif event.key == K_UP:
                    if snake_obj.direction != DOWN:
                        
                        snake_obj.direction = UP
                        pressed = True
                        
                        snake_obj.move(UP, difficulty)

                elif event.key == K_DOWN:
                    if snake_obj.direction != UP:
                        
                        snake_obj.direction = DOWN
                        pressed = True
                        
                        snake_obj.move(DOWN, difficulty)

         
          
                
        
        if collision_check(snake_obj, obstacles) == True:
            SCORE = 0
            game_over(snake_obj, obstacles, difficulty)
            return

        
        if time > 0 and not pressed: 
   
            time = 0
            if snake_obj.direction == LEFT:
                snake_obj.move(LEFT, difficulty)
                
            elif snake_obj.direction == RIGHT:
                snake_obj.move(RIGHT, difficulty)
                
            elif snake_obj.direction == UP:
                snake_obj.move(UP, difficulty)
            
                
            elif snake_obj.direction == DOWN:
                snake_obj.move(DOWN, difficulty)
                
                

            #applecount = 0
                
        if snake_obj.eat_apple(apple):
            apple.place_on_grid(DISPLAYX, DISPLAYY)
            SCORE += 1
            pygame.mixer.music.play()
                    

            #Check if score is a high score
            if SCORE > get_high_score():
                set_high_score(SCORE)
                apple_count(SCORE)
                #applecount += 1

        else:    
            snake_obj.positions.remove(snake_obj.positions[-1])
            snake_obj.tail_coords = snake_obj.positions[-1]

           
            #font = pygame.font.Font("freesansbold.ttf", 18)
            #text = font.render(applecount, True, green, blue)
            #textRect = text.get_rect()
            #textRect.center = (425 // 2, 425 // 2)

            #Try using message for counter overlay


            
            #message(applecount, RED)


        dis.fill(WHITE)
        draw_game_area()
        obstacles.draw_obstacles(dis)
        apple.draw()
        snake_obj.draw()
        
        apple_count(SCORE)
 
        pygame.display.update()
        CLOCK.tick(difficulty)
def draw_game_area():
    # Directly draw the grass3 background
    dis.blit(grass, (0, 0))

def collision_check(snake_obj, obstacles):
    #Checks for collision with world borders.

    if snake_obj.head_coords[0] < 0 or snake_obj.head_coords[1] < 0:

        return True
    if snake_obj.head_coords[0] >= 455 or snake_obj.head_coords[1] >= 455:

        return True

    if obstacles.check_collision(snake_obj):
        return True
    
    for i in range(1, len(snake_obj.positions)):
        
        if snake_obj.positions[i] == snake_obj.head_coords:
            draw_game_area()
            snake_obj.draw()
            pygame.display.update()
            return True
    
    else:
        return False

def text_objects(text, font):
    textsurface = font.render(text, True, BLACK)
    return textsurface, textsurface.get_rect()



def start_screen():

    font = pygame.font.Font(FONT, 60)
    play_font = pygame.font.Font(FONT, 30)
    

    font_surface = font.render("SNAKE", True, WHITE)
    play_surface = play_font.render("Press P to Play", True, WHITE)
    score_surface = play_font.render("High Score: " + str(get_high_score()), True, YELLOW)


    rect_font = font_surface.get_rect()
    play_rect_font = play_surface.get_rect()
    score_rect = score_surface.get_rect()

    rect_font.center = ((DISPLAYX / 2), (DISPLAYY / 2))
    play_rect_font.center = ((DISPLAYX / 2), (DISPLAYY / 1.65))
    score_rect.center = ((DISPLAYX / 2), (DISPLAYY / 1.45))
    draw_game_area()
    dis.blit(font_surface, rect_font)
    dis.blit(play_surface, play_rect_font)
    dis.blit(score_surface, score_rect)
    pygame.display.update()









    #Difficulty Buttons
    
    difficulty_main_font = pygame.font.Font(FONT, 20)
    
    
    difficulty_surface = difficulty_main_font.render("Select Difficulty (changes speed)", True, WHITE)
    
    difficulty_rect_font = difficulty_surface.get_rect()
    
    difficulty_rect_font.center = ((DISPLAYX / 1.95), (DISPLAYY / 1.65))
    
    
    
    
    
    #gameDisplay.blit(TextSurf, TextRect)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    easy_rect = pygame.Rect(25,350,100,50)
    normal_rect = pygame.Rect(175,350,100,50)
    hard_rect = pygame.Rect(350,350,100,50)

    #Easy button

    pygame.draw.rect(dis, WHITE, (25, 350, 100, 50))

    easy_font = pygame.font.Font("freesansbold.ttf", 15)
    textSurf, textRect = text_objects("Easy", easy_font)
    textRect.center = ((25+50), (350 + 25))
    dis.blit(textSurf, textRect)
    
    
    #Normal Button

    pygame.draw.rect(dis, WHITE, (175, 350, 100, 50))

    normal_font = pygame.font.Font("freesansbold.ttf", 15)
    textSurf, textRect = text_objects("Normal", normal_font)
    textRect.center = ((175+50), (350 + 25))
    dis.blit(textSurf, textRect)
    
    #Hard Button
    
    pygame.draw.rect(dis, WHITE, (325, 350, 100, 50))

    normal_font = pygame.font.Font("freesansbold.ttf", 15)
    textSurf, textRect = text_objects("Hard", normal_font)
    textRect.center = ((325+50), (350 + 25))
    dis.blit(textSurf, textRect)
    pygame.display.update()
    
    #Buttons end
    pygame.display.update()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                if event.key == K_p:
                    difficulty = random.choice([7, 15, 40])
                    button_click_sound.play()
                    game_loop(difficulty)
                elif event.key == K_s:
                    button_click_sound.play()
                    settings_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_button(easy_rect):
                    #easy button
                    button_click_sound.play()
                    game_loop(10)
                elif mouse_on_button(normal_rect):
                    #normal button
                    button_click_sound.play()
                    game_loop(15)
                elif mouse_on_button(hard_rect):

                    #hard button
                    button_click_sound.play()
                    game_loop(40)
        CLOCK.tick(FPS)



    
def game_over(snake, obstacles, difficulty):
    game_over_sound.play()

    font = pygame.font.Font(FONT, 60)
    play_font = pygame.font.Font(FONT, 30)

    font_surface = font.render("GAME OVER", True, WHITE)
    play_surface = play_font.render("Press P to play again", True, WHITE)
    main_menu_surface = play_font.render("Press M for Main Menu", True, WHITE)

    rect_font = font_surface.get_rect()
    play_rect_font = play_surface.get_rect()
    menu_text_rect = main_menu_surface.get_rect()

    rect_font.center = ((DISPLAYX / 2), (DISPLAYY / 2.5))
    play_rect_font.center = ((DISPLAYX / 1.95), (DISPLAYY / 1.75))
    menu_text_rect.center = ((DISPLAYX / 1.95), (DISPLAYY / 1.55))

    draw_game_area()
    snake.draw()
    obstacles.draw_obstacles(dis)
    dis.blit(font_surface, rect_font)
    dis.blit(play_surface, play_rect_font)
    dis.blit(main_menu_surface, menu_text_rect)
    pygame.display.update()

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    button_click_sound.play()
                    
                    game_loop(difficulty)
                elif event.key == pygame.K_m:
                    start_screen()

        CLOCK.tick(FPS)
    
def settings_screen():

    color_orders = ['blue', 'red', 'green']
    font = pygame.font.Font(FONT, 40)
    small_font = pygame.font.Font(FONT, 23)
    
    settings_surf = dis.convert_alpha()
    font_surface = font.render("SETTINGS", True, BLACK)
    escape_surface = small_font.render("Press ESC or S to Escape", True, BLACK)
    color_option_text_surface = small_font.render("Color: ", True, BLACK)
    choose_grid_text_surf = small_font.render("Grid: ", True, BLACK)
    choose_grid = small_font.render(str(get_current_background()), True, BLACK)

    settings_background_rect = pygame.Rect(DISPLAYX / 6, DISPLAYY / 6, DISPLAYX / 1.5, DISPLAYY - DISPLAYY / 5)
    color_rect = pygame.Rect(DISPLAYX / 2, DISPLAYY / 2.15, BOX_SIZE * 1.25, BOX_SIZE * 1.25)
    rect_font = font_surface.get_rect()
    escape_rect_font = escape_surface.get_rect()
    color_option_font_rect = color_option_text_surface.get_rect()
    choose_grid_font_rect = choose_grid_text_surf.get_rect()
    choose_grid_rect = choose_grid.get_rect()

    rect_font.center = ((DISPLAYX / 2), (DISPLAYY / 4))
    escape_rect_font.center = ((DISPLAYX / 2), (DISPLAYY / 3))
    color_option_font_rect.center = ((DISPLAYX / 3), (DISPLAYY / 2))
    choose_grid_font_rect.center = ((DISPLAYX / 3), (DISPLAYY / 1.5))
    choose_grid_rect.center = ((DISPLAYX / 2), (DISPLAYY / 1.5))
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_ESCAPE:
                    #Exit setting screen
                    button_click_sound.play()
                    start_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_button(color_rect):
                    button_click_sound.play()
                    pos_current_color = color_orders.index(get_current_color())

                    if pos_current_color == len(color_orders) - 1 :
                        #Last item on the list
                        #switch back to blue
                        change_color_settings(color_orders[0])
                    else:
                        #Switch color to next color on the list
                        next_color = color_orders[pos_current_color + 1]
                        change_color_settings(next_color)
                elif mouse_on_button(choose_grid_rect):
                    button_click_sound.play()
                    change_background()

            draw_game_area()            
            pygame.draw.rect(settings_surf, TRANSPARENTWHITE, settings_background_rect)
            pygame.draw.rect(settings_surf, get_current_color(), color_rect)

            choose_grid = small_font.render(str(get_current_background()), True, BLACK)
            choose_grid_rect = choose_grid.get_rect()
            choose_grid_rect.center = ((DISPLAYX / 2), (DISPLAYY / 1.5))

            dis.blit(settings_surf, (0, 0))
            dis.blit(color_option_text_surface, color_option_font_rect)
            dis.blit(font_surface, rect_font)
            dis.blit(escape_surface, escape_rect_font)            
            dis.blit(choose_grid_text_surf, choose_grid_font_rect)
            dis.blit(choose_grid, choose_grid_rect)
            pygame.display.update()
            CLOCK.tick(FPS)

def mouse_on_button(rectangle):
    mouse_position = pygame.mouse.get_pos()
    #Check to see if the mouse position is on the button
    if mouse_position[0] >= rectangle.topleft[0] and mouse_position[0] <= rectangle.bottomright[0]:
        if mouse_position[1] >= rectangle.topleft[1] and mouse_position[1] <= rectangle.bottomright[1]:
            return True
    return False

def get_current_color():
    settings_file = open("settings.txt", "r")
    lines = settings_file.readlines()
    color_line = lines[0].split(": ")
    color = color_line[1]
    settings_file.close()
    return color.strip()


def change_color_settings(new_color):
    read_settings_file = open("settings.txt", "r")
    all_lines = read_settings_file.readlines()
    all_lines[0] = "Color: " + new_color + "\n"
    read_settings_file.close()

    write_settings_file = open("settings.txt", "w")
    write_settings_file.writelines(all_lines)
    write_settings_file.close()

def get_current_background():
    settings_file = open("settings.txt", "r")
    lines = settings_file.readlines()
    background_line = lines[1].split(": ")
    background = background_line[1]
    settings_file.close()
    return int(background)

def change_background():
    read_settings_file = open("settings.txt", "r")
    all_lines = read_settings_file.readlines()
    read_settings_file.close()
    if get_current_background() == 5:
        #change to 1
        all_lines[1] = "Background: 1"
    else:
        #add 1
        new_background = get_current_background() + 1
        all_lines[1] = "Background: " + str(new_background)
    
    write_settings_file = open("settings.txt", "w")
    write_settings_file.writelines(all_lines)
    write_settings_file.close()

def main():


    while True:
        start_screen()
    
main()
