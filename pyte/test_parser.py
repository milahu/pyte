# python3 -m src.pyte.pyte.test_parser

# ansi color codes https://gist.github.com/Prakasaka/219fe5695beeb4d6311583e79933a009

#from pyte.screens import Screen, DiffScreen, HistoryScreen, DebugScreen
from .screens import Screen, DiffScreen, HistoryScreen, DebugScreen

#from pyte.streams import Stream, ByteStream
from .streams import Stream, ByteStream

terminal_width = 40
terminal_height = 4

class CustomScreen(Screen):
    last_offset = 0
    def draw(self, *args, source=""):
        print("custom listener: draw", repr(args), "source", repr(source))
        super().draw(*args)
    def set_title(self, *args, source=""):
        print("custom listener: set_title", repr(args), "source", repr(source))
    def select_graphic_rendition(self, *args, source=""):
        print("custom listener: select_graphic_rendition", repr(args), "source", repr(source))

screen = CustomScreen(terminal_width, terminal_height)
stream = ByteStream(screen)



stream.feed(b"".join([
    b"\x1b", # esc = \e
    b"]", # osc
    b"2;new title", # params: 2, "new title"
    b"\x07", # bel = \a -> end of string

    b"\x1b", # esc
    b"[", # csi
    b"0;31", # params: 0, 31 -> red
    b"m", # select_graphic_rendition

    b"red", # text

    b"\x1b[0;32m", # esc csi green

    b"green", # text

    b"\x1b[0m", # reset style

    b"default", # text
]))

term_lines = screen.display[:] # copy array
for line_idx, line in enumerate(term_lines):
    print(f"{line_idx:4d} {line} ¶")

# m = esc.SGR
# pyte/escape.py
##: *Select graphics rendition*: The terminal can display the following
##: character attributes that change the character display without
##: changing the character (see :mod:`pyte.graphics`).
#SGR = "m"

# mapping = self.csi = { ... esc.SGR: "select_graphic_rendition", ... }

# event = esc.SGR = "m"
# attr = "select_graphic_rendition"
# dispatcher_dict[todo] = getattr(listener, attr)

# self.listener = screen

# -> \x1b[0;31m will call screen.select_graphic_rendition(0, 31)





# TODO difference next(stream._parser) vs stream._parser.send(b"x")

#print("next")
#taking_plain_text = next(stream._parser)
#print("tpt", taking_plain_text)
# TypeError: 'in <string>' requires string as left operand, not bytes

#print("send")
#taking_plain_text = stream._parser.send(b"xasdf")
#print("tpt", taking_plain_text)
# TypeError: 'in <string>' requires string as left operand, not bytes
