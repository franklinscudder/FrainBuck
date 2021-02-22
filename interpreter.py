
SYMBOLS = "[]+-.,<>"
import os

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
        
    def validateProgram(self, program):
        loopLevel = 0
        
        for char in program:
            if char == "[":
                loopLevel += 1
            elif char == "]":
                loopLevel -= 1
        
        return not loopLevel
    
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
        
        if not self.validateProgram(program):
            print("BF Syntax Error: Unmatched brackets in source!")
            print()
            return None
        
        if program == "":
            print("No valid BrainFuck detected!")
            print()
            return None
        
        print("Executing from: ", scope)
        #print()
        
        while self.pc < len(program) - 1 and self.head < self.tapeLength - 1 and self.head >= 0:
            currentChar = self.getNextChar(program)
            self.processChar(currentChar, program)
            
        if self.head >= self.tapeLength - 1 or self.head < 0:
            print("\nRan out of Tape!")
            self.head = 0
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
            
    def printTape(self, start, length):
        tape = self.tape[start:start+length]
        
        if tape != []:
            if start != 0:
                print("Starting index: ", start)
            
            print("TAPE: |", end="")
            for i in tape[:-1]:
                print(str(i) + "|", end="")
            print(str(tape[-1]) + "|")
        
            if self.head >= length+start:
               print(">".rjust(2*length + 9))
            elif self.head < start:
                print("<".rjust(7))
            else:
                print("^".rjust(2*(self.head-start) + 8))
 
def parseFile(path):
    f = open(path, "r")
    txt = f.read()
    f.close()
    return txt

def showHelp():
    print()
    print("*** FRAINBUCK HELP ***")
    print("Enter a BrainFuck script at the prompt ($) and press enter to execute.")
    print("Enter the path of a .b source file to run it.")
    print("Enter 'h' or 'help' to display this help text.")
    print("Enter 'r' or 'reset' to reset the interpreter state.")
    print("Enter 'q' or 'quit' to quit.")
    print("Enter 'c' or 'clear' to clear the console.")
    print("Enter 't' or 'tape' to adjust the length of memory tape printed after execution.")
    print("Enter 'i' or 'index' to set the starting index of the tape output (default is 0).")
    print()




if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to file to be interpreted")
    args = parser.parse_args()
    TAPE_START = 0
    TAPE_LENGTH = 0
    
    interp = interpreter()
    
    if args.file:
        out = interp.interpret(parseFile(args.file), f"<{args.file}>")
        
        if out != None:
            interp.printTape(TAPE_START, TAPE_LENGTH)
    
    else:
        while 1:
            inp = input("[FrainBuck] $ ")
            if inp.lower() in ["q","quit"]:
                quit()
                
            elif inp.lower() in ["help","h","?"]:
                showHelp()
                
            elif inp.lower() in ["clear","c","cls"]:
                os.system("cls")
                
            elif inp.lower() in ["r","reset"]:
                interp = interpreter()
                print("Interpreter reset!")
                print()
                
            elif inp.lower() in ["tape", "t"]:
                valid = False
                while not valid:
                    try:
                        TAPE_LENGTH = max(0,int(input("Specify how much memory tape to print after execution (0 for no output): ")))
                        valid = True
                    except:
                        print("Must be a positive integer!")
                        
            elif inp.lower() in ["i", "index", "ti", "tapeindex"]:
                valid = False
                while not valid:
                    try:
                        TAPE_START = max(0,int(input("Specify the starting index of printed memory tape (default=0): ")))
                        valid = True
                    except:
                        print("Must be a positive integer!")
                
            elif inp[-2:] == ".b":
                interp = interpreter()
                print("Interpreter reset!")
                out = interp.interpret(parseFile(inp), f"<{inp}>")
                if out != None:
                    interp.printTape(TAPE_START, TAPE_LENGTH)

            else:
                out = interp.interpret(inp, "<input>")
                if out != None:
                    interp.printTape(TAPE_START, TAPE_LENGTH)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        