import gcpu.G0X as GOX

cpu = GOX.cpu("program.hex")
print(cpu.mem.data)