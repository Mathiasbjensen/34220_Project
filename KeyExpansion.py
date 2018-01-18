from Galois import *
# We only need 10 bits of the original rcon and 3 rows of padded 0s.
rcon = np.array([[0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36],
                [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])
sbox = createSbox()

def rotWord(cipherCol):
    """
    :param cipherCol: numpy array
    :return: numpy array
    """
    rotated=np.roll(cipherCol,-1)
    return rotated


def subBytes(state):
    """
    :param state: list OR numpy array
    :return: list
    """
    # Ensures we can both use list and numpy arrays.
    if type(state) != list:
        state=state.tolist()
    for i in range(len(state)):
        state[i]=sbox[state[i]]
    return state


def createKeyExpansion(cipherKey):
    """
    Creates all 11 keys (including the cipherKey
    :param cipherKey: list
    :return: 4x44 2D numpy array
    """
    # Change cipherKey from array to 4 by 4 matrix.
    roundKeys = np.reshape(cipherKey, (4, 4), order='F')

    for i in range(1,11):
        temp = subBytes(rotWord(roundKeys[:,i*4-1]))
        temp = roundKeys[:,i*4-4] ^ temp ^ rcon[:, i-1]
        roundKeys = np.column_stack((roundKeys, temp))
        for j in range(1,4):
            temp = roundKeys[:,i*4+j-1] ^ roundKeys[:,i*4+j-4]
            roundKeys = np.column_stack((roundKeys, temp))

    return roundKeys

