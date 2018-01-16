import numpy as np
#from AES import *
from Galois import *

#cipherKey = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
rcon = np.array([[0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36],
                [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])
sbox = createSbox()

def rotWord(cipherCol):
    rotated=[]
    rotated=np.roll(cipherCol,-1)
    return rotated

def subBytes(state):
    # Ensures we can both use list and numpy arrays.
    if type(state) != list:
        state=state.tolist()
    for i in range(len(state)):
        state[i]=sbox[state[i]]
    return state

#print(rotWord(np.array([43,126,21,22])))

def createKeyExpansion(cipherKey):
    # Change cipherKey from array to 4 by 4 matrix.
    roundKeys = np.reshape(cipherKey, (4, 4), order='F')

    for i in range(1,11):
        temp = subBytes(rotWord(roundKeys[:,i*4-1]))
        temp = roundKeys[:,i*4-4] ^ temp ^ rcon[:, i-1]
        roundKeys = np.column_stack((roundKeys, temp))
        for j in range(1,4):
            temp = roundKeys[:,i*4+j-1] ^ roundKeys[:,i*4+j-4]
            roundKeys = np.column_stack((roundKeys, temp))

        #roundKeys = np.hstack([roundKeys,roundKeys[:,i-4] ^ int((subBytes(rotWord(roundKeys[:,i-1]))),16) ^ rconPad[:,i-4]])

    return roundKeys
#print('----------')
#print(createKeyExpansion(cipherKey))
#keySchedule=createKeyExpansion(cipherKey)
#print(keySchedule[:,4:8])
#print(cipherKey)

