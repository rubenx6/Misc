import pygame
import random
import string

pygame.init()


alph = list(string.ascii_uppercase)
inputs = [] #user-determined inputs
inouts = [] #gate outputs(that can be used as other gate inputs) [not displayed]
outputs = []#circuit outputs [displayed]
usedgates = [] #gates used in circuit (ordered from first added to last)
gatedata = [] #gates data is in sets of threes: gate name, input 1, input 2, gate name, etc
gatelist = ("AND","OR","XOR","NAND","NOR","XNOR","NOT")

scr_w = 1600
scr_h = 900
fps = 144
win = pygame.display.set_mode((scr_w,scr_h))
pygame.display.set_caption("Logic Gate Simulator [Experimental Build]")
clock = pygame.time.Clock()

IMand = [pygame.image.load('images/andgate/andgate0.png'), pygame.image.load('images/andgate/andgate1.png'), pygame.image.load('images/andgate/andgate2.png'), pygame.image.load('images/andgate/andgate3.png')]
IMor = [pygame.image.load('images/orgate/orgate0.png'), pygame.image.load('images/orgate/orgate1.png'), pygame.image.load('images/orgate/orgate2.png'), pygame.image.load('images/orgate/orgate3.png')]
IMxor = [pygame.image.load('images/xorgate/xorgate0.png'), pygame.image.load('images/xorgate/xorgate1.png'), pygame.image.load('images/xorgate/xorgate2.png'), pygame.image.load('images/xorgate/xorgate3.png')]
IMnand = [pygame.image.load('images/nandgate/nandgate0.png'), pygame.image.load('images/nandgate/nandgate1.png'), pygame.image.load('images/nandgate/nandgate2.png'), pygame.image.load('images/nandgate/nandgate3.png')]
IMnor = [pygame.image.load('images/norgate/norgate0.png'), pygame.image.load('images/norgate/norgate1.png'), pygame.image.load('images/norgate/norgate2.png'), pygame.image.load('images/norgate/norgate3.png')]
IMxnor = [pygame.image.load('images/xnorgate/xnorgate0.png'), pygame.image.load('images/xnorgate/xnorgate1.png'), pygame.image.load('images/xnorgate/xnorgate2.png'), pygame.image.load('images/xnorgate/xnorgate3.png')]
IMnot = [pygame.image.load('images/notgate/notgate0.png'), pygame.image.load('images/notgate/notgate1.png')]



class gate:
    def __init__(self,name,in1=None,in2=None,isout=False):
        self.name = name
        self.in1 = in1
        self.in2 = in2
        self.isout = isout
        self.state = 0
        self.facade = eval("IM"+self.name.lower()+"[0]").convert_alpha()
        self.mesh = self.facade.get_rect()
        self.xpos = random.randint(0,1500)
        self.ypos = random.randint(0,800)
        self.mesh.topleft = (self.xpos,self.ypos)
        self.drag = False
             
    def updateFacade(self):
        self.facade = eval("IM"+self.name.lower()+"["+str(self.state)+"]").convert_alpha()

    def logic(self):
        if self.name == "AND":
            if self.in1 == 1 and self.in2 == 1:
                out = 1
                self.state = 3
            elif self.in1 == 1:
                self.state = 1
            elif self.in2 == 1:
                self.state = 2
            else:
                self.state = 0
            if not self.in1 == 1 and self.in2 == 1:
                out = 0
            self.updateFacade()
            return out

        if self.name == "OR":
            if self.in1 == 1 or self.in2 == 1:
                out = 1
            if self.in1 == 1 and self.in2 == 1:
                self.state = 3
            elif self.in1 == 1:
                self.state = 1
            elif self.in2 == 1:
                self.state = 2
            else:
                out = 0
                self.state = 0
            self.updateFacade()
            return out

        if self.name == "NAND":
            if self.in1 == 1 and self.in2 == 1:
                out = 0
                self.state = 3
            elif self.in1 == 1:
                self.state = 1
            elif self.in2 == 1:
                self.state = 2
            else:
                self.state = 0
            if not self.in1 == 1 and self.in2 == 1:
                out = 1
            self.updateFacade()
            return out

        if self.name == "NOR":
            if self.in1 == 1 or self.in2 == 1:
                out = 0            
            if self.in1 == 1 and self.in2 == 1:
                self.state = 3
            elif self.in1 == 1:
                self.state = 1
            elif self.in2 == 1:
                self.state = 2
            else:
                out = 1
                self.state = 0
            self.updateFacade()
            return out

        if self.name == "XOR":
            if self.in1 == self.in2:    out = 0
            if self.in1 == 1 and self.in2 == 1:
                self.state = 3
            elif self.in1 == 1:
                self.state = 1
                out = 1
            elif self.in2 == 1:
                self.state = 2
                out = 1
            else:
                self.state = 0
            self.updateFacade()               
            return out

        if self.name == "XNOR":
            if self.in1 == self.in2:    out = 1
            if self.in1 == 1 and self.in2 == 1:
                self.state = 3
            elif self.in1 == 1:
                self.state = 1
                out = 0
            elif self.in2 == 1:
                self.state = 2
                out = 0
            else:
                self.state = 0
            self.updateFacade()
            return out

        if self.name == "NOT":
            if self.in1 == 1:
                out = 0
                self.state = 1
            else:
                out = 1
                self.state = 0
            self.updateFacade()
            return out
        
