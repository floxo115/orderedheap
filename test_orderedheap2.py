import pytest
import random

from orderedheap_with_references import OrderedHeapElement, OrderedHeap


def create_good_tree(num):
    heap = OrderedHeap()
    inputs = [
        [
            [100, 4, 3],
            [75, -1, 2],
            [50, 1, 4],
            [25, 0, -1],
            [0, 2, 0],
        ],
        [
            [100, -1, 1],
            [75, 0, 3],
            [50, 4, -1],
            [25, 1, 4],
            [0, 3, 2],
        ],
        [
            [100, -1, 2],
            [75, 2, 4],
            [50, 0, 1],
            [25, 4, -1],
            [0, 1, 3],
        ]
    ]

    for i, inp in enumerate(inputs[num]):
        heap.array.append(OrderedHeapElement(None, [inp[0]]))

    for i, inp in enumerate(inputs[num]):
        heap.array[i].previous = None if inp[1] == -1 else heap.array[inp[1]]
        if heap.array[i].previous is None:
            heap.first_inserted = heap.array[i]
        heap.array[i].next = None if inp[2] == -1 else heap.array[inp[2]]
        if heap.array[i].next is None:
            heap.last_inserted = heap.array[i]

    return heap


def print_heap_info(heap: OrderedHeap):
    s = "["
    for el in heap.array:
        s += f"{el.sort_values[0]}, "
    s = s[:-2]
    s += "]"
    s += "["
    cur = heap.first_inserted
    while cur:
        s += f"{cur.sort_values[0]}, "
        cur = cur.next

    s = s[:-2]
    s += "]"

    return s

def is_heap_sorted(heap: OrderedHeap):
    for i in range(len(heap)):
        if not heap.is_leaf(i):
            left_child = heap.get_left_child(i)
            if heap.array[i] < heap.array[left_child]:
                return False

            if left_child + 1 == len(heap):
                continue

            if heap.array[i] < heap.array[left_child + 1]:
                return False

    return True



def test_the_testtrees():
    heap = create_good_tree(0)
    assert print_heap_info(heap) == "[100, 75, 50, 25, 0][75, 50, 0, 100, 25]"
    heap = create_good_tree(1)
    assert print_heap_info(heap) == "[100, 75, 50, 25, 0][100, 75, 25, 0, 50]"
    heap = create_good_tree(2)
    assert print_heap_info(heap) == "[100, 75, 50, 25, 0][100, 50, 75, 0, 25]"


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
                [25, 50, 75, 0, 25],
                "[75, 50, 25, 0, 25][25, 50, 75, 0, 25]"
        ),
        (
                [25, 30, 100, 9, 1000],
                "[1000, 30, 100, 9, 25][25, 30, 100, 9, 1000]"
        ),
        (
                [1000, 80, 90, 30, 20, 50, 10],
                "[1000, 80, 90, 30, 20, 50, 10][1000, 80, 90, 30, 20, 50, 10]"
        ),

    ],
)
def test_heap_creation(inputs, expected):
    heap = OrderedHeap()
    for i in inputs:
        heap.insert_element([i])

    heap.build_heap()
    assert print_heap_info(heap) == expected
    assert heap.first_inserted.sort_values[0] == inputs[0]
    assert heap.last_inserted.sort_values[0] == inputs[-1]
    assert len(heap) == len(inputs)
    assert is_heap_sorted(heap)

def test_heap_creation_fuzzy():
    heap = OrderedHeap()
    for i in range(random.randint(100,100000)):
        heap.insert_element([random.random()])

    # test if the heap with random elements is a true heap
    heap.build_heap()
    assert is_heap_sorted(heap)

    # test if the heap with random elements works as a doubly linked list
    cur = heap.first_inserted
    jumps = 0
    while cur != heap.last_inserted:
        cur = cur.next
        jumps += 1

    assert jumps + 1 == len(heap)

    cur = heap.last_inserted
    jumps = 0
    while cur != heap.first_inserted:
        cur = cur.previous
        jumps += 1

    assert jumps + 1 == len(heap)




