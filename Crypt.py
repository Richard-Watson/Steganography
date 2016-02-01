"""
XOR encryption
Input - bytes
password - string
"""
def cryptXOR(Input, password):
    Output = ""
    for i in range(len(Input)):
        Output += chr(Input[i] ^ ord(password[i % len(password)]))
    return bytes(Output, encoding="iso8859-1")