print("\033c")



# helper code chunk
import string
import random
WORDLIST_FILENAME = "wordlist.txt"
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    Wordlist = line.split()
    print("  ", len(Wordlist), "words loaded.")
    return Wordlist

Wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable

# helper code ^^^







Alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
PlainText = input('What would you like to encode? ').lower()

# single shift encryption
def Encode(PlainText, n):
    CodeText = ''
    PlainText = PlainText.lower()
    for e in PlainText:
        if e in Alpha:
            i = Alpha.index(e)
            o = (i + n) % 27
            CodeText += (Alpha[o])
        else:
            #keeps numbers and punctuation same
            CodeText += e
    return CodeText



# makes sure user enters integer for shift key
while True:
    try:
        n = int(input('Please enter your integer shift key: '))
        break
    except ValueError:
        print('That is not a valid shift key.')
CodeText = Encode(PlainText, n)
print(CodeText)


CodeText = CodeText.lower()

# decodes coded text using known n as a shift key
def Decode(n, CodeText):
    PlainText = ''
    for e in CodeText:
        if e in Alpha:
            o = Alpha.index(e)
            i = (o - n) % 27
            PlainText += Alpha[i]
        else:
            PlainText += e
    return PlainText


# counts how many of decoded words are actual valid words
def MostWords(PlainText):
    GoodWords = 0
    Sep = PlainText.split(" ")
    NumWords = len(Sep)
    for Word in Sep:
        if Word in Wordlist:
            GoodWords += 1
    return GoodWords, NumWords

        
# decodes a message with unknown n shift
def UnknownShift(CodeText, Wordlist):
    n = 0
    KeyScore = []
    PossMess = []
    while n < 27:
        PlainText = Decode(n, CodeText)
        PossMess.append(PlainText)
        KeyScore.append(int(MostWords(PlainText)))
        n += 1
    Shift = KeyScore.index(max(KeyScore))
    print(f'The most likely key shift is {Shift}.')
    print(f'Message most likely reads: {PossMess[Shift]}')
    
    
CodeText = CodeText.lower()
UnknownShift(CodeText, Wordlist)




# multi level encryption

BigShifts = [3, 0, 0, 0, 9, 3, 0, 0, 8, 7]

# shifts elements by BigShifts according to index

def BigEncode(PlainText):
    for i, e in enumerate(BigShifts):
        CodeText = ''
        Place = i
        Shift = e
        for Spot, Letter in enumerate(PlainText):
            if Letter in Alpha:
                if Spot < Place:
                    CodeText += Letter
                else:
                    Orig = Alpha.index(Letter)
                    New = (Orig + Shift) % 27
                    CodeText += Alpha[New]
            else:
                CodeText += Letter
        PlainText = CodeText
    return CodeText

CodeText = BigEncode(PlainText)
print(f' encoded text is {CodeText}')



# when message reaches a space, checks if the slice before space is a word. if not, wont be added to continuing list
def ChkPt(PlainText, f):
    if PlainText[f] == ' ':
        slice = PlainText[:f]
        Score, NumWords = MostWords(slice)
        if Score == NumWords:
            return True
        else:
            return False
    else:
        slice = PlainText[:f+1]
        for word in Wordlist:
            if word.startswith(slice):
                print(word)
                return True
        return False


# step that lists all possible shifts for one point in encryption
def RecStep(s, f):
    PossMess = []
    slice = str(s[f:])
    PlainText = s[:f]
    print(f' og slice {PlainText}')
    for n in range(27):
        PlainText += Decode(n, slice)
        print(f' post decode {PlainText}')
        check = ChkPt(PlainText, f)
        if check == True:
            PossMess.append(PlainText)
        PlainText = s[:f]
        print(f' reset {PlainText}')
    return PossMess



"""
decodes an encryption with unknown values and positions of shifts
although it works, because it was a recursive exercise,
it is extremely slow past 4-5 characters
"""

def BigDecode(CodeText):
    PossMess = []
    Hold = []
    KeyScore = []
    # creates first list of possibilities bc recstep takes a list as argument
    for n in range(27):
        PlainText = Decode(n, CodeText)
        PossMess.append(PlainText)
    print(PossMess)
    f = 1
    # runs all possible shifts
    while f < len(CodeText):
        for s in PossMess:
            Hold.extend(RecStep(s, f))
            PossMess.remove(s)
        PossMess.extend(Hold)
        Hold = []
        f += 1
    # scores each possible message
    for s in PossMess:
        Score, Ignore = MostWords(s)
        KeyScore.append(int(Score))
    # picks message with most words
    Key = KeyScore.index(max(KeyScore))
    Message = PossMess[Key]
    return Message

Message = BigDecode(CodeText)
print(f'The decoded message is: {Message}')
