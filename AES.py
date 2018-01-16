import numpy as np
from Galois import *
from KeyExpansion import *

#sbox=createSbox()
state = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
#state = [0x00, 0x1f, 0x0e, 0x54, 0x3c, 0x4e, 0x08, 0x59, 0x6e, 0x22, 0x1b, 0x0b, 0x47, 0x74, 0x31, 0x1a]
cipherKey = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
#cipherKey = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]



rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

#print(int(0x53,16))
#print(hex(sbox[83]))



#print(subBytes([1,2,3]))


def shiftRows(state):
    # Making the list into a numpy matrix to shift the rows.
    shiftedState=np.reshape(state,(4,4),order='F')
    shiftedState[1] = np.roll(shiftedState[1],-1)
    shiftedState[2] = np.roll(shiftedState[2],-2)
    shiftedState[3] = np.roll(shiftedState[3],-3)
    # Converting the numpy matrix back into a list before returning it.
    shiftedState = np.reshape(shiftedState,(1,16),order='F')
    shiftedState = shiftedState.flatten().tolist()

    return shiftedState
#print(shiftRows(state))

def addRoundKey(state, roundKey):
    roundKey = np.array(state) ^ np.array(roundKey)
    return roundKey

#print(addRoundKey(state,cipherKey))

def getRoundKey(roundNumber):
    if roundNumber == 0:
        roundKey = keys[:,:4]
    else:
        roundKey = keys[:,roundNumber*4:roundNumber*4+4]
    return np.reshape(roundKey, (1, 16), order='F')[0]


def mixColumns(state):
    state = np.reshape(state, (4, 4), order='F')
    mixed = np.zeros((4,4)).astype(int)
    for i in range(4):
        mixed[0,i] = gfMul(0x02,state[0,i]) ^ gfMul(0x03,state[1,i]) ^ state[2,i] ^ state[3,i]
        mixed[1,i] = state[0,i] ^ gfMul(0x02,state[1,i]) ^ gfMul(0x03,state[2,i]) ^ state[3,i]
        mixed[2,i] = state[0,i] ^ state[1,i] ^ gfMul(0x02,state[2,i]) ^ gfMul(0x03,state[3,i])
        mixed[3,i] = gfMul(0x03,state[0,i]) ^ state[1,i] ^ state[2,i] ^ gfMul(0x02,state[3,i])
        # Converting back to a 1d array.
    return np.reshape(mixed,(1,16),order='F')[0]

#print(mixColumns([0xd4,0xbf,0x5d,0x30,0xe0,0xb4,0x52,0xae,0xb8,0x41,0x11,0xf1,0x1e,0x27,0x98,0xe5]))



# ---------------------------------------------------------------------------------------------- #


keys = createKeyExpansion(cipherKey)
#print(keys)
#print('-----------')
#print(getRoundKey(0))
#print(keys[:,:4])
# **Initial round** - add round key (cipherKey since it's initial round. and get a new state.
state=addRoundKey(state,getRoundKey(0))
#print(state)

# **The next 9 rounds**

for i in range(1,10):

    state = subBytes(state)
    state = shiftRows(state)
    state = mixColumns(state)
    state = addRoundKey(state,getRoundKey(i))
    #print(state)


# **Final round**

state = subBytes(state)
state = shiftRows(state)
output = addRoundKey(state,getRoundKey(10))
print(output)

def matrixOutput(state):
    output = np.array([hex(x) for x in state])
    output = np.reshape(output, (4, 4), order='F')
    return output

print(matrixOutput(output))