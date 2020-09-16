'''Author: Jenny Su
Date: May 26 2018
Description: Elmia Sprites'''

import pygame

class Player(pygame.sprite.Sprite):
    '''This class is the player's sprite. This sprite stays at the center for 
    almost the etire game; recentering when teleported'''
    def __init__(self, screen):
        '''This method initailizes the class. Creates .__dx and .__dy variables.'''
        pygame.sprite.Sprite.__init__(self)
        
        # Uploads standing positions facing left sprites
        self.__standL = []
        for sprite in range(5):
            self.__standL.append(pygame.image.load('Player/Left/stand1_' + str(sprite) + '.png'))
            
        # Uploads standing positions facing right sprites
        self.__standR = []
        for sprite in range(5):
            self.__standR.append(pygame.image.load('Player/Right/stand1_' + str(sprite) + '.png'))
            
        # Uploads walking positions facing left sprites
        self.__walkL = []
        for sprite in range(4):
            self.__walkL.append(pygame.image.load('Player/Left/walk1_' + str(sprite) + '.png'))
            
        # Uploads walking positions facing right sprites
        self.__walkR = []
        for sprite in range(4):
            self.__walkR.append(pygame.image.load('Player/Right/walk1_' + str(sprite) + '.png'))
            
        # Uploads jumping positions facing left and right
        self.__jumpL = pygame.image.load('Player/Left/jump_0.png')
        self.__jumpR = pygame.image.load('Player/Right/jump_0.png')
        
        # Creates self.image variable in standing right position
        self.image = self.__standR[0]
        self.image = self.image.convert()
        
        # Creates self.rect
        self.rect = self.image.get_rect()
        
        # Create variables
        self.__spriteNumber = 0
        self.__moving = False
        self.__falling = False
        self.__teleported = False
        self.__direction = 'right'
        
        self.__screen = screen
        self.__dx = 0
        self.__dy = 0
        
        # Positions sprite
        self.reset()
        
    def move(self, direction):
        '''This method changes the sprite direction'''
        self.__moving = True
        self.__direction = direction
        
    def stop(self):
        '''This method stops the player'''
        self.__dx = 0
        self.__moving = False
    
    def reset(self):
        '''Resets the sprite back at the beginning'''
        self.rect.bottom = self.__screen.get_height() - 54
        self.rect.centerx = self.__screen.get_width()/2
        self.__moving = False
        
    def teleport(self, pixPos):
        '''This method teleports the player to the fairy'''
        # Teleports player to pix position; bottom of sprite with the bottom of pix
        self.rect.centerx = pixPos[0]
        self.rect.bottom = pixPos[1]
        self.__falling = True
        self.__teleported = True
        
        # Returns how far the player is from the center
        return self.rect.centerx - (self.__screen.get_width()/2)
        
    def fall(self, ground):
        '''This method lowers the player to the ground after teleporting'''
        # Determines the difference from player.rect.bottom and the ground
        difference = self.rect.bottom - ground
        # Checks if player is still in mid air
        if difference >= 1 or difference < -8:
            self.__dy = 5
            self.__falling = True
        # Otherwise, the player lands on the ground
        elif difference >= -8:
            self.rect.bottom = ground - 1
            self.__dy = 0
            self.__falling = False
        
        return self.__falling
        
    def recenter(self):
        '''This method recenters the player to the center of the screen 
        (horizontally)'''
        self.__dx = (self.rect.centerx - (self.__screen.get_width())/2)/1.2
        if self.__dx < 1 and self.__dx > -1:
            self.__dx = 0
        return self.__dx
    
    def getPosition(self):
        '''This method returns the left, right, top and bottom variables of 
        self.rect in that order'''
        # Sends position
        return (self.rect.left, self.rect.right, self.rect.top, self.rect.bottom)
    
    def isFalling(self):
        '''This method returns the self.__falling variable'''
        return self.__falling
    
    def update(self):
        '''This method updates the sprite'''
        # Adds 0.2 to spriteNumber to slow down the animation speed
        self.__spriteNumber += 0.2
        
        # Checks if player is walking; to make up for the uneven number of sprites
        if self.__moving:
            if self.__spriteNumber >= 3:
                self.__spriteNumber = 0
        # Checks standing, there are 4 sprites in the standing list
        else:
            if self.__spriteNumber >= 4:
                self.__spriteNumber = 0
        
        # Checks if player is walking; changes the sprites into walking animation
        if self.__moving:
            if self.__direction == 'right':
                self.image = self.__walkR[int(self.__spriteNumber)]
            else:
                self.image = self.__walkL[int(self.__spriteNumber)]
        
        # Checks if player is falling; changes to jump sprites\
        if self.__falling:
            if self.__direction == 'right':
                self.image = self.__jumpR
            else:
                self.image = self.__jumpL  
                
        # If more moving or falling, changes animation to standing        
        if not self.__falling and not self.__moving:
            if self.__direction == 'right':
                self.image = self.__standR[int(self.__spriteNumber)]
            else:
                self.image = self.__standL[int(self.__spriteNumber)]
        
        # Positions sprites
        self.rect.centerx -= self.__dx
        self.rect.centery += self.__dy

