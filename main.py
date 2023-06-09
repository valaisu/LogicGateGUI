# This is going to be a program for building logical gates.
# The idea is to make a graphical user interface. Take inspiration
# for example from
# https://www.youtube.com/watch?v=QZwneRb-zqA&t=194s

# TODO: (optional) add tools for editing the buttons/connections
# TODO: save buttons to database
# TODO: once a button is saved, it can be added to the scene
# TODO: add ability to add more inputs to the final button

import pygame
# from typing import Type <- maybe would make thing simpler


class logicBlock:
    def __init__(self, parent, children, operation, index):
        self.parent = parent
        self.children = children
        self.operation = operation
        self.index = index
        self.value = 0


def bond(parent, child, ind): # logicBlock, logicBlock, int
    for i in range(len(parent.children)):
        if parent.children[i].index == ind:
            parent.children[i].parent = []
            parent.children.pop(i)
            break
    parent.children.append(child)
    child.parent = parent
    child.index = ind


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
    def __init__(self, id, LUcorner, color, draggable, inputs, outputs, text, command, outputValue, logicBlock):
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

        self.outputValue = outputValue

        self.logicBlock = logicBlock

    def left(self): return self.LUcorner[0]
    def right(self): return self.LUcorner[0]+100
    def top(self): return self.LUcorner[1]
    def bottom(self): return self.LUcorner[1] + 30 + max(max(len(self.inputs), len(self.outputs))-1, 0) * 20
    def height(self): return self.bottom()-self.top()

    def outputPos(self, index):
        pass


class functionalButton:
    def __init__(self, LUcorner, width, height, text, function, parameter):
        self.LUcorner = LUcorner
        self.width = width
        self.height = height
        self.function = function
        self.text = smallfont.render(text, True, color_black)
        self.parameter = parameter


class sceneOutput:
    def __init__(self, top, bottom, right, outputs):
        self.LUcorner = (0, top)
        self.RDcorner = (right, bottom)
        self.width = right
        self.outputVals = []
        self.outputs = []
        self.logicBlocks = []
        for i in range(outputs):
            self.outputs.append(output(i, (-1, -1)))
            self.outputVals.append(0)
            self.logicBlocks.append(logicBlock([], [], "", -1))
    def addOutput(self):
        self.outputs.append(output(i, (-1, -1)))
        self.outputVals.append(0)
        self.logicBlocks.append(logicBlock([], [], "", -1))

    def removeOutput(self):
        for i in range(len(self.logicBlocks[-1].children)):
            self.logicBlocks[-1].children[i].parent = -1
        self.outputs.pop(-1)
        self.outputVals.pop(-1)
        self.logicBlocks.pop(-1)


    def blockVal(self, block):
        return self.outputVals[self.logicBlocks.index(block)]

    def right(self): return self.RDcorner[0]
    def left(self): return self.LUcorner[0]
    def top(self): return self.LUcorner[1]
    def bottom(self): return self.RDcorner[1]

    def getOutputPos(self):
        outputList = []
        l = len(self.outputs)
        h = self.bottom()
        for i in range(l):
            #print(i, l, (i+1)/(l+1)*h)
            outputList.append((self.right(), 120+(i+1)/(l+1)*h))
        return outputList
    def height(self): return self.bottom()-self.top()


def add_button(btnlist, text, logicBtn, inputs, outputs): # list[button], str, logicBlock, input, output
    btnlist.append(button(len(btnlist)+1,
                          (110, 680),
                          color_dark,
                          True,
                          inputs,
                          outputs,
                          text,
                          "",
                          0,
                          logicBtn
                          ))

def updateBtnPos(btnlist, index, pos): # List[button], int, (int, int)
    btnlist[index].LUcorner = (pos[0] - btnlist[index].width/2, pos[1] - btnlist[index].height()/2)


def getInputs(buttonList): # List[button]
    connections = []
    for i in range(len(buttonList)):
        if i != 0:
            l = len(buttonList[i].inputs)
            for j in range(l):
                connections.append([buttonList[i].left(), buttonList[i].top() + buttonList[i].height()*(j+0.5)/l, i, j])
    return connections # returns a list of [btn left, input y coord, btn index, input index]


