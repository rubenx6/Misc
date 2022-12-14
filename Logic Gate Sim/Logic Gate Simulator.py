import pygame as pg

pg.init()
pg.font.init()

res = [1600,900]
fps = 144

win = pg.display.set_mode(res)
pg.display.set_caption("Logic Gate Simulator [Experimental Build]")
clock = pg.time.Clock()

IMand = [pg.image.load('images/andgate/andgate0.png'), pg.image.load('images/andgate/andgate1.png'), pg.image.load('images/andgate/andgate2.png'), pg.image.load('images/andgate/andgate3.png')]
IMor = [pg.image.load('images/orgate/orgate0.png'), pg.image.load('images/orgate/orgate1.png'), pg.image.load('images/orgate/orgate2.png'), pg.image.load('images/orgate/orgate3.png')]
IMxor = [pg.image.load('images/xorgate/xorgate0.png'), pg.image.load('images/xorgate/xorgate1.png'), pg.image.load('images/xorgate/xorgate2.png'), pg.image.load('images/xorgate/xorgate3.png')]
IMnand = [pg.image.load('images/nandgate/nandgate0.png'), pg.image.load('images/nandgate/nandgate1.png'), pg.image.load('images/nandgate/nandgate2.png'), pg.image.load('images/nandgate/nandgate3.png')]
IMnor = [pg.image.load('images/norgate/norgate0.png'), pg.image.load('images/norgate/norgate1.png'), pg.image.load('images/norgate/norgate2.png'), pg.image.load('images/norgate/norgate3.png')]
IMxnor = [pg.image.load('images/xnorgate/xnorgate0.png'), pg.image.load('images/xnorgate/xnorgate1.png'), pg.image.load('images/xnorgate/xnorgate2.png'), pg.image.load('images/xnorgate/xnorgate3.png')]
IMnot = [pg.image.load('images/notgate/notgate0.png'), pg.image.load('images/notgate/notgate1.png')]

IMin0 = [pg.image.load('images/in0/in0.png'),pg.image.load('images/in0/in1.png')]
IMout0 = [pg.image.load('images/out0/out0.png'),pg.image.load('images/out0/out1.png')]

hint = [pg.image.load('images/hint/hint0.png'),pg.image.load('images/hint/hint1.png'),pg.image.load('images/hint/hint2.png'),pg.image.load('images/hint/hint3.png'),
        pg.image.load('images/hint/hint4.png'),pg.image.load('images/hint/hint5.png'),pg.image.load('images/hint/hint6.png')]

save = pg.image.load('images/save.png')
load = pg.image.load('images/load.png')
clear = pg.image.load('images/clear.png')
info = pg.image.load('images/info.png')

gatelist = ("AND","OR","XOR","NOT","NAND","NOR","XNOR")

class menu:
    def __init__(self):
        self.display = 0
        self.gap = 7
        self.object = []
        self.decal = []
        self.hintdecal = []
        self.hints = []
        self.hint = None
        self.infoicons = []
        self.infodecal = info
        self.decal.append(IMin0[0].convert_alpha())
        self.object.append(self.decal[0].get_rect())
        self.decal.append(IMout0[0].convert_alpha())
        self.object.append(self.decal[1].get_rect())
        for i in range(len(gatelist)):
            self.decal.append(eval("IM"+gatelist[i].lower()+"[0]").convert_alpha())
            self.object.append(self.decal[i+2].get_rect())
            self.infoicons.append(self.infodecal.get_rect())
            self.hintdecal.append(hint[i])
            self.hints.append(self.hintdecal[i].get_rect())
        self.decal.append(save.convert_alpha())
        self.object.append(self.decal[len(self.decal)-1].get_rect())
        self.decal.append(load.convert_alpha())
        self.object.append(self.decal[len(self.decal)-1].get_rect())
        self.decal.append(clear.convert_alpha())
        self.object.append(self.decal[len(self.decal)-1].get_rect())

    def DrawItems(self):
        self.object[0].center = (38,105)
        self.object[1].center = (112,105)
        self.object[9].center = (38,20)
        self.object[10].center = (112,20)
        self.object[11].center = (75,50)
        for i in range(len(gatelist)):
            self.object[i+2].midtop = (75,self.object[i+1].midbottom[1] + self.gap)
            self.infoicons[i].topleft = self.object[i+2].topright
            if self.hint != None:
                if self.hint == i:
                    self.hints[i].topleft = self.infoicons[i].topright
                    win.blit(self.hintdecal[i],self.hints[i]) 
        for i in range(len(self.object)):
            win.blit(self.decal[i],self.object[i])
        for i in range(len(self.infoicons)):
            win.blit(self.infodecal,self.infoicons[i])            
            
