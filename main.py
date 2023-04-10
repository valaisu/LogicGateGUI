# This is going to be a program for building logical gates.
# The idea is to make a graphical user interface. Take inspiration
# for example from
# https://www.youtube.com/watch?v=QZwneRb-zqA&t=194s

#TODO: add draggable buttons CHECK
#TODO: the height of the buttons depends on the amount of connections they have
#TODO: add ability to make connections between buttons
#TODO: add connections also to the scene itself

import pygame
#from typing import Type


class input:
    def __init__(self, id, connections):
        self.id = id
        self.connections = connections
    def addConnection(self, connection): # connection consists of (buttonId, connectionId) pairs
        self.connections.append(connection)

class output:
    def __init__(self, id, connections):
        self.id = id
        self.connections = connections
    def addConnection(self, connection): # connection consists of (buttonId, connectionId) pairs
        self.connections.append(connection)

class button:
    def __init__(self, mid, width, height, color, colorHover, text, textColor, draggable, inputs, outputs):
        self.mid = mid #coord 0,0 at upper left corner
        self.width = width
        self.height = 30+20*max(max(len(inputs), len(outputs))-1, 0)
        self.left = mid[0]-width/2
        self.right = mid[0]+width/2
        self.top = mid[1]-self.height/2
        self.bottom = mid[1]+self.height/2

        self.color = color
        self.colorHover = colorHover

        self.text = smallfont.render(text, True, textColor)

        self.draggable = draggable

        self.inputs = inputs
        self.outputs = outputs

addedBtnCount = 0
color = (255, 255, 255) # white
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

def add_button(btnlist, text):
    btnlist.append(button((60 + addedBtnCount*100, 690), 80, 30, color_dark, color_light, text, (30, 30, 30), True, [input(0, -1)], [output(0, -1)]))

def updateBtn(mid, button):
#def updateBtn(mid, button: Type[button]):
    button.mid = mid
    button.left = mid[0] - button.width / 2
    button.right = mid[0] + button.width / 2
    button.top = mid[1] - button.height / 2
    button.bottom = mid[1] + button.height / 2

def getInputs(buttonList):
    connections = []
    for i in range(len(buttonList)):
        l = len(buttonList[i].inputs)
        for j in range(l):
            connections.append([buttonList[i].left, buttonList[i].top + buttonList[i].height*(j+0.5)/l, i, j])
    return connections

def getOutputs(buttonList):
    connections = []
    for i in range(len(buttonList)):
        l = len(buttonList[i].outputs)
        for j in range(l):
            connections.append([buttonList[i].right, buttonList[i].top + buttonList[i].height*(j+0.5)/l, i, j])
    return connections


pygame.init()
res = (720, 720)

# opens up a window
screen = pygame.display.set_mode(res)

width = screen.get_width()
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
# this font
text = smallfont.render('quit', True, color)


quitButton = button([200, 200], 100, 30, color_dark, color_light, "quit", (30, 30, 30), False, [input(0, -1)], [output(0, -1), output(0, -1)])
addButton = button([200, 300], 100, 30, color_dark, color_light, "add", (30, 30, 30), False, [input(0, -1),input(0, -1), input(0, -1)], [output(0, -1)])

buttons = [quitButton, addButton]
lines = []



dragging = False
dragLine = False
moveInfo = [(0,0),(0,0),-1]
lineStart = (0,0)
# = mouseCoords, buttonCoords, i

while True:
    mouse = pygame.mouse.get_pos()
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            inputList = getInputs(buttons)
            for i in range(len(inputList)):
                if inputList[i][0]-7 <= mouse[0] <= inputList[i][0]+7 and inputList[i][1]-7 <= mouse[1] <= inputList[i][1]+7:
                    dragLine = True
                    lineStart = (inputList[i][0], inputList[i][1])
            # if the mouse is clicked on the
            # button the game is terminated
            # ADD FOR LOOP HERE LATER
            for i in range(len(buttons)):
                if dragLine:
                    break
                if buttons[i].left <= mouse[0] <= buttons[i].right and buttons[i].top <= mouse[1] <= buttons[i].bottom:
                    if i == 0:
                        pygame.quit()
                    if i == 1:
                        text = "test" + str(addedBtnCount)
                        add_button(buttons, text)
                        addedBtnCount += 1
                        getInputs(buttons)
                    if buttons[i].draggable:
                        dragging = True
                        moveInfo = [mouse, buttons[i].mid, i]

        if ev.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                updateBtn(mouse, buttons[moveInfo[2]])
            if dragLine:
                dragLine = False
                outputList = getOutputs(buttons)
                for i in range(len(outputList)):
                    if outputList[i][0] - 7 <= mouse[0] <= outputList[i][0] + 7 and outputList[i][1] - 7 <= mouse[1] <= outputList[i][1] + 7:
                        lines.append([lineStart, (outputList[i][0], outputList[i][1])])


    screen.fill((60, 60, 60))


    # if mouse is hovered on a button it
    # changes to lighter shade
    for i in range(len(buttons)):
        if buttons[i].left <= mouse[0] <= buttons[i].right and buttons[i].top <= mouse[1] <= buttons[i].bottom:
            if dragging and i == moveInfo[2]:
                pygame.draw.rect(screen, buttons[i].colorHover, [mouse[0]-buttons[i].width/2, mouse[1]-buttons[i].height/2, buttons[i].width, buttons[i].height])
            else:
                pygame.draw.rect(screen, buttons[i].colorHover, [buttons[i].left, buttons[i].top, buttons[i].width, buttons[i].height])
        else:
            if dragging and i == moveInfo[2]:
                pygame.draw.rect(screen, buttons[i].color, [mouse[0] - buttons[i].width / 2, mouse[1] - buttons[i].height / 2, buttons[i].width, buttons[i].height])
            else:
                pygame.draw.rect(screen, buttons[i].color, [buttons[i].left, buttons[i].top, buttons[i].width, buttons[i].height])
        inputC = len(buttons[i].inputs)
        for j in range(inputC):
            pygame.draw.circle(screen, (0, 0, 0),(buttons[i].left, buttons[i].top + buttons[i].height * (j + 0.5) / (inputC)), 5)
        outputC = len(buttons[i].outputs)
        for j in range(outputC):
            pygame.draw.circle(screen, (0, 0, 0),(buttons[i].right, buttons[i].top + buttons[i].height * (j + 0.5) / (outputC)), 5)

    # add text on buttons
    for i in range(len(buttons)):
        if dragging and i == moveInfo[2]:
            screen.blit(buttons[i].text, (mouse[0] - buttons[i].width / 2 + 10, mouse[1] - buttons[i].height / 2))
        else:
            screen.blit(buttons[i].text, (buttons[i].left + 10, buttons[i].top + buttons[i].height/2 - 15))

    if dragLine:
        pygame.draw.line(screen, (0, 0, 0), lineStart, mouse)
    for i in range(len(lines)):
        pygame.draw.line(screen, (0, 0, 0), lines[i][0], lines[i][1])
    pygame.draw.line(screen, (0,0,0), (50, 50), (200, 50))
    pygame.draw.circle(screen, (0,0,0), (50,200), 5)
    # updates the frames of the game
    pygame.display.update()