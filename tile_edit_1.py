from tkinter import *
from tkinter import ttk



class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

gui = Bunch()

def make_main_editor(gui):
    gui.tile_size = 16
    gui.cur = (0, 0)

    gui.root = Tk()
    gui.content = ttk.Frame(gui.root)
    gui.tile_view_group = make_tile_view(ttk.Frame(gui.content, borderwidth=2, relief="ridge"), state=gui)
    gui.right_menu_group = make_property_menu(ttk.Frame(gui.content, borderwidth=2, relief="groove"))
    
    gui.content.grid(sticky=(N, S, E, W))
    gui.tile_view_group.frame.grid(row=0, column=0, sticky=(N, S, E, W))
    gui.right_menu_group.frame.grid(row=0, column=1, sticky=(N, S, E, W))

    gui.root.columnconfigure(0, weight=1)
    gui.root.rowconfigure(0, weight=1)
    gui.content.rowconfigure(0, weight=1)
    gui.content.columnconfigure(0, weight=1)
    gui.content.columnconfigure(1, weight=0, minsize=300)

    gui.content.grid_configure(padx=2, pady=2)
    for child in gui.content.winfo_children():
        child.grid_configure(padx=2, pady=2)

def initialize_tile_canvas(c):
    canvas_items = Bunch()

    num_rows = 15
    num_cols = 30

    canvas_items.cells = []
    for row in range(num_rows):

        canvas_items.cells.append([])

        for col in range(num_cols):
            x1 = col * 16
            y1 = row * 16
            x2 = x1 + 16
            y2 = y1 + 16
            tile = Bunch()
            tile.rect = c.create_rectangle(x1, y1, x2, y2)
            # tile.text = 
            canvas_items.cells[row].append(tile)

    return canvas_items

def make_tile_view(frame, state):
    group = Bunch()
    group.frame = frame
    group.children = Bunch()

    c = group.children.canvas = Canvas(frame)
    c.config(background="white")

    c.grid(sticky=(N, S, E, W))

    c.bind("<Motion>", lambda e: mouse_movement_handler(state, e))

    group.canvas_items = initialize_tile_canvas(c)

    # group.canvas_items.cursor.config()

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    return group

def make_property_menu(frame):
    group = Bunch()
    group.frame = frame
    group.children = Bunch()

    group.children.tile_representation_label = ttk.Label(frame, text="Current tile representation:")
    group.children.tile_representation = ttk.Entry(frame)

    group.children.tile_meta_data_label = ttk.Label(frame, text="Meta data for current tile:")
    group.children.tile_meta_data = Text(frame, wrap='word')
    
    
    frame.columnconfigure(0, weight=1)
    
    group.children.tile_representation_label.grid(row=0, sticky=(W, E))
    group.children.tile_representation.grid(row=1, sticky=(N, S, E, W))
    
    group.children.tile_meta_data_label.grid(row=2, sticky=(W, E))
    group.children.tile_meta_data.grid(row=3, sticky=(N, S, E, W))
    frame.rowconfigure(3, weight=1)
    return group

def get_tile_coord(gui):
    return (gui.cur[0]//gui.tile_size, gui.cur[1]//gui.tile_size)

def mouse_movement_handler(gui, e):
    gui.cur = (e.x, e.y)
    print("<{}, {}>, <{}, {}>".format(*gui.cur, *get_tile_coord(gui)))

make_main_editor(gui)

gui.root.mainloop()
