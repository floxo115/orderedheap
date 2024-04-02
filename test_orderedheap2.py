import random

import pytest

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


def is_heap_ordered(heap: OrderedHeap):
    cur = heap.first_inserted
    jumps1 = 0
    while cur != heap.last_inserted:
        cur = cur.next
        jumps1 += 1

    cur = heap.last_inserted
    jumps2 = 0
    while cur != heap.first_inserted:
        cur = cur.previous
        jumps2 += 1

    return jumps1 + jumps2


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
    for i in range(random.randint(100, 100000)):
        heap.insert_element([random.random()])

    # test if the heap with random elements is a true heap
    heap.build_heap()
    assert is_heap_sorted(heap)

    # test if the heap with random elements works as a doubly linked list
    jumps = is_heap_ordered(heap)
    assert jumps + 2 == len(heap) * 2


@pytest.mark.parametrize(
    "heap, expected",
    (
            (create_good_tree(0), "[75, 25, 50, 0][75, 50, 0, 25]"),
    )
)
def test_delete_max(heap, expected):
    len_heap = len(heap)
    heap.delete_max()
    assert print_heap_info(heap) == expected
    assert len(heap) == len_heap -1
    assert is_heap_sorted(heap)
    assert is_heap_ordered(heap) + 2 == 2 * len(heap)

def test_delete_max_from_empty_heap():
    heap = OrderedHeap()
    with pytest.raises(ValueError):
        heap.delete_max()

def test_delete_max_from_heap_with_only_root():
    heap = OrderedHeap()
    heap.insert_element([1000])
    heap.build_heap()
    heap.delete_max()

    assert heap.first_inserted is None
    assert heap.last_inserted is None

    assert len(heap) == 0




def test_delete_max_fuzzy():
    heap = OrderedHeap()
    for i in range(random.randint(100, 1000)):
        heap.insert_element([random.random()])

    heap.build_heap()

    len_heap = len(heap)
    for i in range(1, len_heap):
        heap.delete_max()
        assert is_heap_sorted(heap)
        assert is_heap_ordered(heap) + 2 == 2*len_heap - 2*i


@pytest.mark.parametrize(
    "heap, update, pos, expected",
    (
            (create_good_tree(0), [20], 0, "[75, 25, 50, 20, 0][75, 50, 0, 20, 25]"),
            (create_good_tree(0), [1000], 3, "[1000, 100, 50, 75, 0][75, 50, 0, 100, 1000]"),
    )
)
def test_update_element(heap, update, pos, expected):
    heap.update_node(update, pos)
    assert print_heap_info(heap) == expected


def test_update_element_fuzzy():
    heap = OrderedHeap()
    for i in range(random.randint(100, 1000)):
        heap.insert_element([random.random()])

    heap.build_heap()

    for i in range(50):
        el = random.choice(heap.array)
        heap.update_node([random.random()], el.pos)
        assert is_heap_sorted(heap)
        assert is_heap_ordered(heap) + 2 == 2*len(heap)




