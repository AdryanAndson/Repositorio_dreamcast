class Simple8BitEmulator:
    def __init__(self):
        self.memory = [0] * 256  # 256 bytes of memory
        self.acc = 0  # Accumulator
        self.ip = 0  # Instruction pointer
        self.carry = 0  # Carry flag
        self.zero = 0  # Zero flag
        self.running = True

    def load_program(self, program):
        self.memory[:len(program)] = program

    def fetch(self):
        instruction = self.memory[self.ip]
        self.ip = (self.ip + 1) % 256
        return instruction

    def execute(self, instruction):
        if instruction == 0x00:  # NOP
            pass
        elif instruction == 0x01:  # LDA
            address = self.fetch()
            self.acc = self.memory[address]
        elif instruction == 0x02:  # STA
            address = self.fetch()
            self.memory[address] = self.acc
        elif instruction == 0x03:  # ADD
            address = self.fetch()
            value = self.memory[address]
            result = self.acc + value
            self.carry = 1 if result > 255 else 0
            self.acc = result % 256
            self.zero = 1 if self.acc == 0 else 0
        elif instruction == 0x04:  # SUB
            address = self.fetch()
            value = self.memory[address]
            result = self.acc - value
            self.carry = 1 if result < 0 else 0
            self.acc = result % 256
            self.zero = 1 if self.acc == 0 else 0
        elif instruction == 0x05:  # JMP
            address = self.fetch()
            self.ip = address
        elif instruction == 0x06:  # JC
            address = self.fetch()
            if self.carry:
                self.ip = address
        elif instruction == 0x07:  # JZ
            address = self.fetch()
            if self.zero:
                self.ip = address
        elif instruction == 0xFF:  # HLT
            self.running = False
        else:
            raise ValueError(f"Unknown instruction {instruction:02x}")

    def run(self):
        while self.running:
            instruction = self.fetch()
            self.execute(instruction)

# Programa de exemplo
program = [
    0x01, 0x10,  # LDA 0x10
    0x03, 0x11,  # ADD 0x11
    0x02, 0x12,  # STA 0x12
    0xFF         # HLT
]

# Memória inicial
memory = [0] * 256
memory[0x10] = 5
memory[0x11] = 10

# Inicializar o emulador e carregar o programa
emulator = Simple8BitEmulator()
emulator.load_program(program)
emulator.memory = memory
emulator.run()

# Ver resultado na memória
print(emulator.memory[0x12])  # Deve imprimir 15
