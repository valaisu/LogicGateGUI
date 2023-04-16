# This is going to be a program for building logical gates.
# The idea is to make a graphical user interface. Take inspiration
# for example from
# https://www.youtube.com/watch?v=QZwneRb-zqA&t=194s

#TODO: add draggable buttons CHECK
#TODO: the height of the buttons depends on the amount of connections they have CHECK
#TODO: add ability to make connections between buttons CHECK

#TODO: improve the data structure, redesign class button and add class connection CHECK

#TODO: add connections also to the scene itself CHECK

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
        self.text = smallfont.render(text, True, color_black)
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


class sceneOutput:
    def __init__(self, top, bottom, right, outputs):
        self.LUcorner = (0, top)
        self.RDcorner = (right, bottom)
        self.width = right
        #self.top = top
        #self.bottom = bottom
        #self.right = right
        self.outputs = []
        for i in range(outputs):
            self.outputs.append(output(i, (-1, -1)))

    def right(self): return self.RDcorner[0]
    def left(self): return self.LUcorner[0]
    def top(self): return self.LUcorner[1]
    def bottom(self): return self.RDcorner[1]

    def getOutputPos(self):
        outputList = []
        l = len(self.outputs)
        h = self.bottom() - self.top()
        for i in range(l):
            outputList.append((self.right(), 60+(i+1)/(l+1)*h))
        return outputList
    def height(self): return self.bottom()-self.top()


addedBtnCount = 0
color = (255, 255, 255) # white
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
color_text = (40, 40, 40)
color_black = (0,0,0)

def add_button(btnlist, text):
    btnlist.append(button(len(btnlist)+1,
                          (110+addedBtnCount*120, 680),
                          color_dark,
                          True,
                          [input(0, (-1, -1)), input(0, (-1, -1))],
                          [output(0, (-1, -1)), output(0, (-1, -1))],
                          text, ""
                          ))

def update_btn_pos(btnlist, index, pos): #pos refers to the center coordinate of the button
    btnlist[index].LUcorner = (pos[0] - btnlist[index].width/2, pos[1] - btnlist[index].height()/2)


def getInputs(buttonList):
    connections = []
    for i in range(len(buttonList)):
        if i != 0:
            l = len(buttonList[i].inputs)
            for j in range(l):
                connections.append([buttonList[i].left(), buttonList[i].top() + buttonList[i].height()*(j+0.5)/l, i, j])
    return connections # returns a list of [btn left, btn right, btn index, input index]

def getOutputs(buttonList):
    connections = []
    for i in range(len(buttonList)):
        l = len(buttonList[i].outputs)
        for j in range(l):
            t = buttonList[i]
            connections.append([t.right(), buttonList[i].top() + buttonList[i].height()*(j+0.5)/l,i, j, l])
    return connections


pygame.init()
res = (1500, 800)

# opens up a window
screen = pygame.display.set_mode(res)

width = screen.get_width()
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)
text = smallfont.render('quit', True, color)

sceneOutput = sceneOutput(60, 680, 100, 2)
quitButton = button(0, (10, 10), color_text, False, [input(0, (-1, -1))], [output(0, (-1, -1))], "quit", "pygame.quit")
addButton  = button(1, (130, 10), color_text, False, [input(0, (-1, -1))], [output(0, (-1, -1))], "add", "addBtn")

buttons = [sceneOutput, quitButton, addButton]
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
            # check if we start dragging a line
            for i in range(len(outputList)):
                if outputList[i][0]-7 <= mouse[0] <= outputList[i][0]+7 and outputList[i][1]-7 <= mouse[1] <= outputList[i][1]+7:
                    dragLine = True
                    print(outputList)
                    lineStart = outputList[i]
                    print(i, lineStart)
            # check if we are clicking a button
            for i in range(1, len(buttons)):
                if dragLine:
                    break
                # buttons either do something when they are clicked, or can be dragged around
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
            # if we were dragging a button, drop it
            if dragging:
                dragging = False
                update_btn_pos(buttons, moveInfo[2], mouse)
                buttons[moveInfo[2]].LUcorner = (mouse[0] - buttons[moveInfo[2]].width / 2, mouse[1] - buttons[moveInfo[2]].height()/2)
            # if we were dragging a line, connect it provided we are close enough to an input
            if dragLine:
                dragLine = False
                for i in range(len(inputList)):
                    if inputList[i][0] - 7 <= mouse[0] <= inputList[i][0] + 7 and inputList[i][1] - 7 <= mouse[1] <= inputList[i][1] + 7:
                        buttons[inputList[i][2]].inputs[inputList[i][3]].connections = (lineStart[2], lineStart[3])

    screen.fill((60, 60, 60))
    pygame.draw.line(screen, color_black, (0, 60), (1500, 60))
    pygame.draw.line(screen, color_black, (0, 740), (1500, 740))
    pygame.draw.circle(screen, color_black, (100, 215), 8) #TODO: here youll find the root of the errors, probably should make the scene output more alike with the buttons so all same commands can be applied

    # Draw the scene output
    pygame.draw.rect(screen, color_light, [0, sceneOutput.top(), sceneOutput.right(), sceneOutput.bottom()])
    outputPlaces = sceneOutput.getOutputPos()
    for i in range(len(outputPlaces)):
        pygame.draw.circle(screen, color_black, (outputList[i][0], outputList[i][1]), 5)

    # DRAWING THE BUTTONS
    for i in range(1, len(buttons)):
        # if we hover over a button, make the color lighter
        if buttons[i].left() <= mouse[0] <= buttons[i].right() and buttons[i].top() <= mouse[1] <= buttons[i].bottom():
            # if we are dragging a button, it's position has not officially yet changed
            # so it needs to be drawn differently frm the rest of the buttons
            if dragging and i == moveInfo[2]:
                pygame.draw.rect(screen, buttons[i].colorHover, [mouse[0]-buttons[i].width/2, mouse[1]-buttons[i].height()/2, buttons[i].width, buttons[i].height()])
            else:
                pygame.draw.rect(screen, buttons[i].colorHover, [buttons[i].left(), buttons[i].top(), buttons[i].width, buttons[i].height()])
        # same deal if we are not hovering
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
    for i in range(1, len(buttons)):
        if dragging and i == moveInfo[2]:
            screen.blit(buttons[i].text, (mouse[0] - buttons[i].width / 2 + 10, mouse[1] - buttons[i].height() / 2))
        else:
            screen.blit(buttons[i].text, (buttons[i].left() + 10, buttons[i].top() + buttons[i].height()/2 - 15))

    if dragLine:
        pygame.draw.line(screen, (0, 0, 0), (lineStart[0], lineStart[1]), mouse)

    # Draw the connections between the buttons
    for i in range(1, len(buttons)):
        for j in range(len(buttons[i].inputs)):
            if buttons[i].inputs[j].connections[0] != -1:
                inputC = len(buttons[i].inputs)
                inLoc = (buttons[i].left(), buttons[i].top() + buttons[i].height() * (j + 0.5) / (inputC))
                outputIds = buttons[i].inputs[j].connections
                outputC = len(buttons[outputIds[0]].outputs)
                outLoc = (buttons[outputIds[0]].right(),
                          buttons[outputIds[0]].top() +
                          buttons[outputIds[0]].height() *
                          (outputIds[1] + 0.5) / (outputC))
                pygame.draw.line(screen, (0, 0, 0), inLoc, outLoc)

    # updates the frames of the game
    #[print(buttons[1].inputs[i].connections) for i in range(len(buttons[1].inputs))] # in a way, only inputs exist
    #print("")
    pygame.display.update()