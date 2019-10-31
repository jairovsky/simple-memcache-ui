import urwid
import sys
import logging
from zope.event import notify
from zope.event import subscribers

palette = [('bg', 'white', 'black'),
           ('banner', 'black', 'light gray'),
           ('warn', 'black', 'yellow'),
           ('text',   'white', 'black'),
           ('streak', 'black', 'dark blue'),
           ('line',   'black', 'light gray')]

class MainUI(urwid.WidgetWrap):

    def __init__(self):

        cols = urwid.Columns(
            [
                ('weight',4, KeyListWidget()),
                ('fixed', 1, urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')),
                ('weight',6, ContentDisplayPanel())
            ],
            dividechars=1,
            focus_column=0
        )

        super().__init__(urwid.AttrWrap(cols, 'bg'))

        subscribers.append(self._onevent)

    def _onevent(self, e):

        if e['name'] == 'refresh':
            notify({'name':'refresh-resp', 'data':self.refresh_items()})

        if e['name'] == 'item-clicked':
            notify({'name':'item-loaded', 'data':self.get_item(e['key'])})

        if e['name'] == 'item-delete':
            notify({'name':'item-deleted', 'data':self.del_item(e['key'])})

    def start(self):
        loop = urwid.MainLoop(self, palette, unhandled_input=handle_global_key)
        
        notify({'name': 'refresh'})
        
        loop.run()


class KeyListWidget(urwid.WidgetWrap):

    def __init__(self):
        
        self._contents = []
        self._update_list_box()

        subscribers.append(self._onevent)

    def _onevent(self, e):

        if e['name'] == 'refresh-resp':
            self._contents = e['data']
            self._update_list_box()

        elif e['name'] == 'delete':
            notify({'name': 'item-delete', 'key': self._w.focus.label})
            self._lw.remove(self._w.focus)


    def _update_list_box(self):
        self._lw = self._create_list_walker(self._contents)
        self._w = urwid.ListBox(self._lw)

    def _create_list_walker(self, items):

        if (len(items) == 0):
            widgets = [urwid.Text(('warn', u" no keys found ! "), align='center')]
        else:
            widgets = [urwid.Text(('banner', u"press enter to load key contents: "), align='center')]
        
        for k in items:
            widgets.append(KeyListItem(k))

        return urwid.SimpleFocusListWalker(widgets)


class KeyListItem(urwid.AttrWrap):

    def __init__(self, label):
        btn = urwid.Button(label)
        urwid.connect_signal(btn, 'click', self.on_click)
        super().__init__(btn, 'text', 'line')

    def on_click(self, data):
        notify({'name': 'item-clicked', 'key': self.label})


class ContentDisplayPanel(urwid.WidgetWrap):

    def __init__(self):
        blank = urwid.Divider()
        self.txt = urwid.Text(('text', ''), align='left')
        listbox_content = [
            self.txt
        ]
        
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
    
        super().__init__(listbox)

        subscribers.append(self._onevent)

    def _onevent(self, e):
        
        if e['name'] == 'item-loaded':
            self.txt.set_text(e['data'])


def handle_global_key(key):
    if key == 'q':
        raise urwid.ExitMainLoop()
    
    elif key == 'r':
        notify({'name': 'refresh'})

    elif key == 'd':
        notify({'name': 'delete'})