class source: #circuit input
    def __init__(self,startx,starty,skin=0,state=0):
        self.skin = skin
        self.state = state
        self.facade = eval("IMin"+str(skin)+"["+str(self.state)+"]").convert_alpha()       
        self.startx = startx
        self.starty = starty
        self.outmesh = self.facade.get_rect()
        self.outmesh.center = (self.startx,self.starty)
        self.wirefrom = None
        self.drag = False
        
    def drawMesh(self):
        partlen = self.outmesh.w/4
        self.mesh = self.facade.get_rect()
        self.mesh.w,self.mesh.h,self.mesh.center = self.outmesh.w-partlen,self.outmesh.h-partlen,self.outmesh.center
    def updateFacade(self):
        self.facade = eval("IMin"+str(self.skin)+"["+str(self.state)+"]").convert_alpha()

class output: #circuit output
    def __init__(self,startx,starty,skin=0,state=0):
        self.infrom = None
        self.skin = skin
        self.state = state
        self.facade = eval("IMout"+str(skin)+"[0]").convert_alpha()
        self.startx = startx
        self.starty = starty
        self.inmesh = self.facade.get_rect()
        self.inmesh.center = (self.startx,self.starty)
        self.wirefrom = None
        self.drag = False

    def drawMesh(self):
        partlen = self.inmesh.w/4
        self.mesh = self.facade.get_rect()
        self.mesh.w,self.mesh.h,self.mesh.center = self.inmesh.w-partlen,self.inmesh.h-partlen,self.inmesh.center

    def inRead(self):
        if not self.infrom == None:
            for i in range(wqnt):
                if allwires[i].ID == self.infrom:
                    self.state = allwires[i].signal

    def updateFacade(self):
        self.inRead()
        self.facade = eval("IMout"+str(self.skin)+"["+str(self.state)+"]").convert_alpha()
        

class gate: #logic gate
    def __init__(self,name,startx,starty,in1from=None,in2from=None):
        self.name = name
        self.in1 = 0
        self.in2 = 0
        self.state = 0
        self.facade = eval("IM"+self.name.lower()+"[0]").convert_alpha()
        self.mesh = self.facade.get_rect()
        self.startx = startx
        self.starty = starty
        self.mesh.center = (self.startx,self.starty) 
        self.drag = False
        self.in1from = in1from
        self.in2from = in2from
        self.iomesh = self.facade.get_rect()
        self.ID = None
      
    def ioCycle(self): #calculate output value from input values
        if not self.in1from == None:
            for i in range(wqnt):
                if allwires[i].ID == self.in1from:                  
                    self.in1 = allwires[i].signal
        if not self.in2from == None:
            for i in range(wqnt):
                if allwires[i].ID == self.in2from:
                    self.in2 = allwires[i].signal
        self.output = self.logic()
        self.updateFacade()
         
        
    def drawSubmesh(self):
        half = self.mesh.w/2
        partlen = self.mesh.w/5
        if self.name == "NOT":
            self.in1mesh = self.facade.get_rect()
            self.in1mesh.midleft,self.in1mesh.w = self.mesh.midleft,partlen
        else:
            self.in1mesh = self.facade.get_rect()
            self.in1mesh.x,self.in1mesh.y,self.in1mesh.w,self.in1mesh.h = self.mesh.x,self.mesh.y,partlen,half
            self.in2mesh = self.facade.get_rect()
            self.in2mesh.x,self.in2mesh.y,self.in2mesh.w,self.in2mesh.h = self.mesh.x,self.mesh.y+half,partlen,half

        self.iomesh.midleft,self.iomesh.w = self.mesh.midleft,partlen
        
    def updateFacade(self):
        self.facade = eval("IM"+self.name.lower()+"["+str(self.state)+"]").convert_alpha() #e.g. IMand[0]

    def logic(self): #gate logic
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
            if not (self.in1 == 1 and self.in2 == 1):
                out = 0
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
            if not (self.in1 == 1 and self.in2 == 1):
                out = 1
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
            return out

        if self.name == "NOT":
            if self.in1 == 1:
                out = 0
                self.state = 1
            else:
                out = 1
                self.state = 0
            return out

