#!/usr/bin/python
import Image
import sys
from pietStack import pietStack


class pietInterpreter(object):
    """
    colors = [
        [0xFFC0C0, 0xFFFFC0, 0xC0FFC0, 0xC0FFFF, 0xC0C0FF, 0xFFC0FF],
        [0xFF0000, 0xFFFF00, 0x00FF00, 0x00FFFF, 0x0000FF, 0xFF00FF],
        [0xC00000, 0xC0C000, 0x00C000, 0x00C0C0, 0x0000C0, 0xC000C0]
    ]"""
    colors = [
        ["FFC0C0", "FFFFC0", "C0FFC0", "C0FFFF", "C0C0FF", "FFC0FF"],
        ["FF0000", "FFFF00", "00FF00", "00FFFF", "0000FF", "FF00FF"],
        ["C00000", "C0C000", "00C000", "00C0C0", "0000C0", "C000C0"]
    ]
    """
    black = 0xFFFFFF
    white = 0x000000
    """
    black = "FFFFFF"
    white = "000000"
    DP = 0  # 0-right, 1-down, 2-left, 3-up
    CC = True  # false = right, true = left
    codelValue = 0
    pointerLocation = [0, 0]
    stack = pietStack()

    def pointer(self):
        num = self.stack.view_top()
        if num == 0:
            return
        self.DP += num
        self.DP %= 4

    def codel_toggle(self):
        print('testing codel toggle')
        num = self.stack.view_top()
        while num > 0:
            self.CC = not self.CC
            num = num - 1

    functions = [
        [None, stack.push, stack.pop],
        [stack.add, stack.subtract, stack.multiply],
        [stack.divide, stack.mod, stack.negate],
        [stack.greater, pointer, codel_toggle],
        [stack.duplicate, stack.roll, stack.input],
        [stack.input, stack.output, stack.output]
    ]

    function_names = [
        [None, 'push', 'pop'],
        ['add', 'subtract', 'multiply'],
        ['divide', 'mod', 'negate'],
        ['greater', 'pointer', 'codel'],
        ['duplicate', 'roll', 'input'],
        ['input', 'output', 'output']
    ]

    def __init__(self, filename, debug=False):
        self.im = Image.open(filename)
        self.image = self.im.load()
        self.rgb_im = self.im.convert('RGB')
        # sys.stdout.write(str(self.im.size[0]) + '\n')
        # sys.stdout.write(str(self.im.size[1]))
        self.debug = debug

    def pointer_toggle(self):
        self.DP += 1
        self.DP %= 4

    def process_function(self, change, value):
        # print('change')
        # print(change)
        if change == [0,1]:
            self.stack.push(value)
            # print(value)
            return
        if change == [3,1]:
            self.pointer_toggle()
            return
        if change == [3,2]:
            self.codel_toggle()
            return
        else:
            self.functions[change[0]][change[1]]()

# takes two hex strings and gets the difference between them
    def get_change(self, first, second):
        startx = starty = endx = endy = 0
        for r in range(len(self.colors)):
            for c in range(len(self.colors[0])):
                if self.colors[r][c] == first:
                    startx = c
                    starty = r
                if self.colors[r][c] == second:
                    endx = c
                    endy = r
        if self.debug:
            print('endx: %d , endy: %d' % (endx, endy))
            print('startx: %d , starty: %d' % (startx, starty))
        diffx = endx - startx
        diffy = endy - starty
        if diffy < 0:
            diffy = diffy + 3
        if diffx < 0:
            diffx = diffx + 6
        if self.debug:
            print('function: ' + str(self.function_names[diffx][diffy]))
        return [diffx, diffy]

# checks if a coord is inside the image
    def isViable(self, testLoc):
        return (testLoc[0] >= 0 and testLoc[0] < self.im.size[0] and testLoc[1] >= 0 and testLoc[1] < self.im.size[1])

# convert rgb values to hex string
    def convert(self, tmp):
        r = tmp[0]
        g = tmp[1]
        b = tmp[2]
        hx = '{0:02x}{1:02x}{2:02x}'.format(r, g, b)
        return hx.upper()

# returns the hex string color of the coordinate
    def get_color(self, coord):
        r, g, b = self.rgb_im.getpixel((coord[0], coord[1]))
        if (r,g,b) == (0,0,0):
            return self.black
        if (r,g,b) == (255,255,255):
            pass
            # return self.white
        return self.convert([r,g,b])

# returns the direction of the DP
    def get_test_direction(self, DP):
        tmp = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        return tmp[DP]

    def list_contains(self, l, coord):
        for x in l:
            if x == coord:
                return True
        return False

# takes a coordinate and returns the list of coordinates in that codel
# returns None if the coordinate is not viable
    def get_codel(self, current_pointer):
        current_color = self.get_color(current_pointer)
        codel = [current_pointer]
        past_codel = [current_pointer]

        def flood(coord):
            if not self.isViable(coord):
                return
            for tst in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                tst_coord = [coord[0] + tst[0], coord[1] + tst[1]]
                if not self.isViable(tst_coord):
                    continue
                if self.list_contains(codel, tst_coord):
                    continue
                nxt_color = self.get_color(tst_coord)
                if nxt_color == current_color:
                    codel.append(tst_coord)

        while True:
            for coord in past_codel:
                flood(coord)
                # self.print_codel(codel)
            if codel == past_codel:
                break
            past_codel = codel
        return codel

