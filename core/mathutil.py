#!/usr/bin/python
#coding:utf8

import random
from sb import s, b

################################################################################

small_prime_table = (
	0x0002, 0x0003, 0x0005, 0x0007, 0x000B, 0x000D, 0x0011, 0x0013,
	0x0017, 0x001D, 0x001F, 0x0025, 0x0029, 0x002B, 0x002F, 0x0035,
	0x003B, 0x003D, 0x0043, 0x0047, 0x0049, 0x004F, 0x0053, 0x0059,
	0x0061, 0x0065, 0x0067, 0x006B, 0x006D, 0x0071, 0x007F, 0x0083,
	0x0089, 0x008B, 0x0095, 0x0097, 0x009D, 0x00A3, 0x00A7, 0x00AD,
	0x00B3, 0x00B5, 0x00BF, 0x00C1, 0x00C5, 0x00C7, 0x00D3, 0x00DF,
	0x00E3, 0x00E5, 0x00E9, 0x00EF, 0x00F1, 0x00FB, 0x0101, 0x0107,
	0x010D, 0x010F, 0x0115, 0x0119, 0x011B, 0x0125, 0x0133, 0x0137,

	0x0139, 0x013D, 0x014B, 0x0151, 0x015B, 0x015D, 0x0161, 0x0167,
	0x016F, 0x0175, 0x017B, 0x017F, 0x0185, 0x018D, 0x0191, 0x0199,
	0x01A3, 0x01A5, 0x01AF, 0x01B1, 0x01B7, 0x01BB, 0x01C1, 0x01C9,
	0x01CD, 0x01CF, 0x01D3, 0x01DF, 0x01E7, 0x01EB, 0x01F3, 0x01F7,
	0x01FD, 0x0209, 0x020B, 0x021D, 0x0223, 0x022D, 0x0233, 0x0239,
	0x023B, 0x0241, 0x024B, 0x0251, 0x0257, 0x0259, 0x025F, 0x0265,
	0x0269, 0x026B, 0x0277, 0x0281, 0x0283, 0x0287, 0x028D, 0x0293,
	0x0295, 0x02A1, 0x02A5, 0x02AB, 0x02B3, 0x02BD, 0x02C5, 0x02CF,

	0x02D7, 0x02DD, 0x02E3, 0x02E7, 0x02EF, 0x02F5, 0x02F9, 0x0301,
	0x0305, 0x0313, 0x031D, 0x0329, 0x032B, 0x0335, 0x0337, 0x033B,
	0x033D, 0x0347, 0x0355, 0x0359, 0x035B, 0x035F, 0x036D, 0x0371,
	0x0373, 0x0377, 0x038B, 0x038F, 0x0397, 0x03A1, 0x03A9, 0x03AD,
	0x03B3, 0x03B9, 0x03C7, 0x03CB, 0x03D1, 0x03D7, 0x03DF, 0x03E5,
	0x03F1, 0x03F5, 0x03FB, 0x03FD, 0x0407, 0x0409, 0x040F, 0x0419,
	0x041B, 0x0425, 0x0427, 0x042D, 0x043F, 0x0443, 0x0445, 0x0449,
	0x044F, 0x0455, 0x045D, 0x0463, 0x0469, 0x047F, 0x0481, 0x048B,

	0x0493, 0x049D, 0x04A3, 0x04A9, 0x04B1, 0x04BD, 0x04C1, 0x04C7,
	0x04CD, 0x04CF, 0x04D5, 0x04E1, 0x04EB, 0x04FD, 0x04FF, 0x0503,
	0x0509, 0x050B, 0x0511, 0x0515, 0x0517, 0x051B, 0x0527, 0x0529,
	0x052F, 0x0551, 0x0557, 0x055D, 0x0565, 0x0577, 0x0581, 0x058F,
	0x0593, 0x0595, 0x0599, 0x059F, 0x05A7, 0x05AB, 0x05AD, 0x05B3,
	0x05BF, 0x05C9, 0x05CB, 0x05CF, 0x05D1, 0x05D5, 0x05DB, 0x05E7,
	0x05F3, 0x05FB, 0x0607, 0x060D, 0x0611, 0x0617, 0x061F, 0x0623,
	0x062B, 0x062F, 0x063D, 0x0641, 0x0647, 0x0649, 0x064D, 0x0653
)

