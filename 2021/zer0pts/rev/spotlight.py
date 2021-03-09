import struct
# https://github.com/bozhu/KASUMI-Python/blob/master/kasumi.py
from kasumi import Kasumi


def ida():
    addr = ida_search.find_text(here(), 0, 0, 'unprotect_code', SEARCH_DOWN)
    addr += idaapi.get_item_size(addr)
    idc.add_bpt(addr, 1, idc.BPT_EXEC)
    jumpto(addr)


blocks = [0]*8
blocks[6] = 0x2D9D9AD4ADAF9925
blocks[4] = 0xDC115329AA177509
blocks[2] = 0xE45EF960FBEC841B
blocks[1] = 0xB298DE796E944115
blocks[0] = 0x2DE23334718727BB
blocks[3] = 0x314FC3F835E2958E
blocks[5] = 0x7CB37E8F516BC981
blocks[7] = 0x1808A242A2A693E1


def endian_swap(iv):
    b = struct.pack("<Q", iv)
    b = struct.unpack(">LL", b)
    b = struct.pack("<LL", *b[::-1])
    iv = struct.unpack("<Q", b)[0]
    return iv


if __name__ == '__main__':
    key = bytearray(b"zer0pts CTF 2021")
    # for i in range(0, 16, 2):
    #     key[i:i + 2] = key[i:i + 2][::-1]
    key = int(key.hex(), 16)
    iv = endian_swap(0x786F4620797A614C)

    my_kasumi = Kasumi()
    my_kasumi.set_key(key)

    flag = []
    for b in blocks:
        b = endian_swap(b)
        decrypted = my_kasumi.dec(b) ^ iv
        flag.append(decrypted)
        iv = b

    print(b"".join(struct.pack("<Q", x)[::-1]
                   for x in flag).decode().rstrip('\x00'))
