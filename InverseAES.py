from Galois import *

state = []


def createInvSbox():
    """
    Creates the inverse s-box
    :return: list
    """
    invSbox = [None] * 256
    sbox = createSbox()
    for i in range(256):
        invSbox[sbox[i]] = i
    return invSbox

invSbox = createInvSbox()


def shiftRowsInv(state):
    """
    :param state: list
    :return: list
    """
    # Making the list into a numpy matrix to shift the rows.
    shiftedState=np.reshape(state,(4,4),order='F')
    shiftedState[1] = np.roll(shiftedState[1],1)
    shiftedState[2] = np.roll(shiftedState[2],2)
    shiftedState[3] = np.roll(shiftedState[3],3)
    # Converting the numpy matrix back into a list before returning it.
    shiftedState = np.reshape(shiftedState,(1,16),order='F')
    shiftedState = shiftedState.flatten().tolist()

    return shiftedState


def subBytesInv(state):
    """
    :param state: list OR numpy array
    :return: list
    """
    # Ensures we can both use list and numpy arrays.
    if type(state) != list:
        state=state.tolist()
    for i in range(len(state)):
        state[i]=invSbox[state[i]]
    return state


def mixColumnsInv(state):
    """
    :param state: numpy array
    :return: numpy array
    """
    state = np.reshape(state, (4, 4), order='F')
    mixed = np.zeros((4,4)).astype(int)
    for i in range(4):
        mixed[0,i] = gfMul(0x0e,state[0,i]) ^ gfMul(0x0b,state[1,i]) ^ gfMul(0x0d,state[2,i]) ^ gfMul(0x09,state[3,i])
        mixed[1,i] = gfMul(0x09,state[0,i]) ^ gfMul(0x0e,state[1,i]) ^ gfMul(0x0b,state[2,i]) ^ gfMul(0x0d,state[3,i])
        mixed[2,i] = gfMul(0x0d,state[0,i]) ^ gfMul(0x09,state[1,i]) ^ gfMul(0x0e,state[2,i]) ^ gfMul(0x0b,state[3,i])
        mixed[3,i] = gfMul(0x0b,state[0,i]) ^ gfMul(0x0d,state[1,i]) ^ gfMul(0x09,state[2,i]) ^ gfMul(0x0e,state[3,i])
        # Converting back to a 1d array.
    return np.reshape(mixed,(1,16),order='F')[0]