class wire: #wire
    def __init__(self,incon,outcon,startpos,drawing=False,ID=None):
        self.incon = incon
        self.outcon = outcon
        self.startpos = startpos
        self.endpos = startpos
        self.signal = 0
        self.drawing = drawing
        self.ID = ID
        self.ioStatus = None #true->in false->out
        self.isSet = False
        self.colour = (40,40,40)
        self.position = None
        self.fromsource = False

    def on(self):
        self.signal = 1
        self.colour = (0,150,200)

    def off(self):
        self.signal = 0
        self.colour = (40,40,40)

    def updateWire(self):
        if self.isSet:
            if self.ioStatus == None:
                if self.incon == None: #set wire to gate input
                    self.startpos = allgates[self.incon].iomesh.midleft[0]+95,allgates[self.incon].iomesh.midleft[1]
                    self.endpos = eval("allgates[self.outcon[0]].in"+self.outcon[1]+"mesh.center")
                else: #set wire to gate output
                    self.startpos = eval("allgates[self.outcon[0]].in"+self.outcon[1]+"mesh.center")
                    self.endpos = allgates[self.incon].iomesh.center[0]+80,allgates[self.incon].iomesh.midleft[1]
            elif self.ioStatus == True: #set wire to raw input
                for i in range(iqnt):
                    if i == self.incon:
                        self.startpos = eval("allinputs[i].outmesh."+self.position)
                        self.endpos = eval("allgates[self.outcon[0]].in"+self.outcon[1]+"mesh.center")
            elif self.fromsource != True: #set wire to output display
                for i in range(oqnt):
                    if i == self.outcon:
                        self.startpos = allgates[self.incon].iomesh.midleft[0]+95,allgates[self.incon].iomesh.midleft[1]
                        self.endpos = eval("alloutputs[i].inmesh."+self.position)                   
                
        if self.incon != None:
            if self.ioStatus != True:
                if allgates[self.incon].output == 1:
                    self.on()
                else:
                    self.off()
            else:
                if allinputs[self.incon].state == 1:
                    self.on()
                else:
                    self.off()
        else:
            self.off()         
        pg.draw.line(win,self.colour,self.startpos,self.endpos,5)
                    
gdrag = None
idrag = None
odrag = None
iqnt = 0 #quantity of input objects
oqnt = 0 #quantity of output objects
gqnt = 0 #quantity of logic gates
wqnt = 0 #quantity of wires
inready = False
outready = False
tempdata = None

allgates = []
allwires = []
allinputs = []
alloutputs = []

x = allgates
m = menu()