class TeleportSprites(pygame.sprite.Sprite):
    '''This method triggers the teleport sprites, so that the animation of 
    teleportation would play'''
    def __init__(self):
        '''This function initiates the class'''
        pygame.sprite.Sprite.__init__(self)
        
        # Uploads teleport sprites
        self.__teleport = []
        for sprite in range(16):
            self.__teleport.append(pygame.image.load('Teleport/teleport' + str(sprite) + '.png'))
        
        # Uploads a blank
        self.__blank = pygame.image.load('Light/light3.png')
        
        # Sets variable
        self.__playerPos = (0, 0, 0, 0)
        self.image = self.__blank
        self.rect = self.image.get_rect()
        
        self.__animation = False
        self.__reverseSprites = False
        self.__teleportedNumber = 0
        
    def getPlayerPosition(self, playerPos):
        '''This changes the self.__playerPos variable to a new variable'''
        self.__playerPos = playerPos
        self.__animation = True
    
    def getAnimationStat(self):
        '''This method returns True or False if the animation is done our not'''
        return self.__animation
    
    def update(self):
        '''This method updates the sprite'''
        # If the animation was triggered
        if self.__animation:
            self.image = self.__teleport[int(self.__teleportedNumber)]
            # If the animation sequence started 0 and have not hit the top sprite;
            # Animation sprites get higher
            if not self.__reverseSprites:
                self.__teleportedNumber += 1.5
                # Checks if sequence hits the top sprite
                if self.__teleportedNumber > 15:
                    self.__reverseSprites = True
                    self.__teleportedNumber = 14
                    
            # Reverse animation sequence to conclude it
            else: 
                self.__teleportedNumber -= 1.5
                # Checks if sequence hits the first sprite
                if self.__teleportedNumber < 1:
                    self.__reverseSprites = False
                    self.__animation = False
                    self.__teleportedNumber = 0
                    
        # If animation is not triggered, use a blank
        else:
            self.image = self.__blank
        
        # Positions sprite on the player
        self.rect = self.image.get_rect()
        
        self.rect.left = self.__playerPos[0] - 3
        self.rect.top = self.__playerPos[2]
            
class Fairy(pygame.sprite.Sprite):
    '''This class creates the fairy that is controlled by the player's mouse'''
    def __init__(self):
        '''This method initializes the class'''
        pygame.sprite.Sprite.__init__(self)
        
        # Uploads moving sprites
        self.__move = []
        for sprite in range(4):
            self.__move.append(pygame.image.load('Fairy/move' + str(sprite) + '.png'))
        
        # Uploads skill sprites
        self.__skill = []
        for sprite in range(4):
            self.__skill.append(pygame.image.load('Fairy/skill' + str(sprite) + '.png'))
            
        # Sets self.image
        self.image = self.__move[0]
        self.image.set_colorkey((0, 0, 0))
        
        # Sets variables
        self.__spriteNumber = 0
        self.__teleported = False
        self.rect = self.image.get_rect()
        
    def move(self):
        '''This method makes the fairy follow your mouse cursor'''
        self.rect.center = pygame.mouse.get_pos()
        
    def teleport(self):
        '''This method triggers sprite to change to teleport'''
        self.__teleported = 0
        
    def update(self):
        '''This method updates the sprite'''
        # If the player teleported, change animation to skill animation
        if self.__teleported < 4:
            self.image = self.__skill[int(self.__spriteNumber)]
            self.__teleported += 1
        else:
            self.image = self.__move[int(self.__spriteNumber)]
        
        # Slows down animation sequence
        self.__spriteNumber += 0.2
        if self.__spriteNumber >= 3:
            self.__spriteNumber = 0

