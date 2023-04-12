# This is going to be a program for building logical gates.
# The idea is to make a graphical user interface. Take inspiration
# for example from
# https://www.youtube.com/watch?v=QZwneRb-zqA&t=194s

#TODO: add draggable buttons CHECK
#TODO: the height of the buttons depends on the amount of connections they have CHECK
#TODO: add ability to make connections between buttons CHECK

#TODO: improve the data structure, redesign class button and add class connection

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
    def __init__(self, id, LUcorner, color, draggable, inputs, outputs, text, command):
        self.id = id
        self.text = smallfont.render(text, True, color)
        self.LUcorner = LUcorner

        self.color = color
        self.colorHover = (color[0]+30, color[1]+30, color[2]+30)

        self.draggable = draggable
        self.inputs = inputs
        self.outputs = outputs

        self.width = self.right()-self.left()

        self.command = command
    def left(self): return self.LUcorner[0]
    def right(self): return self.LUcorner[0]+100
    def top(self): return self.LUcorner[1]
    def bottom(self): return self.LUcorner[1] + 30 + max(max(len(self.inputs), len(self.outputs))-1, 0) * 20
    def height(self): return self.bottom()-self.top()

    def outputPos(self, index):
        pass


addedBtnCount = 0
color = (255, 255, 255) # white
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
color_text = (40, 40, 40)

def add_button(btnlist, text):
    btnlist.append(button(len(btnlist), (30+addedBtnCount*120, 660), color_dark, True, [input(0, (-1, -1))], [output(0, (-1, -1))], text, ""))

def update_btn_pos(btnlist, index, pos): #pos refers to the center coordinate of the button
    btnlist[index].LUcorner = (pos[0] - btnlist[index].width/2, pos[1] - btnlist[index].height()/2)


def getInputs(buttonList):
    connections = []
    for i in range(len(buttonList)):
        l = len(buttonList[i].inputs)
        for j in range(l):
            connections.append([buttonList[i].left(), buttonList[i].top() + buttonList[i].height()*(j+0.5)/l, i, j])
    return connections # returns a list of [btn left, btn right, btn index, input index]

def getOutputs(buttonList):
    connections = []
    for i in range(len(buttonList)):
        l = len(buttonList[i].outputs)
        for j in range(l):
            connections.append([buttonList[i].right(), buttonList[i].top() + buttonList[i].height()*(j+0.5)/l, i, j, l])
    return connections


pygame.init()
res = (720, 720)

# opens up a window
screen = pygame.display.set_mode(res)

width = screen.get_width()
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)
text = smallfont.render('quit', True, color)

quitButton = button(0, (200, 200), color_text, False, [input(0, (-1, -1))], [output(0, (-1, -1)), output(0, (-1, -1))], "quit", "pygame.quit")
addButton  = button(1, (200, 300), color_text, False, [input(0, (-1, -1))], [output(0, (-1, -1))], "add", "addBtn")

buttons = [quitButton, addButton]
connectionList = []



dragging = False
dragLine = False
moveInfo = [(0,0),(0,0),-1]
lineStart = [0,0,0,0]
# = mouseCoords, buttonCoords, i

commandDictionary = {"pygame.quit": pygame.quit, "addBtn": addButton}


