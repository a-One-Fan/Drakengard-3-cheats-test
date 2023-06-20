# Drakengard-3-cheats

Here I will store some attempts for making basic cheats or whatever else for Drakengard 3 on RPCS3.

Currently, this repo includes a script that will let you fly around.
Flying into certain areas out-of-order may crash the game. Keep this in mind as RPCS3 currently does not have savestates working properly.

Here's a preview gif:

![flying preview](preview_fly.gif)

For using the script (control.py): Turn off any multiplayer games to not flag any anti-cheats. Get python (preferably 3.10), and cheat engine. Open up cheat engine and RPCS3. Run the game, get into a level, run the script, e.g. double click it. Follow its instructions.



# Stuff found so far

The recompiled code for what looks to be the player's final position is, in bytes:

C4 C1 79 7E C8 C5 FB 11 9D 28 01 00 00 48 8B 8D C0 00 00 00 48 89 4D 38 C5 F9 7E C1 C5 EB 58 95 48 01 00 00 C5 EB 5A D2 C5 EA 5A DA C5 F9 7E D2 C5 FB 11 9D 30 01 00 00 0F 38 F1 4C 18 54 44 0F 38 F1 44 18 58 0F 38 F1 54 18 5C

The juicy part is the 3 movs in sequence, to 300000000 (RPCS3's memory offset for the emulated memory) + rax + 54/58/5c. Sadly I have no idea how to track rax back to what it is.
The script uses this.

Additionally, I managed to find the recompiled code for the vertical rotation around the player for the camera:

0F 38 F0 8B 9C C4 A0 01 C5 EB 5A D2 C5 F9 6E F1 C5 EA 5A D2 C5 CA 5A F6 C5 F3 59 D2 C5 FB 11 B5 50 01 00 00 41 0F 38 F0 8C 18 5C D6 9A 01 C5 F9 6E F9 C5 C2 5A FF C4 E2 D1 B9 DF C5 FB 11 BD 58 01 00 00 C5 E3 5A DB C5 E2 5A DB C5 FB 58 C6 C5 FB 5A C0 C5 F3 59 DB C5 FA 5A C0 C5 E3 5A DB C5 EB 5A D2 C5 FB 11 85 28 01 00 00 C5 E2 5A E3 C5 EA 5A EA C5 F3 59 C0 C5 F9 7E D9 C4 C1 79 7E D0 C5 FB 5A C0 C5 FB 11 A5 38 01 00 00 C5 FB 11 AD 30 01 00 00 C5 FA 5A C8 C5 F9 7E C2 C5 FB 11 8D 20 01 00 00 0F 38 F1 4C 18 24 44 0F 38 F1 44 18 28 0F 38 F1 54 18 2C

The script does not use this.
Eventually, I will dig in more.