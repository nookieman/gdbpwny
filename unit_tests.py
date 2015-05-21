from gdbpwny.Memory import Address, MemorySegment

import unittest

class AddressTest(unittest.TestCase):
    def test_init(self):
        address = Address(b"\x93\xbf\x43\x12")
        self.assertEqual(address[0], 0x93)
        self.assertEqual(address[1], 0xbf)
        self.assertEqual(address[2], 0x43)
        self.assertEqual(address[3], 0x12)

        address = Address(4321)
        self.assertEqual(address[0], 0x10)
        self.assertEqual(address[1], 0xe1)

        address = Address("0x95bf43a2")
        self.assertEqual(address[0], 0x95)
        self.assertEqual(address[1], 0xbf)
        self.assertEqual(address[2], 0x43)
        self.assertEqual(address[3], 0xa2)

        address = Address("ff4ea24242a1")
        self.assertEqual(address[0], 0xff)
        self.assertEqual(address[1], 0x4e)
        self.assertEqual(address[2], 0xa2)
        self.assertEqual(address[3], 0x42)
        self.assertEqual(address[4], 0x42)
        self.assertEqual(address[5], 0xa1)

    def test_add(self):
        a = Address(b"\x12\x34\x56")
        b = Address(b"\x12\x34")
        summed = a + b
        comparator = Address(b"\x12\x46\x8a")
        self.assertEqual(summed, comparator)

        summed = a + b"\x12\x34"
        self.assertEqual(summed, comparator)

        summed = a + 0x1234
        self.assertEqual(summed, comparator)

        summed = a + 6
        comparator = Address(b"\x12\x34\x5c")
        self.assertEqual(summed, comparator)

        summed = a + 1234
        comparator = Address(b"\x12\x39\x28")
        self.assertEqual(summed, comparator)

    def test_str(self):
        address = Address(b"\x01")
        self.assertEqual(str(address), "01")
        address = Address(1)
        self.assertEqual(str(address), "01")
        address = Address(b"\xaf\x42\x23\xff\x5a\x77")
        self.assertEqual(str(address), "af4223ff5a77")
        address = Address(0x616161424242BBBB)
        self.assertEqual(str(address), "616161424242bbbb")
        address = Address(54321)
        self.assertEqual(str(address), "d431")


class MemorySegmentTest(unittest.TestCase):
    def test_find_sequence(self):
        address = Address(b"\x12\x34\x56\x78")
        memory_bytes = bytearray(b"foobarBBBBtesttest")
        memory_segment = MemorySegment(address, memory_bytes)
        position = memory_segment.find_sequence(bytearray(b"BBBB"))
        self.assertEqual(position, Address(b"\x12\x34\x56\x7e"))

        address = Address(0xbeef57ea)
        memory_bytes = bytearray(b"laberlaber")
        memory_segment = MemorySegment(address, memory_bytes)
        position = memory_segment.find_sequence(bytearray(b"l"))
        self.assertEqual(position, address)

    def test_find_sequence_fail(self):
        address = Address(0xbeef57ea)
        memory_bytes = bytearray(b"laber")
        memory_segment = MemorySegment(address, memory_bytes)
        position = memory_segment.find_sequence(bytearray(b"BBBBBBBB"))
        self.assertEqual(position, None)


if __name__ == "__main__":
    unittest.main()
