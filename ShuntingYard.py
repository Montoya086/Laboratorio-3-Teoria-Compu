import re
from CreateTree import buildTree, printTree, getLevels,graphTree
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
def ShuntingYard (expression):
    closingBrackets = [")", "]", "}"]
    openingBrackets = ["(", "[", "{"]
    
    def isOperator(char):
        return char in {'|', '^', '*'}

    def precedence(char):
        if char == '|':
            return 1
        elif char == '^':
            return 2
        elif char == '*':
            return 3
        return 0

    def convertPlus(expression):
        i=0
        new_expression=""
        for c in expression:
            if c == '+':
                if expression[i-1] in closingBrackets:
                    for j in range(i-1, -1, -1):
                        if expression[j] in openingBrackets:
                            new_expression += expression[j:i] + "*"
                            break
            else:
                new_expression += c
            i+=1
        return new_expression

    def convertCharClass(expression):
        new_expression = ""
        flag = True
        i=0
        for c in expression:
            if flag:
                if c == '[':
                    new_expression += '('
                    flag = False
                elif c == ']':
                    new_expression += ')'
                else:
                    new_expression += c
            else:
                if expression[i+1] == ']':
                    new_expression += c
                    flag = True
                else:
                    new_expression += c + '|'
            i+=1
        return new_expression
    
    def convertInterrogation(expression):
        stack = []
        openBracketList=[]
        i=0
        for c in expression:
            if c == '?':
                if expression[i-1] == ')':
                    for j in range(i-1, -1, -1):
                        if expression[j] == ')':
                            stack.append(expression[j])
                        elif expression[j] == '(':
                            stack.pop()
                            if(len(stack) == 0):
                                openBracketList.append(j+1)
                                break
                else:
                    openBracketList.append(i-1)
                    
            i+=1
        
        newExpression = ""
        i=0
        for c in expression:
            if i in openBracketList:
                count = openBracketList.count(i)
                newExpression += '('*count+c
            elif c == '?':
                newExpression += c + ')'
            else:
                newExpression += c
            i+=1
                        

        return newExpression.replace('?', '|ε')
    
    def convertConcatenation(expression):

        pattern = r'(?<=[a-zA-Z0-9*.ε)\\])(?=[a-zA-Z0-9.(\\@ε])'
        expression = re.sub(pattern, '^', expression)

        pattern = r'(?<=[)\\@])(?=[(a-zA-Z0-9.ε\\@])'
        expression = re.sub(pattern, '^', expression)

        expression = expression.replace('\\^', '\\')

        i = 0
        new_expression = ""
        for c in expression:
            if i !=0 and i != len(expression)-1:
                if c in openingBrackets or c in closingBrackets:
                    if expression[i-1] == "\\":
                        if expression[i+1] != "^":
                            new_expression += c+"^"
                        else:
                            new_expression += c
                    else:
                        new_expression += c
                else:
                    new_expression += c
            else:
                new_expression += c
            i+=1

        return new_expression
    
    def convertRegex(expression):
        return convertConcatenation(convertInterrogation(convertCharClass(convertPlus(expression))).replace('E', 'ε'))
    
    print("-------------------------")
    print("Original expression: "+expression.replace('E', 'ε'))
    print("-------------------------")
    expression = convertRegex(expression)
    print("-------------------------")
    print("Explicit expression: "+expression)
    print("-------------------------")
    print("Steps: ")
    
    queue = []
    stack = []
    #ShuntingYard
    i=0
    for char in expression:
        if char.isalnum() or (char=="(" and expression[i-1] == "\\") or (char==")" and expression[i-1] == "\\"):
            if(char=="n"):
                if(expression[i-1]!="\\"):
                    queue.append(char)
                    print("Enqueue: "+char)
                else:
                    queue.append("\\"+char)
                    print("Enqueue: \\"+char)
            else:
                queue.append(char)
                print("Enqueue: "+char)
        elif isOperator(char):
            print("Operator \""+char+"\" found, evaluating precedence in stack...")
            while (stack and isOperator(stack[-1]) and precedence(stack[-1]) >= precedence(char)):
                c = stack.pop()
                print("Stack pop: "+c)
                queue.append(c)
                print("Enqueue: "+c)
            stack.append(char)
            print("Stack push: "+char)
            print("Operator \""+char+"\" successfully pushed to stack!")
        elif char == '(' and expression[i-1] != '\\':
            stack.append(char)
            print("Stack push: "+char)
        elif char == ')' and expression[i-1] != '\\':
            print("Open parenthesis found, searching for pair...")
            while stack and stack[-1] != '(':
                c=stack.pop()
                print("Stack pop: "+c)
                queue.append(c)
                print("Enqueue: "+c)
            c= stack.pop()
            print("Pair found!")
            print("Stack pop: "+c)
        i+=1

    while stack:
        c=stack.pop()
        print("Stack pop: "+c)
        queue.append(c)
        print("Enqueue: "+c)

    #End of ShuntingYard

    string=''.join(queue)
    
    res=""
    i = 0
    for c in string:  
        if(c=='\\'):
            if(string[i+1]=='n'):
                res += '\\'
            else:
                res += ''
        else:
            res += c
        i+=1

    return(res)
    

    



fixedlines = []
for line in open("InfixExp.txt"):
    fixedlines.append(line.replace(" ", "").replace("\n", ""))

j=0
for line in fixedlines:
    postfixExp = ShuntingYard(line)
    print("\n********************* Result *********************\n"+postfixExp+"\n*****************************************************")
    tree = buildTree(postfixExp)
    print("Syntactical tree:\n")
    level = ""
    for i in range(getLevels(tree)):
        level += "  L"+str(i)
    print(level+"\n")
    printTree(tree)
    treeGraph=graphTree(tree)
    treeGraph.render('./Graphs/SyntacticTree'+str(j+1), view=True)
    j+=1
