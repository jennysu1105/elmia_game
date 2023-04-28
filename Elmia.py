'''Author: Jenny Su
Date: May 26 2018
Description: The main module that runs the program for "Elmia"
             May 5:   Coded Player Class, Fairy Class; made sure that the teleport,
                      fall and recenter methods worked. Took out the recenter 
                      methods for now and replaced it with controllable movements
             May 9:   Coded Platform Class and Wall Class; Player cannot go 
                      through sides and top from walking
             May 15:  Coded Energy Bar Class and Life Class; Player cannot 
                      infinitely teleport
             May 17:  Graphics Update
             May 26:  Coded Timer. Started coding Menu.
             May 28:  Coded PastTimeKeeper; made sure high score tab works and 
                      best score display in main game works. Creating first map.'''

import pygame, mySprites, menuSprites
pygame.init()

def endGameScreen(screen, background, finishedGame):
    '''This function shows the end game screen; if the player finish'''
    # Entities
    # Music
    # If the game was not finished; when the player loses all their lives
    #  play this music
    if not finishedGame:
        pygame.mixer.music.load('sound/[MapleStory BGM] Ellinel The Fairy Forest (KMST 1.2.477).mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1) 
    
    # Otherwise, the player finished; play this music
    else:
        pygame.mixer.music.load('sound/Tokyo Ghoul  OST - Nine[Full].mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)         
    
    # Objects
    titleBack = menuSprites.Background(False)
    titleBack.image.blit(pygame.image.load('EndGameScreen/Game Over.png'), (0, 0))
    
    backToTitle = menuSprites.GameButton(screen, False, 'BackToTitleScreen')
    exitGame = menuSprites.GameButton(screen, False, 'ExitGame')
    
    # Create groups
    buttonGroup = pygame.sprite.Group(backToTitle, exitGame)
    allSprites = pygame.sprite.OrderedUpdates(titleBack, buttonGroup)
    
    # Assign
    toMenu = False
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Loop
    while keepGoing:
     
        # Time
        clock.tick(30)
        
        # Events
        # Checks if the mouse is hovering a button
        buttonHovering = 'None'
        for button in buttonGroup:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.hover(True)
                buttonHovering = button.getFunction()
            else:
                button.hover(False)
        
        # Key Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False        
            
            if event.type == pygame.MOUSEBUTTONUP:
                if not (buttonHovering == 'None'):
                    if buttonHovering == 'BackToTitleScreen':
                        toMenu = True
                    
                    elif buttonHovering == 'exitGame':
                        toMenu = False
                    
                    keepGoing = False

        # Refresh Screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
     
        pygame.display.flip()    
    
    # If toMenu is true, it returns the player back to the title screen
    return keepGoing, toMenu

def tutorialGuide(textNumber, screen, wallList, wolfList, lightList, text):
    '''This function provides the tutorial round guidlines'''
    # Checks which step of the tutorial the player is on; textNumber makes sure
    # each text is displayed once
    if textNumber == 0:
        if wallList[1].rect.left < screen.get_width():
            textNumber += 1
            text.nextText()
    elif textNumber == 1:
        if lightList[0].rect.left +10 < screen.get_width():
            textNumber += 1
            text.nextText()
    elif textNumber == 2:
        if lightList[2].rect.left + 50 < screen.get_width():
            textNumber += 1
            text.nextText()
    elif textNumber == 3:
        if wolfList[0].rect.left + 50 < screen.get_width():
            textNumber += 1
            text.nextText()  
    return textNumber

def changeMap(level, screen):
    '''This function changes the map'''
    # Open file
    infile = open('mapData/map' + str(level) + '.txt', 'r')
    # Unique Objects
    backgroundImage = mySprites.Background()
    player = mySprites.Player(screen)
    teleportAnimation = mySprites.TeleportSprites()
    pix = mySprites.Fairy()
    energyBar = mySprites.EnergyBar(screen)
    timer = mySprites.Timer()
    bestTime = mySprites.PastTimesKeeper(level, False)
    
    # Reads the first line of file giving the End Zone's coordinates
    line = infile.readline().strip()
    lineSplit = line.split(' ')
    
    endZone = mySprites.EndZone((int(lineSplit[0]), int(lineSplit[1])))
    
    # Reads the second line of file giving the End Zone Wall's coordinates.
    # Makes it so that the player can walk through the wall to reach the end zone
    line = infile.readline().strip()
    lineSplit = line.split(' ')
    
    endZoneWall = mySprites.Wall(int(lineSplit[0]), (int(lineSplit[1]), int(lineSplit[2])), screen)
    
    # Reads the third line of file giving the Platforms' size and location
    line = infile.readline().strip()
    firstSplit = line.split(',')
    
    platformProp = []
    for index in range(len(firstSplit)):
        platformProp.append(firstSplit[index].split(' '))
        
    platformList = []
    for platforms in range(len(platformProp)):
        platform = mySprites.Platform(int(platformProp[platforms][0]), (int(platformProp[platforms][1]), screen.get_height() - int(platformProp[platforms][2])))
        platformList.append(platform)
        
    platformGroup = pygame.sprite.Group(platformList)
    
    # Reads the fourth line of file giving the Walls' size and location
    line = infile.readline().strip()
    firstSplit = line.split(',')
    
    wallProp = []
    for index in range(len(firstSplit)):
        wallProp.append(firstSplit[index].split(' '))
        
    wallList = []
    for walls in range(len(wallProp)):
        wall = mySprites.Wall(int(wallProp[walls][0]), (int(wallProp[walls][1]), int(wallProp[walls][2])), screen)
        wallList.append(wall)
        
    wallGroup = pygame.sprite.Group(wallList)
    
    # Reads the fifth line of file giving the Lights' coordinates
    line = infile.readline().strip()
    firstSplit = line.split(',')
    
    lightPositions = []
    
    for index in range(len(firstSplit)):
        lightPositions.append(firstSplit[index].split(' '))    
        
    lightList = []
    
    for lights in range(len(lightPositions)):
        light = mySprites.Light((int(lightPositions[lights][0]), screen.get_height() - int(lightPositions[lights][1])))
        lightList.append(light) 
    
    lightGroup = pygame.sprite.Group(lightList)
    
    # Reads the sixth line of the file giving the Wolfs' coordinates and platform
    line = infile.readline().strip()
    firstSplit = line.split(',')
    
    wolfProp = []
    for index in range(len(firstSplit)):
        wolfProp.append(firstSplit[index].split(' '))    
        
    wolfList = []
    for wolves in range(len(wolfProp)):
        wolf = mySprites.Wolf((int(wolfProp[wolves][0]), screen.get_height() - int(wolfProp[wolves][1])), int(wolfProp[wolves][2]))
        wolfList.append(wolf)
        
    wolfGroup = pygame.sprite.Group(wolfList)
    
    infile.close()
    # Group Bundles
    blocksGroup = pygame.sprite.OrderedUpdates(platformGroup, wallGroup, wolfGroup)
    
    allMovingSprites = pygame.sprite.Group(blocksGroup, lightGroup, endZoneWall)
    
    allSprites = pygame.sprite.OrderedUpdates(endZone, backgroundImage, blocksGroup, player, teleportAnimation, lightGroup, pix, endZoneWall, energyBar, timer, bestTime)   
    
    # Returns all Groups and lists
    return backgroundImage, player, teleportAnimation, pix, energyBar, timer, bestTime, endZone, platformList, platformGroup, wallList, wallGroup, lightList, lightGroup, wolfList, wolfGroup, blocksGroup, allMovingSprites, allSprites
    
def mainGame(screen, background, tutorial):
    '''This function plays the game'''
    # Entities  
    # Checks if it is the tutorial; if yes, set up the buttons that will guide them
    if tutorial:
        level = 0
        buttonA = menuSprites.TutorialButtons('A', screen)
        buttonD = menuSprites.TutorialButtons('D', screen)
        buttonSPACE = menuSprites.TutorialButtons('SPACE', screen)
        text = menuSprites.TutorialText()  
        textNumber = 0
        
    else:
        level = 1    
    
    # Calls function to create map and set Group variables
    backgroundImage, player, teleportAnimation, pix, energyBar, timer, bestTime, endZone, platformList, platformGroup, wallList, wallGroup, lightList, lightGroup, wolfList, wolfGroup, blocksGroup, allMovingSprites, allSprites = changeMap(level, screen)
    
    # Checks if it is a tutorial and add the buttons to allSprites
    if tutorial:
        allSprites.add(buttonA, buttonD, buttonSPACE, text)
    
    # Creates the lifeCounter and adds it to allSprites
    lifeCounter = mySprites.LifeCounter(screen)
    allSprites.add(lifeCounter)
    
    # Music
    pygame.mixer.music.load('sound/Ori and the Blind Forest OST - 18 - The Waters Cleansed (feat. Tom Boyd).mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)  
    
    # Sound Effects
    magicSounds = []
    for sound in range(3):
        sound = pygame.mixer.Sound('sound/soundEffects/Magic' + str(sound) + '.wav')
        sound.set_volume(0.5)
        magicSounds.append(sound)
    
    footsteps = pygame.mixer.Sound('sound/soundEffects/Walking on grass (sound effect).wav')
    footsteps.set_volume(0.1)
    
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Checks if player would like a tutorial
    # Necessary check variables
    #  Keeps track of keys going down or if key goes up
    keydown = [False, 'none']
    #  Keeps platforms moving together
    platformdx = 5
    individualdx = 0
    #  Check is the player is centered on the map
    notCentered = False
    #  Checks if the player has enough energy to teleport
    canTeleport = True
    teleported = False
    
    #  Controls how far to quit
    toMenu = True
    
    # Loop
    while keepGoing:
     
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                # Starts the timer
                timer.start()
                # Teleports player to fairy
                if event.key == pygame.K_SPACE:
                    canTeleport = energyBar.teleported()
                    if canTeleport:
                        differ = player.teleport((pix.rect.centerx, pix.rect.bottom))
                        # Plays teleport sound effect
                        magicSounds[1].play()
                        # Starts animation
                        teleportAnimation.getPlayerPosition(player.getPosition())
                        teleported = True
                    falling = True
                    keydown = [False, 'space']
                    notCentered = True  
                    if tutorial:
                        buttonSPACE.pressed(True)    
                # Walks right; changes keydown
                elif event.key == pygame.K_d:
                    keydown = [True, 'd']
                    if tutorial:
                        buttonD.pressed(True)
                # Walks left
                elif event.key == pygame.K_a:
                    keydown = [True, 'a']  
                    if tutorial:
                        buttonA.pressed(True)
                # Checks if escape key was pressed, if yes, it returns to a menu        
                elif event.key == pygame.K_ESCAPE:
                    toMenu = True
                    keepGoing = False
            # Otherwise, if the escape key is not pressed, the game exits comepletely
            elif event.type == pygame.QUIT:
                toMenu = False
                keepGoing = False
            # Moves Pix    
            elif event.type == pygame.MOUSEMOTION:
                pix.move()
                
            elif event.type == pygame.KEYUP:
                # Stops player
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    keydown = [False, 'up']
                    # Checks if it is a tutorial, if yes, it will fill show that
                    # the player pressed the button on screen
                    if tutorial:
                        if event.key == pygame.K_d:
                            buttonD.pressed(False)
                        else:
                            buttonA.pressed(False)
                elif event.key == pygame.K_SPACE:
                    if tutorial:
                        buttonSPACE.pressed(False)
        
        # Updates tutorial text
        if tutorial:
            textNumber = tutorialGuide(textNumber, screen, wallList, wolfList, lightList, text)
            
        # Checks if a key is being held down                                
        if keydown[0]:
            # When player wants to move right
            if keydown[1] == 'd':
                platformdx = -5
                player.move('right')
                # Checks if player bumps into a wall from the side
                for block in blocksGroup:
                    individualdx = block.start('right', player.getPosition())
                    if individualdx > platformdx:
                        platformdx = individualdx
                        
            # When player wants to move left            
            if keydown[1] == 'a':
                platformdx = 5
                player.move('left')
                # Checks if player bumps into a wall from the side
                for block in blocksGroup:
                    individualdx = block.start('left', player.getPosition())
                    if individualdx < platformdx:
                        platformdx = individualdx 
            # Plays footstep sound effect if player in not falling            
            if not player.isFalling():       
                footsteps.play(-1)
            else:
                # Otherwise, stop the sound
                footsteps.stop()
            
            # Changes all platform dx so that all platforms are moving the same 
            # time and distance
            for block in allMovingSprites:
                block.changedx(platformdx)
            backgroundImage.changedx(platformdx)
            endZone.changedx(platformdx)
        
        # Otherwise, a key isn't held down, but if there is another action 
        # happening, it goes here
        
        else:
            # Resets the map after a death
            if keydown[1] == 'collide':
                for block in allMovingSprites:
                    block.reset()   
                player.reset()
                backgroundImage.reset()
                endZone.reset()
                energyBar.reset()
                if not tutorial:
                    lifeCounter.died()
                keydown = [False, 'reseted']
                
            # Stops all movement of objects in allMovingSprites class
            else:
                footsteps.stop()
                for block in allMovingSprites:
                    block.stop()
                backgroundImage.stop()
                endZone.stop()
                player.stop()
        
        # Plays animation once player teleported
        if teleported:
            if teleportAnimation.getAnimationStat():
                teleportAnimation.getPlayerPosition(player.getPosition())
            else:
                teleported = False
            
        # Controls player's fall method        
        falling = False
        platformUnder = False
        for platform in platformGroup:
            position = player.getPosition()
            if platform.rect.left < position[1] and platform.rect.right > position[0]:
                falling = player.fall(platform.rect.top)
                platformUnder = True
                break
                
        if not platformUnder:
            player.fall(screen.get_height()+80)
        
        # Controls recenter methods for all objects with the method
        if notCentered:
            dx = player.recenter()
            
            for block in allMovingSprites:
                block.recenter(differ, dx)
            backgroundImage.recenter(differ, dx)
            endZone.recenter(differ, dx)
                
            if dx == 0:
                notCentered = False
            
            differ = 0
        
        # Collision Detection
        if pygame.sprite.spritecollide(player, blocksGroup, False) or position[2] + 2 >= screen.get_height():
            keydown = [False, 'collide']
            if tutorial:
                text.reset()
        
        if lifeCounter.getLives() == 0:
            keepGoing, toMenu = endGameScreen(screen, background, False)
                
        for light in pygame.sprite.spritecollide(player, lightGroup, False):
            # Checks if light is valid
            if light.getValid():
                magicSounds[0].play()
                light.remove()
                if energyBar.isMax():
                    lifeCounter.gainLife()
                energyBar.reset()
        
        # Regenerates energy bar slowly
        energyBar.regenerate(not falling)
        for wolf in wolfGroup:
            wolf.walk((platformList[wolf.getPlatform()].rect.left, platformList[wolf.getPlatform()].rect.right)) 
        
        # Checks if player reached the end zone
        if player.rect.colliderect(endZone.rect):
            # Plays level finish sound effect
            magicSounds[2].play()
            # Stops timer
            timer.stop()
            # Records map time
            bestTime.newTime(level, timer.getTime())
            # Stops footstep sound
            footsteps.stop()
            
            # If it is tutorial reset the life counter
            if tutorial:
                lifeCounter.reset()
            
            # Adds to the level
            level += 1
            # If there are no more maps, change it into the end game screen
            if level == 3:
                keepGoing, toMenu = endGameScreen(screen, background, True)
            
            # Otherwise, change the map
            else:
                tutorial = False
                
                backgroundImage, player, teleportAnimation, pix, energyBar, timer, bestTime, endZone, platformList, platformGroup, wallList, wallGroup, lightList, lightGroup, wolfList, wolfGroup, blocksGroup, allMovingSprites, allSprites = changeMap(level, screen)
                
                allSprites.add(lifeCounter)
                allSprites.clear(screen, background)
                allSprites.update()
                allSprites.draw(screen)            
                
                keydown = [False, 'finish']

        # Refresh screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
     
        pygame.display.flip()
    
    return toMenu, keepGoing

def highScores(screen, background):
    '''This function diplays the top 10 high scores if there are enough 
    recorded times.'''
    # Entities
    titleBack = menuSprites.Background(False)
    times = mySprites.PastTimesKeeper('all', True)
    
    # Create Groups
    allSprites = pygame.sprite.OrderedUpdates(titleBack, times)
    
    # Assign Variables
    clock = pygame.time.Clock()
    keepGoing = True
    toMenu = False
    
    scrolling = [False, 'none']

    # Loop
    while keepGoing:
        
        # Time
        clock.tick(30)
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Checks if escape key was pressed, if yes, return to the menu
                if event.key == pygame.K_ESCAPE:
                    toMenu = True
                    keepGoing = False
            # If escape key was not pressed, but it is still in the pygame.QUIT
            # category, quit the game completely
            if event.type == pygame.QUIT:
                keepGoing = False 
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If scroll wheel is upward; right now there is no need
                if event.button == 4:
                    scrolling = [True, 'up']
                    
                # If scroll wheel is downward
                elif event.button == 5:
                    scrolling = [True, 'down']
            
            elif event.type == pygame.MOUSEBUTTONUP:
                # When it stops it stops scrolling; again no need because high scores
                # is not long enough; not enough maps
                if event.button == 4 or event.button == 5:
                    scrolling = [False, 'none']
                    times.stop()
        
        # Scrolls high scores
        if scrolling[0]:
            times.scroll(scrolling[1])
            
        # Refresh Screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
     
        pygame.display.flip()        
    
    return toMenu, keepGoing

def menu(screen, background):
    '''This function opens the menu until the player is ready'''
    # Create Objects
    titleBack = menuSprites.Background(True)
    
    # Sound
    hoverSound = pygame.mixer.Sound('sound/soundEffects/Magic3.wav')
    hoverSound.set_volume(0.01)
    
    # Buttons
    startMainGame = menuSprites.GameButton(screen, True, 'StartMainGame')
    startTutorial = menuSprites.GameButton(screen, True, 'StartTutorial')
    highScore = menuSprites.GameButton(screen, True, 'HighScore')
    
    # Sets up bundles
    buttonGroup = pygame.sprite.Group(startMainGame, startTutorial, highScore)
    allSprites = pygame.sprite.OrderedUpdates(titleBack, buttonGroup)
    
    # Assign
    tutorial = False
    gameStart = False
    openHighScores = False
    
    clock = pygame.time.Clock()
    keepGoing = True
    
    # Loop
    while keepGoing:
     
        # Time
        clock.tick(30)
        
        # Events
        buttonHovering = 'None'
        # Checks if the mouse is hovering a button
        for button in buttonGroup:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.hover(True)
                buttonHovering = button.getFunction()
                # Play hovering sound
                hoverSound.play()
            else:
                button.hover(False)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False        
            
            if event.type == pygame.MOUSEBUTTONUP:
                if not (buttonHovering == 'None'):
                    if buttonHovering == 'StartMainGame':
                        # Starts game, at the first level
                        tutorial = False
                        gameStart = True
                    
                    elif buttonHovering == 'StartTutorial':
                        # Starts game, at tutorial level
                        tutorial = True
                        gameStart = True
                    
                    elif buttonHovering == 'HighScore':
                        # Opens high score tab
                        openHighScores = True
                    
                    # Any of these events stop the loop
                    keepGoing = False

        # Refresh Screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
     
        pygame.display.flip()
        
    return keepGoing, openHighScores, gameStart, tutorial
    
def main():
    '''This function defines the 'mainline logic' for our game.'''
     
    # Display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Elmia")
     
    # Entities
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    
    # Music
    pygame.mixer.music.load('sound/Ori and the Blind Forest OST - 08 - Up the Spirit Caverns Walls (feat. Tom Boyd).mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    
    # Assign
    keepGoing = True
    gameStart = False
    tutorial = False
    openHighScore = False
    
    # Loop
    while keepGoing:
        # Opens menu
        keepGoing, openHighScore, gameStart, tutorial = menu(screen, background)
        while openHighScore:
            # Opens high score tab; best times
            keepGoing, openHighScore = highScores(screen, background)
        while gameStart:
            # Starts game
            keepGoing, gameStart = mainGame(screen, background, tutorial)
            
            # Replays title music if the player returns to title screen after dying
            # or beating the game
            pygame.mixer.music.load('sound/Ori and the Blind Forest OST - 08 - Up the Spirit Caverns Walls (feat. Tom Boyd).mp3')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)            
    
    # Close the game window
    pygame.quit()        
 
# Call the main function
main()
