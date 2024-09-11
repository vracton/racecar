![image](https://github.com/user-attachments/assets/8ddb8564-94db-4fff-b3b4-5134dc44d4a1)


# Installation

1. Install Visual Studio Code and the python extension.
2. Install Python 3.9.7 (other versions may not work).
3. **WINDOWS ONLY** Enable Hyper-V (if you have it) and WSL.
4. **WINDOWS ONLY** Download Ubuntu from the Windows Store. Run it and do as prompted.
5. **WINDOWS ONLY** Download [X Server](https://sourceforge.net/projects/xming/).
6. **WINDOWS ONLY** Run the XLaunch app and in display settings, set the display number to `42`
7. Run the following commands to install the simulator and then do as prompted.
```bash
git clone https://github.com/MITRacecarNeo/racecar-neo-installer.git
bash racecar-neo-installer/racecar-student/scripts/setup.sh
racecar cd
code .
```
8. You can then create a new file using the code from this repository.
9. Then, run the simulator and enter a map.
10. Once doing so, open a terminal in VSCode and enter `racecar sim {FILE_NAME}.py`.

Enjoy!
