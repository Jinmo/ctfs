key = [30L, 5L, 14L, 10L, 26L, 6L, 9L, 18L, 10L, 111L, 48L, 44L, 107L, 19L, 26L, 57L, 85L, 52L, 92L, 45L, 3L, 88L, 86L, 56L, 61L, 84L, 28L, 41L, 104L, 29L, 58L, 13L, 37L, 11L, 69L, 26L, 104L, 9L, 0L]
ciphertext = bytearray('flag{this_is_a_fake_flag_dig_deeper_:(}')
print bytearray([x ^ y for x, y in zip(key, ciphertext)])