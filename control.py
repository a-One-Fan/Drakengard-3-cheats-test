from ctypes import *
from ctypes.wintypes import *
import struct
import time

import subprocess
import sys
subprocess.call([sys.executable, "-m", "pip","install","pynput"])

import pynput
from pynput.keyboard import Key as pk

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
WriteProcessMemory = windll.kernel32.WriteProcessMemory
CloseHandle = windll.kernel32.CloseHandle
GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId
FindWindowA = windll.user32.FindWindowA

PROCESS_ALL_ACCESS = 0x1F0FFF

fps = 60.0
spf = 1.0 / fps

def get_rpcs3_pid():
    pid = int(subprocess.check_output("powershell.exe Get-Process | Where {$_.ProcessName -Like \'rpcs3\'} | select Id | Format-Table -HideTableHeaders").decode())
    return pid

target_pid = get_rpcs3_pid()
if target_pid < 1:
    target_pid = int(input(f"Could not get PID of RPCS3 ({target_pid}); please enter it manually:"))
else:
    print(f"Found RPCS3 with pid {target_pid}.")

processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, target_pid)
if processHandle < 1:
    print("Could not open specified process.")
    exit()

def writeBEFloat(address, value):
    be_buffer = c_char_p(struct.pack('>f', value))
    written = c_size_t(0)
    WriteProcessMemory(processHandle, c_void_p(address), be_buffer, 4, byref(written))
    written = written.value
    if(written != 4):
        print("Could not properly write BE float! (", written, ")")
    return written

base_address = 0x24099E30
print("Keep in mind that this script, or cheat engine itself, may flag games' anti-cheat!\n\n")
print("Search for the following array of bytes (NOT within 30... to 32...) in cheat engine:\n\n")
print("C4 C1 79 7E C8 C5 FB 11 9D 28 01 00 00 48 8B 8D C0 00 00 00 48 89 4D 38 C5 F9 7E C1 C5 EB 58 95 48 01 00 00 C5 EB 5A D2 C5 EA 5A DA C5 F9 7E D2 C5 FB 11 9D 30 01 00 00 0F 38 F1 4C 18 54 44 0F 38 F1 44 18 58 0F 38 F1 54 18 5C")
print("\n\nAdd it to the address list. There are 3 mov lines in sequence, adding 0x54, 0x58 and 0x5C. Add a hardware breakpoint in the middle one. Copy RAX, and paste it here, then enter:\n")
base_address = int(input(), 16)
print("\nTo avoid annoying jitters while moving, nop the 3 mov lines (replace them with code that does nothing).")
print("Move with wasd and space/shift or q/e. ")
pos_address = 0x300000000 + base_address + 0x54
# 327FAA214
# 327FF6C64
# 327E41894
# C4 C1 79 7E C8 C5 FB 11 9D 28 01 00 00 48 8B 8D C0 00 00 00 48 89 4D 38 C5 F9 7E C1 C5 EB 58 95 48 01 00 00 C5 EB 5A D2 C5 EA 5A DA C5 F9 7E D2 C5 FB 11 9D 30 01 00 00 0F 38 F1 4C 18 54 44 0F 38 F1 44 18 58 0F 38 F1 54 18 5C
# ^ player pos
# 0F 38 F0 8B 9C C4 A0 01 C5 EB 5A D2 C5 F9 6E F1 C5 EA 5A D2 C5 CA 5A F6 C5 F3 59 D2 C5 FB 11 B5 50 01 00 00 41 0F 38 F0 8C 18 5C D6 9A 01 C5 F9 6E F9 C5 C2 5A FF C4 E2 D1 B9 DF C5 FB 11 BD 58 01 00 00 C5 E3 5A DB C5 E2 5A DB C5 FB 58 C6 C5 FB 5A C0 C5 F3 59 DB C5 FA 5A C0 C5 E3 5A DB C5 EB 5A D2 C5 FB 11 85 28 01 00 00 C5 E2 5A E3 C5 EA 5A EA C5 F3 59 C0 C5 F9 7E D9 C4 C1 79 7E D0 C5 FB 5A C0 C5 FB 11 A5 38 01 00 00 C5 FB 11 AD 30 01 00 00 C5 FA 5A C8 C5 F9 7E C2 C5 FB 11 8D 20 01 00 00 0F 38 F1 4C 18 24 44 0F 38 F1 44 18 28 0F 38 F1 54 18 2C
# ^ camera 1
# C5 F9 6E F9 C5 C2 5A FF C4 E2 D1 B9 DF C5 FB 11 BD 58 01 00 00 C5 E3 5A DB C5 E2 5A DB C5 FB 58 C6 C5 FB 5A C0 C5 F3 59 DB C5 FA 5A C0 C5 E3 5A DB C5 EB 5A D2 C5 FB 11 85 28 01 00 00 C5 E2 5A E3 C5 EA 5A EA C5 F3 59 C0 C5 F9 7E D9 C4 C1 79 7E D0 C5 FB 5A C0 C5 FB 11 A5 38 01 00 00 C5 FB 11 AD 30 01 00 00 C5 FA 5A C8 C5 F9 7E C2 C5 FB 11 8D 20 01 00 00 0F 38 F1 4C 18 24 44 0F 38 F1 44 18 28 0F 38 F1 54 18 2C
# camera 2
# C5 E3 5A DB C5 E2 5A DB C5 FB 58 C6 C5 FB 5A C0 C5 F3 59 DB C5 FA 5A C0 C5 E3 5A DB C5 EB 5A D2 C5 FB 11 85 28 01 00 00 C5 E2 5A E3 C5 EA 5A EA C5 F3 59 C0 C5 F9 7E D9 C4 C1 79 7E D0 C5 FB 5A C0 C5 FB 11 A5 38 01 00 00 C5 FB 11 AD 30 01 00 00 C5 FA 5A C8 C5 F9 7E C2 C5 FB 11 8D 20 01 00 00 0F 38 F1 4C 18 24 44 0F 38 F1 44 18 28 0F 38 F1 54 18 2C 48 83 C4 28 E9 1F 00 00 00 BA 1C 21 96 00 48 89 E9 E8 A7 0D 02 00 48 83 C4 28 C3 66 66 66 66 2E 0F 1F 84 00 00 00 00 00
# cmaera 3

