import sys
import re
import os

keywordList = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]

symbolList = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

opList = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

inComment = False

index = 0
className = ""

staticCount = 0
fieldCount = 0
localCount = 0
argCount = 0

ifCount = 0
elseCount = 0
whileCount = 0
exitCount = 0

opDict = {
    '+' : "add",
    '-' : "sub",
    '*' : "call Math.multiply 2",
    '/' : "call Math.divide 2",
    '&' : "and",
    '|' : "or",
    '<' : "lt",
    '>' : "gt",
    '=' : "eq"
}

classSymbolTable = {

}

subSymbolTable = {

}

def main():

    fileOrFolder = sys.argv[1]

    tokenList = []

    if(not os.path.isfile(fileOrFolder)):
        directoryList = os.listdir(fileOrFolder)
        filesToProcess = []

        for file in directoryList:
            if file.endswith(".jack"):
                filesToProcess.append(fileOrFolder + "/" + file)
        
        for file in filesToProcess:
            tokenList = tokenize(file) 
            xmlFileName = file.replace(".jack", ".vm")
            file = open(xmlFileName, 'w')
            createParseList(tokenList, file)
            file.close()

    elif(os.path.isfile(fileOrFolder)):
        file = fileOrFolder
        tokenList = tokenize(file)

        xmlFileName = file.replace(".jack", ".vm")
        xmlFile = open(xmlFileName, 'w')
        createParseList(tokenList, xmlFile)
        xmlFile.close()

def tokenize(fileName):

    global inComment

    readFile = open(fileName, "r")
    toParse = readFile.read()

    allLines = re.split("\n", toParse)
    allWords = []

    for line in allLines:
        #ignore // comments
        locationOfSlashComment = line.find("//")
        if(locationOfSlashComment != -1):
            if(locationOfSlashComment == 0):
                continue
            else:
                line = line[:locationOfSlashComment]
        
        #ignore /** */ comments
        locationOfStarComment = line.find("/**")
        if(locationOfStarComment != -1):
            inComment = True
            commentEndLocation = line.find("*/")
            if(commentEndLocation != -1):
                inComment = False
                line = line[:locationOfStarComment] + line[commentEndLocation + 2:]
            else:
                line = line[:locationOfStarComment]

        locationOfCommentEnd = line.find("*/")
        if(locationOfCommentEnd != -1):
            inComment = False
            line = line[locationOfCommentEnd + 2:]
        
        starCommentCont = line.find("*")
        if((starCommentCont != -1) and (inComment)):
            line = line[:starCommentCont]

        locationOfQuote = line.find("\"")

        #custom method for string parsing
        if(locationOfQuote != -1):
            inString = False
            customList = []
            curWord = ""
            for character in line:
                if((character == "\"") and (not inString)):
                    inString = True
                    customList.append(curWord)
                    curWord = "\""
                    continue
                if(not inString):
                    if(not character.isspace()):
                        curWord = curWord + character
                        if(line[len(line) - 1] == character):
                            customList.append(curWord)
                    else:
                        customList.append(curWord)
                        curWord = ""
                elif(inString):
                    curWord = curWord + character
                    if(character == "\""):
                        inString = False
                        customList.append(curWord)
                        curWord = ""

            for word in customList:
                if(len(word) > 0):
                    allWords.append(word)

        else:
            wordList = re.split(r'\s', line)

            for word in wordList:
                if(len(word) > 0):
                    allWords.append(word)

    tokenList = []
    for word in allWords:
        for character in word:
            if(character in symbolList):
                word = re.sub('\\' + character, ' ' + character + ' ', word)
        if(word[0] != "\""):
            word = re.split(r'\s', word)
            for token in word:
                if(token != ''):
                    tokenList.append(token)
        else:
            tokenList.append(word)
        
    return tokenList

            
def writeToken(token):

    if(token in keywordList):
        return "<keyword> " + token + " </keyword>\n"

    elif(token in symbolList):
        if(token == '<'):
            token = "&lt;"
        elif(token == '>'):
            token = "&gt;"
        elif(token == "\""):
            token = "&quot;"
        elif(token == "&"):
            token = "&amp;"

        return "<symbol> " + token + " </symbol>\n"
    
    elif(token.isdigit()):
        return "<integerConstant> " + token + " </integerConstant>\n"

    elif(token[0] == '"' and token[-1] == '"'):
        token = re.sub('"', "", token)
        return "<stringConstant> " + token + " </stringConstant>\n"

    elif(len(re.findall("[a-zA-Z_.$:][\\w.$:]*", token)) > 0):
        return "<identifier> " + token + " </identifier>\n"

