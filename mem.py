from exceptions import CannotAllocateMemoryException


class Fragment:
    def __init__(self, buffer, start, end):
        self.buffer = buffer
        self.start = start
        self.end = end
        self.size = end - start

    def __repr__(self):
        return 'FRAGMENT[{}..{}]{}'.format(
            self.start,
            self.end,
            self.buffer.buffer[self.start:self.end],
        )

    def __setitem__(self, index, value):
        assert self.size > index
        self.buffer.buffer[index + self.start] = value

    def __getitem__(self, index):
        assert self.size > index
        return self.buffer.buffer[index + self.start]

    def move(self, index):
        diff = self.start - index
        assert diff >= 0
        self.buffer.buffer[self.start - diff:self.end - diff] = self.buffer.buffer[self.start:self.end]
        self.start -= diff
        self.end -= diff

    def init(self, value=None):
        self.buffer.buffer[self.start:self.end] = [value] * self.size


class Buffer:
    def __init__(self, size):
        self.cursor = 0
        self.free_cells = size
        self.buffer = [None] * size
        self.fragments = []

    def __repr__(self):
        return 'BUFFER{}'.format(self.buffer)

    def alloc(self, size):
        if size > self.free_cells:
            raise CannotAllocateMemoryException

        fragment = Fragment(self, self.cursor, self.cursor + size)
        self.fragments.append(fragment)
        self.cursor += size
        self.free_cells -= size
        return fragment

    def free(self, fragment):
        self.fragments.remove(fragment)
        self.free_cells += fragment.size
        self.cursor = self.defragmentation()

    def defragmentation(self):
        cursor = 0
        for fragment in self.fragments:
            if fragment.start != cursor:
                fragment.move(cursor)
            cursor += fragment.size
        return cursor


class MemoryManager:
    def __init__(self, size):
        self._buffer = Buffer(size)

    def alloc(self, size):
        return self._buffer.alloc(size)

    def free(self, block):
        self._buffer.free(block)
