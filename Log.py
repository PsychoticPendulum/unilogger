#! /usr/bin/env python3

from ANSI import *

class LVL:
    INFO = 0
    WARNING = 1
    ERROR = 2

class LOG:
    logs = []

    def Log(lvl, txt): # Example: [TYPE]	Message
        print(UTIL.CLEARLINE, end="")
        
        match lvl:
            case LVL.INFO:      msg = f"{FG.GREEN}{UTIL.BOLD}[INFO]{UTIL.RESET}{FG.GREEN}\t\t{txt}{UTIL.RESET}"
            case LVL.WARNING:   msg = f"{FG.YELLOW}{UTIL.BOLD}[WARNING]{UTIL.RESET}{FG.YELLOW}\t{txt}{UTIL.RESET}"
            case LVL.ERROR:     msg = f"{FG.RED}{UTIL.BOLD}[ERROR]{UTIL.RESET}{FG.RED}\t\t{txt}{UTIL.RESET}"
            case _:             msg = f"{UTIL.REVERSE}{txt}{UTIL.RESET}"
        
        LOG.logs.append(msg)
        print(msg)


def Log(lvl, txt): # Example: [TYPE]	Message
    LOG.Log(lvl,txt)