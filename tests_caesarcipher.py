from caesarcipher import *

def test_apply_shift():
    """
    Unit test for apply_shift
    """
    failure = False
    shifted_words = {('abcd!', 1):'bcde!', ('$#$@#', 10): '$#$@#', ('', 1): '', ('hello', 2):'jgnnq'}
    for (word, shift) in shifted_words.keys():
        message = Message(word)
        shifted_word = message.apply_shift(shift)
        if shifted_word != shifted_words[(word, shift)]:
            print("FAILURE: test_apply_shift()")
            print(f'Expected {shifted_words[(word,shift)]} but got {shifted_word}')
            failure = True
    if not failure:
        print('SUCCESS: test_apply_shift()')

def test_decrypt_message():
    """
    Unit test for decrypt_message
    """
    failure = False
    encrypted_words = {'jgnnq':(24, 'hello'), 'jgnnq!':(24, 'hello!'), '':(0, '')}
    for word in encrypted_words.keys():
        ciphertext = CiphertextMessage(word)
        decrypted_word = ciphertext.decrypt_message()
        if decrypted_word != encrypted_words[word]:
            print("FAILURE: test_decrypt_message()")
            print(f'Expected {encrypted_words[word]} but got {decrypted_word}')
            failure = True
    if not failure:
        print('SUCCESS: test_decrypt_message()')



print("----------------------------------------------------------------------")
print("Testing apply_shift()...")
test_apply_shift()

print("----------------------------------------------------------------------")
print("Testing decrypt_message()...")
test_decrypt_message()
