# FrainBuck
 A Python BrainFuck interpreter/console

Usage
===========

To access the interactive console, use the command ```FrainBuck``` in the (Windows) command line 
from your installation folder. You can now enter single lines of BrainFuck code at the prompt ```$``` and press 
enter to run it. The commands ```help``` and ```quit``` can also be used, as well as ```reset``` which 
will reset the tape and R/W head position.

To run a brainfuck source file use the command ```FrainBuck %filepath%```. The file path can be 
relative or absolute.

Input is given as a single ASCII charachter per input request, when and EOF/EOL charachter is needed
you must press enter with no input specified.

Requirements
===============
The program requires Python >=3.7 installed on Windows.