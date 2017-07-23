#!/usr/bin/python

import telnetlib
import time
import sys

user = "admin"
password = "password"
modemIP = "192.168.68.1"
debugLogging = False

def connect(A):
    tnA = telnetlib.Telnet(A)
    logger(tnA.read_until('Login:', 5))
    tnA.write(user + '\n')
    logger(tnA.read_until('Password:', 5))
    tnA.write(password + '\n')
    logger(tnA.read_until('> ', 5))
    tnA.write("sh" + '\n')
    logger(tnA.read_until("# ", 5))
    return tnA

def disconnect(tn):
    tn.write("exit\n")
    tn.write("exit\n")
    time.sleep(3)
    logger(tn.read_very_eager())
    tn.close()
    return

def checkMasq(tn):
    tn.write("iptables -vnL -t nat | grep MASQUERADE | grep -v 192.168.68.0" + '\n')
    time.sleep(5)
    logger(tn.read_until('\n'))
    masqText = tn.read_until('# ')
    logger(masqText)
    logger(masqText.count('0.0.0.0/0'))
    if masqText.count('0.0.0.0/0') == 2:
        return True
    elif masqText.count('0.0.0.0/0') > 2:
        logger("More than two matches for 0.0.0.0/0! Aborting.")
        sys.exit("More than two matches for 0.0.0.0/0! Aborting.")
    else:
        return False

def setMasq(tn):
    tn.write("iptables -t nat -I POSTROUTING 1 -o ptm0.1 -j MASQUERADE" + '\n')
    logger(tn.read_until('\n'))
    time.sleep(3)
    return

def logger(msg):
    if debugLogging:
        x = str(msg)
        msglines = x.splitlines()
        for x in msglines:
            print("Debug: " + x)
    return msg

logger("About to connect.")
tnModem = connect(modemIP)
logger("Logged in, checking MASQ:")
masqPresent = checkMasq(tnModem)
logger(masqPresent)

if masqPresent:
    logger("MASQ check done, disconnecting:")
else:
    logger("MASQ check failed, adding MASQ line.")
    setMasq(tnModem)
    if not debugLogging:
        print("Modem was missing MASQUERADE line. Added.")

logger("Disconnecting.")
disconnect(tnModem)
logger("All done.")