def SaveCircuit(): #save circuit data to file
    print("What would you like to name your circuit?")
    filename = input(">")
    filename += ".txt"
    file = open(filename,"w+")
    file.write('{0},{1},{2},{3}\n'.format(iqnt,oqnt,gqnt,wqnt))
    if iqnt != 0:
        for i in range(iqnt):
            file.write('{0},{1},{2},{3}\n'.format(allinputs[i].outmesh.center[0],allinputs[i].outmesh.center[1],allinputs[i].skin, allinputs[i].state))
        file.write("\n")
    if oqnt != 0:
        for i in range(oqnt):
            file.write('{0},{1},{2}\n'.format(alloutputs[i].inmesh.center[0],alloutputs[i].inmesh.center[1],alloutputs[i].skin))
        file.write("\n")
    if gqnt != 0:
        for i in range(gqnt):
            file.write('{0},{1},{2}\n'.format(gatelist.index(x[i].name),x[i].mesh.center[0],x[i].mesh.center[1]))
        file.write("\n")
    for i in range(wqnt):
        file.write('{0},{1},{2},{3}\n{4}\n'.format(allwires[i].incon,allwires[i].outcon,allwires[i].ioStatus,allwires[i].fromsource,allwires[i].position))
    file.close()
    print("Circuit saved to",filename)

def LoadCircuitData(): #load circuit data from file
    print("What circuit would you like to load?")
    filename = input(">")
    filename = filename + ".txt"
    file = open(filename,"r")
    reader = file.readlines()
    i,o,g,w = eval(reader[0])
    return filename,i,o,g,w

def MapFile(): #map circuit onto editor
    filename,IN,OUT,GATE,WIRE = LoadCircuitData()
    file = open(filename,"r")
    reader = file.readlines()
    counter = 1
    temp1,temp2,temp3,temp4,temp5 = 0,0,0,0,0
    if IN != 0:
        for i in range(IN): #creating inputs
            temp1,temp2,temp3,temp4 = eval(reader[counter])
            allinputs.append(source(temp1,temp2,temp3,temp4))
            counter += 1
        counter += 1
    if OUT != 0:
        for i in range(OUT): #creating outputs
            temp1,temp2,temp3 = eval(reader[counter])
            alloutputs.append(output(temp1,temp2,temp3))
            counter += 1
        counter += 1
    if GATE != 0:
        for i in range(GATE): #creating gate
            temp1,temp2,temp3 = eval(reader[counter])
            x.append(gate(gatelist[temp1],temp2,temp3))
            x[i].ID = i
            x[i].ioCycle()
            x[i].drawSubmesh()
            counter += 1
    if WIRE != 0:
        for i in range(WIRE): #creating wires
            counter += 1
            temp1,temp2,temp3,temp4 = eval(reader[counter])
            counter+=1
            temp5 = reader[counter]
            allwires.append(wire(temp1,temp2,(0,0)))
            allwires[i].ID = i
            allwires[i].ioStatus,allwires[i].fromsource,allwires[i].position = temp3,temp4,temp5
            if temp3 != False: #assigning object I/O ports to connected wires
                if temp2[1] == '1':
                    x[temp2[0]].in1from = i
                else:
                    x[temp2[0]].in2from = i
            else:
                alloutputs[temp2].infrom = i
            allwires[i].isSet = True
        
    return(IN,OUT,GATE,WIRE)
        
