from InverseAES import *
from KeyExpansion import *

#sbox=createSbox()
#state = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
#state = [0x00, 0x1f, 0x0e, 0x54, 0x3c, 0x4e, 0x08, 0x59, 0x6e, 0x22, 0x1b, 0x0b, 0x47, 0x74, 0x31, 0x1a]
cipherKey = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]



# shiftRows: Takes a list and outputs a list.
def shiftRows(state):
    """
    :param state: Takes a list
    :return: Outputs a shifted list.
    """
    # Making the list into a numpy matrix to shift the rows.
    shiftedState=np.reshape(state,(4,4),order='F')
    shiftedState[1] = np.roll(shiftedState[1],-1)
    shiftedState[2] = np.roll(shiftedState[2],-2)
    shiftedState[3] = np.roll(shiftedState[3],-3)
    # Converting the numpy matrix back into a list before returning it.
    shiftedState = np.reshape(shiftedState,(1,16),order='F')
    shiftedState = shiftedState.flatten().tolist()

    return shiftedState

def addRoundKey(state, roundKey):
    """
    :param state: List
    :param roundKey: List
    :return: the product of the 2 lists XOR'd.
    """
    roundKey = np.array(state) ^ np.array(roundKey)
    return roundKey


# getRoundKey:
def getRoundKey(roundNumber):
    """
    Takes a round number (0-10) and returns the round key as a numpy array.
    :param roundNumber: Int (0-10)
    :return: List (Round Number)
    """
    keys = createKeyExpansion(cipherKey)
    if roundNumber == 0:
        roundKey = keys[:,:4]
    else:
        roundKey = keys[:,roundNumber*4:roundNumber*4+4]
    return np.reshape(roundKey, (1, 16), order='F')[0]

# Takes an array and returns an array.
def mixColumns(state):
    """
    :param state: numpy array
    :return: numpy array
    """
    state = np.reshape(state, (4, 4), order='F')
    mixed = np.zeros((4,4)).astype(int)
    for i in range(4):
        mixed[0,i] = gfMul(0x02,state[0,i]) ^ gfMul(0x03,state[1,i]) ^ state[2,i] ^ state[3,i]
        mixed[1,i] = state[0,i] ^ gfMul(0x02,state[1,i]) ^ gfMul(0x03,state[2,i]) ^ state[3,i]
        mixed[2,i] = state[0,i] ^ state[1,i] ^ gfMul(0x02,state[2,i]) ^ gfMul(0x03,state[3,i])
        mixed[3,i] = gfMul(0x03,state[0,i]) ^ state[1,i] ^ state[2,i] ^ gfMul(0x02,state[3,i])
        # Converting back to a 1d array.
    return np.reshape(mixed,(1,16),order='F')[0]

def matrixOutput(state):
    """
    Illustrates the state (vector) as a 4x4 matrix with hex elements.
    :param state: numpy array
    :return: 2D numpy array (hexadecimals)
    """
    output = np.array([hex(x) for x in state])
    output = np.reshape(output, (4, 4), order='F')
    return output