class Blocks(pygame.sprite.Sprite):
    '''This class is the parent class of all moving background blocks'''
    def __init__(self, pos):
        '''This method initiates the class'''
        pygame.sprite.Sprite.__init__(self)
        
        # Set Variables
        self.__position = pos
        
        self.__displacement = 0
        self.__dx = 0
        self.__differ = 0
        
    def start(self, direction, playerPos):
        '''This method sets .__dx variable when the player is confirmed to be 
        ready'''
        # Checks if player is on the same place horizontally
        if self.rect.bottom - 5 >= playerPos[2] and self.rect.top + 5  <= playerPos[3]:
            if direction == 'right':
                # Checks if player is on the same place vertically
                # If it is close, keeps the player from walking into the block from the left
                if self.rect.left - 10 < playerPos[1] and self.rect.right > 338:
                    self.__dx = playerPos[1]- self.rect.left
                # If the player is not near by, walk normally
                else:
                    self.__dx = -5
            elif direction == 'left':
                # Checks if player is on the same place vertically
                # If it is close, keeps the player from walking into the block from the right
                if self.rect.right + 10 > playerPos[0] and self.rect.left < 302:
                    self.__dx = playerPos[0]-self.rect.right
                # If player is not near by, walk normally
                else:
                    self.__dx = 5
            # If in a standstill, sprite stops
            else:
                self.__dx = 0
        # If the player is not in the same horizontal section, walk normally
        else: 
            if direction == 'right':
                self.__dx = -5
            else:
                self.__dx = 5
        
        # Returns dx to be compared with the other platforms and walls
        return self.__dx
    
    def changedx(self, dx):
        '''This method changes .__dx to mimic the others'''
        self.__dx = dx
        
    def reset(self):
        '''This method resets the block in its original position'''
        self.rect.left = self.__position[0]
        self.rect.top = self.__position[1]
        self.__dx = 0
    
    def stop(self):
        '''This method stops the map movement when the player hits a wall'''
        self.__dx = 0
    
    def recenter(self, differ, displacement):
        '''This method makes up for the displacement of the player from the
        horizontal center'''
        self.__displacement = displacement
        # Differ keeps all the player at the same place
        self.__differ = differ - 2
        self.__dx += displacement
    
    def update(self):
        '''This method updates the sprite'''
        self.rect.centerx += self.__dx-self.__differ*2 
        self.__differ = 0
        self.__dx -= self.__displacement
        
class Platform(Blocks):
    '''This class creates platforms for the player to jump on'''
    def __init__(self, size, pos):
        '''This method initiates the class'''
        # Uses Block's methods and variables
        Blocks.__init__(self, pos)
        
        # Uploads big platform
        self.__bigImage = pygame.image.load('Others/Platform.png')
        
        # Creates surface
        self.image = pygame.Surface((50*size, 50))
        self.image = self.image.convert()
        self.image.fill((100, 100, 100))
        # Blits big platform on image surface to create the right size
        self.image.blit(self.__bigImage, (0, 0))
        self.image.set_colorkey((100, 100, 100))
        
        # Creates rect
        self.rect = self.image.get_rect()
        
        self.reset()

class Wall(Blocks):
    '''This class creates a wall, forcing the player to teleport'''
    def __init__(self, size, pos, screen):
        '''This initiates the class'''
        Blocks.__init__(self, pos)
        
        # Uploads big wall photo
        self.__colour = pygame.image.load('Others/Wall.png')
        
        # Creates surface with correct criteria
        self.image = pygame.Surface((50*size, screen.get_height() + 10))
        self.image = self.image.convert()
        
        # Blits big wall photo onto the surface to fit the size
        self.image.blit(self.__colour, (0, 0))
        
        # Creates self.rect
        self.rect = self.image.get_rect()
        
        self.reset()

