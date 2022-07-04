import sys, platform
import binascii, subprocess
from secrets import token_urlsafe
from string import digits, punctuation

# -------------------------------------- #
#  BANNER                                #
# -------------------------------------- #
print("\033[93m")
print("  __ )   |               |        \ \     /     _)  |")
print("  __ \   |   _` |   __|  |  /      \ \   /  _ \  |  |")
print("  |   |  |  (   |  (       <        \ \ /   __/  |  |")
print(" ____/  _| \__,_| \___| _|\_\        \_/  \___| _| _____|")
print("                                       v1.1.5\033[00m")

# -------------------------------------- #
#  SETUP                                 #
# -------------------------------------- #
# Check args:
if len(sys.argv) != 2:
    print("\n\033[94m[*]\033[00m Usage: {0} path/to/file.py".format(sys.argv[0]))
    sys.exit()
# Check System:
if platform.system() != "Linux":
    print("\n\033[93m[!] {0} should be used in Linux environments!\033[00m".format(sys.argv[0]))

# Encrypt function:
def encrypt(content: str, key: str) -> bytes:
    key_id = 0
    xored = ""
    for key_id, c in enumerate(content):
        xored += chr(ord(key[key_id % len(key)]) ^ ord(c))
        key_id += 1
    return binascii.hexlify(xored.encode())

# Check for compiling:
generated_file = False
# -------------------------------------- #
#  READ FILE                             #
# -------------------------------------- #
print("\n\033[94m[*]\033[00m Reading {0}:    ".format(sys.argv[1]), end="")
try:
    with open(sys.argv[1], "r") as fl:
        data = fl.read().split("#-----#")
        print("\033[92mDONE\033[00m")
except Exception as error:
    print("\033[91mERROR\033[00m")
    print("\t" + str(error))
    sys.exit()

# -------------------------------------- #
#  PREPARE CRYPTER STUFF                 #
# -------------------------------------- #
# Generate key:
print("\033[94m[*]\033[00m Generating key:    ", end="")
unique_key = token_urlsafe(128)
for i in "{0}".format(digits + punctuation):
    if i in unique_key:
        unique_key = unique_key.replace(i, "")
print("\033[92mDONE\033[00m")

# Generate decrypt function:
print("\033[94m[*]\033[00m Generating decrypt function:    ", end="")
decrypt_function = """def decrypt(content: bytes, key='{0}') -> str:
    key_id = 0
    xored = ''
    for key_id, c in enumerate(binascii.unhexlify(content).decode()):
        xored += chr(ord(key[key_id % len(key)]) ^ ord(c))
        key_id += 1
    return xored
""".format(unique_key)
print("\033[92mDONE\033[00m")

# -------------------------------------- #
#  PREPARE HEADER                        #
# -------------------------------------- #
print("\033[94m[*]\033[00m Preparing header:    ", end="")
header = "import binascii;" + data[0].replace("\n", ";")
header += "\n{0}".format(decrypt_function)
print("\033[92mDONE\033[00m")

# -------------------------------------- #
#  ENCRYPTING PAYLOAD                    #
# -------------------------------------- #
print("\033[94m[*]\033[00m Encrypting payload:    ", end="")
try:
    payload = data[1] #.replace("\n", ";")
    encoded_payload = encrypt(payload, unique_key)
    print("\033[92mDONE\033[00m")
except Exception as error:
    print("\033[91mERROR\033[00m")
    print("\t" + str(error))
    sys.exit()

# -------------------------------------- #
#  CREATE FOOTER                         #
# -------------------------------------- #
print("\033[94m[*]\033[00m Generating file footer:    ", end="")
footer = 'exec(decrypt({0}))'.format(encoded_payload)
print("\033[92mDONE\033[00m")

# -------------------------------------- #
#  CREATE NEW FILE                       #
# -------------------------------------- #
print("\033[94m[*]\033[00m Exporting file:    ", end="")
try:
    new_filename = "{0}.output.py".format(sys.argv[1])
    with open(new_filename, "w") as fl:
        fl.write(header + "\n")
        fl.write(footer)
    generated_file = True
    print("\033[92mDONE\033[00m")
    print("\tFile exported to \033[92m{0}\033[00m\n".format(new_filename))
except Exception as error:
    print("\033[91mERROR\033[00m")
    print("\t" + str(error))
    sys.exit()

# -------------------------------------- #
#  COMPILE                               #
# -------------------------------------- #
if generated_file:
    print("\033[94m[*]\033[00m Compile? [y/N]:")
    opt = input(">>> ").lower()
    if opt in ["yes", "y"]:
        comp_key = token_urlsafe(256)
        for i in punctuation:
            if i in comp_key:
                comp_key = comp_key.replace(i, "")

        print("\033[94m[*]\033[00m Compiling:    ", end="")
        # Compile:
        try:
            cmd = "pyinstaller --distpath . --name {2} --noconfirm --onefile --key {0} --noconsole {1}".format(comp_key, new_filename, sys.argv[1].split(".")[0])
            subprocess.run(cmd, shell=True)
            # Clean:
            cmd = "rm -rf build/ {0}.spec".format(sys.argv[1].split(".")[0])
            subprocess.run(cmd, shell=True)
            # SUCCESS:
            print("\033[92mDONE\033[00m")
        except Exception as error:
            # ERROR:
            print("\033[91mERROR\033[00m")
            print("\t" + str(error))
            sys.exit()

# -------------------------------------- #
#  CLOSE BLACK VEIL                      #
# -------------------------------------- #
print("\033[94m[*]\033[00m Thank you.")
