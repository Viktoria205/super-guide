#!/usr/bin/env python

import pygame
import sys
import os
import time
import random
import pygame_menu
pygame.init()

surface = pygame.display.set_mode((600, 400)) #Tworzenie okna gry
bg_image = pygame.image.load(os.path.join('images', 'snake.jpg'))
HIGH_SCORES = 'highscore.txt'
SIZE_BLOCK = 20                       #Kolory i glowne wartosci
FRAME_COLOR = (0, 255, 204)
RED = (224, 0, 0)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
BROWN = (200, 100, 40)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN = 1
health = 3
stageon = True
DIFFICULTY = ['EASY']
size = (SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * SIZE_BLOCK + HEADER_MARGIN)
print(size) 

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 28)
health_img = pygame.image.load(os.path.join('images', 'heart.jpg'))
health_img = pygame.transform.scale(health_img, (30, 30))
    

RULES = ['In the Snake game, the player uses the','arrow keys to move the snake around',
 'the board. When the snake finds food,', 'it eats it and thus is large in size.',           #Menu dla Rules
 'You have 3 lives and 4 tries. When the snake', 'leaves the playing field or stumbles',
 'with itself, one life is lost and the snake', 'appears from the brown square (house).',
'The goal is to make the snake as big', 'as possible and earn points.']
rules = pygame_menu.Menu(
        height = size[1] * 0.9,
        theme = pygame_menu.themes.THEME_GREEN,
        title = 'Rules',
        width = size[0]  * 0.95)
for m in RULES:
    rules.add.label(m ,align = pygame_menu.locals.ALIGN_LEFT, font_size = 20)
    rules.add.vertical_margin(5)

ABOUT_AUTHOR = ['My name is Viktoriia.','I am a 1st year student of WUST.',
 'I created a Snake because I remembered', 'how I loved to play if as a child.',          #Menu dla About author
 'I am very glad that you are playing my game.']
about_author = pygame_menu.Menu(
        height = size[1] * 0.7,
        theme = pygame_menu.themes.THEME_GREEN,
        title = 'About author',
        width = size[0]  * 0.95)
for m in ABOUT_AUTHOR:
    about_author.add.label(m ,align = pygame_menu.locals.ALIGN_LEFT, font_size = 20)
    about_author.add.vertical_margin(5)
    
high = pygame_menu.Menu(
        height = size[1] * 0.7,
        theme = pygame_menu.themes.THEME_GREEN,
        title = 'High score',
        width = size[0]  * 0.95)
open_txt = open(HIGH_SCORES, 'r')
text = 'High score : ' + open_txt.read()                                            #Menu dla High score
high.add.label(text, align = pygame_menu.locals.ALIGN_CENTER, font_size = 40)
high.add.image(os.path.join('images', 'high.jpg'), angle = 0, scale = (0.15, 0.15))
open_txt.close()
    
class SnakeBlock:
    """Klasa, ktora reprezentuje kafelki dla Snake."""
    
    def __init__(self, x, y):
        """Konstruktor, ktory tworzy koordynaty x i y dla kafelek.
    
    @pam x : (float) pozioma koordynata kafelka, 
    @pam y : (float) pionowa koordynata kafelka. """
       
        self.x = x
        self.y = y
        pygame.mixer.init()
        
    def inside(self):
        """Funkcja, ktora sprawdza czy znajduje sie Snake na polu gry.
        
        return True : (bool), jesli x i y sa poprawne,
               False : (bool), jesli x i y nie sa poprawne"""
        
        return 0 <= self.x < SIZE_BLOCK and 0 <= self.y < SIZE_BLOCK
    
    def __eq__(self, other):
        """Funkcja, ktora sprawdza czy obiekt jest klasy SnakeBlock"""
        
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y
    
    
def draw_block(color, row, column):
    """Funkcja, ktora rysuje kolumny i wiersze pola dla gry."""
    
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1), 
                                             HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1), 
                                             SIZE_BLOCK, SIZE_BLOCK])
def highs(x):
    """Funkcja, ktora sprawdza czy ilosc punktow jest wieksz od juz zapisanej, jeli nie, to\
 zapisuje nowa najwieksza ilosc punkow w grze."""
 
    total1 = int(x)
    f = open(HIGH_SCORES, 'r+')
    s = f.read()
    n = int(s)
    if total1 > n:
        f = open(HIGH_SCORES, 'w+')
        f.write(str(total1))
    else:
        pass
    f.close()

def show_health():
    global health
    show = 0
    k = 330
    while show != health:
        screen.blit(health_img, (k , 20))
        k += 40
        show += 1
def show_game_over(total):
    font = pygame.font.SysFont('arial', 30)
    f = font.render('Game over', True, BROWN)
    f_esc = font.render(f'Your score : {total}', True, BROWN)
    screen.blit(pygame.image.load(os.path.join('images', 'dead_snake.jpg')), (0,0))
    screen.blit(f, (90,115))
    screen.blit(f_esc, (78,150))
    pygame.display.flip()
    time.sleep(5)
    os._exit(0)
    pygame.quit()
    stageon = False
    
def set_difficulty(value: tuple[any, int], difficulty: str):
    """Funkcja, ktora sprawdza jaki poziom trudnosci jest wybrany.
     
     @pam value : (tuple) 
     @pam difficulty : (str) """
      
    selected, index = value
    print('Selected difficulty: "{0}" ({1}) at index {2}'
          ''.format(selected, difficulty, index))
    DIFFICULTY[0] = difficulty
    