class Light(Blocks):
    '''This class gives the player extra energy to continue teleporting and a
    life if they have a full energy bar'''
    def __init__(self, pos):
        '''This function initiates the class and creates the light'''
        Blocks.__init__(self, pos)
        
        # Uploads all light sprites
        self.__lightSprites = []
        for light in range(4):
            self.__lightSprites.append(pygame.image.load('Light/light'+str(light)+ '.png'))
        
        # Creates self.image
        self.image = self.__lightSprites[0]
        self.rect = self.image.get_rect()
        
        # Creates variables
        self.__reverseSprites = False
        self.__spriteNumber = 0
        self.__position = pos
        self.__valid = True
        self.__displacement = 0
        self.__dx = 0
        self.__differ = 0
        
        self.reset()
        
    def start(self, direction, playerPos):
        '''This method sets .__dx variable when the player is confirmed to be 
        ready'''
        # See blocks for description
        if self.rect.bottom - 5 >= playerPos[2] and self.rect.top + 5  <= playerPos[3]:
            if direction == 'right':
                if self.rect.left - 10 < playerPos[1] and self.rect.right > 338:
                    self.__dx = playerPos[1]- self.rect.left
                else:
                    self.__dx = -5
            elif direction == 'left':
                if self.rect.right + 8 > playerPos[0] and self.rect.left < 302:
                    self.__dx = playerPos[0]-self.rect.right
                else:
                    self.__dx = 5
            else:
                self.__dx = 0
        else: 
            if direction == 'right':
                self.__dx = -5
            else:
                self.__dx = 5
                
        return self.__dx
    
    def changedx(self, dx):
        '''This method changes .__dx to mimic the others'''
        self.__dx = dx
        
    def stop(self):
        '''This method stops the map movement when the player hits a wall'''
        self.__dx = 0
    
    def recenter(self, differ, displacement):
        '''This method makes up for the displacement of the player from the
        horizontal center'''
        self.__displacement = displacement
        self.__differ = differ - 2
        self.__dx += displacement 
        
    def remove(self):
        '''This method temporarily delete the light'''
        self.image = self.__lightSprites[3]
        self.__valid = False
    
    def reset(self):
        '''This method resets the block in its original position'''
        self.rect.left = self.__position[0]
        self.rect.top = self.__position[1]
        self.__dx = 0
        
        self.image = self.__lightSprites[0]
        self.__valid = True
    
    def getValid(self):
        '''This method returns the valid variable'''
        return self.__valid
    
    def update(self):
        '''This method updates the sprite'''
        self.rect.centerx += self.__dx-self.__differ*2 
        self.__differ = 0
        self.__dx -= self.__displacement    
        
        # Checks if light is valid; if yes, start animation
        if self.__valid:
            self.image = self.__lightSprites[int(self.__spriteNumber)]
            if self.__reverseSprites:
                self.__spriteNumber -= 0.2
                if self.__spriteNumber <= 0:
                    self.__reverseSprites = False
                    
            # Reverses animation
            else:
                self.__spriteNumber += 0.2
                if self.__spriteNumber >= (len(self.__lightSprites) - 1):
                    self.__reverseSprites = True
        
