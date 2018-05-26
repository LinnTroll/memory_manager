import unittest

from mem import MemoryManager
from exceptions import CannotAllocateMemoryException


class TestMemoryManager(unittest.TestCase):

    def test_alloc_less(self):
        mm = MemoryManager(10)
        mm.alloc(9)

    def test_alloc_equal(self):
        mm = MemoryManager(10)
        mm.alloc(10)

    def test_alloc_more(self):
        mm = MemoryManager(10)
        self.assertRaises(CannotAllocateMemoryException, mm.alloc, 11)

    def test_alloc_partial(self):
        mm = MemoryManager(10)
        mm.alloc(3)
        mm.alloc(3)
        mm.alloc(3)
        mm.alloc(1)

    def test_alloc_partial_more(self):
        mm = MemoryManager(10)
        mm.alloc(3)
        mm.alloc(3)
        mm.alloc(3)
        self.assertRaises(CannotAllocateMemoryException, mm.alloc, 3)

    def test_free_equal(self):
        mm = MemoryManager(10)
        fr = mm.alloc(10)
        mm.free(fr)
        mm.alloc(10)

    def test_free_partial(self):
        mm = MemoryManager(10)
        fr1 = mm.alloc(3)
        mm.alloc(3)
        mm.alloc(3)
        mm.free(fr1)
        mm.alloc(4)

    def test_free_partial_overflow(self):
        mm = MemoryManager(10)
        fr1 = mm.alloc(3)
        mm.alloc(3)
        mm.alloc(3)
        mm.free(fr1)
        self.assertRaises(CannotAllocateMemoryException, mm.alloc, 5)

    def test_defragmentation(self):
        mm = MemoryManager(10)
        fr1 = mm.alloc(3)
        fr2 = mm.alloc(3)
        fr3 = mm.alloc(4)
        fr1.init('a')
        fr2.init('b')
        fr3.init('c')
        mm.free(fr2)
        self.assertEqual(mm._buffer.buffer[3:7], ['c'] * 4)
        mm.free(fr1)
        self.assertEqual(mm._buffer.buffer[0:4], ['c'] * 4)
        fr4 = mm.alloc(6)
        fr4.init('d')
        self.assertEqual(mm._buffer.buffer[4:10], ['d'] * 6)
        mm.free(fr3)
        self.assertEqual(mm._buffer.buffer[0:6], ['d'] * 6)


if __name__ == '__main__':
    unittest.main()
