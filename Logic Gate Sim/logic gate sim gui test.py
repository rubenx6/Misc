import pygame
import random

pygame.init()
pygame.font.init()



res = [1600,900]
fps = 144

win = pygame.display.set_mode(res)
pygame.display.set_caption("Logic Gate Simulator [Experimental Build]")
clock = pygame.time.Clock()

IMand = [pygame.image.load('images/andgate/andgate0.png'), pygame.image.load('images/andgate/andgate1.png'), pygame.image.load('images/andgate/andgate2.png'), pygame.image.load('images/andgate/andgate3.png')]
IMor = [pygame.image.load('images/orgate/orgate0.png'), pygame.image.load('images/orgate/orgate1.png'), pygame.image.load('images/orgate/orgate2.png'), pygame.image.load('images/orgate/orgate3.png')]
IMxor = [pygame.image.load('images/xorgate/xorgate0.png'), pygame.image.load('images/xorgate/xorgate1.png'), pygame.image.load('images/xorgate/xorgate2.png'), pygame.image.load('images/xorgate/xorgate3.png')]
IMnand = [pygame.image.load('images/nandgate/nandgate0.png'), pygame.image.load('images/nandgate/nandgate1.png'), pygame.image.load('images/nandgate/nandgate2.png'), pygame.image.load('images/nandgate/nandgate3.png')]
IMnor = [pygame.image.load('images/norgate/norgate0.png'), pygame.image.load('images/norgate/norgate1.png'), pygame.image.load('images/norgate/norgate2.png'), pygame.image.load('images/norgate/norgate3.png')]
IMxnor = [pygame.image.load('images/xnorgate/xnorgate0.png'), pygame.image.load('images/xnorgate/xnorgate1.png'), pygame.image.load('images/xnorgate/xnorgate2.png'), pygame.image.load('images/xnorgate/xnorgate3.png')]
IMnot = [pygame.image.load('images/notgate/notgate0.png'), pygame.image.load('images/notgate/notgate1.png')]

winsurface = pygame.display.get_surface()
rectangle = pygame.rect.Rect(100, 100, 100, 100)
rectangle_draging = False

gatelist = ("AND","OR","XOR","NAND","NOR","XNOR","NOT")

       
class gate:
    def __init__(self,name,in1from=None,in2from=None,isout=False):
        self.name = name
        self.in1 = 0
        self.in2 = 0
        self.isout = isout
        self.state = 0
        self.facade = eval("IM"+self.name.lower()+"["+str(self.state)+"]").convert_alpha()
        self.mesh = self.facade.get_rect()
        self.startx = random.randint(0,1500)
        self.starty = 200
        self.mesh.topleft = (self.startx,self.starty) 
        self.drag = False
        self.in1from = in1from
        self.in2from = in2from

    def ioCycle(self):
        if not self.in1from == None:
            self.in1 = allgates[self.in1from].output
        
        if not self.in2from == None:
            self.in2 = allgates[self.in2from].output
        self.output = self.logic()
         
        
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

        self.inmesh = self.facade.get_rect()
        self.inmesh.midleft,self.inmesh.w = self.mesh.midleft,partlen

        #self.outmesh = self.facade.get_rect()
        #self.outmesh.midright,self.outmesh.w = self.mesh.midright,partlen

        
        
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
            if not (self.in1 == 1 and self.in2 == 1):
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
            if not (self.in1 == 1 and self.in2 == 1):
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
        
gdrag = None
gqnt = 5

allgates = []
for i in range(gqnt):
    g = random.choice(gatelist)
    x = gate(g,random.randint(0,1),random.randint(0,1))
    allgates.append(x)
    x.logic()
x = allgates
#mainloop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(gqnt):
                    if x[i].mesh.collidepoint(event.pos):
                        if not x[i].inmesh.collidepoint(event.pos):                       
                            if not x[i].inmesh.collidepoint(event.pos[0]-80,event.pos[1]):
                                x[i].drag = True
                                gdrag = i
                                mouse_x, mouse_y = event.pos
                                offset_x = x[i].mesh.x - mouse_x
                                offset_y = x[i].mesh.y - mouse_y
                        #else:
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                try:
                    if gdrag in range(gqnt):                
                        x[gdrag].drag = False
                        gdrag = None
                except ValueError:
                    continue

        elif event.type == pygame.MOUSEMOTION:
            try:
                if gdrag in range(gqnt):
                    if x[gdrag].drag == True:
                        mouse_x, mouse_y = event.pos
                        x[gdrag].mesh.x = mouse_x + offset_x
                        x[gdrag].mesh.y = mouse_y + offset_y
            except ValueError:continue


    win.fill((100,100,100))
    keys = pygame.key.get_pressed()
    for i in range(gqnt):
        win.blit(x[i].facade,x[i].mesh)
        allgates[i].drawSubmesh()
    pygame.display.flip()
    clock.tick(fps)


    



pygame.quit()