def SelectGate(): #function for user to choose the next gate they would like to use
    answererror = True
    print("What gate do you want?(add 'out' to the gate if it is used for a final output) type 'gates' to get a list of options")
    while answererror == True:
        answer = input(">").upper()
        if not answer == "GATES":
            gatedata.append(answer)
            if "OUT" in answer:
                answer = answer.replace("OUT",'')
            if answer in gatelist:     answererror = False
            else:   print("invalid logic gate, try again")
        else:   print(gatelist)
    return answer

def SelectInputsForGate(): #function to determine where the current gate receives its inputs from
    chosengate = SelectGate()
    if not chosengate == "NOT":
        print("Which input values would you like to use?(gX for gate outputs where X is an integer)")
        inputA = input("inputA>")
        inputB = input("inputB>")
        gatedata.append(str(inputA))
        gatedata.append(str(inputB))
        usedgates.append(chosengate)
    else:
        print("Which input value would you like to use?(gX for gate outputs where X is an integer)")
        inputA = input("input>")
        gatedata.append(inputA)
        gatedata.append("X")
        usedgates.append(chosengate)

def InputQuant(): #user chooses how many inputs the circuit has 
    print("How many inputs do you want?")
    inputamount = input(">")
    while not int(inputamount) in range(1,27):
        print("Invalid value, try again.")
        inputamount = input(">")
    return inputamount
                              
def AskAmounts(): #user determines state of inputs
    print("How many logic gates are you using?")
    gatecount = int(input(">"))
    for i in range(gatecount):
        SelectInputsForGate()
    

def SaveCircuit(): #save circuit date to file
    print("What would you like to name your circuit?")
    filename = input(">")
    filename = filename + ".txt"
    file = open(filename,"w+")
    file.write(inputquant)
    file.write("\n")
    file.write(str(gatedata))
    file.write("\n")
    file.write(str(usedgates))
    file.close()
    print("Circuit saved to",filename)

def LoadCircuit(): #load circuit data from file
    print("What circuit would you like to load?")
    filename = input(">")
    filename = filename + ".txt"
    file = open(filename,"r")
    reader = file.readlines()
    inputquant = int(reader[0])
    gatedata = eval(reader[1])
    usedgates = eval(reader[2])
    return inputquant, gatedata, usedgates #all the data required to create a circuit

inputquant, gatedata, usedgates = LoadCircuit()

inputs = (1,0,1)

gdrag = 99

#def GatePassing():

    

gatearray = []
x = gate("XOR",1,0)

gatearray.append(x)
x(inputA,inputB)
x.logic()
RunCircuit2()
x = gatearray
#mainloop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(len(usedgates)):
                    if x[i].mesh.collidepoint(event.pos):
                        x[i].drag = True
                        gdrag = i
                        mouse_x, mouse_y = event.pos
                        offset_x = x[i].mesh.x - mouse_x
                        offset_y = x[i].mesh.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if gdrag in range(len(usedgates)):                
                    x[gdrag].drag = False
                    gdrag = 99

        elif event.type == pygame.MOUSEMOTION:
            if gdrag in range(len(usedgates)):
                if x[gdrag].drag == True:
                    mouse_x, mouse_y = event.pos
                    x[gdrag].mesh.x = mouse_x + offset_x
                    x[gdrag].mesh.y = mouse_y + offset_y


    win.fill((100,100,100))
    keys = pygame.key.get_pressed()
    print(usedgates)
    for i in range(len(usedgates)):
        win.blit(x[i].facade,x[i].mesh)
    pygame.display.flip()
    clock.tick(fps)

    



pygame.quit()

