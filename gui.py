import tkinter
import time
from game import Engine

class MockEngine:
    """Mock for developing frontend"""
    def __init__(self):
        self.count = 0

    def get_next(self):
        self.count += 1
        template = [
                [0,0,0,0],
                [0,0,0,0],
                [0,2,4,8],
                [16,32,64,128]]

        return [[self.count * item for item in row] for row in template]

def color_from_num(num):
    """Returns a string color to use for the tile, given numeric val"""
    val = int(num)
    if val == 0:
        return "snow3"
    elif val <= 2:
        return "snow1"
    elif val <= 4:
        return "pale goldenrod"
    elif val <= 8:
        return "salmon1"
    elif val <= 16:
        return "coral1"
    elif val <= 32:
        return "salmon"
    elif val <= 64:
        return "red"
    else:
        return "gold"


def run(engine):
    """Main loop of function. Run until game is finished"""
    top = tkinter.Tk()
    top.configure(background="grey")
    
    labels = []
    for r in range(4):
        row = []
        for c in range(4):
            row.append(tkinter.StringVar())
        labels.append(row)

    state = engine.get_next() #initial state
    frames = []
    for r in range(4):
        row = []
        for c in range(4):
            row.append(None)
        frames.append(row)

    for r in range(4):
        for c in range(4):
            f = tkinter.LabelFrame(top, height=200, width=200)
            f.grid(row=r,column=c)
            l = tkinter.Label(f, textvariable=labels[r][c], width=10, height=5, bg='snow3')
            l.pack()
            frames[r][c] = l

    start = time.time()
    printed = False
    while True:
        new_state = engine.get_next()
        if new_state != None:
            state = new_state
        else:
            if not printed:
                print(time.time() - start)
                printed = True
        for r in range(4):
            for c in range(4):
                labels[r][c].set(str(state[r][c]) if state[r][c] != 0 else "")
                frames[r][c].configure(bg=color_from_num(state[r][c]))

        top.update_idletasks()
        top.update()

run(Engine())