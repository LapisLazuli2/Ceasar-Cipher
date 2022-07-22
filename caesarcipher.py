import string

WORDLIST_FILENAME = 'words.txt'

def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # print("Loading word list from file...")
    inFile = open(file_name, 'r')
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

class Message(object):
    def __init__(self, text):
        '''
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.set_message_text(text)
        self.set_valid_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def set_message_text(self, newtext):
        '''
        Used to set the value of self.message text

        self.message_text (string, determined by input text)
        '''
        self.message_text = newtext

    def set_valid_words(self, filename):
        '''
        Used to set the value of self.valid_words

        self.valid_words (list, determined using helper function load_words)
        '''
        self.valid_words = load_words(filename)

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        has 52 keys of all the uppercase letters and all the lowercase
        letters.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        shift_dict = {}
        shifted_letter_index = 0
        index = -1

        for letter in string.ascii_lowercase:
            index += 1
            shifted_letter_index = index + shift
            while shifted_letter_index >= 26:
                shifted_letter_index -= 26
            shift_dict[letter] = string.ascii_lowercase[shifted_letter_index]
            shift_dict[letter.upper()] = string.ascii_lowercase[shifted_letter_index].upper()

        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift.

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every alphabet character is shifted
             down the alphabet by the input shift
        '''
        message_text = self.get_message_text()
        shifted_message_text = ''
        shift_dict = self.build_shift_dict(shift)

        for letter in message_text:
            if letter not in string.ascii_letters:
                shifted_message_text += letter
            else:
                shifted_message_text += shift_dict[letter]

        return shifted_message_text


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.set_shift(shift)
        self.set_encryption_dict()
        self.set_message_text_encrypted()

    def set_shift(self, newshift):
        '''
        Used to set the value of self.shift

        self.shift (integer, determined by the input shift)
        '''
        self.shift = newshift

    def set_encryption_dict(self):
        '''
        Used to set the value of self.encryption_dict

        self.encryption_dict (dictionary, built using shift)
        '''
        self.encryption_dict = self.build_shift_dict(self.get_shift())

    def set_message_text_encrypted(self):
        '''
        Used to set the value of self.message_text_encrypted

        self.message_text_encrypted (string, created using shift)
        '''
        self.message_text_encrypted = self.apply_shift(self.get_shift())


    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.set_shift(shift)
        self.set_encryption_dict()
        self.set_message_text_encrypted()


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypts self.message_text by trying every possible shift value
        and finding the "best" one. "Best" here is defined as the shift that
        creates the maximum number of real words when apply_shift(shift) is used
        on the message text. If s is the original shift value used to encrypt
        the message, then 26 - s is expected to be the best shift value
        for decrypting it.

        For example: 'a' shifted by 1 equals 'b', thus 'b' shifted by 26-1
        equals 'a' because shifting 'b' by 25 would be the 26th index of alphabet
        (which is 'a' since 'z' is the 25th )
        {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8,
        'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16,
        'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,
        'z': 25}

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, the function only returns one of
        those shifts and its corresponding decrypted message

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        print('Decrypting text...')
        count_valid_words = 0
        decrypted_message_dict = {}

        for value in range(0, 26+1):
            decrypted_message = self.apply_shift(26-value)
            for word in decrypted_message.split():
                if is_word(self.get_valid_words(), word):
                    count_valid_words += 1
            decrypted_message_dict[count_valid_words] = (26-value, decrypted_message)
            #maybe change the above code because multiple things could be mapped/override the same count value
            # if count_valid_words > 0:
            #     print(f'Testing shift value of {26-value}. Produced {count_valid_words} valid English words')
            # else:
            #     print(f'Testing shift value of {26-value}. Produced gibberish')
            count_valid_words = 0


        most_valid_words = max(decrypted_message_dict.keys())
        return decrypted_message_dict[most_valid_words]



if __name__ == '__main__':
    print('-------------------------------------')
    print('Ceasar Cipher encrypts and decrypts messages by shifting all the letters in the message by a certain value.')
    print("For example 'abc' shifted by 1 is 'def'")
    print('-------------------------------------')
    story = get_story_string()
    print('This is an encrypted demo story:')
    print(story)
    print('-------------------------------------')
    print('The program itself does not know the orignal shift value used to encrypt this message but will try to find\nit in order to decrypt the story.')
    print('The program can try to find the shift value by trying various shift values on the encrypted message and deciding')
    print('which value is the best value by looking at whether the decrypted message consists of valid English words instead')
    print('of gibberish.')
    print('-------------------------------------')
    user_input = input('Press enter to decrypt the story.')
    print('-------------------------------------')
    ciphertext = CiphertextMessage(story)
    decrypted_message = ciphertext.decrypt_message()
    print('Most suitable shift value found was:', decrypted_message[0])
    print('Decrypted story:', decrypted_message[1])