def createParseList(tokenList, fileToWrite):
    global index
    global staticCount
    global fieldCount
    global localCount
    global argCount
    global ifCount
    global elseCount
    global whileCount
    global exitCount

    index = 0
    staticCount = 0
    fieldCount = 0
    localCount = 0
    argCount = 0
    ifCount = 0
    elseCount = 0
    whileCount = 0
    exitCount = 0

    compileClass(tokenList, fileToWrite)

def compileClass(tokenList, fileToWrite):
    global index
    global className
    global classSymbolTable

    classSymbolTable.clear

    index += 1 #skip class
    className = tokenList[index] #save className
    index += 1 #skip className
    index += 1 #skip {
    compileClassVarDec(tokenList, fileToWrite)
    compileSubroutine(tokenList, fileToWrite)
    index += 1 #skip }

def compileClassVarDec(tokenList, fileToWrite):
    global index
    while((tokenList[index] == "static") or (tokenList[index] == "field")):
        varKind = tokenList[index]
        index += 1 #skip 'static' | field
        varType = tokenList[index]
        index += 1 #skip type
        varName = tokenList[index]
        index += 1 #skip varName
        addSymbol(varName, varType, varKind)
        while(tokenList[index] == ","):
            index += 1 #skip ,
            moreVarName = tokenList[index]
            addSymbol(moreVarName, varType, varKind)
            index += 1 #skip varName
        index += 1 #skip ;
    
def compileVarDec(tokenList, fileToWrite):
    global index
    while(tokenList[index] == "var"):
        index += 1 #skip var
        varType = tokenList[index] #type
        index += 1 #skip type
        varName = tokenList[index] #varName
        index += 1 #skip varName

        addSymbol(varName, varType, "local")

        while(tokenList[index] == ","):
            index += 1 #skip ,
            moreVarName = tokenList[index] #varName
            addSymbol(moreVarName, varType, "local")
            index += 1 #skip varName
            
        index += 1 #skip ;

def compileSubroutine(tokenList, fileToWrite): 
    global index
    global className
    global argCount

    while((tokenList[index] == "constructor") or (tokenList[index] == "function") or (tokenList[index] == "method")):
        refreshSubCounts() #zeroes out local and arg

        if (tokenList[index] == "constructor"):
            index += 1 #skip constructor|function|method
            constructorType = tokenList[index] #save void|type, it's the class
            index += 1 #skip void|type
            subroutineName = tokenList[index]
            index += 1 #skip subroutineName
            index += 1 #skip (
            # #parameterList
            if(tokenList[index] != ')'): #if it doesn't just close, then there's parameters to process
                compileParameter(tokenList, fileToWrite)
            
            index += 1 #skip )

            numVars = countVars(tokenList, index)

            writeLine("function " + constructorType + "." + subroutineName + " " + str(numVars), fileToWrite)

            writeLine("push constant " + str(fieldCount), fileToWrite)
            writeLine("call Memory.alloc 1", fileToWrite)
            writeLine("pop pointer 0", fileToWrite)

            compileSubroutineBody(tokenList, fileToWrite) 

        elif(tokenList[index] == "function"):
            index += 1 #skip constructor|function|method
            index += 1 #skip void|type
            subroutineName = tokenList[index]
            index += 1 #skip subroutineName
            index += 1 #skip (
            #parameterList
            if(tokenList[index] != ')'): #if it doesn't just close, then there's parameters to process
                compileParameter(tokenList, fileToWrite)

            index += 1 #skip )

            numVars = countVars(tokenList, index)

            writeLine("function " + className + "." + subroutineName + " " + str(numVars), fileToWrite)

            compileSubroutineBody(tokenList, fileToWrite)
        
        elif(tokenList[index] == "method"):

            argCount += 1

            index += 1 #skip constructor|function|method
            index += 1 #skip void|type
            subroutineName = tokenList[index]
            index += 1 #skip subroutineName
            index += 1 #skip (
            # #parameterList
            if(tokenList[index] != ')'): #if it doesn't just close, then there's parameters to process
                compileParameter(tokenList, fileToWrite)
            
            index += 1 #skip )

            numVars = countVars(tokenList, index)

            writeLine("function " + className + "." + subroutineName + " " + str(numVars), fileToWrite)

            writeLine("push argument 0", fileToWrite)
            writeLine("pop pointer 0", fileToWrite)

            compileSubroutineBody(tokenList, fileToWrite)

