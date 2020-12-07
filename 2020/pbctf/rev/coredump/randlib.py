def _(x):
    return x & 0xffffffff


class Context:
    def __init__(self, seed):
        self.state = [0] * 624
        self.state[0] = seed
        for i in range(623):
            seed = (6069 * seed) & 0xffffffff
            self.state[i + 1] = seed
        self.pos = 624

    def generate(self):
        pos = self.pos
        next_pos = pos + 1
        if (pos > 623):
            if (pos != 624):
                raise "?"
                self.__init__(4357)
            v10 = self.state[:]
            for i in range(1, 625):
                x = v10[i - 1] & 0x80000000 | v10[i % 0x270] & 0x7FFFFFFF
                xA = x >> 1
                self.state[i - 1] = [0, 0x9908B0DF][x &
                                                    1] ^ self.state[(i + 396) % 0x270] ^ xA
            next_pos = 1
            pos = 0
        v5 = self.state[pos]
        self.pos = next_pos
        v6 = ((_(v5) ^ _(v5 >> 11)) << 7) & 0x9D2C5680 ^ v5 ^ (v5 >> 11) ^ ((
            ((_(v5) ^ _(v5 >> 11)) << 7) & 0x9D2C5680 ^ _(v5) ^ _(v5 >> 11)) << 15) & 0xEFC60000
        return (v6 >> 18) ^ v6


def decrypt(payload, off):
    rng = Context(off)
    payload = bytearray(payload)
    for i in range(len(payload)):
        payload[i] = payload[i] ^ (rng.generate() | 0x80) & 0xff
    return payload
