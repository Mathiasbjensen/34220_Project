import binascii

def stringToState(a):
    if len(a) > 16:
        return "The given input is more than 16 bytes."
    output = [0]*16
    for i in range(len(a)):
        output[i] = ord(a[i])
    #output = [ord(x) for x in a]

    return output
print(stringToState('Thats my kung fu'))
test = stringToState('Thats my kung fu')


def stateToString(a):
    if len(a) > 16:
        return "This should never happen"
    output = ""
    for i in range(len(a)):

        #print(chr(a[i]))
        output = output + chr(a[i])
    return output

#print(stateToString(test))

