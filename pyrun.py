import os
import pygame
import sys

###################################################
DEBUG_LEVEL = 2 # 0: Info, 1: Warnings 2: Errors
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
    debug = Debugger('Get Shortcut File')
    debug.log(debug.LV_LOG,
        "Getting Shortcut: %s" % name)

    for filename in os.listdir(SHORTCUTS_FOLDER):
        f = os.path.join(SHORTCUTS_FOLDER, filename)
        matches = filename.lower().find(name.lower(), 0, len(name.lower()))
        if os.path.isfile(f):
            debug.log(debug.LV_LOG,
                "Found file: %s" % filename)
            debug.log(debug.LV_LOG,
                "Matches: %s" % matches)
            if matches != -1:
                return f, filename.rsplit('.', 1)[0]

    return (None, None)


def start_shortcut(shortcut_dir):
    os.startfile(shortcut_dir)

def try_lookup_shortcut(name):
    debug = Debugger('Try Lookup Shortcut')

    # Testing
    """
    if len(sys.argv) < 2:
        debug.log(debug.LV_ERR,
            "Name argument must not be blank")
        exit(1)

    name = sys.argv[1]
    """
    if len(name) < 1:
        debug.log(debug.LV_ERR,
            "Name must not be a blank string")
        exit(1)

    (shortcut_file, shortcut_filename) = get_shortcut_file(name)
    if not shortcut_file:
        debug.log(debug.LV_ERR,
            "File `%s` cannot be found" % name)
        exit(1)

    success = start_shortcut(shortcut_file)

def open_window():
    debug = Debugger("Open Window")

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((500, 500), pygame.NOFRAME)
    

    font = pygame.font.Font('font.ttf', 20)
    request = ""
    placeholder = "Input text here"

    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        active = False
                    case pygame.K_RETURN:
                        try_lookup_shortcut(request)
                        active = False
                    case pygame.K_BACKSPACE:
                        if len(request) > 0:
                            request = request[:-1]
                            debug.log(debug.LV_LOG,
                                "Request: %s" % request)
                            (_, shortcut_filename) = get_shortcut_file(request)
                            if len(request) < 1:
                                placeholder = "Input text here"
                            elif shortcut_filename:
                                placeholder = shortcut_filename
                            else:
                                placeholder = ''

                    case _:
                        request += event.unicode
                        debug.log(debug.LV_LOG,
                            "Request: %s" % request)
                        (_, shortcut_filename) = get_shortcut_file(request)
                        if shortcut_filename:
                            placeholder = shortcut_filename
                        elif len(request) < 1:
                            placeholder = "Input text here"
                        else:
                            placeholder = ''

        screen.fill((40, 40, 40))


        placeholdersurface = font.render(placeholder, True, (80, 73, 69))
        textsurface = font.render(request, True, (235, 219, 178))

        screen.blit(placeholdersurface, (0, 0))
        screen.blit(textsurface, (0, 0))


        pygame.display.update()


def main():
    debug = Debugger('Main')

    debug.log(debug.LV_LOG,
        "Shortcuts Folder: %s" % SHORTCUTS_FOLDER)
    
    debug.log(debug.LV_LOG,
        "Folder Exists: %s" % os.path.exists(SHORTCUTS_FOLDER))

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
