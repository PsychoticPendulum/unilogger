#! /usr/bin/env python3

from PyTerm import *


class CLI:

    CMD     = ""
    CMDLIST = [""] * 9
    POS     = 0
    PROMPT  = f"{UTIL.CLEARLINE}{UTIL.BOLD}"


    # Display last command(s)
    def LastCommand():
        SaveCursor()

        # Create Commandstack
        if len(CLI.CMD):
            CLI.CMDLIST.append(CLI.CMD)
            if len(CLI.CMDLIST) >= 10:
                del CLI.CMDLIST[0]

        SetCursor(0,0)
        # Print commandstack
        for CMD in CLI.CMDLIST:
            TERM.Printf(f"{FG.GREEN}{CMD}\n")

        RestoreCursor()


    # Throw warning if command does not exist
    def UnknownCommand(cmd):
        Log(LVL.WARNING, f"Unknown command: {UTIL.UNDERLINE}{cmd}")
        # Add command to commandstack, but make it red
        CLI.CMD = f"{FG.RED}{CLI.CMD}"
        # Print message telling user how to access the help menu
        TERM.Printf(f"Type {UTIL.UNDERLINE}help{UTIL.RESET} for a list of commands\n")


class COMMAND:
    
    # Adds another entry to 
    def Entry():
        SetCursor(0,INFO.Position()+1)
        TERM.Printc("\n")
        
        # Create questions array
        questions = [
            "What?                     ",
            "How much?                 "
        ]
    
        try:
            # Prompt user for input
            answers = BOX.Prompt(questions,color=f"{FG.WHITE}")
            # Confirm input, write to file
            if TERM.Confirm("Do you want to write these changes? "):
                FILE.Write(answers, f"{SYSTEM.PATH}{SYSTEM.NAME}")

        # Give user a way to exit out of this menu without selecting anything    
        except KeyboardInterrupt:
            return
    

    # Change the file that is currently worked on
    def File():
        # List contents of directory for better overview of what files already exist
        COMMAND.List()

        TERM.Overlay()
        SetCursor(0,INFO.Position()+1)
        TERM.Printc("\n")
        
        try:
            # Prompt user for input, set file to input
            file = BOX.Prompt(["What file will you be working on? "],color=f"{FG.WHITE}")
            SYSTEM.NAME = file[0]
    
        # Give user a way to exit out of this menu without selecting anything    
        except KeyboardInterrupt:
            return


    # Read contents of currently selected file    
    def Read():
        FILE.Read(f"{SYSTEM.PATH}{SYSTEM.NAME}",csv=True)


    # List contents of current directory
    def List():
        FILE.List(f"{SYSTEM.PATH}")


    # Delete currently selected file    
    def Delete():
        FILE.Delete(f"{SYSTEM.PATH}{SYSTEM.NAME}")
    

    # Open file in users main editor
    def Open():
        editor = os.popen("echo $EDITOR").read().rstrip("\n")
        os.system(f"{editor} {SYSTEM.PATH}{SYSTEM.NAME}")

#   ------------------------------
#   |           _HELP            |
#   ------------------------------
class HELP:

    # Array of commands and their respective tooltips
    COMMANDS = [
        f"{UTIL.BOLD}help            {UTIL.RESET}{UTIL.ITALICS}Show list of commands",
        f"{UTIL.BOLD}exit            {UTIL.RESET}{UTIL.ITALICS}Close this program",
        f"{UTIL.BOLD}clear           {UTIL.RESET}{UTIL.ITALICS}Clear the screen",
        "",
        f"{UTIL.BOLD}entry           {UTIL.RESET}{UTIL.ITALICS}Add another entry",
        "",
        f"{UTIL.BOLD}read            {UTIL.RESET}{UTIL.ITALICS}Read contents of file",
        f"{UTIL.BOLD}list            {UTIL.RESET}{UTIL.ITALICS}List current directory",
        f"{UTIL.BOLD}delete          {UTIL.RESET}{UTIL.ITALICS}Delete current file",
        f"{UTIL.BOLD}file            {UTIL.RESET}{UTIL.ITALICS}Change current file",
        f"{UTIL.BOLD}open            {UTIL.RESET}{UTIL.ITALICS}Open current file in editor",
        "",
        f"{UTIL.BOLD}version         {UTIL.RESET}{UTIL.ITALICS}Display current version",
        f"{UTIL.BOLD}credits         {UTIL.RESET}{UTIL.ITALICS}Display credits",
        f"{UTIL.BOLD}license         {UTIL.RESET}{UTIL.ITALICS}Display license",
    ]

    # Draw Help Menu
    def Help():
        TERM.Printc(f"\n{UTIL.UNDERLINE}List of available commands:\n\n")
        
        index = 0
        for COMMAND in HELP.COMMANDS:
            # Indexstring is to display line numbers: 12 | command ... tooltip
            index       += 1
            indexstr    = " " * (3 - len(str(index))) + str(index) 

            TERM.Printc(f"{FG.CYAN} {indexstr} {UNICODE.VERTICAL[1]}{UTIL.RESET}  {COMMAND}\n")