def start_the_game(difficulty: list) : 
    """Funkcja, ktora zaczyna gre. """ 
    
    assert isinstance(difficulty, list)
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)
    
    def random_block():
        """Funkcja, ktora sprawdza czy kafelek jest zajety przez Snake czy nie."""
        x = random.randint(1, COUNT_BLOCKS - 1)
        y = random.randint(1, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_block:
            empty_block.x = random.randint(1, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(1, COUNT_BLOCKS - 1)
        return empty_block

    snake_block = [SnakeBlock(1, 19), SnakeBlock(1, 18), SnakeBlock(1, 17)]  #Poczatkowe rozmiszczenie Snake
    apple = random_block()
    d_row = buf_row = 0
    d_col = buf_col = -1
    total = 0
    speed = 1
    
    while stageon:
        global health
        pygame.mixer.music.pause()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1
                
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0,0, size[0], HEADER_MARGIN])
        show_health()
        
        text_total = courier.render(f"Total: {total}", 0, WHITE)  #Total i speed pod czas gry
        text_speed = courier.render(f"Speed: {speed}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 160, SIZE_BLOCK))
    
        for row in range(COUNT_BLOCKS):        
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE
            
                draw_block(color, row, column)   #Rysowanie pola dla gry
        draw_block(BROWN, 1, 19)        #Rysowanie domku
        
        head = snake_block[-1]
        
        for x in range(20):                              #Zderzenia ze scianami dla liczniku zyc
            if head == SnakeBlock(x, 20):
                crash = pygame.mixer.Sound(os.path.join('sound', 'crash.mp3'))
                pygame.mixer.Sound.play(crash)
                if health == 0:

                    show_game_over(total)
                    return False
                else:
                    health -= 1
                    head = SnakeBlock(1, 19)
                    d_row = buf_row = 0
                    d_col = buf_col = -1
                
        for x in range(20):
            if head == SnakeBlock(x, -1):
                crash = pygame.mixer.Sound(os.path.join('sound', 'crash.mp3'))
                pygame.mixer.Sound.play(crash)
                if health == 0:

                    show_game_over(total)
                    return False
                else:
                    health -= 1
                    head = SnakeBlock(1, 19)
                    d_row = buf_row = 0
                    d_col = buf_col = -1
                
        for x in range(20):
            if head == SnakeBlock(20, x):
                crash = pygame.mixer.Sound(os.path.join('sound', 'crash.mp3'))
                pygame.mixer.Sound.play(crash)
                if health == 0:

                    show_game_over(total)
                    return False
                else:
                    health -= 1
                    head = SnakeBlock(1, 19)
                    d_row = buf_row = 0
                    d_col = buf_col = -1
                
        for x in range(20):
            if head == SnakeBlock(-1, x):
                crash = pygame.mixer.Sound(os.path.join('sound', 'crash.mp3'))
                pygame.mixer.Sound.play(crash)
                if health == 0:

                    show_game_over(total)
                    return False
                else:
                    health -= 1
                    head = SnakeBlock(1, 19)
                    d_row = buf_row = 0
                    d_col = buf_col = -1
            
            
        draw_block(RED, apple.x, apple.y)   #Rysowanie jablka
        
        for block in snake_block:
            draw_block(SNAKE_COLOR, block.x, block.y)  #Rysowanie Snake
            
        pygame.display.flip()      
        
        if apple == head:                           #"Dodanie" jablka do Snake
            sound = pygame.mixer.Sound(os.path.join('sound', 'sound.mp3'))
            pygame.mixer.Sound.play(sound)
            total += 1
            speed = total//5 + 1
            snake_block.append(apple)
            apple = random_block()
        
        d_row = buf_row
        d_col = buf_col
      
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)
    
        if new_head in snake_block:              #Sprawdzenie czy Snake nie zdarzyla sie sama z soba
            crash = pygame.mixer.Sound(os.path.join('sound', 'crash.mp3'))
            pygame.mixer.Sound.play(crash)
            if health == 0:

                show_game_over(total)
                return False
            else :
                health -=1
                new_head = SnakeBlock(1, 18)
                d_row = buf_row = 0
                d_col = buf_col = -1
            
        
        snake_block.append(new_head)
        snake_block.pop(0)
    
        if difficulty == 'EASY':         #Sprawdzenie poziomu trudnosci
            timer.tick(3 + speed)
        elif difficulty == 'HARD':
            timer.tick(5 + speed)
        
theme = pygame_menu.themes.THEME_GREEN        #Menu
theme.set_background_color_opacity(0.87)
menu = pygame_menu.Menu('Welcome', 430, 400,theme = theme)

menu.add.button('Play', start_the_game, DIFFICULTY)
menu.add.selector('Difficulty :', [('Speed low', 'EASY'), ('Speed high', 'HARD')], onchange = set_difficulty)
menu.add.button('Rules', rules)
menu.add.button('High score', high)
menu.add.button('About author', about_author)
menu.add.button('Exit', pygame_menu.events.EXIT)
pygame.mixer.music.load(os.path.join('sound', 'background.mp3'))
pygame.mixer.music.play()

while True:

    screen.blit(bg_image, (0,0))

    events = pygame.event.get()
    for event in events:                                   #Wyswietlanie menu i gry
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
     
    if stageon == False:
        pygame.display.flip()
        time.sleep(5)
        os._exit(0)
        pygame.quit()
        