def getOutputs(buttonList): # List[button]
    connections = []
    for i in range(len(buttonList)):
        l = len(buttonList[i].outputs)
        for j in range(l):
            t = buttonList[i]
            connections.append([t.right(), buttonList[i].top() + buttonList[i].height()*(j+0.5)/l,i, j, l])
    return connections # returns a list of [btn right, output y coord, btn index, input index]


def showVal(button): # button
    button.text = smallfont.render(str(button.outputValue), True, color_black)


def updateV2(block): # block
    # TODO: add bool that tells wether the outputval has been updated during this iteration
    if block.operation == "&":
        #print("&")
        values = []
        tot = len(block.children)
        for i in range(tot): # TODO: consider if tot should be replaced by len(inputs)
            values.append(updateV2(block.children[i]))
        val = 1
        for i in range(len(values)):
            val = val & values[i]
        return val
    elif block.operation == "!":
        #print("!")
        temp = updateV2(block.children[0])
        if temp == 0: return 1
        else: return 0
    elif block.operation == "c":
        #print("c")
        try:
            return updateV2(block.children[0])
        except IndexError:
            return 0
    elif block.operation == "":
        #print("empty")
        return block.value

def addSceneOutput(funcBtns, sOutput): # List[functionalButton], sceneOutput
    tot = len(sOutput.outputs)
    c = 0
    for i in range(len(funcBtns)):
        if funcBtns[i].function == "binary":
            yCoord = sOutput.height() * (0.5 + c) / (tot + 1) + 45
            funcBtns[i].LUcorner = (funcBtns[i].LUcorner[0], yCoord)
            c += 1
    yCoord = sOutput.height() * (0.5 + c) / (tot + 1) + 45
    funcBtns.append(functionalButton((30, yCoord), 30, 30, "0", "binary", tot))
    sOutput.addOutput()

def removeSceneOutput(funcBtns, sOutput, btns): # List[functionalButton], sceneOutput, List[button]
    tot = len(sOutput.outputs)
    c = 0
    for i in range(len(funcBtns)):
        if funcBtns[i].function == "binary":
            yCoord = sOutput.height() * (0.5 + c) / (tot-1) + 45
            funcBtns[i].LUcorner = (funcBtns[i].LUcorner[0], yCoord)
            c += 1
            if c == tot:
                funcBtns.pop(i)
                sOutput.removeOutput()
    for i in range(1, len(btns)):
        for j in range(len(btns[i].inputs)):
            if btns[i].inputs[j].connections == (0, tot-1):
                btns[i].inputs[j].connections = (-1, -1)
                #return (i, j)


def sceneToButton(btns): # List[button]
    # find a buttons with function "c" (should only be 1)
    # recursively go through all other buttons
    startInd = 1
    while True:
        if btns[startInd].logicBlock.operation == 'c':
            break
        startInd += 1
    print(startInd, btns[startInd].logicBlock.operation)
    taskList = [] # information will be stored here in format
    # List[operation participant participant...;]
    # for example string "&01;" would mean AND operation between values of
    # operations at indices 0 and 1. A valid string would also for example be
    # "!0;". Mere ";" means this place is occupied by one of sceneOutputs values
    def createTaskList(block): # logicBlock
        #print(block.operation, block.children)
        if block.operation == "&":
            createTaskList(block.children[0])
            #print("and")
            val0 = len(taskList)-1
            createTaskList(block.children[1])
            val1 = len(taskList)-1
            taskList.append(["&", val0, val1])
        elif block.operation == "!":
            createTaskList(block.children[0])
            val0 = len(taskList)-1
            taskList.append(["!", val0])
            #print("not")
        elif block.operation == "":
            #print("space")
            taskList.append([""])

    def taskListToText(taskList): # List[str]
        text = ""
        for i in range(len(taskList)):
            text += ''.join(map(str, taskList[i])) + ';'
        return text + '\n'

    createTaskList(btns[startInd].logicBlock.children[0])
    taskList.append(["c", len(taskList)-1])

    f = open("buttonDB.txt", "a")
    f.write(taskListToText(taskList))
    f.close()


