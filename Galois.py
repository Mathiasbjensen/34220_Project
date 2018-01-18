import numpy as np
np.set_printoptions(threshold=np.nan)

galois = np.array([[0,0,0,0,0,0,0,1]])
primitive=[0,0,0,1,1,0,1,1]

# Creating galois field 2^8.
for i in range(256):
    # When the left most bit is 1:
    if galois[i,0]==1:
        temp = np.roll(galois[i],-1)
        temp[-1]=0
        temp = temp ^ galois[i]
        galois = np.vstack([galois,(temp ^ primitive)])
    else:
        galois = np.vstack([galois,(np.roll(galois[i],-1)) ^ galois[i]])


def findIndex(hexa):
    """
    Takes a hex string and finds the alpha index in the Galois Field.
    :param hexa: hex string
    :return: int
    """
    # Converting from hexa to binary.
    input = bin(int(hexa, 16))[2:].zfill(8)
    # converting to a list so we can compare (==).
    input = np.array([int(x) for x in str(input)])
    # Getting the index of galois
    alphaIndex = np.where(np.all(input == galois, axis=1))
    # [0][0] due to the output np.where gives.
    return alphaIndex[0][0]


def findInverse(hexa):
    """
    Takes a hex and returns the multiplicative inverse in binary (8 bits).
    :param hexa: hex string
    :return: bin
    """
    if isinstance(hexa,np.ndarray):
        hexa = ''.join(str(x) for x in hexa)
        hexa = hex(int(hexa, 2))
    if int(hexa,16) == 0:
        return np.array([0,0,0,0,0,0,0,0])
    alphaIndex=findIndex(hexa)
    invAlphaIndex = 256-alphaIndex-1
    return galois[invAlphaIndex]


def sboxElement(hexa):
    """
    Finds the specific s-box element for a hex
    :param hexa: hex string
    :return: numpy array - 1 byte, each element a bin.
    """
    b = np.flip(findInverse(hexa),0)
    c = np.array([1,1,0,0,0,1,1,0])
    output=np.array([None]*8)
    for i in range(8):
        output[i] = b[i] ^ b[(i+4)%8] ^ b[(i+5)%8] ^ b[(i+6)%8] ^ b[(i+7)%8] ^ c[i]
    return np.flip(output,0)


def createSbox():
    """
    Creates the s-box
    :return: int list
    """
    sbox=[None]*256
    sbox[0]=0x63
    for i in range(1,256):
            #temp = format(i, '#04x')
        temp = sboxElement(hex(i))
        temp = ''.join(str(x) for x in temp)
        temp = int(temp,2)
        sbox[i]=temp
    return sbox


def gfMul(a,b):
    """
    Multiplication in the Galois Field
    :param a: hex
    :param b: hex
    :return: int - The product of a and b in the Galois Field.
    """
    # In case we have 0, which is not a part of our galois.
    if a == 0 or b == 0:
        return 0
    index = (findIndex(hex(a))+findIndex(hex(b))) % 255
    value = galois[index]
    value = ''.join(str(x) for x in value)
    # and now to int
    return int(value,2)