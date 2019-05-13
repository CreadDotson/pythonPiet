class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[-1]

    def __repr__(self):
        print(self.items)


class pietStack(object):

    def __init__(self):
        self.memory = Stack()

    def view_top(self):
        return self.memory.pop()

    def empty(self):
        return self.memory.isEmpty()

    def push(self, num):
        self.memory.push(num)

    def pop(self):
        self.memory.pop()

    def add(self):
        first = self.memory.pop()
        second = self.memory.pop()
        tot = first + second
        self.memory.push(tot)

    def subtract(self):
        first = self.memory.pop()
        second = self.memory.pop()
        tot = first - second
        self.memory.push(tot)

    def multiply(self):
        first = self.memory.pop()
        second = self.memory.pop()
        tot = first * second
        self.memory.push(tot)

    def divide(self):
        first = self.memory.pop()
        second = self.memory.pop()
        tot = first / second
        self.memory.push(tot)

    def mod(self):
        first = self.memory.pop()
        second = self.memory.pop()
        tot = first % second
        self.memory.push(tot)

    def negate(self):
        top = self.memory.pop()
        if top == 1:
            self.memory.push(0)
        elif top == 0:
            self.memory.push(1)
        else:
            self.memory.push(top)

    def greater(self):
        first = self.memory.pop()
        second = self.memory.pop()
        topBigger = first - second > 0
        num = 1 if topBigger else 0
        self.memory.push(num)

    def duplicate(self):
        num = self.memory.pop()
        self.memory.push(num)
        self.memory.push(num)

    def roll(self):
        # print(self.memory)
        first = self.memory.pop()
        second = self.memory.pop()
        tempStack = Stack()
        for i in range(second):
            temp = self.memory.pop()
            tempStack.push(temp)
        self.memory.push(first)
        for i in range(second):
            temp = tempStack.pop()
            self.memory.push(temp)

    def input(self):
        x = input('#!:')
        self.memory.push(x)

    def output(self):
        print(self.memory.pop())
        ##print(chr(self.memory.pop()))
        ##print(str(self.memory.pop()))
