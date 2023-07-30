from graphviz import Digraph
class Node():
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def isOperator(c):
    operators = ['*', '|', '^']
    if c in operators:
        return True
    else:
        return False

def isnonBinaryOperator(c):
    nonBinaryOperators = ['*']
    if c in nonBinaryOperators:
        return True
    else:
        return False

def buildTree(postfixExp):
    stack = []
    for c in postfixExp:
        if c == ' ':
            continue
        elif isOperator(c):
            if isnonBinaryOperator(c):
                right = stack.pop()
                stack.append(Node(c))
                stack[-1].right = right
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(Node(c))
                stack[-1].left = left
                stack[-1].right = right
        else:
            stack.append(Node(c))
    return stack[0]

def printTree(tree, level=0):
    if tree != None:
        printTree(tree.right, level+1)
        print(' ' * 4 * level + '->', tree.data)
        printTree(tree.left, level+1)

def getLevels(tree):
    if tree == None:
        return 0
    else:
        return max(getLevels(tree.left), getLevels(tree.right)) + 1
    
def graphTree(tree):
    tGraph = Digraph(comment='Syntactic tree', format='png')
    
    def addNode(node):
        if node:
            tGraph.node(str(id(node)), node.data)
            if node.left:
                tGraph.edge(str(id(node)), str(id(node.left)))
                addNode(node.left)
            if node.right:
                tGraph.edge(str(id(node)), str(id(node.right)))
                addNode(node.right)

    addNode(tree)
    return tGraph