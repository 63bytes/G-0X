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
    data = str(hex(int(data)))
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
        count = 0
        for x in range(address_size**2):
            self.data.update({toHex(x, CONFIG_HEX_SIZE):0})
    def get(self, address):
        return self.data[toHex(address,2)]
    def set(self, address, data):
        if int(address,16)<=int(self.address_end, 16):
            self.data[address] = data
            logging.log(logging.DEBUG, f"MEMORY - Address {address} set to {data}")
        else:
            logging.log(logging.ERROR, f"MEMORY - Address out of range({self.address_end})")
        if data>255:
            self.data[address] = 255
            logging.log(logging.WARNING, f"MEMORY - Data over 255, reseting to 255")

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
    def NOP(self):#No operation - 00
        logging.log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-1, CONFIG_HEX_SIZE)} - NOP (No operation)")
    def ADD(self):
        item1 = self.getNext()
        item2 = self.getNext()
        logging.log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-3, CONFIG_HEX_SIZE)} - ADD (Add) address {item1}({self.mem.get(item1)}) + address {item2}({self.mem.get(item2)})")
        self.mem.set(toHex(item1), self.mem.get(item1)+self.mem.get(item2))
    
    def HLT(self):#Halt the program - FF
        self.running =  False
        logging.log(logging.DEBUG, f"INSTRUCTION {toHex(self.pointer-1, CONFIG_HEX_SIZE)} - HLT (Halt)")
        logging.log(logging.INFO, f"Program halted")
    ##########################
    def execute(self):
        instruc = toHex(self.getNext(),2)
        print(instruc)
        if instruc=="00":
            self.NOP()
        elif instruc=="01":
            self.ADD()
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
                logging.log(logging.INFO, self.mem.data)
                break
            self.execute()