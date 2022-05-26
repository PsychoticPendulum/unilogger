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
