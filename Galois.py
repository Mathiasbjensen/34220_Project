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
        #2+2
        #For 1 i første kolonne
    else:
        galois = np.vstack([galois,(np.roll(galois[i],-1)) ^ galois[i]])


#print(galois)
# convert int to list
#[int(x) for x in str(test2)]

# convert hexa to bin (string).
#bin(int(0x53))[2:].zfill(8)


def findInverse(hexa):
    #Converting from hexa to binary.
    input = bin(int(hexa,16))[2:].zfill(8)
    #print("input")
    #print(input)
    #converting to a list so we can compare (==).
    input = np.array([int(x) for x in str(input)])
    #print(input)
    alphaIndex = np.where(np.all(input==galois,axis=1))
    #print("alpha")
    #print(alphaIndex)
    invAlphaIndex = 256-alphaIndex[0]-1
    #print(invAlphaIndex)
    invAlphaIndex = invAlphaIndex[0]
    #print(invAlphaIndex)
    #print(galois[invAlphaIndex])
    #print(galois[254])
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

#test33=sboxElement(0x03)
#print(findInverse(0x03))
#print(sboxElement(0x03))
#
#for j in range(8)
#print(test33[1])

def createSbox():
    sbox=[None]*256
    sbox[0]='0x63'
    for i in range(1,256):
        #if i <= 15:
            #temp = format(i, '#04x')
        temp = sboxElement(hex(i))
        temp = ''.join(str(x) for x in temp)
        temp = hex(int(temp,2))
        sbox[i]=temp
        #else:
         #   sbox[i]=sboxElement(hex(i))

    return sbox

print(findInverse(hex(2)))
print(sboxElement(hex(2)))
print('-----------')
print(createSbox())
#print(findInverse(hex(1)))

#print(findInverse(hex()))
#print(findInverse(str(hex(17))))
#for i in range(16):
 #   print(format(i, '#04x'))
# '0x55' --> 0x55

def gfMul(a,b):
    a = bin(int(a,16))[2:].zfill(8)
    b = bin(int(b,16))[2:].zfill(8)
    #converting to a list so we can compare (==).
    a = np.array([int(x) for x in str(a)])
    b = np.array([int(x) for x in str(b)])
    aIndex = np.where(np.all(a==galois,axis=1))
    bIndex = np.where(np.all(b==galois,axis=1))
    invAIndex = 256-aIndex[0]-1
    invBIndex = 256-bIndex[0]-1
    #converting to a list so we can compare (==).
    input = np.array([int(x) for x in str(input)])
    #print(input)
    alphaIndex = np.where(np.all(input==galois,axis=1))
    #print("alpha")
    #print(alphaIndex)
    invAlphaIndex = 256-alphaIndex[0]-1
    #print(invAlphaIndex)
    invAlphaIndex = invAlphaIndex[0]

