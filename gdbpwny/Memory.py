from binascii import hexlify, unhexlify

class Address(bytearray):
    def __init__(self, address=None):
        if isinstance(address, int):
            address = self.int2bytes(address)
        if isinstance(address, str):
            if address.startswith("0x"):
                address = address[2:]
            address = unhexlify(address)
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


class MemorySegment(bytearray):
    def __init__(self, start_address, byte_array=b""):
        self.start_address = start_address
        super().__init__(byte_array)

    def find_sequence(self, sequence):
        sequence_address = None
        offset = self.find(sequence)
        if not offset < 0:
            a1 = Address(self.start_address)
            a2 = Address(offset)
            sequence_address = a1 + a2
        return sequence_address

    def get_memory(self, address, length=0):
        offset = self.start_address - address
        assert(offset > 0)                   #TODO: add reasonable exceptions
        assert(offset + length <= len(self)) #      for these cases
        memory_bytes = self[offset:] if length == 0 else self[offset:offset+length]
        return MemorySegment(address, memory_bytes)
