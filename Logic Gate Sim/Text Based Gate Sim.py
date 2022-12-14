import string
alph = list(string.ascii_uppercase)
inputs = [] #user-determined inputs
inouts = [] #gate outputs(that can be used as other gate inputs) [not displayed]
outputs = []#circuit outputs [displayed]
usedgates = [] #gates used in circuit (ordered from first added to last)
gatedata = [] #gates data is in sets of threes: gate name, input 1, input 2, gate name, etc
gatelist = ("AND","OR","XOR","NAND","NOR","XNOR","NOT")

class gatelogic(object): #gate logic
    def __init__(self,in1,in2):
        self.in1 = in1
        self.in2 = in2
    def ANDgate(self):
        if int(self.in1) == 1 and int(self.in2) == 1:    out = 1
        else:    out = 0
        return out

    def ORgate(self):
        if int(self.in1) == 1 or int(self.in2) == 1:    out = 1
        else:    out = 0
        return out

    def NANDgate(self):
        if int(self.in1) == 1 and int(self.in2) == 1:    out = 0
        else:    out = 1
        return out

    def NORgate(self):
        if int(self.in1) == 1 or int(self.in2) == 1:    out = 0
        else:    out = 1
        return out

    def XORgate(self):
        if self.in1 == self.in2:    out = 0
        else:    out = 1
        return out

    def XNORgate(self):
        if self.in1 == self.in2:    out = 1
        else:    out = 0
        return out

    def NOTgate(self):
        if int(self.in1) == 1:    out = 0
        else:    out = 1
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

def RunCircuit(): #function to run the circuit
    for i in range(len(usedgates)):
        outputready = False
        gate = gatedata[i*3]
        inputA = gatedata[(i*3)+1]
        inputB = gatedata[(i*3)+2]
        if "OUT" in gate:
            outputready = True
        if not "NOT" in gate:
            if "g" in inputA:
                inputA = inputA.replace("g",'')
                inputA = str(inouts[int(inputA)-1])
            else:
                inputA = str(inputs[int(inputA)-1])
            if "g" in inputB:
                inputB = inputB.replace("g",'')
                inputB = str(inouts[int(inputB)-1])
            else:
                inputB = str(inputs[int(inputB)-1])
            x = gatelogic(inputA,inputB)
            inouts.append(eval("x."+usedgates[i]+"gate()"))
            if outputready == True: outputs.append(eval("x."+usedgates[i]+"gate()"))
        else:
            if "g" in inputA:
                inputA = inputA.replace("g",'')
                inputA = str(inouts[int(inputA)-1])
            else:
                inputA = str(inputs[int(inputA)-1])
            x = gatelogic(inputA,"X")
            inouts.append(eval("x."+usedgates[i]+"gate()"))
            if outputready == True: outputs.append(eval("x."+usedgates[i]+"gate()"))
                              
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

    
print("Would you like to load a circuit?(Y/N)")
askload = input(">").upper()
if askload == "Y":
    inputquant, gatedata, usedgates = LoadCircuit()
else:
    inputquant = InputQuant()
    AskAmounts()
    print("Would you like to save this circuit?(Y/N)")
    askload = input(">").upper()
    if askload == "Y":
        SaveCircuit()
while 1 == 1:
    print("Please set values for input variables. (0/1)")
    for i in range(int(inputquant)):
        inputs.append(input("input"+alph[i]+">"))
    RunCircuit()                                                           
    for i in range(len(outputs)):
        print("output"+alph[i]+" = "+str(outputs[i]))

    outputs, inouts, inputs = [],[],[]
    





    