def compileSubroutineBody(tokenList, fileToWrite):
    global index
    index += 1 #skip {
    compileVarDec(tokenList, fileToWrite) #varDec*
    compileStatements(tokenList, fileToWrite) #statements
    index += 1 #skip }

def compileParameter(tokenList, fileToWrite):
    global index

    varType = tokenList[index] #type
    index += 1 #skip type

    varName = tokenList[index] #varName
    index += 1 #skip varName

    addSymbol(varName, varType, "arg") #add this var to the argument list

    while(tokenList[index] == ","):
        index += 1 #skip ,
        moreVarType = tokenList[index] #type
        index += 1 #skip moreType
        moreVarName = tokenList[index] #varName
        index += 1 #skip moreVarName
        addSymbol(moreVarName, moreVarType, "arg") #add this to the argument list

def compileStatements(tokenList, fileToWrite):
    global index
    while(isStatement(tokenList[index])):
        if(tokenList[index] == "let"):
            compileLetStatement(tokenList, fileToWrite)
        elif(tokenList[index] == "if"):
            compileIfStatement(tokenList, fileToWrite)
        elif(tokenList[index] == "while"):
            compileWhileStatement(tokenList, fileToWrite)
        elif(tokenList[index] == "do"):
            compileDoStatement(tokenList, fileToWrite)
        elif(tokenList[index] == "return"):
            compileReturnStatement(tokenList, fileToWrite)

def compileLetStatement(tokenList, fileToWrite):
    global index

    index += 1 #skip let
    varName = tokenList[index] #varName
    index += 1 #skip varName

    if(tokenList[index] == '['): #if command is something like let a[i] = expression
        index += 1 #skip [
        writeLine("push " + readSymbolTable(varName), fileToWrite)
        compileExpression(tokenList, fileToWrite)
        writeLine("add", fileToWrite)
        index += 1 #skip ]
        index += 1 #skip =
        compileExpression(tokenList, fileToWrite) #expression
        writeLine("pop temp 0" , fileToWrite)
        writeLine("pop pointer 1", fileToWrite)
        writeLine("push temp 0", fileToWrite)
        writeLine("pop that 0", fileToWrite)

    else: #not an array
        index += 1 #skip =
        compileExpression(tokenList, fileToWrite) #expression
        writeLine("pop " + readSymbolTable(varName), fileToWrite)

    index += 1 #skip ;

def compileIfStatement(tokenList, fileToWrite):
    global index
    global ifCount
    global elseCount

    index += 1 #skip if
    index += 1 #skip (
    
    compileExpression(tokenList, fileToWrite) #expression
    writeLine("not", fileToWrite) #write 'not'
    writeLine("if-goto ifLabel" + str(ifCount), fileToWrite) #write if-goto statement

    index += 1 #skip )
    index += 1 #skip {
    compileStatements(tokenList, fileToWrite) #statements
    index += 1 #skip }

    writeLine("goto elseLabel" + str(elseCount), fileToWrite) #write goto statement

    writeLine("label ifLabel" + str(ifCount), fileToWrite)

    if(tokenList[index] == "else"):
        index += 1 #skip else
        index += 1 #skip {
        compileStatements(tokenList, fileToWrite) #statements
        index += 1 #skip }
    
    writeLine("label elseLabel" + str(elseCount), fileToWrite)
    
    ifCount += 1 #increment ifCount
    elseCount += 1 #increment elseCount

def compileWhileStatement(tokenList, fileToWrite):
    global index
    global whileCount
    global exitCount

    curWhileCount = whileCount
    curExitCount = exitCount

    index += 1 #skip while
    index += 1 #skip (
    
    writeLine("label whileLabel" + str(curWhileCount), fileToWrite) 
    compileExpression(tokenList, fileToWrite) #expression
    writeLine("not", fileToWrite)
    writeLine("if-goto exitLabel" + str(curExitCount), fileToWrite)

    whileCount += 1
    exitCount += 1

    index += 1 #skip )
    index += 1 #skip {
    
    compileStatements(tokenList, fileToWrite) #statements

    writeLine("goto whileLabel" + str(curWhileCount), fileToWrite)
    writeLine("label exitLabel" + str(curExitCount), fileToWrite)

    index += 1 #skip }

