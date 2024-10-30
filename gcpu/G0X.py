import logging
logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG
)

CONFIG_HEX_SIZE = 2

def log(level, message):
    print(message)
    logging.log(level, message)

################################################# Utilities
def toHex(data, length=0):
    data = str(hex(data))
    data = data.split("x")[1]
    while len(data)<length:
        data = "0" + data
    return data

def getProgram(file):
    data = open(file, "rb").read()
    program = []
    for x in range(len(data)):
        program.append(int(data[x]))
    return program
#################################################
class MEMORY:
    def __init__(self, address_size, data_size):
        self.address_size = address_size
        self.address_end = toHex(address_size**2-1, CONFIG_HEX_SIZE)
        self.data = {}
        self.debug = True
        count = 0
        for x in range(address_size**2):
            self.data.update({toHex(x, CONFIG_HEX_SIZE):0})
    def get(self, address):
        if type(address)==int:
            address = toHex(address,CONFIG_HEX_SIZE)
        return self.data[address]
    def set(self, address, data):
        if int(address,16)<=int(self.address_end, 16):
            self.data[address] = data
            if self.debug:
                log(logging.DEBUG, f"MEMORY - Address {address} set to {data}")
        else:
            if self.debug:
                log(logging.ERROR, f"MEMORY - Address out of range({self.address_end})")
        if data>255:
            self.data[address] = 255
            if self.debug:
                log(logging.WARNING, f"MEMORY - Data over 255, reseting to 255")

class cpu:
    def __init__(self,file):
        logging.log(logging.INFO, "CPU initialized")
        self.program = getProgram(file)
        self.running = False
        self.mem = MEMORY(16,8)
        self.mem.debug = False
        for x in range(len(self.program)):
            self.mem.set(toHex(x,CONFIG_HEX_SIZE), self.program[x])
        self.mem.debug = True
        self.pointer = 0
    ########################## Instruction set
    def NOP(self):#No operation - 00
        log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-1, CONFIG_HEX_SIZE)} - NOP (No operation)")
    def HLT(self):#Halt the program - FF
        self.running =  False
        log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-1, CONFIG_HEX_SIZE)} - HLT (Halt)")
        log(logging.INFO, f"Program halted")
    def GTO(self):
        item1 = self.getNext()
        log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-2, CONFIG_HEX_SIZE)} - GTO (Go To) Pointer set to {item1}")
        self.pointer = item1
    def IFS(self):
        item1 = self.mem.get(toHex(self.getNext()))
        item2 = self.mem.get(toHex(self.getNext()))
        item3 = self.getNext()
        if item1==item2:
            self.pointer=item3
        log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-4, CONFIG_HEX_SIZE)} - IFS (If same) If {item1}={item2} then pointer set to {item3}")
    
    def ADD(self): #
        item1 = self.getNext()
        item2 = self.getNext()
        log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-3, CONFIG_HEX_SIZE)} - ADD (Add) address {item1}({self.mem.get(item1)}) + address {item2}({self.mem.get(item2)})")
        self.mem.set(toHex(item1), self.mem.get(item1)+self.mem.get(item2))
    def SUB(self):#subtract - 02
        item1 = self.getNext()
        item2 = self.getNext()
        log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-3, CONFIG_HEX_SIZE)} - SUB (Subtract) address {item1}({self.mem.get(item1)}) - address {item2}({self.mem.get(item2)})")
        self.mem.set(toHex(item1), self.mem.get(item1)-self.mem.get(item2))
    
    
    ##########################
    def execute(self):
        instruc = toHex(self.getNext(),2)
        if instruc=="00":
            self.NOP()
        elif instruc=="01":
            self.HLT()
        elif instruc=="02":
            self.GTO()
        elif instruc=="07":
            self.IFS()
        elif instruc=="10":
            self.ADD()
        elif instruc=="11":
            self.SUB()
        else:
            log(logging.WARN, f"OP Code unknown ({instruc})")
    def getNext(self):
        self.pointer+=1
        print(self.pointer)
        return self.mem.get(toHex(self.pointer-1, CONFIG_HEX_SIZE))
    def run(self):
        log(logging.INFO, "Program started")
        self.running = True
        while True:
            if self.running == False:
                logging.log(logging.INFO, self.mem.data)
                break
            self.execute()