class Wolf(Blocks):
    '''This class creates a wolf that runs on a platform back and forth: poses 
    as an obstacle so that the Player has to be wary if they want to go on the 
    platform. Touching the sprite will lead to a death.'''
    def __init__(self, pos, platform):
        '''This method initiates the class; placing it on the map on the correct 
        platform.'''
        Blocks.__init__(self, pos)
        
        # Uploads Wolf biting sprites looking left
        self.__biteL = []
        for sprite in range(6):
            self.__biteL.append(pygame.image.load('Wolf/Left/bite' + str(sprite) + '.png'))
        
        # Uploads Wolf biting sprites looking right
        self.__biteR = []
        for sprite in range(6):
            self.__biteR.append(pygame.image.load('Wolf/Right/bite' + str(sprite) + '.png'))
        
        # Uploads Wolf walk animation looking left
        self.__walkL = []
        for sprite in range(4):
            self.__walkL.append(pygame.image.load('Wolf/Left/walk' + str(sprite) + '.png'))
        
        # Uploads Wolf walk animation looking right
        self.__walkR = []
        for sprite in range(4):
            self.__walkR.append(pygame.image.load('Wolf/Right/walk' + str(sprite) + '.png'))
        
        # Upload's Wolf's normal face
        self.__faceL = pygame.image.load('Wolf/Left/face.png')
        self.__faceR = pygame.image.load('Wolf/Right/face.png')
        
        # Start with normal walking animation
        self.image = self.__walkR[0]
        
        # Blits face onto body
        self.image.blit(self.__faceR, (0, 0))
        self.image = self.image.convert()
        
        # Takes down the platform it is on
        self.__platform = platform
        self.rect = self.image.get_rect()
        
        # Set Variables
        self.__direction = 'right'
        self.__legSpriteNumber = 0
        self.__faceSpriteNumber = 0
        self.__playerNearby = False
        self.__dx = 6
        
        self.__position = pos
        
        self.__displacement = 0
        self.__changedx = 0
        self.__differ = 0
        
        self.reset()
    
    def getPlatform(self):
        '''This method returns what platform the wolf is on'''
        return self.__platform
    
    def walk(self, edge):
        '''This method makes sure the wolf moves around and turns after reaching 
        the edge of the platform.'''
        # Checks for edges
        if self.__direction == 'right':
            if self.rect.right >= edge[1]:
                self.__dx -= 10
                self.rect.right = edge[1] - 1
                self.__direction = 'left'
        else:
            if self.rect.left <= edge[0]:
                self.__dx += 10
                self.rect.left = edge[0] + 1
                self.__direction = 'right'

    def start(self, direction, playerPos):
        '''This method sets .__dx variable when the player is confirmed to be 
        ready'''
        # See Blocks explanation
        if self.rect.bottom - 5 >= playerPos[2] and self.rect.top + 5  <= playerPos[3]:
            if direction == 'right':
                if self.rect.left - 100 < playerPos[1] and self.rect.right > 338:
                    self.__playerNearby = True
                else:
                    self.__playerNearby = False
            elif direction == 'left':
                if self.rect.right + 100 > playerPos[0] and self.rect.left < 302:
                    self.__playerNearby = True
                else:
                    self.__playerNearby = False
            else:
                self.__changedx = 0

        if direction == 'right':
            self.__changedx = -5
        else:
            self.__changedx = 5
                
        return self.__changedx
    
    def changedx(self, dx):
        '''This method changes .__dx to mimic the others'''
        self.__changedx = dx
        self.__dx += dx
        
    def reset(self):
        '''This method resets the block in its original position'''
        self.rect.left = self.__position[0]
        self.rect.top = self.__position[1]
        self.__dx = 5
    
    def stop(self):
        '''This method stops the map movement when the player hits a wall'''
        if self.__direction == 'right':
            self.__dx = 3
        
        else:
            self.__dx = -3
    
    def recenter(self, differ, displacement):
        '''This method makes up for the displacement of the player from the
        horizontal center'''
        self.__displacement = displacement
        self.__differ = differ -2
        self.__dx += displacement
    
    def update(self):
        '''This method updates the sprite'''
        # Fills image to reset it
        self.image.fill((113, 113, 113))
        
        # Slows down animation
        self.__legSpriteNumber += 0.2
        if self.__legSpriteNumber >= 4:
            self.__legSpriteNumber = 0
            
        # Depending on direction, change the face and body
        if self.__direction == 'right':
            if self.__playerNearby:
                self.image.blit(self.__biteR[int(self.__faceSpriteNumber)], (0, 0))
                self.__faceSpriteNumber += 0.5
                if self.__faceSpriteNumber >= 6:
                    self.__faceSpriteNumber = 0
            else:
                self.image.blit(self.__faceR, (0, 0))
            self.image.blit(self.__walkR[int(self.__legSpriteNumber)], (0, 0))
        
        else:
            if self.__playerNearby:
                self.image.blit(self.__biteL[int(self.__faceSpriteNumber)], (0, 0))
                self.__faceSpriteNumber += 0.2
                if self.__faceSpriteNumber >= 6:
                    self.__faceSpriteNumber = 0            
            else:
                self.image.blit(self.__faceL, (0, 0))
            self.image.blit(self.__walkL[int(self.__legSpriteNumber)], (0, 0))
        
        # Set colorkey
        self.image.set_colorkey((113, 113, 113))
        
        # Reposition sprite
        self.rect.centerx += self.__dx-self.__differ*2 
        self.__differ = 0
        self.__dx -= self.__displacement
        self.__dx -= self.__changedx
        self.__changedx = 0