player_setpos_bytes = bytes([0xC4, 0xC1, 0x79, 0x7E, 0xC8, 0xC5, 0xFB, 0x11, 0x9D, 0x28, 0x01, 0x00, 0x00, 0x48, 0x8B, 0x8D, 0xC0, 0x00, 0x00, 0x00, 0x48, 0x89, 0x4D, 0x38, 0xC5, 0xF9, 0x7E, 0xC1, 0xC5, 0xEB, 0x58, 0x95, 0x48, 0x01, 0x00, 0x00, 0xC5, 0xEB, 0x5A, 0xD2, 0xC5, 0xEA, 0x5A, 0xDA, 0xC5, 0xF9, 0x7E, 0xD2, 0xC5, 0xFB, 0x11, 0x9D, 0x30, 0x01, 0x00, 0x00, 0x0F, 0x38, 0xF1, 0x4C, 0x18, 0x54, 0x44, 0x0F, 0x38, 0xF1, 0x44, 0x18, 0x58, 0x0F, 0x38, 0xF1, 0x54, 0x18, 0x5C])
""" The assembly for what the player's final position is set to """

def all_found(list):
    for i in range(len(list)):
        if list[i] < 0:
            return False
    return True

def read_connected(chunk1, chunk2, chunksize, i):
    if i < chunksize:
        return chunk1[i][0]
    else:
        return chunk2[i-chunksize][0]

def maprange(oldmin, oldmax, newmin, newmax, val):
    fac = (val-oldmin)/(oldmax-oldmin)
    return newmin + fac*(newmax-newmin)

def scanMemory(the_bytes: list[bytes], chunksize = 1048576):
    results = [-1 for i in range(len(the_bytes))]
    chunk1 = create_string_buffer(chunksize)
    chunk2 = create_string_buffer(chunksize)
    bytes_read = c_size_t(0)

    start   = 0x0800000000
    end     = 0x3000000000
    i = start
    ReadProcessMemory(processHandle, c_void_p(i), chunk2, chunksize, byref(bytes_read))
    if bytes_read.value <= 0:
        print("Couldn't read memory!")
    lasttime = time.time_ns()
    while i < end:
        if not i % 0x5000000:
            print(f"Read 0x5mil ({maprange(start, end, 0, 100.0, i)}%, {(time.time_ns() - lasttime) / 1000000.0}ms)...")
            lasttime = time.time_ns()
        i += chunksize
        chunk1 = chunk2
        ReadProcessMemory(processHandle, c_void_p(i), chunk2, chunksize, byref(bytes_read))
        if bytes_read.value <= 0:
            print("Couldn't read memory!")
        for j in range(len(the_bytes)):
            ln = len(the_bytes[j])
            if results[j] >= 0:
                continue

            k = 0
            while k < chunksize:
                l = 0
                while l < ln:
                    lk = k + l
                    if lk < chunksize:
                        c = chunk1[lk][0]
                    else:
                        c = chunk2[lk - chunksize][0]
                    if c != the_bytes[j][l]:
                        break
                    l += 1
                if l == ln:
                    results[j] = i+k
                k += 1
        
        if all_found(results):
            break
    
    return results

# TODO?:
# nop the 3 movs
# mov [rip+???], rax
# sleep for spf
# read rip+???
# nop that out, we have pos_address

move = [[False, False], [False, False], [False, False]]
move_sensitivity = 20

stop = False

def get_kv(key):
    kv = [[False, False], [False, False], [False, False]]
    safechar = ''
    try:
        safechar = key.char
    except:
        pass

    kv[0][0] = safechar == 'w'
    kv[0][1] = safechar == 's'
    kv[1][0] = safechar == 'd'
    kv[1][1] = safechar == 'a'
    kv[2][0] = key == pk.space or safechar == 'e'
    kv[2][1] = key == pk.shift or safechar == 'q'

    return kv

def set_mov(list, use_or = True):
    for i in range(3):
        for j in range(2):
            if use_or:
                move[i][j] = move[i][j] or list[i][j]
            else:
                move[i][j] *= not list[i][j]

def key_pressed(key):
    if key == pk.esc:
        stop = True
    set_mov(get_kv(key))

def key_released(key):
    set_mov(get_kv(key), False)

pos = [-18000.0, -300.0, 4000.0]

#print("Scanning memory...")
#scan_res = scanMemory([player_setpos_bytes])
#scan_text = ["Player location"]
#print("Got results:")
#for i in range(len(scan_res)):
#    print(scan_text[i])
#    if scan_res[i] > 0:
#        print(hex(scan_res[i]))
#    else:
#        print("Didn't find")
#    print("")
#exit()

listener = pynput.keyboard.Listener(on_press=key_pressed, on_release=key_released)
listener.start()
#listener.join()
print("Working...")
while not stop:
    for i in range(3):
        for j in range(2):
            pos[i] += move[i][j] * move_sensitivity * (1.0 if j == 0 else -1.0)

    writeBEFloat(pos_address, pos[0])
    writeBEFloat(pos_address+4, pos[1])
    writeBEFloat(pos_address+8, pos[2])
    time.sleep(spf)

CloseHandle(processHandle)  