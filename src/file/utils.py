import string

VALID_CHARS = "-_.!@$%^&() {0}{1}".format(string.ascii_letters, string.digits)

def createValidName(originalName):
    fileName = ''.join(c for c in originalName if c in VALID_CHARS)
    return fileName


def isNameValid(name):
    for char in name:
        if char not in VALID_CHARS:
            return False
        
    return True