def printRelations(block): # logicBlock
    for i in range(len(block.children)):
        printRelations(block.children[i])
    print("rel: " + str(block.operation))


addedBtnCount = 0
color = (255, 255, 255) # white
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
color_text = (40, 40, 40)
color_black = (0,0,0)



pygame.init()
res = (1500, 800)

# opens up a window
screen = pygame.display.set_mode(res)

width = screen.get_width()
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)
text = smallfont.render('quit', True, color)

sceneOutput = sceneOutput(60, 680, 100, 4)
quitButton = button(0, (10, 10), color_text, False, [input(0, (-1, -1))], [output(0, (-1, -1))], "quit", "pygame.quit", 0, logicBlock([], [], "", -1))
andButton = button(1, (130, 10), color_text, False, [input(0, (-1, -1))], [output(0, (-1, -1))], "and", "andBtn", 0, logicBlock([], [], "", -1))
notButton = button(2, (250, 10), color_text, False, [input(0, (-1, -1))], [output(0, (-1, -1))], "not", "invBtn", 0, logicBlock([], [], "", -1))
outputVal = button(3, (1000, 400), color_text, True, [input(0, (-1, -1))], [], "", "showVal", 0, logicBlock([], [], "c", -1))
# TODO: investigate why outputVal btn doesn't move
rmOutput = button(0, (370, 10), color_text, False, [input(0, (-1, -1))], [output(0, (-1, -1))], "rmOp", "rmOutput", 0, logicBlock([], [], "", -1))
addOutput = button(0, (490, 10), color_text, False, [input(0, (-1, -1))], [output(0, (-1, -1))], "adOp", "addOutput", 0, logicBlock([], [], "", -1))
buttonToDb = button(0, (1000, 10), color_text, False, [input(0, (-1, -1))], [output(0, (-1, -1))], "toDB", "buttonToDb", 0, logicBlock([], [], "", -1))



logicBlocks = []
funcButtons = []
for i in range(len(sceneOutput.outputs)): # TODO: the positions of the buttons are wrong, fix this CHECK
    yCoord = sceneOutput.height()*(0.5+i)/len(sceneOutput.outputs)+45
    funcButtons.append(functionalButton((30, yCoord), 30, 30, "0", "binary", i))
buttons = [sceneOutput, quitButton, andButton, notButton, outputVal, rmOutput, addOutput, buttonToDb]
connectionList = []

dragging = False
dragLine = False
moveInfo = [(0,0),(0,0),-1]
# = mouseCoords, buttonCoords, i
lineStart = [0,0,0,0]

