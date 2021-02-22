# FrainBuck
 A Python BrainFuck interpreter/console

Usage
===========

To access the interactive console, use the command ```frainbuck``` in the (Windows) command line 
from your installation folder. You can now enter single lines of BrainFuck code at the prompt ```$``` and press 
enter to run it. 

To run a brainfuck source file use the command ```frainbuck %filepath%```. The file path can be 
relative or absolute. You can now also run BrainFuck source files from the interactive console simply by
inputting their path, ensuring it ends ```.b```.

Input is buffered so that multiple input characters can be given in one go. All inputs add a zero
to the buffer after themselves. When the buffer is empty, the next ```,``` will again prompt the user
for input.

Interpreter Control Commands
===============================
For a list of interpreter commands, enter ```h``` or ```help``` in the interactive console. These are:
* 'h' or 'help' to display this help text.
* 'r' or 'reset' to reset the interpreter state.
* 'q' or 'quit' to quit.
* 'c' or 'clear' to clear the console.
* 't' or 'tape' to adjust the length of memory tape printed after execution.
* 'i' or 'index' to set the starting index of the tape output (default is 0).

Requirements
===============
The program requires Python >=3.7 installed on Windows.

Credit and License
====================
Relesed under the MIT software license. Feel free to adapt and distribute with acknowledgment.
The demo source files here were all written by Daniel B. Cristofani at http://brainfuck.org/,
except for mandlebrot.b which was written by Erik Bosman at https://copy.sh/brainfuck/.