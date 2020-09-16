'''Author: Jenny Su
Date: May 26 2018
Description: Menu sprites; buttons'''

import pygame

class GameButton(pygame.sprite.Sprite):
    '''This function creates the button to start the main game'''
    def __init__(self, screen, menu, button):
        '''This method initializes the class'''
        pygame.sprite.Sprite.__init__(self)
        
        # Upload buttons
        self.__buttons = []
        
        # If it is in the menu; upload these variables
        if menu:
            for sprite in range(2):
                self.__buttons.append(pygame.image.load('images/Menu/'+ button + str(sprite) + '.png'))
        
        # Otherwise it is part of the end game screen; upload these variables
        else:
            for sprite in range(2):
                self.__buttons.append(pygame.image.load('images/EndGameScreen/' + button + str(sprite) + '.png'))
        
        # Set image as the unlit button sprite
        self.image = self.__buttons[0]
        
        self.rect = self.image.get_rect()
        
        self.rect.centerx = screen.get_width()/2
        
        # Set button locations
        if button == 'StartMainGame':
            self.rect.top = 200
        
        elif button == 'StartTutorial':
            self.rect.top = 293
        
        elif button == 'BackToTitleScreen':
            self.rect.top = 230
        
        elif button == 'ExitGame':
            self.rect.top = 325
            
        else:
            self.rect.top = 386
        
        # Set variables
        self.__buttonFunction = button
        self.__hover = False
        
    def hover(self, hovering):
        '''This method changes the sprite so that it can change colours when it 
        is hovered.'''
        if hovering:
            self.__hover = True
        
        else:
            self.__hover = False
    
    def getFunction(self):
        '''This method returns the button function'''
        return self.__buttonFunction
    
    def update(self):
        '''This method updates the sprite'''
        if self.__hover:
            self.image = self.__buttons[1]
        
        else:
            self.image = self.__buttons[0]

class Background(pygame.sprite.Sprite):
    '''This class creates the background'''
    def __init__(self, menu):
        pygame.sprite.Sprite.__init__(self)
        
        # Upload menu image; with title and bright
        if menu:
            self.image = pygame.image.load('images/Menu/MenuBack.png')
        
        # Upload background image; without title and dark 
        else:
            self.image = pygame.image.load('images/Menu/MenuBack1.png')
        
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        self.rect.top = 0
        self.rect.left = 0

class TutorialButtons(pygame.sprite.Sprite):
    '''This class creates the tutorial buttons to guide the player'''
    def __init__(self, button, screen):
        '''This method initiates the class, it takes the identification of the 
        buttons and shows when it is pressed.'''
        pygame.sprite.Sprite.__init__(self)
        
        # Uploads buttons
        self.__buttons = []
        for sprite in range(6):
            self.__buttons.append(pygame.image.load('images/Tutorial/Button' + str(sprite) + '.png'))
        
        # Checks which button it is and set images
        if button == 'A':
            self.image = self.__buttons[4]
        
        elif button == 'D':
            self.image = self.__buttons[3]
        
        else:
            self.image = self.__buttons[5]
        
        self.rect = self.image.get_rect()
        
        # Checks which button it is and locates it
        if button == 'A':
            self.rect.left = screen.get_width() - 190
            self.rect.top = 100
        
        elif button == 'D':
            self.rect.right = screen.get_width() - 10
            self.rect.top = 100
        
        else:
            self.rect.left = screen.get_width() - 190
            self.rect.top = 170
        
        # Sets variables
        self.__button = button
    
    def pressed(self, pressing):
        '''This method checks if the player is currently pressing the button'''
        # Checks if button is being pressed
        if pressing:
            if self.__button == 'A':
                self.image = self.__buttons[0]
            elif self.__button == 'D':
                self.image = self.__buttons[1]
            else:
                self.image = self.__buttons[2]
        else:
            if self.__button == 'A':
                self.image = self.__buttons[4]
            
            elif self.__button == 'D':
                self.image = self.__buttons[3]
            
            else:
                self.image = self.__buttons[5]            

class TutorialText(pygame.sprite.Sprite):
    '''This class displays text to explain the game and its mechanics'''
    def __init__(self):
        '''This method initiates the class, loading the first text'''
        pygame.sprite.Sprite.__init__(self)
        
        # Uploads texts images to guide player during the tutorial
        self.__texts = []
        for sprite in range(5):
            self.__texts.append(pygame.image.load('images/Tutorial/Text/Text' + str(sprite) + '.png'))
        
        # Sets image
        self.image = self.__texts[0]
        
        self.rect = self.image.get_rect()
        self.rect.top = 100
        self.rect.left = 10
        
        # Sets variables
        self.__textNumber = 0
        
    def nextText(self):
        '''This method changes the text number when the player completes the 
        tutorial text'''
        self.__textNumber += 1
        self.image = self.__texts[self.__textNumber]
    
    def reset(self):
        '''This method resets the text when player dies in the tutorial'''
        self.__textNumber = 0
        self.image = self.__texts[self.__textNumber]        