def compileDoStatement(tokenList, fileToWrite):
    global index
    index += 1 #skip do
    compileSubroutineCall(tokenList, fileToWrite) #subroutineCall
    index += 1 #skip ;
    writeLine("pop temp 0", fileToWrite)

def compileReturnStatement(tokenList, fileToWrite):
    global index

    index += 1 #skip return
    if(tokenList[index] != ';'):
        compileExpression(tokenList, fileToWrite) #compile any expressions
    else:
        writeLine("push constant 0", fileToWrite)
    writeLine("return", fileToWrite) #write return
    index += 1 #skip ;

def compileExpression(tokenList, fileToWrite):
    global index
    compileTerm(tokenList, fileToWrite) #term
    while(tokenList[index] in opList):
        op = tokenList[index] #save op
        index += 1 #skip op
        compileTerm(tokenList, fileToWrite) #term
        writeLine(opDict[op], fileToWrite)

def compileTerm(tokenList, fileToWrite):
    global index

    typeOfToken = tokenType(tokenList[index])

    if(typeOfToken == "integerConstant"): #integerConstant
        writeLine("push constant " + tokenList[index], fileToWrite)
        index += 1

    elif(typeOfToken == "stringConstant"): #stringConstant
        noQuotes = tokenList[index].replace("\"", "")
        writeLine("push constant " + str(len(noQuotes)), fileToWrite)
        writeLine("call String.new 1", fileToWrite)

        for character in noQuotes:
            writeLine("push constant " + str(ord(character)), fileToWrite)
            writeLine("call String.appendChar 2", fileToWrite)
        index += 1 #skip the string

    elif(typeOfToken == "keywordConstant"): #keywordConstant
        linesToWrite = []
        tokenToProcess = tokenList[index]
        if(tokenToProcess == "true"):
            linesToWrite.append("push constant 1")
            linesToWrite.append("neg")
        elif(tokenToProcess == "false"):
            linesToWrite.append("push constant 0")
        elif(tokenToProcess == "null"):
            linesToWrite.append("push constant 0")
        elif(tokenToProcess == "this"):
            linesToWrite.append("push pointer 0")
        for line in linesToWrite:
            writeLine(line, fileToWrite)
        
        index += 1

    elif(typeOfToken == "unaryOp"): #unaryOp
        unaryOp = tokenList[index] #save unaryOp
        index = index + 1 #skip past unaryOp
        compileTerm(tokenList, fileToWrite) #term
        if(unaryOp == "-"):
            writeLine("neg", fileToWrite)
        elif(unaryOp == "~"):
            writeLine("not", fileToWrite)

    elif(tokenList[index] == "("): #if this is a expression in parentheses
        index += 1 #skip (
        compileExpression(tokenList, fileToWrite)
        index += 1 #skip )

    else: #this could be a var, an array, or a subroutine
        alreadyProcessed = False

        if(index < len(tokenList) - 1):
            if(tokenList[index + 1] == "["): #if this upcoming data structure is an array
                varName = tokenList[index] #varName
                writeLine("push " + readSymbolTable(varName), fileToWrite)
                index += 1 #skip varName
                index += 1 #skip [
                compileExpression(tokenList, fileToWrite)
                writeLine("add", fileToWrite)
                writeLine("pop pointer 1", fileToWrite)
                index += 1 #skip ]
                writeLine("push that 0", fileToWrite)
                alreadyProcessed = True

            elif((tokenList[index + 1] == "(") or (tokenList[index + 1] == ".")): #if this upcoming data is a subroutine call
                compileSubroutineCall(tokenList, fileToWrite)
                alreadyProcessed = True

        if(not alreadyProcessed):
            varName = tokenList[index]
            if(readSymbolTable(varName) != None):
                writeLine("push " + readSymbolTable(varName), fileToWrite) #varName
            index += 1 #skip varName

