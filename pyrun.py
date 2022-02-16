import os
import pygame

###################################################
DEBUG_LEVEL = 0 # 0: Info, 1: Warnings 2: Errors
SHORTCUTS_FOLDER = os.path.join(
    os.environ['LOCALAPPDATA'],
    'Pyrun',
)
###################################################

class Debugger:
    LV_LOG = 0
    LV_WARN = 1
    LV_ERR = 2

    def __init__(self, name):
        self.name = name

    def log(self, level, message):
        if DEBUG_LEVEL <= level:
            match level:
                case 0:
                    print('[INFO] %s' % message)
                case 1:
                    print('[WARN] %s' % message)
                case 2:
                    print('[ERR] %s' % message)

def get_shortcut_file(name):
    pass


def open_window():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False

def main():
    debug = Debugger('Main')

    debug.log(debug.LV_LOG,
        "Shortcuts Folder: %s" % SHORTCUTS_FOLDER)
    
    debug.log(debug.LV_LOG,
        "Exists: %s" % os.path.exists(SHORTCUTS_FOLDER))

    if not os.path.exists(SHORTCUTS_FOLDER):
        debug.log(debug.LV_WARN,
            "Cannot find shortcuts folder, generating")
        try:
            os.makedirs(SHORTCUTS_FOLDER)
        except OSError:
            debug.log(debug.LV_ERR,
                "Cannot create shortcuts folder")
            exit(1)

    debug.log(debug.LV_LOG,
        "Starting pygame window")
    open_window()
    debug.log(debug.LV_LOG,
        "Exit")

if __name__ == '__main__':
    main()
