def stringToState(a):
    if len(a) > 16:
        return "The given input is more than 16 bytes."
    output = [0]*16
    for i in range(len(a)):
        output[i] = ord(a[i])

    return output
test = stringToState('Thats my kung fu')


def stateToString(a):
    if len(a) > 16:
        return "This should never happen"
    output = ""
    for i in range(len(a)):
        output = output + chr(a[i])
    return output


