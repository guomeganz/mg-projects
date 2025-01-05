# Jack to VM Compiler

## Behavior

Compiler.py translates Jack, a Java-like programming language, into VM code via indirect recursion. Jack is a simplified version of Java used for the nand2tetris course. Documentation of the Jack language can be found in the nand2tetris textbook by Noam Nisan and Shimon Schocken, which can be found on the following site:

https://www.nand2tetris.org/

The following is an example of Jack code:

class SnakeUnit {

    field int x;
    field int y;
    field int size;
    
    constructor SnakeUnit new(int xCo, int yCo, int sizeOfUnit) {
        let x = xCo;
        let y = yCo;
        let size = sizeOfUnit;
        return this;
    }

    method int getX() {
        return x;
    }
} 

## Input

The folder "Seven" contains a .jack file called "Main." Compiler.py is called in the terminal, and can take Seven or Main.jack as an argument.

## Output

When Compiler.py is run for the first time, a new file called "Main.vm" will be created in Seven. Main.vm contains the translated VM code for Main.jack produced by Compiler.py.

When Compiler.py is run again, if Main.vm is not deleted by the user, Main.vm will be updated to reflect any changes in Main.jack.