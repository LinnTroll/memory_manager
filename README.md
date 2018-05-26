# Memory manager

This is the simplest implementation of the memory manager.

I chose this algorithm, because it is the simplest possible, with the minimum probability of error resolution.
This algorithm is far from optimal, and there are many possibilities for its optimization.

The main principle of the algorithm:
  - We have a buffer of the specified size
  - We can allocate areas from the buffer using the alloc method, while there is enough space in the buffer
  - If there is not enough space in the buffer, we will get an exception
  - To clear the memory area from the buffer, we pass the object returned by the alloc method to the free method
  - After any execution of free methods, we run defragmrntation
  - Defragmentation goes through all the fragments in the buffer, and moves them close to each other, filling holes
    from remote objects and freeing up a maximum of free space at the end of the buffer

In the future, to optimize this algorithm, we can take:
  - Run defragmentation only from the element that we deleted, because it's useless to go through all the previous ones
  - Start defragmentation only if there is not enough free space at the end of the buffer
  - Implement an algorithm that controls free spaces between occupied areas of the buffer, and allows to allocate there
    new areas of memory, if they fit there

## How to use:

```
from mem import MemoryManager

mm = MemoryManager(10)
fragment1 = mm.alloc(8)
fragment2 = mm.alloc(2)

fragment1.init('a')
fragment2.init('b')

print(fragment1)
print(fragment2)
```

## How to run tests:

```
python test.py
```