def compileSubroutineCall(tokenList, fileToWrite):
    global index
    global className

    numExpressions = 0

    if(index < len(tokenList) - 1):
        
        if(tokenList[index + 1] == "("): #subroutineName(expressionList)
            subroutineName = tokenList[index] #subroutineName
            index += 1 #skip subroutineName
            index += 1 #skip (
            
            writeLine("push pointer 0", fileToWrite) # <--
            
            if(tokenList[index] != ")"): #expressionList
                numExpressions = compileExpressionList(tokenList, fileToWrite)

            index += 1 #skip )

            #add this object to the argument
            numExpressions += 1

            writeLine("call " + className + "." + subroutineName + " " + str(numExpressions), fileToWrite)

        elif(tokenList[index + 1] == "."): #className|varName.subroutineName(expressionList)
            classVarName = tokenList[index] #className | varName
            index += 1 #skip className | varName
            index += 1 #skip .

            #this part deals with method calls
            potentialObject = readSymbolTable(classVarName) #this returns something like "local 3"
            objectType = readTypeSymbolTable(classVarName) #this returns something like "Point"

            if(potentialObject != None):
                writeLine("push " + potentialObject, fileToWrite)
                classVarName = objectType

            #subroutineName(expressionList)
            subroutineName = tokenList[index] #subroutineName
            index += 1 #skip subroutineName
            index += 1 #skip (
            
            if(tokenList[index] != ")"): #expressionList
                numExpressions = compileExpressionList(tokenList, fileToWrite)

            if(potentialObject != None):
                numExpressions += 1
                
            index += 1 #skip )

            writeLine("call " + classVarName + "." + subroutineName + " " + str(numExpressions), fileToWrite)

def compileExpressionList(tokenList, fileToWrite):
    global index
    numExpressions = 0

    compileExpression(tokenList, fileToWrite) #expression
    numExpressions += 1

    while(tokenList[index] == ","):
        index += 1 #skip ,
        compileExpression(tokenList, fileToWrite) #expression
        numExpressions += 1
    
    return numExpressions
    
def tokenType(token):
    if((token in keywordList) and (token == "true" or token == "false" or token == "null" or token == "this")):
        return "keywordConstant"
    
    elif token in keywordList:
        return "keyword"
    
    elif((token in symbolList) and token == "-" or token == "~"):
        return "unaryOp"

    elif token in symbolList:
        return "symbol"
    
    elif token.isdigit():
        return "integerConstant"

    elif token[0] == '"' and token[-1] == '"':
        return "stringConstant"

    elif len(re.findall("[a-zA-Z_.$:][\\w.$:]*", token)) > 0:
        return "identifier"
    
def isStatement(token):
    return (token == "let" or token == "if" or token == "while" or token=="do" or token == "return")
    
def writeLine(stringToWrite, fileToWrite):
    fileToWrite.write(stringToWrite + "\n")

def addSymbol(varName, varType, varKind):
    global staticCount
    global fieldCount
    global localCount
    global argCount

    if(varKind == "field"):
        classSymbolTable[varName] = (varType, varKind, fieldCount)
        fieldCount += 1
    elif(varKind == "static"):
        classSymbolTable[varName] = (varType, varKind, staticCount)
        staticCount += 1 
    elif(varKind == "local"):
        subSymbolTable[varName] = (varType, varKind, localCount)
        localCount += 1 
    elif(varKind == "arg"):
        subSymbolTable[varName] = (varType, varKind, argCount)
        argCount += 1

def readSymbolTable(name):
    #read from subroutine
    if(name in subSymbolTable):
        (varType, varKind, varCount) = subSymbolTable[name]
        if (varKind == "arg"):
            return "argument " + str(varCount)
        elif(varKind == "local"):
            return "local " + str(varCount)
    #read from class
    elif(name in classSymbolTable):
        (varType, varKind, varCount) = classSymbolTable[name]
        if (varKind == "static"):
            return "static " + str(varCount)
        elif(varKind == "field"):
            return "this " + str(varCount)
    else:
        return None

def readTypeSymbolTable(name):
    #read from subroutine
    if(name in subSymbolTable):
        (varType, varKind, varCount) = subSymbolTable[name]
        return varType
    #read from class
    elif(name in classSymbolTable):
        (varType, varKind, varCount) = classSymbolTable[name]
        return varType
    else:
        return None

def countVars(tokenList, curIndex):
    numVars = 0
    curIndex += 1 #skip the {
    while(tokenList[curIndex] == "var"):

        numVars += 1 #we have a var

        curIndex += 1 #skip var
        curIndex += 1 #skip type
        curIndex += 1 #skip varName

        while(tokenList[curIndex] == ","):
            curIndex += 1 #skip ,
            numVars += 1 #another valid var
            curIndex += 1 #skip varName
        
        curIndex += 1 #skip ;
    
    return numVars

def refreshSubCounts():
    global localCount
    global argCount
    global subSymbolTable

    localCount = 0
    argCount = 0
    subSymbolTable.clear()

main()