# takes the pointer, gets the image, cc, and dp, to get the next pointer
# doesn't check for black blocks
    def get_next_edge(self, current_pointer, codel):

        def get_right_edge(codel):
            edge = [codel[0]]
            for coord in codel:
                if coord[0] > edge[0][0]:
                    edge = [coord]
                if coord[0] == edge[0][0]:
                    edge.append(coord)
            return edge

        def get_left_edge(codel):
            edge = [codel[0]]
            for coord in codel:
                if coord[0] < edge[0][0]:
                    edge = [coord]
                if coord[0] == edge[0][0]:
                    edge.append(coord)
            return edge

        def get_top_edge(codel):
            edge = [codel[0]]
            for coord in codel:
                if coord[1] < edge[0][1]:
                    edge = [coord]
                if coord[1] == edge[0][1]:
                    edge.append(coord)
            return edge

        def get_bottom_edge(codel):
            edge = [codel[0]]
            for coord in codel:
                if coord[1] > edge[0][1]:
                    edge = [coord]
                if coord[1] == edge[0][1]:
                    edge.append(coord)
            return edge

        def get_top(edge):
            nxt = edge[0]
            for coord in edge:
                if coord[1] < nxt[1]:
                    nxt = coord
            return nxt

        def get_bottom(edge):
            nxt = edge[0]
            for coord in edge:
                if coord[1] > nxt[1]:
                    nxt = coord
            return nxt

        def get_left(edge):
            nxt = edge[0]
            for coord in edge:
                if coord[0] < nxt[0]:
                    nxt = coord
            return nxt

        def get_right(edge):
            nxt = edge[0]
            for coord in edge:
                if coord[0] > nxt[0]:
                    nxt = coord
            return nxt

        #DP = 0  # 0-right, 1-down, 2-left, 3-up
        #CC = True  # false = right, true = left

        if not self.isViable(current_pointer):
            return
        # current_color = self.get_color(current_pointer)
        if self.DP == 0:
            edge = get_right_edge(codel)
            if self.CC:
                return get_top(edge)
            else:
                return get_bottom(edge)
        elif self.DP == 1:
            edge = get_bottom_edge(codel)
            if self.CC:
                return get_right(edge)
            else:
                return get_left(edge)
        elif self.DP == 2:
            edge = get_left_edge(codel)
            if self.CC:
                return get_bottom(edge)
            else:
                return get_top(edge)
        elif self.DP == 3:
            edge = get_top_edge(codel)
            if self.CC:
                return get_left(edge)
            else:
                return get_right(edge)
        return

# prints the coordinates in a grid to stdout
    def print_codel(self, codel):
        sys.stdout.write('\n')
        for x in range(self.im.size[1]):
            for y in range(self.im.size[0]):
                if [y, x] in codel:
                    sys.stdout.write('|88')
                else:
                    sys.stdout.write('|__')
            sys.stdout.write('|\n')

# main loop
    def start(self):
        counter = 8
        while counter > 0:
            codel = self.get_codel(self.pointerLocation)
            if self.debug:
                self.print_codel(codel)
            next_edge = self.get_next_edge(self.pointerLocation, codel)
            tst_dir = self.get_test_direction(self.DP)
            if(not next_edge or
            not self.isViable([next_edge[0] + tst_dir[0], next_edge[1] + tst_dir[1]]) or
            self.get_color([next_edge[0] + tst_dir[0], next_edge[1] + tst_dir[1]]) is self.black):
                if counter % 2 == 0:
                    self.CC = not self.CC
                else:
                    self.pointer_toggle()
                if self.debug:
                    print('CC: ' + str(self.CC))
                    print('DP: ' + str(self.DP))
                counter -= 1
                continue
            next_coord = [next_edge[0] + tst_dir[0], next_edge[1] + tst_dir[1]]
            change = self.get_change(self.get_color(self.pointerLocation), self.get_color(next_coord))
            # fun = self.functions[change[0]][change[1]]
            funName = self.function_names[change[0]][change[1]]
            self.process_function(change, len(codel))
            """
            if funName == 'push':
                fun(len(codel))
                print('pushing to stack')
                print(len(codel))
            else:
                fun()
            if self.debug:
                print(self.get_color(next_coord))
                print(next_coord)
                print(counter)
            """
            self.pointerLocation = next_coord
            counter = 8


filename = "progs/Piet_hello.png"
if len(sys.argv) > 1:
    filename = sys.argv[1]

inter = pietInterpreter(filename)
"""
inter.DP = 1
inter.CC = not inter.CC
codel = inter.get_codel([29, 12])
print('codel')
inter.print_codel(codel)
edge = inter.get_next_edge([29, 12])
print(edge)
inter.print_codel([edge])
"""
inter.start()