################################################################################

def bytes2list(data):
    return [ord(c) for c in data]

def list2bytes(byte_list):
    return ''.join([chr(x) for x in byte_list])

def bytes2int(data):
    '''
    '\x12\x34\x56\x78' => 0x12345678
    '''
    v = 0
    for c in data:
        v <<= 8
        v |= ord(c)
    return v

def int2bytes(n, length = -1):
    '''
    0x12345678 => '\x12\x34\x56\x78'
    '''
    datas = []
    while n:
        datas.append(chr(n & 0xFF))
        n >>= 8
    datas.reverse()
    data = ''.join(datas)
    data_len = len(data)
    if length > data_len:
        data = '\x00' * (length - data_len) + data
    return data

def left_shift_1bit(data):
    datas = []
    length = len(data)
    msb = 0
    for i in range(length - 1, -1, -1):
        d = ord(data[i])
        d = (d << 1) | msb
        msb = (d >> 8)
        d &= 0xFF
        datas.append(chr(d))
    datas.reverse()
    return ''.join(datas)

def get_ber_bytes(length):
    data = ''
    if length < 128:
        data = chr(length)
    elif length < 256:
        data = '\x81' + chr(length)
    elif length < 65536:
        data = '\x82' + chr((length>>8)&0xFF) + chr(length&0xFF)
    else:
        data = '\x83' + chr((length >> 16)&0xFF) + chr((length>>8)&0xFF) + chr(length&0xFF)
    return data

def get_ber_length(bytes):
    i = 0
    #L
    L = ord(bytes[i])
    i += 1

    l_length = 1
    if (L == 0x81):
        L = ord(bytes[i])
        i += 1
        l_length += 1
        assert((L >= 128) and (L <= 255))
    elif (L == 0x82):
        L = (ord(bytes[i]) << 8) | ord(bytes[i+1])
        i += 2
        l_length += 2
        assert((L >= 256) and (L <= 65535))
    elif (L == 0x83):
        L = (ord(bytes[i]) << 16) | (ord(bytes[i+1]) << 8) | ord(bytes[i+2])
        i += 3
        l_length += 3
        assert(L >= 65536)
    else:
        assert(L <= 127)
    return (l_length, L, bytes[i:])


################################################################################

def is_small_prime(n):
    flag = True
    if n < 2:
        return False
    k = 2
    while (k * k) <= n:
        if n % k == 0:
            flag = False
            break
        k += 1
    return flag

################################################################################

def random_bytes(length):
    datas = []
    for i in range(length):
        datas.append(chr(random.randint(0x00, 0xFF)))
    return ''.join(datas)

def random_nozero_bytes(length):
    datas = []
    i = 0
    while True:
        if i == length:
            break
        v = random_bytes(1)
        if v == '\x00':
            continue
        else:
            datas.append(v)
            i += 1
    return ''.join(datas)

################################################################################

def zero_pad(data, length):
    len1 = len(data)
    if length > len1:
        data = '\x00' * (length - len1) + data
    return data

def xor(A, B):
    assert(len(A) == len(B))
    return ''.join([chr(ord(A[i]) ^ ord(B[i])) for i in range(len(A))])

def checksum(bytes):
    r = 0
    for c in bytes:
        r ^= ord(c)
    return chr(r)

def compute_crc(data, init_value = 0x6363):
    wCrc = init_value
    for c in data:
        ch = (ord(c) ^ (wCrc & 0x00ff)) & 0x00ff
        ch = (ch ^ (ch << 4)) & 0x00ff
        wCrc = ((wCrc >> 8) & 0x00ff) ^ (ch << 8) ^ (ch << 3) ^ (ch >> 4)
    ret1 = chr(wCrc & 0x00ff)
    ret2 = chr((wCrc >> 8) & 0x00ff)
    return ret1 + ret2

################################################################################

def main():
    '''
    v = int("12345678" * 1000)
    print hex(v)
    bytes = int2bytes(v, 0x08)
    print s(bytes)
    v = bytes2int(bytes)
    print hex(v)
    '''

    a1 = "1122334455 66 77"
    a2 = b(a1)
    a3 = s(a2, ', ', '(byte)0x')
    print a1
    print a3


if __name__ == '__main__':
    main()

