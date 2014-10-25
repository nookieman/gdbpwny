from binascii import hexlify

class Address(bytearray):
    def __init__(self, address=None):
        if isinstance(address, int):
            address = self.int2bytes(address)
        super().__init__(address)

    @staticmethod
    def int2bytes(address):
        hex_string = hex(address)[2:]
        if len(hex_string) % 2 == 1:
            hex_string = "0{}".format(hex_string)
        return bytes.fromhex(hex_string)

    def __add__(self, other):
        if isinstance(other, int):
            other = Address(other)
        s1 = Address(self if len(self) > len(other) else other)
        s2 = self if not len(self) > len(other) else other
        carry = 0
        last_index = 0
        for index in range(-1, -len(s2)-1, -1):
            s = s1[index] + s2[index] + carry
            #print("adding: {0:x} + {1:x} + {2:x} = {3:x}".format(s1[index], s2[index], carry, s))
            if s > 255:
                carry = 1
                s %= 256
            else:
                carry = 0
            s1[index] = s
            last_index = index
        while carry:
            last_index -= 1
            s = s1[last_index] + 1
            if s > 255:
                s %= 256
                carry = 1
        return Address(s1)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return hexlify(self).decode('ascii')