#   ------------------------------
#   |          _FILES            |
#   ------------------------------
class FILE:


    def Read(file, csv=False):
        try:
            f = open(file, "r")

            index = 0
            # Vertical padding
            TERM.Printc("\n")
            # Draw information about what is being done
            TERM.Printc(f"Listing contents of: {UTIL.UNDERLINE}{file}\n\n")

            # Go through file line by line
            for line in f.readlines():
                # Indexstring is to display line numbers: 12 | command ... tooltip
                index       += 1
                indexstr    = " " * (3 - len(str(index))) + str(index)
                # Remove newline character from every line
                line        = line.rstrip("\n")

                # Handle csv files properly 
                if csv:
                    parts = line.split(",")

                    # Print line index
                    TERM.Printc(f"{FG.RED} {indexstr} {UNICODE.VERTICAL[BOX.STYLE.EDGY]}{UTIL.RESET}  ")

                    # Print line
                    for part in parts:
                        if index == 1: print(f"{UTIL.REVERSE}",end="")
                        # Buffer is 16 for each entry of csv
                        if len(part): buffer = " " * (16 - len(part))
                        else: buffer = ""
                        TERM.Printf(f"{part}{buffer}")

                else:
                    # If file is not an csv, just print the line
                    TERM.Printc(f"{FG.RED} {indexstr} {UNICODE.VERTICAL[BOX.STYLE.EDGY]}{UTIL.RESET}  {line}")

                TERM.Printf("\n")

            f.close()

        except PermissionError:
            Log(LVL.ERROR, f"Insufficient permissions to read: {UTIL.BOLD}{file}")
        
        except FileNotFoundError:
            Log(LVL.ERROR, f"File does not exist: {UTIL.BOLD}{file}")
    

    def Write(msg, file, csv=False):
        
        if not FILE.Exists(file):
            
            # Warn if file does not exist. Prompt to create file. 
            Log(LVL.WARNING, "File does not exist ...") 
            if not TERM.Confirm("Do you want to create it?"):
                return

            # Ask for headline of file 
            answer = BOX.Prompt(["Enter header line: "],color=f"{FG.WHITE}")
            answer = answer[0]

            # Actually write contents to file
            try:
                f = open(file, "w")
                f.write(f"Date,Time,{answer}")
                f.close()
            
            # TODO: Add exception handling
            except:
                Log(LVL.ERROR, "Something happenend! The devs have not yet added proper handling of this error.")
                return

        try:
            f = open(file, "a")

            # Always add Date and Time to entry
            f.write(f"\n{SYSTEM.Date()},{SYSTEM.Time()},")
            
            # Writing is generally done in csv style (as of now)
            for txt in msg:
                f.write(f"{txt},")

            f.close()
        
        except PermissionError:
            Log(LVL.ERROR, f"Insufficient permissions to read: {UTIL.BOLD}{file}")
        
        except FileNotFoundError:
            Log(LVL.ERROR, f"File does not exist: {UTIL.BOLD}{file}")

        except IsADirectoryError:
            Log(LVL.ERROR, f"File is a directory: {UTIL.BOLD}{file}")


    def List(directory):
        try:
            # Create array containing all files
            files = os.listdir(directory)
            index = 0

            # Draw header line explaining what is being done
            TERM.Printc("\n")
            TERM.Printc(f"Listing the contents of: {UTIL.UNDERLINE}{directory}\n\n")

            # Create two arrays to seperate directories from regular files
            directories = []
            logfiles = []

            # Fill the arrays according to the filetypes
            for file in files:
                # The currently selected file will be drawn in reversed colors
                style = "" 
                if file == SYSTEM.NAME: style += f"{UTIL.REVERSE}"
                if os.path.isdir(f"{SYSTEM.PATH}{file}"):   directories.append(f"  {UTIL.BOLD}{FG.YELLOW}{style}{file}")
                else:                                       logfiles.append(f"  {style}{file}")

            # Now merge the arrays for easier iteration
            files = directories
            for logfile in logfiles:
                files.append(f"{logfile}")

            for file in files:
                # Indexstring still displaying line numbers nicely
                index       += 1
                indexstr    = " " * (3 - len(str(index))) + str(index)

                # Draw the final output
                TERM.Printc(f"{FG.MAGENTA} {indexstr} {UNICODE.VERTICAL[BOX.STYLE.EDGY]}{UTIL.RESET}  {file}\n")
        
        except PermissionError:
            Log(LVL.ERROR, f"Insufficient permissions to read: {UTIL.BOLD}{file}")
        
        except FileNotFoundError:
            Log(LVL.ERROR, f"File does not exist: {UTIL.BOLD}{file}")


    def Delete(file,nowarn=False):

        # Warn the user that files are going to be destroyed
        if not nowarn:
            Log(LVL.WARNING, f"You are about to delete {UTIL.UNDERLINE}{file}")
            if not TERM.Confirm("Do you want to continue?"):
                return

        try:
            os.remove(file)
        
        except PermissionError:
            Log(LVL.ERROR, f"Insufficient permissions to read: {UTIL.BOLD}{file}")
        
        except FileNotFoundError:
            Log(LVL.ERROR, f"Directory does not exist: {UTIL.BOLD}{file}")

        except IsADirectoryError:
            # Warn the user that this might be a bad idea, like TikTok, but worse
            Log(LVL.WARNING, "File is a directory!")
            # Give user another chance to abort
            if not TERM.Confirm(f"Are you {UTIL.BOLD}really{UTIL.RESET} sure you want to do this?"):
                return
            # Get list of files in that directory
            files = os.listdir(f"{file}")
            # Iterate through every file
            for subject in files:
                Log(LVL.INFO, f"Deleting {UTIL.UNDERLINE}{subject}")
                # Use recursion to delete subfolders etc.
                FILE.Delete(f"{file}/{subject}",nowarn=True)
            os.rmdir(file)


    def Exists(path):
        return os.path.exists(path)


    def MakeDirectory(path):
        if FILE.Exists(path):
            Log(LVL.WARNING, f"Directory already exists: {UTIL.BOLD}{path}")
            return

        try:
            os.mkdir(path)
        
        except PermissionError:
            Log(LVL.ERROR, f"Insufficient permissions to write in: {UTIL.BOLD}{path}")



