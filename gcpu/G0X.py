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
        program.append(toHex(data[x],2))
    return program
#################################################
class MEMORY:
    def __init__(self, address_size, data_size):
        self.address_size = address_size
        self.address_end = toHex(address_size**2-1, CONFIG_HEX_SIZE)
        self.data = {}
        count = 0
        for x in range(address_size**2):
            self.data.update({toHex(x, CONFIG_HEX_SIZE):"0"*CONFIG_HEX_SIZE})
    def get(self, address):
        return self.data[address]
    def set(self, address, data):
        if int(address, 16)<=int(self.address_end, 16):
            self.data[address] = data
        else:
            logging.log(logging.ERROR, f"MEMORY - Address {address} was set to but is out of range({self.address_end})")

class cpu:
    def __init__(self,file):
        logging.log(logging.INFO, "CPU initialized")
        self.program = getProgram(file)
        self.running = False
        self.mem = MEMORY(16,8)
        for x in range(len(self.program)):
            self.mem.set(toHex(x,CONFIG_HEX_SIZE), self.program[x])
        self.pointer = 0
    ########################## Instruction set
    def NOP(self):#No operation  
        logging.log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-1, CONFIG_HEX_SIZE)} - NOP (No operation)")
    def HLT(self):#Halt the program
        self.running =  False
        logging.log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-1, CONFIG_HEX_SIZE)} - HLT (Halt)")
        logging.log(logging.INFO, f"Program halted")
    ##########################
    def execute(self):
        instruc = self.getNext()
        print(instruc)
        if instruc=="00":
            self.NOP()
        elif instruc=="ff":
            self.HLT()
        else:
            logging.log(logging.WARN, f"OP Code unknown ({instruc})")
    def getNext(self):
        self.pointer+=1
        return self.mem.get(toHex(self.pointer-1, CONFIG_HEX_SIZE))
    def run(self):
        logging.log(logging.INFO, "Program started")
        self.running = True
        for x in range(len(self.program)):
            if self.running == False:
                break
            self.execute()