import numpy as np



np.set_printoptions(threshold=np.nan)
#galois = np.empty(shape=(256,8))
#print(galois.shape)
galois = np.array([[0,0,0,0,0,0,0,1]])
primitive=[0,0,0,1,1,0,1,1]

#shiftedState[1] = np.roll(shiftedState[1],-1)
# Creating galois field 2^8.
for i in range(256):
    if galois[i,0]==1:
        temp = np.roll(galois[i],-1)
        temp[-1]=0
        temp = temp ^ galois[i]
        galois = np.vstack([galois,(temp ^ primitive)])
        #For 1 i første kolonne
    else:
        galois = np.vstack([galois,(np.roll(galois[i],-1)) ^ galois[i]])



# findIndex: Takes a hexadecimal and gives the alpha index number.
def findIndex(hexa):
    # Converting from hexa to binary.
    input = bin(int(hexa, 16))[2:].zfill(8)
    # converting to a list so we can compare (==).
    input = np.array([int(x) for x in str(input)])
    # Getting the index of galois
    alphaIndex = np.where(np.all(input == galois, axis=1))
    # [0][0] due to the output np.where gives.
    return alphaIndex[0][0]

# findInverse: Takes a hex and returns its multiplicative inverse in bin.
def findInverse(hexa):
    ##input = bin(int(hexa,16))[2:].zfill(8)
    alphaIndex=findIndex(hexa)
    invAlphaIndex = 256-alphaIndex-1
    #print(invAlphaIndex)
    invAlphaIndex = invAlphaIndex
    return galois[invAlphaIndex]
#print('---------------------')
#print(findInverse(0x02))

# Find det alfa som er de 2 alfaers produkt.
#print(galois[1+254 % 255])


def sboxElement(hexa):
    # Flipper så vi har de vigtigste bit først (?).
    b = np.flip(findInverse(hexa),0)
    c = np.array([1,1,0,0,0,1,1,0])
    output=np.array([None]*8)
    for i in range(8):
        output[i] = b[i] ^ b[(i+4)%8] ^ b[(i+5)%8] ^ b[(i+6)%8] ^ b[(i+7)%8] ^ c[i]
    #converting from list to hex

    return np.flip(output,0)


def createSbox():
    sbox=[None]*256
    sbox[0]='0x63'
    for i in range(1,256):
            #temp = format(i, '#04x')
        temp = sboxElement(hex(i))
        temp = ''.join(str(x) for x in temp)
        temp = hex(int(temp,2))
        sbox[i]=temp
        #else:
         #   sbox[i]=sboxElement(hex(i))

    return sbox

#print(findInverse(hex(2)))
#print(sboxElement(hex(2)))
#print('-----------')
#print(createSbox())
#print(findInverse(hex(1)))

#print(findInverse(hex()))
#print(findInverse(str(hex(17))))
#for i in range(16):
 #   print(format(i, '#04x'))
# '0x55' --> 0x55
#print('-----------')
#print(findIndex(hex(3)))

# takes 2 hexadecimals and multiplies them - returns their galois product index.
def gfMul(a,b):
    return (findIndex(a)+findIndex(b)) % 255
#print('------------')
#print(gfMul(hex(0x57),hex(0x83)))
#print(galois[178])

print(galois)

def createRcon():
    rcon=[None]*12
    rcon[0]='0x8d'
    rcon[1]='0x01'
    for i in range(2,12):
        rcon[i]=hex(2*(pow(2,i-2))%256)

    return rcon

print(createRcon())