def Prompt():
    TERM.Overlay()

    SetCursor(0, CLI.POS)
    CLI.LastCommand()
    CLI.CMD = input(f"{CLI.PROMPT}>> {UTIL.RESET}")

    SetCursor(0,TERM.Height()+1)
    match CLI.CMD.lower():
        # Basic terminal commands
        case "help":    HELP.Help()
        case "clear":   Clear()
        case "exit":    TERM.Exit()

        # Dosage functions
        case "entry":   COMMAND.Entry()

        # File handling
        case "file":    COMMAND.File()
        case "list":    COMMAND.List()
        case "delete":  COMMAND.Delete()
        case "read":    COMMAND.Read()
        case "open":    COMMAND.Open()
        # Info
        case "version": INFO.Version()
        case "credits": INFO.Credits()
        case "license": INFO.License()

        # In case the command is invalid
        case "":        print(f"{UTIL.CLEARLINE}")
        case _:         CLI.UnknownCommand(CLI.CMD)


def Init():

    INFO.LOGO = [
        f"    _ᓚᘏᗢ_       _ _                    ",
        f"   | | | |_ __ (_) |    ___ᓚᘏᗢ__ _     ",
        f"   | | | | '_ \| | |   / _ \ / _` |    ",
        f"   | |_| | | | | | |__| (_) | (_| |    ",
        f"    \___/|_| |_|_|_____\___/ \__, |    ",
        f"                             |___/     ",
        f"{INFO.VERSION} by {INFO.CREDITS}"
    ]

    SYSTEM.PATH = f"/home/{SYSTEM.USER}/.log/"

    # Choose file
    Clear()
    pos = 13
    SetCursor(0,pos)
    SetCursor(0,pos-3)
    COMMAND.File()

    CLI.POS = len(INFO.LOGO)+2

    while True:

        try:
            Prompt()

        except KeyboardInterrupt:
            Log(LVL.WARNING, "Exiting due to KeyboardInterrupt ...")
            TERM.Exit()


if __name__ == "__main__":
    Init()