#mainloop
run = True
while run:
    win.fill((60,60,60))
    pg.draw.rect(win,(80,80,80),pg.Rect(0,0,150,res[1]))
    m.DrawItems()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3: #right-click
                if inready or outready:
                    for i in range(wqnt):
                        if not allwires[i].isSet: #cleanup loose wires with right-click               
                            wqnt -= 1
                            inready = False
                            outready = False
                            allwires.remove(allwires[i])
                            tempdata = i
                            for i in range(gqnt):
                                if x[i].in1from == tempdata:
                                    x[i].in1from = None
                                if x[i].in2from == tempdata:
                                    x[i].in2from = None
                            for i in range(oqnt):
                                if alloutputs[i].infrom == tempdata:
                                    alloutputs[i].infrom = None
                            tempdata = None        
                else:
                    for i in range(iqnt):
                        if allinputs[i].outmesh.collidepoint(event.pos):
                            if allinputs[i].state == 0:
                                allinputs[i].state = 1
                            else:
                                allinputs[i].state = 0
                    
            if event.button == 1: #left-click
                if m.object[9].collidepoint(event.pos): #save button clicked
                     SaveCircuit()
                if m.object[10].collidepoint(event.pos): #load button clicked
                     x.clear()
                     allinputs.clear()
                     alloutputs.clear()
                     allwires.clear()
                     iqnt,oqnt,gqnt,wqnt = 0,0,0,0
                     try:
                         iqnt,oqnt,gqnt,wqnt = MapFile()
                         print("Load Successful")
                     except:
                         print("Load Failed")
                         x.clear()
                         allinputs.clear()
                         alloutputs.clear()
                         allwires.clear()
                         iqnt,oqnt,gqnt,wqnt = 0,0,0,0
                if m.object[11].collidepoint(event.pos): #clear editor button clicked
                     x.clear()
                     allinputs.clear()
                     alloutputs.clear()
                     allwires.clear()
                     iqnt,oqnt,gqnt,wqnt = 0,0,0,0
                for i in range(len(gatelist)): #logic gate pulled from menu
                    if m.object[i+2].collidepoint(event.pos):
                        x.append(gate(gatelist[i],event.pos[0],event.pos[1]))
                        gqnt += 1
                        x[gqnt-1].ID = gqnt-1
                    if m.infoicons[i].collidepoint(event.pos):
                        if m.hint != i:
                            m.hint = i
                        else:
                            m.hint = None
        
                if m.object[0].collidepoint(event.pos): #input object pulled from menu
                     allinputs.append(source(event.pos[0],event.pos[1]))
                     iqnt += 1
                if m.object[1].collidepoint(event.pos): #output object pulled from menu
                     alloutputs.append(output(event.pos[0],event.pos[1]))
                     oqnt += 1
                
                                                                      
                for i in range(iqnt):
                    if allinputs[i].outmesh.collidepoint(event.pos): 
                        if not inready:                                 
                            radius = 15
                            if event.pos[0] in range(allinputs[i].outmesh.midtop[0]-radius,allinputs[i].outmesh.midtop[0]+radius):
                                if event.pos[1] in range(allinputs[i].outmesh.midtop[1],allinputs[i].outmesh.midtop[1]+radius):
                                    allinputs[i].wirefrom = "midtop"
                            if event.pos[0] in range(allinputs[i].outmesh.midright[0]-radius,allinputs[i].outmesh.midright[0]):
                                if event.pos[1] in range(allinputs[i].outmesh.midright[1]-radius,allinputs[i].outmesh.midright[1]+radius):
                                    allinputs[i].wirefrom = "midright"
                            if event.pos[0] in range(allinputs[i].outmesh.midbottom[0]-radius,allinputs[i].outmesh.midbottom[0]+radius):
                                if event.pos[1] in range(allinputs[i].outmesh.midbottom[1]-15,allinputs[i].outmesh.midbottom[1]):
                                    allinputs[i].wirefrom = "midbottom"
                            if event.pos[0] in range(allinputs[i].outmesh.midleft[0],allinputs[i].outmesh.midleft[0]+radius):
                                if event.pos[1] in range(allinputs[i].outmesh.midleft[1]-radius,allinputs[i].outmesh.midleft[1]+radius):
                                    allinputs[i].wirefrom = "midleft"
                            if outready:
                                if not allinputs[i].wirefrom == None:
                                    if tempdata != None: #set wire on raw input 
                                        if tempdata[0] == "w":                                                                                      
                                            if "g" in tempdata:
                                                allwires[wqnt-1].position = allinputs[i].wirefrom
                                                allwires[wqnt-1].ioStatus = True
                                                allwires[wqnt-1].incon = i
                                                tempdata = None
                                                for i in range(wqnt):
                                                    if  allwires[i].drawing == True:
                                                            allwires[i].drawing = False
                                                            allwires[i].isSet = True
                                                outready = False
                            elif not outready:
                                if not allinputs[i].wirefrom == None: #create new wire from raw input
                                    allwires.append(wire(i,None,getattr(allinputs[i].outmesh,allinputs[i].wirefrom),True,wqnt))
                                    allwires[wqnt].position = allinputs[i].wirefrom
                                    wqnt += 1
                                    allwires[wqnt-1].ioStatus = True
                                    inready = True                                    
                                    tempdata = "w",wqnt-1,"i"
                                    allinputs[i].wirefrom = None
                                    allwires[wqnt-1].fromsource = True
                            
                                elif gdrag == None and odrag == None: #being drag input display
                                            allinputs[i].drag = True
                                            idrag = i
                                            mouse_x, mouse_y = event.pos
                                            offset_x = allinputs[i].outmesh.x - mouse_x
                                            offset_y = allinputs[i].outmesh.y - mouse_y

                for i in range(oqnt):
                    if alloutputs[i].inmesh.collidepoint(event.pos):
                        if not outready:
                            radius = 15
                            if event.pos[0] in range(alloutputs[i].inmesh.midtop[0]-radius,alloutputs[i].inmesh.midtop[0]+radius): #find if user clicked edge of output display
                                if event.pos[1] in range(alloutputs[i].inmesh.midtop[1],alloutputs[i].inmesh.midtop[1]+radius):
                                    alloutputs[i].wirefrom = "midtop"
                            if event.pos[0] in range(alloutputs[i].inmesh.midright[0]-radius,alloutputs[i].inmesh.midright[0]):
                                if event.pos[1] in range(alloutputs[i].inmesh.midright[1]-radius,alloutputs[i].inmesh.midright[1]+radius):
                                    alloutputs[i].wirefrom = "midright"
                            if event.pos[0] in range(alloutputs[i].inmesh.midbottom[0]-radius,alloutputs[i].inmesh.midbottom[0]+radius):
                                if event.pos[1] in range(alloutputs[i].inmesh.midbottom[1]-15,alloutputs[i].inmesh.midbottom[1]):
                                    alloutputs[i].wirefrom = "midbottom"
                            if event.pos[0] in range(alloutputs[i].inmesh.midleft[0],alloutputs[i].inmesh.midleft[0]+radius):
                                if event.pos[1] in range(alloutputs[i].inmesh.midleft[1]-radius,alloutputs[i].inmesh.midleft[1]+radius):
                                    alloutputs[i].wirefrom = "midleft"
                            if inready:
                                if allwires[wqnt-1].fromsource == False: #set wire on output display
                                    if not alloutputs[i].wirefrom == None and alloutputs[i].infrom == None:
                                        if tempdata != None:
                                            if tempdata[0] == "w":
                                                allwires[wqnt-1].position = alloutputs[i].wirefrom
                                                alloutputs[i].infrom = wqnt-1
                                                allwires[wqnt-1].outcon = i
                                                allwires[wqnt-1].ioStatus = False                                                
                                                tempdata = None
                                                alloutputs[i].wirefrom = None
                                                for i in range(wqnt):
                                                    if allwires[i].drawing == True:
                                                        allwires[i].drawing = False
                                                        allwires[i].isSet = True
                                                inready = False                                
                            elif not inready:  
                                if not alloutputs[i].wirefrom == None and alloutputs[i].infrom == None: #create new wire from raw output
                                    allwires.append(wire(None,i,getattr(alloutputs[i].inmesh,alloutputs[i].wirefrom),True,wqnt))
                                    alloutputs[i].infrom = wqnt
                                    allwires[wqnt].position = alloutputs[i].wirefrom
                                    wqnt += 1
                                    allwires[wqnt-1].ioStatus = False
                                    outready = True                                    
                                    tempdata = "w",wqnt-1,"o"
                                    alloutputs[i].wirefrom = None
                                elif gdrag == None and idrag == None: #being drag output display                               
                                    alloutputs[i].drag = True
                                    odrag = i
                                    mouse_x, mouse_y = event.pos
                                    offset_x = alloutputs[i].inmesh.x - mouse_x
                                    offset_y = alloutputs[i].inmesh.y - mouse_y
                        
                for i in range(gqnt):
                    if x[i].mesh.collidepoint(event.pos):
                        if not x[i].iomesh.collidepoint(event.pos):                       
                            if not x[i].iomesh.collidepoint(event.pos[0]-80,event.pos[1]):
                                if not outready:
                                    if not inready:
                                        if idrag == None and odrag == None:
                                            x[i].drag = True
                                            gdrag = i
                                            mouse_x, mouse_y = event.pos
                                            offset_x = x[i].mesh.x - mouse_x
                                            offset_y = x[i].mesh.y - mouse_y
                            else:
                                if not outready:
                                    if not inready: #create new wire from gate output
                                        allwires.append(wire(x[i].ID,None,(x[i].iomesh.center[0]+80,x[i].iomesh.center[1]),True,wqnt))
                                        wqnt += 1
                                        inready = True                                    
                                        tempdata = "w","g"
                            if outready: #set wire on gate output
                                if x[i].iomesh.collidepoint(event.pos[0]-80,event.pos[1]):
                                    if "g" in tempdata:
                                        if i != allwires[wqnt-1].outcon[0]: #isn't trying to connect to itself
                                            tempdata = i
                                            allwires[wqnt-1].incon = allgates[tempdata].ID
                                            tempdata = None
                                            for i in range(wqnt):
                                                if  allwires[i].drawing == True:
                                                    allwires[i].drawing = False
                                                    allwires[i].isSet = True
                                            outready = False                                                
                                    elif "o" in tempdata:
                                        tempdata = i
                                        allwires[wqnt-1].incon = allgates[tempdata].ID
                                        tempdata = None
                                        for i in range(wqnt):
                                            if  allwires[i].drawing == True:
                                                allwires[i].drawing = False
                                                allwires[i].isSet = True
                                        outready = False
                        elif inready:                            
                            if not outready: #set wire on gate input
                                if x[i].in1mesh.collidepoint(event.pos): #is on input 1
                                    if allwires[wqnt-1].ioStatus == None:
                                        if i != allwires[wqnt-1].incon: #isn't trying to connect to itself
                                            if x[i].in1from == None:
                                                if tempdata != None:
                                                    if tempdata[0] == "w":                                                                                                                                                          
                                                        x[i].in1from = wqnt-1
                                                        allwires[wqnt-1].outcon = allgates[i].ID,"1"                                                
                                                        inready = False
                                                        tempdata = None
                                                        for i in range(wqnt):
                                                            if allwires[i].drawing == True:
                                                                allwires[i].drawing = False
                                                                allwires[i].isSet = True
                                    else:
                                        if x[i].in1from == None:
                                            if tempdata != None:
                                                if tempdata[0] == "w":                                                                                                                                                          
                                                    x[i].in1from = wqnt-1
                                                    allwires[wqnt-1].outcon = allgates[i].ID,"1"                                                
                                                    inready = False
                                                    tempdata = None
                                                    for i in range(wqnt):
                                                        if allwires[i].drawing == True:
                                                            allwires[i].drawing = False
                                                            allwires[i].isSet = True
                                                  
                                elif x[i].in2mesh.collidepoint(event.pos): #is on input 2
                                    if allwires[wqnt-1].ioStatus == None:
                                        if i != allwires[wqnt-1].incon: #isn't trying to connect to itself
                                            if x[i].in2from == None:     
                                                if tempdata != None:
                                                    if tempdata[0] == "w":                                                                                                                                                          
                                                        x[i].in2from = wqnt-1
                                                        allwires[wqnt-1].outcon = allgates[i].ID,"2"                                                
                                                        inready = False
                                                        tempdata = None
                                                        for i in range(wqnt):
                                                            if allwires[i].drawing == True:
                                                                allwires[i].drawing = False
                                                                allwires[i].isSet = True
                                    else:
                                        if x[i].in2from == None:
                                            if tempdata != None:
                                                if tempdata[0] == "w":                                                                                                                                                          
                                                    x[i].in2from = wqnt-1
                                                    allwires[wqnt-1].outcon = allgates[i].ID,"2"                                                
                                                    inready = False
                                                    tempdata = None
                                                    for i in range(wqnt):
                                                        if allwires[i].drawing == True:
                                                            allwires[i].drawing = False
                                                            allwires[i].isSet = True
                        else:
                            if not outready: #create new wire from gate input
                                try:
                                    if x[i].in1mesh.collidepoint(event.pos) and x[i].in1from == None:
                                        allwires.append(wire(None,(x[i].ID,"1"),(x[i].in1mesh.center[0],x[i].in1mesh.center[1]),True,wqnt))
                                        wqnt += 1
                                        x[i].in1from = wqnt - 1
                                        outready = True                                    
                                        tempdata = "w","g"
                                    elif x[i].in2mesh.collidepoint(event.pos) and x[i].in2from == None:
                                        allwires.append(wire(None,(x[i].ID,"2"),(x[i].in2mesh.center[0],x[i].in2mesh.center[1]),True,wqnt))
                                        wqnt += 1
                                        x[i].in2from = wqnt - 1
                                        outready = True                                    
                                        tempdata = "w","g"
                                except AttributeError:
                                    continue
                                
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                try:
                    if gdrag in range(gqnt):                
                        x[gdrag].drag = False
                        gdrag = None
                except ValueError:
                    continue
                try:
                    if idrag in range(iqnt):                
                        allinputs[idrag].drag = False
                        idrag = None
                except ValueError:
                    continue
                try:
                    if odrag in range(oqnt):                
                        alloutputs[odrag].drag = False
                        odrag = None
                except ValueError:
                    continue

        elif event.type == pg.MOUSEMOTION:            
            if inready == True or outready == True:
                    for i in range(wqnt):
                        if allwires[i].drawing:
                            allwires[i].endpos = event.pos
                        
            try:
                if gdrag in range(gqnt):
                    if x[gdrag].drag == True:
                        mouse_x, mouse_y = event.pos
                        x[gdrag].mesh.x = mouse_x + offset_x
                        x[gdrag].mesh.y = mouse_y + offset_y                
            except ValueError:
                continue
            try:
                if idrag in range(iqnt):
                    if allinputs[idrag].drag == True:
                        mouse_x, mouse_y = event.pos
                        allinputs[idrag].outmesh.x = mouse_x + offset_x
                        allinputs[idrag].outmesh.y = mouse_y + offset_y                
            except ValueError:continue
            try:
                if odrag in range(oqnt):
                    if alloutputs[odrag].drag == True:
                        mouse_x, mouse_y = event.pos
                        alloutputs[odrag].inmesh.x = mouse_x + offset_x
                        alloutputs[odrag].inmesh.y = mouse_y + offset_y                
            except ValueError:continue
    
    keys = pg.key.get_pressed() 
    for i in range(wqnt):
        allwires[i].updateWire()
    for i in range(gqnt):
        win.blit(x[i].facade,x[i].mesh)
        x[i].ioCycle()
        allgates[i].drawSubmesh()
    for i in range(oqnt):
        win.blit(alloutputs[i].facade,alloutputs[i].inmesh)
        alloutputs[i].drawMesh()
        alloutputs[i].updateFacade()
    for i in range(iqnt):
        win.blit(allinputs[i].facade,allinputs[i].outmesh)
        allinputs[i].drawMesh()
        allinputs[i].updateFacade()
    if keys[pg.K_f]:
        iqnt,oqnt,gqnt,wqnt = MapFile()
        
    if keys[pg.K_ESCAPE]: #cleanup loose wires with ESC       
        for i in range(wqnt):
            if not allwires[i].isSet:                
                wqnt -= 1
                inready = False
                outready = False
                allwires.remove(allwires[i])
                tempdata = i
                for i in range(gqnt):
                    if x[i].in1from == tempdata:
                        x[i].in1from = None
                    if x[i].in2from == tempdata:
                        x[i].in2from = None
                tempdata = None
    
    pg.display.flip()
    clock.tick(fps)

pg.quit()

