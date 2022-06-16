#! /usr/bin/env python3

from Log        import *

import datetime as dt

import os
import sys

EXIT_SUCCESS    = 0
EXIT_FAILURE    = 1

#   ------------------------------
#   |          _INFO             |
#   ------------------------------
class INFO:

    VERSION     = "v1.3.6"
    CREDITS     = "PsychicPenguin"
    LICENSE     = "GNU Public License 3.0"

    LOGO = [
        "   ____       _____                     ",
        "  |  _ \ _   |_   _|__ _ __ _ __ ___    ",
        "  | |_) | | | || |/ _ \ '__| '_ ` _ \   ",
        "  |  __/| |_| || |  __/ |  | | | | | |  ",
        "  |_|    \__, ||_|\___|_|  |_| |_| |_|  ",
        "         |___/                          ",
        ""
    ]


    # Return position after INFO.LOGO is drawn
    def Position():
        return (len(INFO.LOGO)+1)


    # Draw Box with current version
    def Version():
        BOX.Info([INFO.VERSION],color=f"{FG.CYAN}",style=BOX.STYLE.ROUND)


    # Draw Box with license
    def License():
        BOX.Info([INFO.LICENSE],color=f"{FG.CYAN}",style=BOX.STYLE.ROUND)
    

    # Draw Box with credits
    def Credits():
        BOX.Info([INFO.CREDITS],color=f"{FG.CYAN}",style=BOX.STYLE.ROUND)


#   ------------------------------
#   |         _UNICODE           |
#   ------------------------------
class UNICODE:

    TOPRIGHT    = ["╮","┓","╗","╮","-"]
    VERTICAL    = ["│","┃","║","╎","|"]
    BOTTOMLEFT  = ["╰","┗","╚","╰","-"]
    TOPLEFT     = ["╭","┏","╔","╭","-"]
    BOTTOMRIGHT = ["╯","┛","╝","╯","-"]
    HORIZONTAL  = ["─","━","═","╌","-"]


#   ------------------------------
#   |          _SYSTEM           |
#   ------------------------------
class SYSTEM:
    
    # Set sane default values
    OS      = "TempleOS" 
    USER    = "TerryADavis"
    NAME    = "HolyC"
    PATH    = "/"


    # Is run if sys.platform == win32
    def Windows():
        SYSTEM.OS   = "Windows"
        SYSTEM.USER = os.popen("echo %username%").read().rstrip("\r\n")
        SYSTEM.PATH = f"C:\\Users\\{SYSTEM.USER}\\appdata\\local\\{SYSTEM.NAME}\\"


    # Is run if sys.platform == linux
    def Linux():
        SYSTEM.OS   = "Linux"
        SYSTEM.USER = os.popen("echo $USER").read().rstrip("\n")
        SYSTEM.PATH = f"/home/{SYSTEM.USER}/.local/share/{SYSTEM.NAME}/"


    # Is run if sys.platform == darwnin
    def macOS():
        SYSTEM.USER = os.popen("echo $USER").read().rstrip("\n")
        SYSTEM.PATH = f"/Users/{SYSTEM.USER}/..."


    # Returns current date as dd:mm:yy
    def Date():
        return dt.date.today().strftime("%d.%m.%y")


    # Returns current time as HH:MM:SS
    def Time():
        return dt.datetime.now().strftime("%H:%M:%S")

#   ------------------------------
#   |          _STATUS           |
#   ------------------------------
class STATUS:

    # Left and Right texts in statusbar. indexed as SIDE[POSITION]
    LEFT    = [
        f"",
        f"{SYSTEM.PATH}"
    ]
    RIGHT   = [
        f"{INFO.VERSION}",
        f"{INFO.LICENSE}"
    ]

    TOP     = 0
    BOTTOM  = 1
    PADDING = "  "
    STYLE   = f"{FG.GREEN}{UTIL.REVERSE}"


    # Draw a status bar
    def Bar(bottom=False):
        # Save cursor and set position
        SaveCursor()
        SetCursor(0, TERM.Height() * int(bottom))

        # Set content to update automatically every frame
        # STATUS.LEFT[int(bottom)] = f"{SYSTEM.PATH}{SYSTEM.NAME}"

        # Create the line that will be printed as a status bar
        # It's like regex, easy to write, hard to read ... But it does make sense, I promise 
        textlength  = len(STATUS.LEFT[int(bottom)]) + len(STATUS.RIGHT[int(bottom)]) + len(STATUS.PADDING) * 2
        buffer      = " " * (TERM.Width() - textlength)
        msg         = f"{STATUS.PADDING}{STATUS.LEFT[int(bottom)]}{buffer}{STATUS.RIGHT[int(bottom)]}{STATUS.PADDING}" 

        TERM.Printc(f"{STATUS.STYLE}{msg}")
        RestoreCursor()

