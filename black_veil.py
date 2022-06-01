import sys
import binascii
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
print("                                       v1.0.0\033[00m")

# -------------------------------------- #
#  SETUP                                 #
# -------------------------------------- #
# Check args:
if len(sys.argv) != 2:
    print("\n\033[94m[*]\033[00m Usage: {0} path/to/file.py".format(sys.argv[0]))
    sys.exit()

# Encrypt function:
def encrypt(content: str, key: str) -> bytes:
    key_id = 0
    xored = ""
    for key_id, c in enumerate(content):
        xored += chr(ord(key[key_id % len(key)]) ^ ord(c))
        key_id += 1
    return binascii.hexlify(xored.encode())

# -------------------------------------- #
#  READ FILE                             #
# -------------------------------------- #
print("\n\033[94m[*]\033[00m Reading {0}:\t\t\t".format(sys.argv[1]), end="")
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
print("\033[94m[*]\033[00m Generating key:\t\t\t\t", end="")
unique_key = token_urlsafe(128)
for i in "{0}".format(digits + punctuation):
    if i in unique_key:
        unique_key = unique_key.replace(i, "")
print("\033[92mDONE\033[00m")

# Generate decrypt function:
print("\033[94m[*]\033[00m Generating decrypt function:\t\t", end="")
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
print("\033[94m[*]\033[00m Preparing header:\t\t\t\t", end="")
header = "import binascii;" + data[0].replace("\n", ";")
header += "\n{0}".format(decrypt_function)
print("\033[92mDONE\033[00m")

# -------------------------------------- #
#  ENCRYPTING PAYLOAD                    #
# -------------------------------------- #
print("\033[94m[*]\033[00m Encrypting payload:\t\t\t\t", end="")
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
print("\033[94m[*]\033[00m Generating file footer:\t\t\t", end="")
footer = 'exec(decrypt({0}))'.format(encoded_payload)
print("\033[92mDONE\033[00m")

# -------------------------------------- #
#  CREATE NEW FILE                       #
# -------------------------------------- #
print("\033[94m[*]\033[00m Exporting file:\t\t\t\t", end="")
try:
    new_filename = "{0}.output.py".format(sys.argv[1])
    with open(new_filename, "w") as fl:
        fl.write(header + "\n")
        fl.write(footer)
    print("\033[92mDONE\033[00m")
    print("\tFile exported to \033[92m{0}\033[00m\n".format(new_filename))
except Exception as error:
    print("\033[91mERROR\033[00m")
    print("\t" + str(error))
    sys.exit()