class Background(pygame.sprite.Sprite):
    '''This class creates creates the background'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        # Sets image
        self.image = pygame.image.load('Others/background.png')
        self.image = self.image.convert()
        
        # Sets rect
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        
        # Sets Variables
        self.__displacement = 0
        self.__dx = 0
        self.__differ = 0
    
    def changedx(self, dx):
        '''This method changes .__dx to mimic the others'''
        # Slows down moving background
        if dx > 0:
            self.__dx = dx - 3
        elif dx < 0:
            self.__dx = dx + 3
        else:
            self.__dx = dx
        
    def reset(self):
        '''This method resets the block in its original position'''
        self.rect.left = 0
        self.rect.top = 0
        self.__dx = 0
    
    def stop(self):
        '''This method stops the map movement when the player hits a wall'''
        self.__dx = 0
    
    def recenter(self, differ, displacement):
        '''This method makes up for the displacement of the player from the
        horizontal center'''
        self.__displacement = displacement
        self.__differ = differ - 2
        self.__dx += displacement
    
    def update(self):
        '''This method updates the sprite'''
        self.rect.centerx += self.__dx-self.__differ*2 
        self.__differ = 0
        self.__dx -= self.__displacement
        
class EnergyBar(pygame.sprite.Sprite):
    '''This class keeps track of the energy used by the player'''
    def __init__(self, screen):
        '''This method initiates the object: it begins with a full bar: with 
        each teleport, 1/3 of the bar disappears and unless you have 1/3 of the 
        bar full, the player will be unable to teleport.'''
        pygame.sprite.Sprite.__init__(self)
        
        # Creates border sprite for energy bar
        self.__border = pygame.image.load('Others/EnergyBar.png') 
        
        # Sets Variables
        self.__screen = screen
        self.__energyLeft = 198
        self.update()
    
    def teleported(self):
        '''This method removes 1/3 of the energy bar after teleporting, returns 
        true or false depending if the player has enough energy to teleport'''
        # Drains energy so that player cannot teleport unless player has 1/2 of the energy bar
        if self.__energyLeft >= 99:
            self.__energyLeft -= 99
            return True
        else:
            return False
    
    def reset(self):
        '''This method resets the bar when the player dies so that it is back to 
        full or when they hit a light'''
        self.__energyLeft = 198
        
    def regenerate(self, standing):
        '''This method adds 1 energy every frame'''
        if self.__energyLeft < 198:
            # Regenerates the energy bar quicker while standing
            if standing:
                self.__energyLeft += 1.5
            self.__energyLeft += 1
    
    def isMax(self):
        '''This method returns True or False according to the ammount of energy
        the amount of energy left; to check if the player can get another life 
        after hitting a light'''
        if self.__energyLeft == 198:
            return True
        else:
            return False
    
    def update(self):
        '''This method updates the energy bar; recreates the self.image attribute
        and self.rect attribute'''
        # Creates surface
        self.image = pygame.Surface((254, 56))
        
        # Takes energy Left and fills the bar for how much is left
        self.__energy = pygame.Surface((int(self.__energyLeft), 56))
        self.__energy.fill((68, 159, 229))
        
        # Blits border onto the image/bar
        self.image.blit(self.__energy, (48, 0))
        self.image.blit(self.__border, (0, 0))
        self.rect = self.image.get_rect()
        
        self.rect.centery = 30
        self.rect.centerx = self.__screen.get_width()/2 +10
        
class LifeCounter(pygame.sprite.Sprite):
    '''This class keeps track of the amount of lives the player has left'''
    def __init__(self, screen):
        '''This method initiates the life counter class: the starting amount of 
        lives is 5: when the energy bar is full and the player touches a light,
        they gain a life.'''
        pygame.sprite.Sprite.__init__(self)
        
        # Loads fonts
        self.__font = pygame.font.Font('BebasNeue Regular.ttf', 20)
        self.__border = pygame.image.load('Others/lifeBar.png')
        
        # Sets variables
        self.__screen = screen
        self.__lives = 5
        
        self.update()
        
    def died(self):
        '''This method removes a life from the __lives variable when the player 
        dies'''
        self.__lives -= 1
    
    def gainLife(self):
        '''This method adds a life to __lives variable when the player collects 
        a light while at ful energy'''
        self.__lives += 1
    
    def getLives(self):
        '''This method returns the number of lives the player has left; 
        self.__lives variable'''
        return self.__lives
    
    def reset(self):
        '''This method resets the amount of lives after playing the tutorial and
        moving on to the main game'''
        self.__lives = 5
    
    def update(self):
        '''This method updates the visual so that the player can see how many
        lives they have left'''
        # Creates surface
        self.image = pygame.Surface((254, 30))
        self.image.convert()
        self.image.fill((0, 0, 0))
        
        # fills in the hearts of the life counter
        self.__life = pygame.Surface((17 + 27*(self.__lives), 30))
        self.__life.fill((229, 68, 68)) 
        
        # Buts the border and life
        self.image.blit(self.__life, (0, 0))
        self.image.blit(self.__border, (0, 0))
        
        # If player has more than 5 lives, add a '+ x' lives
        if self.__lives > 5:
            self.__extraLives = self.__font.render('+ ' + str(self.__lives - 5), 1, (0, 0, 0))         
            self.image.blit(self.__extraLives, (160, 5))
        
        self.rect = self.image.get_rect()
        
        self.rect.centerx = self.__screen.get_width()/2 +10
        self.rect.centery = 70

class EndZone(Blocks):
    '''This class creates the endzone of the game'''
    def __init__(self, pos):
        '''This method initiates the class and sets the position'''
        Blocks.__init__(self, pos)
        
        self.image = pygame.Surface((400, 700))
        self.image = self.image.convert()
        
        self.rect = self.image.get_rect()
        
        self.reset()

class Timer(pygame.sprite.Sprite):
    '''This class keeps track of how much time had passed since the Player made 
    theer first move up to the time the player completed them.'''
    def __init__(self):
        '''This method initiates the function'''
        pygame.sprite.Sprite.__init__(self)
        
        # Loads font
        self.__font = pygame.font.Font('BebasNeue Regular.ttf', 40)
        
        # Sets variables
        self.__seconds = 0
        self.__frames = 0
        self.__start = False
        
    def start(self):
        '''This method signals the start of the timer'''
        self.__start = True
    
    def stop(self):
        '''This method signals when the timer should stop'''
        self.__start = False
    
    def getTime(self):
        '''This method returns the player's new time appon completing a level'''
        return self.__seconds
    
    def update(self):
        '''This method updates the timer'''
        # When player starts moving, begin the timer
        if self.__start:
            self.__frames += 1
        
        # Every 30 frames add a second
        if self.__frames == 30:
            self.__seconds += 1
            self.__frames = 0
        
        # If seconds are single digits after taking away the minutes
        if self.__seconds - (int(self.__seconds/60)*60) < 10:
            self.image = self.__font.render('Run Time: ' + str(self.__seconds/60) + ':0' + str(self.__seconds - (int(self.__seconds/60)*60)), 1, (255, 255, 255))
        
        # If seconds are double digits after taking away the minutes
        else:
            self.image = self.__font.render('Run Time: ' + str(self.__seconds/60) + ':' + str(self.__seconds - (int(self.__seconds/60)*60)), 1, (255, 255, 255))
        
        self.rect = self.image.get_rect()
        
        self.rect.left = 10
        self.rect.top = 10