while True:
    mouse = pygame.mouse.get_pos()

    outputList = getOutputs(buttons) #[x, y, btnInd, outputInd, totOutputs]
    inputList = getInputs(buttons)

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            # check if we start dragging a line
            for i in range(len(outputList)):
                if outputList[i][0]-7 <= mouse[0] <= outputList[i][0]+7 and outputList[i][1]-7 <= mouse[1] <= outputList[i][1]+7:
                    dragLine = True
                    lineStart = outputList[i]
            # check if we are clicking a functional button
            for i in range(len(funcButtons)):
                if funcButtons[i].LUcorner[0] <= mouse[0] <= funcButtons[i].LUcorner[0] + funcButtons[i].width and funcButtons[i].LUcorner[1] <= mouse[1] <= funcButtons[i].LUcorner[1] + funcButtons[i].height:
                    sceneOutput.outputVals[i] = (sceneOutput.outputVals[i]+1)%2
                    sceneOutput.logicBlocks[i].value = sceneOutput.outputVals[i]
            # check if we are clicking a button
            for i in range(1, len(buttons)):
                if dragLine:
                    break
                # buttons either do something when they are clicked, or can be dragged around
                if buttons[i].left() <= mouse[0] <= buttons[i].right() and buttons[i].top() <= mouse[1] <= buttons[i].bottom():
                    if buttons[i].command == 'pygame.quit':
                        pygame.quit()
                    elif buttons[i].command == 'andBtn':
                        logicBlocks.append(logicBlock([], [], "&", -1))
                        add_button(buttons, "AND", logicBlocks[-1], [input(0, (-1, -1)), input(0, (-1, -1))], [output(0, (-1, -1))])
                        addedBtnCount += 1
                    elif buttons[i].command == 'invBtn':
                        logicBlocks.append(logicBlock([], [], "!", -1))
                        add_button(buttons, "NOT", logicBlocks[-1], [input(0, (-1, -1))], [output(0, (-1, -1))])
                        addedBtnCount += 1
                    elif buttons[i].command == 'showVal':
                        showVal(buttons[i]) # TODO: should update automatically
                        print("----------------")
                        printRelations(buttons[i].logicBlock)
                    elif buttons[i].command == 'rmOutput':
                        removeSceneOutput(funcButtons, sceneOutput, buttons)
                    elif buttons[i].command == 'addOutput':
                        addSceneOutput(funcButtons, sceneOutput)
                    elif buttons[i].command == 'buttonToDb':
                        sceneToButton(buttons)
                    elif buttons[i].draggable:
                        dragging = True
                        moveInfo = [mouse, buttons[i].LUcorner, i]

        if ev.type == pygame.MOUSEBUTTONUP:
            # if we were dragging a button, drop it
            if dragging:
                dragging = False
                updateBtnPos(buttons, moveInfo[2], mouse)
                buttons[moveInfo[2]].LUcorner = (mouse[0] - buttons[moveInfo[2]].width / 2, mouse[1] - buttons[moveInfo[2]].height()/2)
            # if we were dragging a line, connect it provided we are close enough to an input
            if dragLine:
                dragLine = False
                for i in range(len(inputList)):
                    if inputList[i][0] - 7 <= mouse[0] <= inputList[i][0] + 7 and inputList[i][1] - 7 <= mouse[1] <= inputList[i][1] + 7:
                        buttons[inputList[i][2]].inputs[inputList[i][3]].connections = (lineStart[2], lineStart[3])
                        if lineStart[2] < len(buttons[0].outputs):
                            bond(buttons[inputList[i][2]].logicBlock, buttons[0].logicBlocks[lineStart[3]], inputList[i][3])
                        else:
                            bond(buttons[inputList[i][2]].logicBlock, buttons[lineStart[2]].logicBlock, inputList[i][3]) #

    screen.fill((60, 60, 60))
    pygame.draw.line(screen, color_black, (0, 60), (1500, 60))
    pygame.draw.line(screen, color_black, (0, 740), (1500, 740))

    # Draw the scene output
    pygame.draw.rect(screen, color_light, [0, sceneOutput.top(), sceneOutput.right(), sceneOutput.bottom()])
    outputPlaces = sceneOutput.getOutputPos()
    for i in range(len(outputPlaces)):
        pygame.draw.circle(screen, color_black, (outputList[i][0], outputList[i][1]), 5)

    # DRAWING THE BUTTONS
    # functional buttons (currently only the 1/0 outputs)
    for i in range(len(funcButtons)):
        if funcButtons[i].LUcorner[0] <= mouse[0] <= funcButtons[i].LUcorner[0]+funcButtons[i].width and funcButtons[i].LUcorner[1] <= mouse[1] <= funcButtons[i].LUcorner[1]+funcButtons[i].height:
            pygame.draw.rect(screen, color_light, [funcButtons[i].LUcorner[0], funcButtons[i].LUcorner[1], funcButtons[i].width, funcButtons[i].height])
        else:
            pygame.draw.rect(screen, color_dark, [funcButtons[i].LUcorner[0], funcButtons[i].LUcorner[1], funcButtons[i].width, funcButtons[i].height])
    # connectable buttons
    for i in range(1, len(buttons)):
        # if we hover over a button, make the color lighter
        if buttons[i].left() <= mouse[0] <= buttons[i].right() and buttons[i].top() <= mouse[1] <= buttons[i].bottom():
            # if we are dragging a button, it's position has not officially yet changed
            # ,so it needs to be drawn differently frm the rest of the buttons
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
    for i in range(len(funcButtons)):
        screen.blit(smallfont.render(str(sceneOutput.outputVals[i]), True, color_black), funcButtons[i].LUcorner)
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

    buttons[4].outputValue = updateV2(buttons[4].logicBlock)

    # updates the frames of the game
    pygame.display.update()