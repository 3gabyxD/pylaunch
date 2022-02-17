import os
import pygame
import sys
import win32gui
import shutil

###################################################
DEBUG_LEVEL = 0 # 0: Info, 1: Warnings 2: Errors
SHORTCUTS_FOLDER = os.path.join(
    os.environ['LOCALAPPDATA'],
    'Pyrun',
)
PLACEHOLDER_TEXT = "pyrun"
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

    if len(name) < 1:
        debug.log(debug.LV_WARN,
            "`Name` should not be an empty string")
        return (None, None)

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

def get_placeholder(request, shortcut_filename=None):
    if len(request) < 1:
        return PLACEHOLDER_TEXT
    if shortcut_filename:
        return shortcut_filename
    return ''

def windowEnumerationHandler(hwnd, windows):
    windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def front(win_name):
    windows = []
    win32gui.EnumWindows(windowEnumerationHandler, windows)
    for i in windows:
        if i[1] == win_name:
            win32gui.ShowWindow(i[0],5)
            win32gui.SetForegroundWindow(i[0])
            break

def open_window():
    debug = Debugger("Open Window")
    debug.log(debug.LV_LOG,
        "Initialize Pygame")

    pygame.init()
    pygame.font.init()

    padding = 10
    font_size = 30

    screen = pygame.display.set_mode((600+padding*2, font_size+padding*2), pygame.NOFRAME)
    pygame.display.set_caption('Pyrun')

    font = pygame.font.Font('font.ttf', font_size)
    request = ""
    placeholder = PLACEHOLDER_TEXT

    debug.log(debug.LV_LOG,
        "Focusing Window")

    front('Pyrun')

    debug.log(debug.LV_LOG,
        "Focused Window")

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
                    case pygame.K_UP | pygame.K_TAB:
                        debug.log(debug.LV_LOG, "Up Arrow")
                        (_, shortcut_filename) = get_shortcut_file(request)
                        if shortcut_filename:
                            request = shortcut_filename
                    case pygame.K_BACKSPACE:
                        if len(request) > 0:
                            request = request[:-1]
                            debug.log(debug.LV_LOG,
                                "Request: %s" % request)
                            (_, shortcut_filename) = get_shortcut_file(request)
                            placeholder = get_placeholder(request, shortcut_filename)
                    case _:
                        request += event.unicode
                        debug.log(debug.LV_LOG,
                            "Request: %s" % request)
                        (_, shortcut_filename) = get_shortcut_file(request)
                        placeholder = get_placeholder(request, shortcut_filename)

        # Rendering
        screen.fill((40, 40, 40))

        placeholdersurface = font.render(placeholder[len(request):], True, (80, 73, 69))
        color = (235, 219, 178)
        if len(placeholder) < 1:
            color = (204, 36, 29)
        elif placeholder == request:
            color = (152, 152, 26)

        textsurface = font.render('> ' + request, True, color)

        screen.blit(placeholdersurface, (padding + textsurface.get_width(), padding))
        screen.blit(textsurface, (padding, padding))

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

    if len(sys.argv) > 1:
        func = sys.argv[1]
        if func == "reg":
            debug.log(debug.LV_LOG,
                "Running `reg`")

            if len(sys.argv) < 3:
                debug.log(debug.LV_ERR,
                    "Path missing")
                exit(1)

            dir = sys.argv[2]
            if not os.path.exists(dir):
                debug.log(debug.LV_ERR,
                    "Directory path does not exist")

            debug.log(debug.LV_LOG,
                "Directory path: %s" % os.path.basename(dir))
            for fn in os.listdir(dir):
                debug.log(debug.LV_LOG,
                    "File: %s" % fn)
                if fn.rsplit('.', 1)[1] == 'lnk':
                    debug.log(debug.LV_LOG,
                        "File `%s` is a shortcut" % fn)
                    shutil.copy(os.path.join(dir, fn), SHORTCUTS_FOLDER)
                    debug.log(debug.LV_LOG,
                        "Copied file")


    else:
        debug.log(debug.LV_LOG,
            "Starting pygame window")
        open_window()
        debug.log(debug.LV_LOG,
            "Exit")

if __name__ == '__main__':
    main()
