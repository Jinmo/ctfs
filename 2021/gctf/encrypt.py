import random

for key in range(26):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    shifted = alphabet[key:] + alphabet[:key]
    dictionary = dict(zip(alphabet, shifted))

    print(''.join([
        dictionary[c]
        if c in dictionary
        else c
        for c in 'egddagzp_ftue_rxms_iuft_rxms_radymf'
    ]))
