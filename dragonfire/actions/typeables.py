#
# This file is part of Dragonfly.
# (c) Copyright 2007, 2008 by Christo Butcher
# Licensed under the LGPL.
#
#   Dragonfly is free software: you can redistribute it and/or modify it 
#   under the terms of the GNU Lesser General Public License as published 
#   by the Free Software Foundation, either version 3 of the License, or 
#   (at your option) any later version.
#
#   Dragonfly is distributed in the hope that it will be useful, but 
#   WITHOUT ANY WARRANTY; without even the implied warranty of 
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public 
#   License along with Dragonfly.  If not, see 
#   <http://www.gnu.org/licenses/>.
#

"""
    This file builds the mapping from key-name to Typeable instances.
"""


import win32con
from dragonfire.actions.keyboard import keyboard, Typeable


#---------------------------------------------------------------------------
# Mapping of name -> typeable.

symbols = {}

for i in xrange(33, 126):
    symbols[chr(i)] = keyboard.get_typeable(char=chr(i))


keys = {
    # Whitespace and editing keys
    "enter":            Typeable(code=win32con.VK_RETURN, name='enter'),
    "tab":              Typeable(code=win32con.VK_TAB, name='tab'),
    "space":            Typeable(code=win32con.VK_SPACE, name='space'),
    "backspace":        Typeable(code=win32con.VK_BACK, name='backspace'),
    "delete":           Typeable(code=win32con.VK_DELETE, name='delete'),
    "del":              Typeable(code=win32con.VK_DELETE, name='del'),

    # Modifier keys
    "shift":            Typeable(code=win32con.VK_SHIFT, name='shift'),
    "control":          Typeable(code=win32con.VK_CONTROL, name='control'),
    "ctrl":             Typeable(code=win32con.VK_CONTROL, name='ctrl'),
    "alt":              Typeable(code=win32con.VK_MENU, name='alt'),

    # Special keys
    "escape":           Typeable(code=win32con.VK_ESCAPE, name='escape'),
    "insert":           Typeable(code=win32con.VK_INSERT, name='insert'),
    "pause":            Typeable(code=win32con.VK_PAUSE, name='pause'),
    "win":              Typeable(code=win32con.VK_LWIN, name='win'),
    "apps":             Typeable(code=win32con.VK_APPS, name='apps'),
    "popup":            Typeable(code=win32con.VK_APPS, name='popup'),

    # Navigation keys
    "up":               Typeable(code=win32con.VK_UP, name='up'),
    "down":             Typeable(code=win32con.VK_DOWN, name='down'),
    "left":             Typeable(code=win32con.VK_LEFT, name='left'),
    "right":            Typeable(code=win32con.VK_RIGHT, name='right'),
    "pageup":           Typeable(code=win32con.VK_PRIOR, name='pageup'),
    "pgup":             Typeable(code=win32con.VK_PRIOR, name='pgup'),
    "pagedown":         Typeable(code=win32con.VK_NEXT, name='pagedown'),
    "pgdown":           Typeable(code=win32con.VK_NEXT, name='pgdown'),
    "home":             Typeable(code=win32con.VK_HOME, name='home'),
    "end":              Typeable(code=win32con.VK_END, name='end'),

    # Number pad keys
    "npmul":            Typeable(code=win32con.VK_MULTIPLY, name='npmul'),
    "npadd":            Typeable(code=win32con.VK_ADD, name='npadd'),
    "npsep":            Typeable(code=win32con.VK_SEPARATOR, name='npsep'),
    "npsub":            Typeable(code=win32con.VK_SUBTRACT, name='npsub'),
    "npdec":            Typeable(code=win32con.VK_DECIMAL, name='npdec'),
    "npdiv":            Typeable(code=win32con.VK_DIVIDE, name='npdiv'),
    "numpad0":          Typeable(code=win32con.VK_NUMPAD0, name='numpad0'),
    "np0":              Typeable(code=win32con.VK_NUMPAD0, name='np0'),
    "numpad1":          Typeable(code=win32con.VK_NUMPAD1, name='numpad1'),
    "np1":              Typeable(code=win32con.VK_NUMPAD1, name='np1'),
    "numpad2":          Typeable(code=win32con.VK_NUMPAD2, name='numpad2'),
    "np2":              Typeable(code=win32con.VK_NUMPAD2, name='np2'),
    "numpad3":          Typeable(code=win32con.VK_NUMPAD3, name='numpad3'),
    "np3":              Typeable(code=win32con.VK_NUMPAD3, name='np3'),
    "numpad4":          Typeable(code=win32con.VK_NUMPAD4, name='numpad4'),
    "np4":              Typeable(code=win32con.VK_NUMPAD4, name='np4'),
    "numpad5":          Typeable(code=win32con.VK_NUMPAD5, name='numpad5'),
    "np5":              Typeable(code=win32con.VK_NUMPAD5, name='np5'),
    "numpad6":          Typeable(code=win32con.VK_NUMPAD6, name='numpad6'),
    "np6":              Typeable(code=win32con.VK_NUMPAD6, name='np6'),
    "numpad7":          Typeable(code=win32con.VK_NUMPAD7, name='numpad7'),
    "np7":              Typeable(code=win32con.VK_NUMPAD7, name='np7'),
    "numpad8":          Typeable(code=win32con.VK_NUMPAD8, name='numpad8'),
    "np8":              Typeable(code=win32con.VK_NUMPAD8, name='np8'),
    "numpad9":          Typeable(code=win32con.VK_NUMPAD9, name='numpad9'),
    "np9":              Typeable(code=win32con.VK_NUMPAD9, name='np9'),

    # Function keys
    "f1":               Typeable(code=win32con.VK_F1, name='f1'),
    "f2":               Typeable(code=win32con.VK_F2, name='f2'),
    "f3":               Typeable(code=win32con.VK_F3, name='f3'),
    "f4":               Typeable(code=win32con.VK_F4, name='f4'),
    "f5":               Typeable(code=win32con.VK_F5, name='f5'),
    "f6":               Typeable(code=win32con.VK_F6, name='f6'),
    "f7":               Typeable(code=win32con.VK_F7, name='f7'),
    "f8":               Typeable(code=win32con.VK_F8, name='f8'),
    "f9":               Typeable(code=win32con.VK_F9, name='f9'),
    "f10":              Typeable(code=win32con.VK_F10, name='f10'),
    "f11":              Typeable(code=win32con.VK_F11, name='f11'),
    "f12":              Typeable(code=win32con.VK_F12, name='f12'),
    "f13":              Typeable(code=win32con.VK_F13, name='f13'),
    "f14":              Typeable(code=win32con.VK_F14, name='f14'),
    "f15":              Typeable(code=win32con.VK_F15, name='f15'),
    "f16":              Typeable(code=win32con.VK_F16, name='f16'),
    "f17":              Typeable(code=win32con.VK_F17, name='f17'),
    "f18":              Typeable(code=win32con.VK_F18, name='f18'),
    "f19":              Typeable(code=win32con.VK_F19, name='f19'),
    "f20":              Typeable(code=win32con.VK_F20, name='f20'),
    "f21":              Typeable(code=win32con.VK_F21, name='f21'),
    "f22":              Typeable(code=win32con.VK_F22, name='f22'),
    "f23":              Typeable(code=win32con.VK_F23, name='f23'),
    "f24":              Typeable(code=win32con.VK_F24, name='f24'),

    # Multimedia keys
    "volumeup":         Typeable(code=win32con.VK_VOLUME_UP, name='volumeup'),
    "volup":            Typeable(code=win32con.VK_VOLUME_UP, name='volup'),
    "volumedown":       Typeable(code=win32con.VK_VOLUME_DOWN, name='volumedown'),
    "voldown":          Typeable(code=win32con.VK_VOLUME_DOWN, name='voldown'),
    "volumemute":       Typeable(code=win32con.VK_VOLUME_MUTE, name='volumemute'),
    "volmute":          Typeable(code=win32con.VK_VOLUME_MUTE, name='volmute'),
    "tracknext":        Typeable(code=win32con.VK_MEDIA_NEXT_TRACK, name='tracknext'),
    "trackprev":        Typeable(code=win32con.VK_MEDIA_PREV_TRACK, name='trackprev'),
    "playpause":        Typeable(code=win32con.VK_MEDIA_PLAY_PAUSE, name='playpause'),
    "browserback":      Typeable(code=win32con.VK_BROWSER_BACK, name='browserback'),
    "browserforward":   Typeable(code=win32con.VK_BROWSER_FORWARD, name='browserforward'),
}
