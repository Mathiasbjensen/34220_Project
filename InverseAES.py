import numpy as np
from Galois import *

state = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]


def sboxElementInv(hexa):
    # Flipper så vi har de vigtigste bit først (?).
    #b = np.flip(findInverse(hexa),0)
    #b = np.flip(galois[findIndex(hex(hexa))],0)
    b = galois[findIndex(hex(hexa))]
    c = np.array([0,0,0,0,0,1,0,1])
    c = np.flip(c,0)
    #c = np.array([1,1,0,0,0,1,1,0])
    #c = np.array([0,1,1,0,0,0,1,1])
    output=np.array([None]*8)
    for i in range(8):
        output[i] = b[i] ^ b[(i+4)%8] ^ b[(i+5)%8] ^ b[(i+6)%8] ^ b[(i+7)%8] ^ c[i]
    output = findInverse(output)
    #converting from list to hex

    return output

print(sboxElementInv(0x01))
#print(findIndex(hex(1)))

def shiftRowsInv(state):
    # Making the list into a numpy matrix to shift the rows.
    shiftedState=np.reshape(state,(4,4),order='F')
    shiftedState[1] = np.roll(shiftedState[1],1)
    shiftedState[2] = np.roll(shiftedState[2],2)
    shiftedState[3] = np.roll(shiftedState[3],3)
    # Converting the numpy matrix back into a list before returning it.
    shiftedState = np.reshape(shiftedState,(1,16),order='F')
    shiftedState = shiftedState.flatten().tolist()

    return shiftedState

print(shiftRowsInv(state))


"""def subBytes(state):
    # Ensures we can both use list and numpy arrays.
    if type(state) != list:
        state=state.tolist()
    for i in range(len(state)):
        state[i]=invSbox[state[i]]
    return state"""

def mixColumnsInv(state):
    state = np.reshape(state, (4, 4), order='F')
    mixed = np.zeros((4,4)).astype(int)
    for i in range(4):
        mixed[0,i] = gfMul(0x0e,state[0,i]) ^ gfMul(0x0b,state[1,i]) ^ gfMul(0x0d,state[2,i]) ^ gfMul(0x09,state[3,i])
        mixed[1,i] = gfMul(0x09,state[0,i]) ^ gfMul(0x0e,state[1,i]) ^ gfMul(0x0b,state[2,i]) ^ gfMul(0x0d,state[3,i])
        mixed[2,i] = gfMul(0x0d,state[0,i]) ^ gfMul(0x09,state[1,i]) ^ gfMul(0x0e,state[2,i]) ^ gfMul(0x0b,state[3,i])
        mixed[3,i] = gfMul(0x0b,state[0,i]) ^ gfMul(0x0d,state[1,i]) ^ gfMul(0x09,state[2,i]) ^ gfMul(0x0e,state[3,i])
        # Converting back to a 1d array.
    return np.reshape(mixed,(1,16),order='F')[0]