#   ------------------------------
#   |           _BOX             |
#   ------------------------------
class BOX:

    class STYLE:
        ROUND   = 0
        EDGY    = 1
        DOUBLE  = 2
        DOTTED  = 3


    # Draws a box around a text, centered in the terminal
    def Info(msg,color=f"{FG.CYAN}",style=0):
        # Set sane default value if called incorrectly
        if 0 > style > 3:
            style = 0

        padding     = " "
        length      = 0
        
        for line in msg:
            # Make the line even if uneven to avoid misplaced vertical lines
            if len(line) % 2:
                line += " "
            # Adjust padding accordingly
            if len(line) + len(padding) * 2 > length:
                length = len(line) + len(padding) * 2

        # Get starting position. It's really just terminal_width / 2 - box_width / 2
        pos         = f"{UTIL.RIGHT}" * int(TERM.Width() / 2 - length / 2)
        # Create the horizontal line as length of text + padding
        horizontal  = f"{UNICODE.HORIZONTAL[style]}" * (length + 2)

        # Draw Top Line
        TERM.Printc(f"{pos}{color}{UNICODE.TOPLEFT[style]}{horizontal}{UNICODE.TOPRIGHT[style]}{UTIL.RESET}\n")
        
        # Draw Middle Line(s) containing the text
        for line in msg:
            if len(line) % 2:
                line += " "
            buffer = " " * int((length - len(line) + len(padding) * 2) / 2)
            TERM.Printc(f"{pos}{color}{UNICODE.VERTICAL[style]}{buffer}{line}{buffer}{UNICODE.VERTICAL[style]}{UTIL.RESET}\n")

        # Draw Bottom Line
        TERM.Printc(f"{pos}{color}{UNICODE.BOTTOMLEFT[style]}{horizontal}{UNICODE.BOTTOMRIGHT[style]}{UTIL.RESET}\n")


    # Returns an array of answers
    def Prompt(msg,color=f"{FG.YELLOW}",style=1):
        # Set sane default value if called incorrectly
        if 0 > style > 3:
            style = 1

        answer      = [] 
        padding     = "  "
        length      = TERM.Width() - len(padding) * 2
        pos         = f"{UTIL.RIGHT}" * len(padding)
        horizontal  = f"{UNICODE.HORIZONTAL[style]}" * (length - len(padding))

        # Draw empty box
        TERM.Printc(f"{padding}{color}{UNICODE.TOPLEFT[style]}{horizontal}{UNICODE.TOPRIGHT[style]}{UTIL.RESET}\n")
        for txt in msg:
            buffer = " " * (length - len(padding))
            TERM.Printc(f"{padding}{color}{UNICODE.VERTICAL[style]}{buffer}{UNICODE.VERTICAL[style]}{UTIL.RESET}\n")
        TERM.Printc(f"{padding}{color}{UNICODE.BOTTOMLEFT[style]}{horizontal}{UNICODE.BOTTOMRIGHT[style]}{UTIL.RESET}\n")

        SaveCursor()
        
        # Go up until at top line of box
        for i in range(len(msg)+1):
            TERM.Printf(f"{UTIL.UP}")
        # Draw middle lines and append results of input() to answer[]
        for txt in msg:
           TERM.Printf(f"{padding}{color}{UNICODE.VERTICAL[style]}{padding}") 
           answer.append(input(f"{color}{txt} "))
           TERM.Printf(f"{UTIL.RESET}")
        
        RestoreCursor()

        return answer


#   ------------------------------
#   |          _PAGER            |
#   ------------------------------
class PAGER: # TODO: Make this piece of shit work

    STYLE = f"{UTIL.CLEARLINE}{UTIL.RESET}{UTIL.REVERSE}{UTIL.BOLD}"

    class KEYS:
        QUIT    = "q"
        PAGE    = "n"


    def Page(arr, length):
#        CursorOff()

        length = int(length)

        index = 0
        for line in arr:
            try:
                index += 1

                if index > length:
                    SetCursor(0,TERM.Height())

                    key = input(f"{PAGER.STYLE}Press RETURN to continue, CTRL+C to quit ...{UTIL.RESET}{UTIL.UP}")
                    match key:
                        case "n":   index = 0
                        case _:     continue

                TERM.Printc(f"{line}")
                TERM.Overlay()
            
            except KeyboardInterrupt:
                TERM.Printf("\n")
                break

        SaveCursor()
        SetCursor(0,TERM.Height())
        TERM.Printc("")
        RestoreCursor()
        CursorOn()


