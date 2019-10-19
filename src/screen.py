import urwid
import sys
import logging

logging.basicConfig(filename='log.txt',level=logging.DEBUG,format='%(asctime)s %(message)s')

palette = [('bg', 'white', 'black'),
           ('banner', 'black', 'light gray'),
           ('text',   'white', 'black'),
           ('streak', 'black', 'dark blue'),
           ('line',   'black', 'light gray')]


class MainWindow(urwid.WidgetWrap):

    def __init__(self, on_update, on_get_key):
        
        self.keys = KeyListWidget(on_update, on_get_key)
        self.content = ContentDisplayPanel()
        # self.ctrl = ctrl

        cols = urwid.Columns(
            [
                ('weight',4, self.keys),
                ('fixed', 1, urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')),
                ('weight',6, self.content)
            ],
            dividechars=1,
            focus_column=0)

        cols = urwid.AttrWrap(cols, 'bg')

        super().__init__(cols)


class KeyListWidget(urwid.WidgetWrap):

    def __init__(self, on_update, on_get_key):
        self.contents = []
        
        self._on_update = on_update
        self._on_get_key = on_get_key
        self._update_list_box()

    def _update_list_box(self):
        self.contents = self._on_update()
        lw = self._create_list_walker(self.contents)
        self._w = urwid.ListBox(lw)

    def _create_list_walker(self, items):

        widgets = [urwid.Text(('banner', u" Current keys: "), align='center')]
        for k,d in items:
            widgets.append(KeyListItem(k,d, self._on_get_key))


        return urwid.SimpleFocusListWalker(widgets)

    def add_key(self, k, data):
        self.contents.append((k, data))
        self._update_list_box()


class KeyListItem(urwid.AttrWrap):

    def __init__(self, label, data, on_get_key):
        btn = urwid.Button(label, user_data=data)
        urwid.connect_signal(btn, 'click', on_get_key, data)
        super().__init__(btn, 'text', 'line')
        




class ContentDisplayPanel(urwid.WidgetWrap):

    def __init__(self):
        blank = urwid.Divider()
        txt = urwid.Text(('text', ''), align='left')
        listbox_content = [
            txt
        ]
        
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
    
        super().__init__(listbox)


def handle_global_key(key):
    if key in ('q'):
        raise urwid.ExitMainLoop()

def start(on_update, on_get_key):
    w = MainWindow(on_update, on_get_key)
    loop = urwid.MainLoop(w, palette, unhandled_input=handle_global_key)
    loop.run()
    return w