class PastTimesKeeper(pygame.sprite.Sprite):
    '''This class displays the best time of each level to the player'''
    def __init__(self, level, menu):
        '''This method initiates the sprite, taking the currect level and 
        finding its best time to display'''
        pygame.sprite.Sprite.__init__(self)
        
        # Loads fonts for different sizes
        self.__fonts = []
        for size in (16, 24, 40):
            self.__fonts.append(pygame.font.Font('BebasNeue Regular.ttf', size))
        
        # If this is called from the menu; do this
        if menu:
            # Creates Surface
            self.image = pygame.Surface((640, 1000))
            self.image = self.image.convert()
            self.rect = self.image.get_rect()
            
            # Creates mapTimes list
            self.__mapTimes = []
            
            # There are 3 maps; this reads the files of times for each level
            for map in range(3):
                infile = open('times/map' + str(map) + '.txt', 'r')
                line = infile.readline().strip()
                times = line.split(' ')
                
                # If the file is empty change it into a blank time slot (--:--)
                if times[0] == '':
                    times[0] = '--:--'                
                
                # Changes all the number strings into integers
                for index in range(len(times)):
                    try:
                        times[index] = int(times[index])
                    except ValueError:
                        pass
                
                # Sorts numbers
                times.sort()
                
                # See how many empty times slots there are
                emptyTimes = 10 - len(times)
                
                # Add an blank time slot
                if emptyTimes > 0:
                    for time in range(emptyTimes):
                        times.append('--:--')
                
                # Adds times list to mapTimes list
                self.__mapTimes.append(times)
                
                # Closes file
                infile.close()
            
            # Blits HIGH SCORE
            self.image.blit((self.__fonts[2].render('HIGH SCORES', 1, (255, 255, 255))), (10, 10))
            
            # For each level, create a tab
            for level in range(3):
                
                # Prints 'MAP. level'
                self.image.blit((self.__fonts[1].render('MAP' + str(level + 1), 1, (255, 255 ,255))), (30, 50 + 85*level))
                
                # Takes the top 10 times
                for number in range(10):
                    
                    # If the slot isn't blank; write each time
                    if not (self.__mapTimes[level][number]  == '--:--'):
                        
                        # If seconds without minutes is single digit
                        if self.__mapTimes[level][number] - int(self.__mapTimes[level][number]/60) * 60 >10:
                            cell = self.__fonts[0].render(str(number+1) + '. ' + str(self.__mapTimes[level][number]/60) + ':' + str(self.__mapTimes[level][number] - int(self.__mapTimes[level][number])/60*60), 1, (255, 255, 255))
                            
                        # Otherwise:
                        else: 
                            cell = self.__fonts[0].render(str(number+1) + '. ' + str(self.__mapTimes[level][number]/60) + ':0' + str(self.__mapTimes[level][number] - int(self.__mapTimes[level][number]/60)*60), 1, (255, 255, 255))
                    
                    # If the slot is empty
                    else:
                        cell = self.__fonts[0].render(str(number+1) + '. --:--', 1, (255, 255, 255))
                    
                    # if the cell is 5 or below it belongs in the first row
                    if number <= 4:
                        self.image.blit(cell, (40 + 112*number, 50 + 85*level + 30*(int(number/5)+1)))
                        
                    # If 6-10, the cell belongs to the second row
                    else:
                        self.image.blit(cell, (40 + 112*(number-5), 50 + 85*level + 30*(int(number/5)+1)))
            
            # Set colorkey
            self.image.set_colorkey((0, 0, 0))
                    
            self.__dx = 0
            
        # If it is not part of the menu
        else:
            self.changeLevel(level)
        
        # Sets variables
        self.__menu = menu
        
        self.update()
        
    def newTime(self, level, time):
        '''This method appends to the files of each map'''
        infile = open('times/map' + str(level) + '.txt', 'a')
        infile.write(str(time) + ' ')
        infile.close()
        
    def changeLevel(self, level):
        '''This method changes the best time reference level'''
        
        # Opens file
        infile = open('times/map'+str(level)+'.txt', 'r')
        
        line = infile.readline().strip()
        times = line.split(' ')
        
        # If the file is empty create an empty slot
        if times[0] == '':
            times[0] = '--:--'
        
        # Changes all number strings into integers
        for index in range(len(times)):
            try:
                times[index] = int(times[index])
            except ValueError:
                pass
        
        # Sort numbers
        times.sort()        
        
        # If the quickest time is not an empty cell
        if not(times[0] == '--:--'):
            self.__bestTime = times[0]
        else:
            self.__bestTime = '--:--'
               
        infile.close()
    
    def stop(self):
        '''This method stops the scrolling'''
        self.__dx = 0
        
    def scroll(self, direction):
        '''This method scrolls the sprite; up and down'''
        if direction == 'up':
            if self.rect.top > 0:
                self.__dx = -5
        else:
            if self.rect.bottom < 1000:
                self.__dx = 5
                
    def update(self):
        '''This method appends to the files of each map'''
        # If it is not in the menu; display the best time while the player is in game
        if not self.__menu:
            if not(self.__bestTime == '--:--'):
                self.image = self.__fonts[2].render('Best Time: ' + str(self.__bestTime/60) + ':' + str(self.__bestTime - (self.__bestTime/60*60)), 1, (255, 255, 255))
            else:
                self.image = self.__fonts[2].render('Best Time: --:--', 1, (255, 255, 255))
            self.rect = self.image.get_rect()
            
            self.rect.left = 10
            self.rect.top = 60