#   ------------------------------
#   |           _TERM            |
#   ------------------------------
class TERM:
    

    # Print a formatted message, no new line at the end
    def Printf(msg):
        print(f"{msg}{UTIL.RESET}",end="")
    

    # Print message and clear current line, no new line at the end
    def Printc(msg):
        TERM.Printf(f"{UTIL.CLEARLINE}{msg}")


    # Function to list entries in an array
    def List(items,color=f"{FG.GREEN}"):
        index = 0
        for item in items:
                # Indexstring still displaying line numbers nicely
                index       += 1
                indexstr    = " " * (3 - len(str(index))) + str(index)

                # Draw the final output
                TERM.Printc(f"{color} {indexstr} {UNICODE.VERTICAL[BOX.STYLE.DOUBLE]}{UTIL.RESET}  {item}\n")



    # Prints a feedback at the right side of the screen
    def Feedback(msg,color=f"{FG.GREEN}"):
        # Position is width - length of msg
        pos     = TERM.Width() - (len(msg) + 2)
        buffer  = f"{UTIL.RIGHT}" * pos
        TERM.Printc(f"{UTIL.UP}{buffer}{color}{UTIL.BOLD}{UTIL.REVERSE} {msg} {UTIL.RESET}\n")


    # Prompt the user to confirm a command. Use to prevent user from messing up
    def Confirm(msg):
        # Prompt user with msg and convert answer to bool
        success = bool("y" in (input(f"{UTIL.BOLD}{msg} [Y/n] ")).lower())
        # Set msg and color depending on value of $success
        msg     = "  Success!  " if success else " Discarded! "
        color   = f"{FG.GREEN}" if success else f"{FG.RED}"
        TERM.Feedback(msg,color=color)
        return success


    # Cleanly exit the program
    def Exit():
        # Clear screen
        Clear()
        # Reset cursor
        SetCursor(0,0)

        # Print full log
        for log in LOG.logs:
            TERM.Printf(f"{log}\n")

        # Quit 
        quit()


    # Returns the width of the terminal in columns
    def Width():
        return os.get_terminal_size().columns

    # Returns the height of the terminal in rows
    def Height():
        return os.get_terminal_size().lines


    # Print an overlay, Logo and Statusbar
    def Overlay():
        SaveCursor()

        SetCursor(0,0)
        
        # StatusBar
        STATUS.Bar(bottom=True)
        # Logobox
        BOX.Info(INFO.LOGO,color=f"{FG.GREEN}",style=BOX.STYLE.DOUBLE)

        RestoreCursor()


    # Initialize the module
    def Init():
        # this line makes ansi work on windows, doesn't hurt on unix-based systems either
        os.system("")
#        Clear()
#        Log(LVL.INFO, "Initializing PyCurse Module ...")

        # Operating System
 #       Log(LVL.INFO, "Checking Operating System ...")
        match sys.platform:
            case "win32":   SYSTEM.Windows()
            case "linux":   SYSTEM.Linux()
            case "darwin":
                SYSTEM.macOS()
                Log(LVL.ERROR, f"macOS is not yet supported")
                return EXIT_FAILURE
            case _:
                Log(LVL.ERROR, f"Operating System not supported: {UTIL.UNDERLINE}{sys.platform}")
                return EXIT_FAILURE 
  #      TERM.Feedback(f"{SYSTEM.OS}")

        # Create working directory if not already exists
        # if not FILE.Exists(f"{SYSTEM.PATH}"):
        #     FILE.MakeDirectory(f"{SYSTEM.PATH}")


        return EXIT_SUCCESS


#   ------------------------------
#   |         _SETTINGS          |
#   ------------------------------
class SETTINGS:

    def Load():
        Log(LVL.INFO, "Loading settings from file ...")
    
    
    def Save():
        Log(LVL.INFO, "Saving settings to file ...") 


#   ------------------------------
#   |        _INITIALIZE         |
#   ------------------------------
if __name__ == "__main__":
    if sys.argv[1] == "--version":
        print(INFO.VERSION)
        quit()

if TERM.Init() != EXIT_SUCCESS:
    Log(LVL.ERROR, "Failed to initialize module")
    TERM.Exit()

