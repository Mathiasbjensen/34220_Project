from AES import *
from InputText import *

# State and Cipher Key.
state = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
cipherKey = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]

print('----- MESSAGE -----')
print(matrixOutput(state))
def Encryption(state):
    # --- Initial round ---
    state = addRoundKey(state, getRoundKey(0))

    # --- The next 9 rounds ---
    for i in range(1, 10):
        state = subBytes(state)
        state = shiftRows(state)
        state = mixColumns(state)
        state = addRoundKey(state, getRoundKey(i))

    # --- Final round ---
    state = subBytes(state)
    state = shiftRows(state)
    encrypted = addRoundKey(state, getRoundKey(10))

    return encrypted

encrypted=Encryption(state)
print('----- ENCRYPTED -----')
print(matrixOutput(encrypted))


def Decryption(encrypted):
    # --- Initial round ---
    state = encrypted
    state = addRoundKey(state, getRoundKey(10))

    # --- The next 9 rounds ---
    for i in range(9, 0, -1):
        state = shiftRowsInv(state)
        state = subBytesInv(state)
        state = addRoundKey(state, getRoundKey(i))
        state = mixColumnsInv(state)
    # --- Final Round ---
    state = shiftRowsInv(state)
    state = subBytesInv(state)
    return addRoundKey(state, getRoundKey(0))

decrypted=Decryption(encrypted)
print('----- DECRYPTED -----')
print(matrixOutput(decrypted))