while True:
    mouse = pygame.mouse.get_pos()

    outputList = getOutputs(buttons)
    inputList = getInputs(buttons)

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            #print(inputList)
            #[print(buttons[i].LUcorner, buttons[i].left()) for i in range(len(buttons))]
            for i in range(len(inputList)):
                if inputList[i][0]-7 <= mouse[0] <= inputList[i][0]+7 and inputList[i][1]-7 <= mouse[1] <= inputList[i][1]+7:
                    dragLine = True
                    lineStart = inputList[i]

            for i in range(len(buttons)):
                if dragLine:
                    break
                if buttons[i].left() <= mouse[0] <= buttons[i].right() and buttons[i].top() <= mouse[1] <= buttons[i].bottom():
                    if buttons[i].command == 'pygame.quit':
                        pygame.quit()
                    elif buttons[i].command == 'addBtn':
                        add_button(buttons, "test")
                        addedBtnCount += 1

                    elif buttons[i].draggable:
                        dragging = True
                        moveInfo = [mouse, buttons[i].LUcorner, i]

        if ev.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                update_btn_pos(buttons, moveInfo[2], mouse)
                buttons[moveInfo[2]].LUcorner = (mouse[0] - buttons[moveInfo[2]].width / 2, mouse[1] - buttons[moveInfo[2]].height()/2)

            if dragLine:
                dragLine = False
                for i in range(len(outputList)):
                    if outputList[i][0] - 7 <= mouse[0] <= outputList[i][0] + 7 and outputList[i][1] - 7 <= mouse[1] <= outputList[i][1] + 7:
                        buttons[outputList[i][2]].outputs[outputList[i][3]].connections = (lineStart[2], lineStart[3])

    screen.fill((60, 60, 60))

    # DRAWING THE BUTTONS
    # if mouse is hovered on a button it
    # changes to lighter shade
    for i in range(len(buttons)):
        if buttons[i].left() <= mouse[0] <= buttons[i].right() and buttons[i].top() <= mouse[1] <= buttons[i].bottom():
            if dragging and i == moveInfo[2]:
                pygame.draw.rect(screen, buttons[i].colorHover, [mouse[0]-buttons[i].width/2, mouse[1]-buttons[i].height()/2, buttons[i].width, buttons[i].height()])
            else:
                pygame.draw.rect(screen, buttons[i].colorHover, [buttons[i].left(), buttons[i].top(), buttons[i].width, buttons[i].height()])
        else:
            if dragging and i == moveInfo[2]:
                pygame.draw.rect(screen, buttons[i].color, [mouse[0] - buttons[i].width / 2, mouse[1] - buttons[i].height() / 2, buttons[i].width, buttons[i].height()])
            else:
                pygame.draw.rect(screen, buttons[i].color, [buttons[i].left(), buttons[i].top(), buttons[i].width, buttons[i].height()])
        # Draw in/outputs
        inputC = len(buttons[i].inputs)
        for j in range(inputC):
            pygame.draw.circle(screen, (0, 0, 0),(buttons[i].left(), buttons[i].top() + buttons[i].height() * (j + 0.5) / (inputC)), 5)
        outputC = len(buttons[i].outputs)
        for j in range(outputC):
            pygame.draw.circle(screen, (0, 0, 0),(buttons[i].right(), buttons[i].top() + buttons[i].height() * (j + 0.5) / (outputC)), 5)

    # add text on buttons
    for i in range(len(buttons)):
        if dragging and i == moveInfo[2]:
            screen.blit(buttons[i].text, (mouse[0] - buttons[i].width / 2 + 10, mouse[1] - buttons[i].height() / 2))
        else:
            screen.blit(buttons[i].text, (buttons[i].left() + 10, buttons[i].top() + buttons[i].height()/2 - 15))

    if dragLine:
        pygame.draw.line(screen, (0, 0, 0), (lineStart[0], lineStart[1]), mouse)

    # Draw the connections between the buttons
    for i in range(len(buttons)):
        for j in range(len(buttons[i].outputs)):
            if buttons[i].outputs[j].connections[0] != -1:
                outputC = len(buttons[i].outputs)
                outLoc = (buttons[i].right(), buttons[i].top() + buttons[i].height() * (j + 0.5) / (outputC))
                inputIds = buttons[i].outputs[j].connections
                inputC = len(buttons[inputIds[0]].inputs)
                inLoc = (buttons[inputIds[0]].left(), buttons[inputIds[0]].top() + buttons[inputIds[0]].height() * (inputIds[1] + 0.5) / (inputC))
                pygame.draw.line(screen, (0, 0, 0), outLoc, inLoc)

    # updates the frames of the game
    pygame.display.update()