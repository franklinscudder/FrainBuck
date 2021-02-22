
SYMBOLS = "[]+-.,<>"

class interpreter:
    def __init__(self, initialTape=None, initialHeadIdx=None, tapeLength=30000, asChar=True):
        self.loopEntries = []
        self.asChar = asChar
        self.tapeLength = tapeLength
        self.tape = initialTape if initialTape else [0]*tapeLength
        self.head = initialHeadIdx if initialHeadIdx else 0
        self.pc = -1
        self.inputBuffer = []
        
    def cleanProg(self, program):
        cleaned = program
        
        for char in program:
            if char not in SYMBOLS:
                cleaned = cleaned.replace(char, "")
                
        return cleaned
    
    def read(self):
        return self.tape[self.head]
    
    def write(self, val):
        self.tape[self.head] = int(val) % 256
    
    def inc(self):
        self.tape[self.head] = (self.tape[self.head] + 1) % 256
    
    def dec(self):
        self.tape[self.head] = (self.tape[self.head] - 1) % 256
    
    def enterLoop(self, program):
        if self.read() == 0:
            loopDepth = 1
            while loopDepth > 0:
                char = self.getNextChar(program)
                loopDepth += 1 if char == "[" else 0
                loopDepth -= 1 if char == "]" else 0
            
        else:
            self.loopEntries.append(self.pc)
    
    def exitLoop(self):
        if self.read() != 0:
            self.pc = self.loopEntries.pop() - 1
        else:
            self.loopEntries.pop()
    
    def getNextChar(self, program):
        self.pc += 1
        return program[self.pc]
    
    def processInput(self):
        valid = False
        
        while not valid:
            if len(self.inputBuffer) == 0:
                inp = input("\nEnter input: ")
                valid, inp = self.verifyInput(inp)
                self.inputBuffer += inp[1:]
                
                inp = inp[0]
                    
            else:
                inp = self.inputBuffer.pop(0)
                valid = True
                
        self.write(inp)
        
    def verifyInput(self, inp):
        valid = False
        out = []
        for char in inp:
            try:
                char = ord(char)
                if char >= 0 and char <= 255:
                    valid = True
                else:
                    print("Invalid input!")
                out.append(char)
            except:
                print("Invalid input!")
                
                
        out.append(0)
        return valid, out
    
    def interpret(self, program, scope):
        self.pc = -1
        program = self.cleanProg(program)
        
        if program == "":
            print("No valid BrainFuck detected!")
            return None
        
        print("Executing from: ", scope)
        print()
        
        while self.pc < len(program) - 1 and self.head < self.tapeLength - 1:
            currentChar = self.getNextChar(program)
            self.processChar(currentChar, program)
            
        if self.head >= self.tapeLength - 1:
            print("\nRan out of Tape!")
        else:
            print("\nExecution Completed Successfully!")
        return self.tape
        
    def processChar(self, char, program):
        if char == "+":
            self.inc()
        elif char == "-":
            self.dec()
        elif char == ">":
            self.head += 1
        elif char == "<":
            self.head -= 1
        elif char == ".":
            val = chr(self.read()) if self.asChar else self.read()
            print(val,end="")
        elif char == ",":
            self.processInput()
        elif char == "[":
            self.enterLoop(program)
        elif char == "]":
            self.exitLoop()
        else:
            raise RuntimeError("Unrecognized BF command! " + char)
 
def parseFile(path):
    f = open(path, "r")
    txt = f.read()
    f.close()
    return txt

def showHelp():
    print()
    print("*** FRAINBUCK HELP ***")
    print("Enter a BrainFuck script at the prompt ($) and press enter to execute.")
    print("Enter 'h' to display this help text.")
    print("Enter 'r' or 'reset' to reset the interpreter state.")
    print("Enter 'q' or 'quit' to quit.")
    print()

def printTape(tape):
    print("TAPE: |", end="")
    for i in tape[:-1]:
        print(str(i) + "|", end="")
    print(str(tape[-1]) + "|")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to file to be interpreted")
    args = parser.parse_args()
    
    interp = interpreter()
    
    if args.file:
        out = interp.interpret(parseFile(args.file), f"<{args.file}>")
        
        if out != None:
            printTape(out[:25])
    
    else:
        while 1:
            inp = input("[FrainBuck] $ ")
            if inp.lower() in ["q","quit"]:
                quit()
                
            elif inp.lower() in ["help","h"]:
                showHelp()
                
            elif inp.lower() in ["r","reset"]:
                interp = interpreter()
                print("Interpreter reset!")
                
            elif inp[-2:] == ".b":
                interp = interpreter()
                print("Interpreter reset!")
                out = interp.interpret(parseFile(inp), f"<{inp}>")
                if out != None:
                    printTape(out[:25])

            else:
                out = interp.interpret(inp, "<input>")
                if out != None:
                    printTape(out[:25])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        