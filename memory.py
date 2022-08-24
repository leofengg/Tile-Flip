#memory game where you try to find 2 matching tiles

import pygame, random

def main():

    #initialize pygame
    pygame.init()
    #create display window
    pygame.display.set_mode((525, 425))
    #set title
    pygame.display.set_caption('Memory')
    #get display surface
    w_surface = pygame.display.get_surface()
    #create game
    game = Game(w_surface)
    #start game
    game.play()
    #quit game
    pygame.quit()

class Game():

    def __init__(self, surface):
        #initialize game objects

        #general game objects
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        #game specific objects   
        self.score = 0
        
        #lists for removed tiles
        #temporary removed tile
        self.temp_remove = []
        #perm removed tile
        self.perm_remove = []
        #image name of revealed tile
        self.tile_index = []
        
        #create images
        self.images = []
        self.get_images()
        self.randomize_images()

        #list of revealed images
        self.revealed = [] 

        #game board
        self.board_size = 4
        self.board = []
        self.create_board()        

    def create_board(self):
    #create the tiles board layout 
        self.boarder_width = 5
        #get blank column on right side
        width = self.surface.get_width()//5
        width2 = self.surface.get_width() - width
        width3 = width2//4

        #get height
        height = (self.surface.get_height() - self.boarder_width)//4
        index = 0

        for row_index in range(0, self.board_size):
        #create row as empty list
            row = []
            for col_index in range(0, self.board_size):
                #create tile using row and column index
                x = col_index * width3 + self.boarder_width
                y = row_index * height + self.boarder_width
                #append tile object to row
                self.tile = Tile(x, y, width, height, self.images[index], self.surface)
                self.board.append(self.tile)
                index = index + 1

    def get_images(self):

        number = 0
        #make 2 sets of images
        while number != 2:
            for x in range(1,9):
                self.images.append('image{}.bmp'.format(str(x)))   
            number += 1

    def randomize_images(self):
        #randomize order of images
        random.shuffle(self.images)   

    def play(self):
        #until play closes window
        while not self.close_clicked:
            #update frames
            self.handle_events()
            self.draw()

            #check for gameover conditions
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_clock.tick(self.FPS)


    def handle_events(self):
        #handle events that occur in game
        events = pygame.event.get()
        for event in events:
            #quit game
            if event.type == pygame.QUIT:
                self.close_clicked = True
            #mouse 
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse(event)

    def draw(self):
        #draw all game objects
        #fill background color
        self.surface.fill(self.bg_color)
        #show score//time
        self.display_score()
        #draw tiles
        for tile in self.board:
            tile.draw()
        #draw all revealed tiles 
        for image in self.perm_remove:
            image.draw()

        #render created objects
        pygame.display.update()

    def handle_mouse(self, event):
        #if mouse is clicked

        if event.button == 1:
            for tile in self.board:
                #check if mouse is on specific tile
                if tile.check_position(event.pos) == True:
                    #add clicked tile to lists 
                    index = self.board.index(tile)
                    self.temp_remove.append(self.images[index])
                    self.tile_index.append(tile)
                    #reveal clicked tile
                    tile.reveal() 

    def display_score(self):
        #display the score
        score_image = pygame.font.SysFont('',64).render(str(self.score), True, pygame.Color('white'))
        #get position
        score_top_left = (self.surface.get_width() - score_image.get_width(), 0)
        #show on screen
        self.surface.blit(score_image, score_top_left)

    def update(self):
        #update the game 
        self.score = pygame.time.get_ticks() // 1000
        
        #update board if tiles are matching
        #runs after player clicks 2 tiles
        if len(self.temp_remove) == 2:
            #if both tiles match
            if self.check_tile() == True:
                #add tile to perm remove
                for tile in self.tile_index:
                    self.perm_remove.append(tile)
                #empty both lists for next 2 tiles
                self.temp_remove.clear()
                self.tile_index.clear()
            #if tiles don't match  
            else:
                #delay time to display tiles
                pygame.time.delay(700)
                #hide non matching tiles
                for tile in self.tile_index:
                    tile.hide()
                #empty both lists for next 2 tiles
                self.temp_remove.clear()
                self.tile_index.clear()
    
    def check_tile(self):
        #check if tiles match
        #if both tiles match
        if self.temp_remove[0] == self.temp_remove[1]:
            return True
        #if tiles don't match
        else:
            return False
        
    def decide_continue(self):
        #game ends if all 16 tiles are revealed
        if len(self.perm_remove) == 16:
            self.continue_game = False


class Tile():

    def __init__(self, x, y, width, height, image, surface):
        #init all tile objects
        self.image = pygame.image.load(image)
        self.cover = pygame.image.load('image0.bmp')
        self.rect = pygame.Rect(x, y, width, height)
        self.covered = True
        self.surface = surface        

    def draw(self):
        #if tile is still covered
        if self.covered == True:
            self.surface.blit(self.cover, self.rect)
        #if tile is revealed
        elif self.covered == False:
            self.surface.blit(self.image, self.rect)

    def check_position(self, pos):
        #detemine if mouse is on specific tile
        if self.rect.collidepoint(pos) and self.covered == True:
            return True

    def reveal(self):
        #reveal image
        self.covered = False

    def hide(self):
        #cover image
        self.covered = True

main()    