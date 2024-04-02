from orderedHeap import OrderedHeapElement, OrderedHeap

heap = OrderedHeap()
pos = -1
# for i in range(30):
#     pos = heap.insert(pos, i)
# print(heap)
#
# for el in heap.array:
#     print(heap.where_is_element(el))
#
# print()
# heap.array[0].value = -100000
# print(heap.heapify(0))
#
# for i, el in enumerate(heap.array):
#     assert heap.where_is_element(el) == i
#
# print(heap)

import numpy as np
pos = -1
for i in range(5000000):
    heap.insert(pos, np.random.random())

for _ in range(5000000):
    heap.delete_element(0)


