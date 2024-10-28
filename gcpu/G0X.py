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
            self.data.update({toHex(x, CONFIG_HEX_SIZE):"0"*data_size})
    def get(self, address):
        return self.data[address]
    def set(self, address, data):
        try:
            self.data[address] = data
        except IndexError:
            logging.log(logging.ERROR, f"MEMORY - Address {address} was set to but is out of range({self.address_end})")

class INSTRUCTIONS:
    def NOP(args):#No operation  
        logging.log(logging.DEBUG, f"INSTRUCTION - NOP (No operation) Args:{args}")
   
def execute(instruc, args):
    if instruc=="00":
        INSTRUCTIONS.NOP()

class cpu:
    def __init__(self,file):
        self.program = getProgram(file)
        self.mem = MEMORY(16,8)
        for x in range(len(self.program)):
            self.mem.set(toHex(x,CONFIG_HEX_SIZE), self.program[x])
        