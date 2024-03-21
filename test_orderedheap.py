import pytest

from orderedHeap import OrderedHeapElement, OrderedHeap


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

    for inp in inputs[num]:
        prev_input = inp[1]
        next_input = inp[2]
        value = inp[0]
        heap.array.append(OrderedHeapElement(prev_input, next_input, value))

    return heap


def print_heap_info(heap: OrderedHeap):
    s = ""
    for el in heap.array:
        s += f"[{el.previous_idx}, {el.next_idx}, {el.value}]"
    return s


@pytest.mark.parametrize("heap, swap_index, expected", [
    [
        create_good_tree(0), 4,
        "[1, 3, 100][2, 0, 0][4, 1, 50][0, -1, 25][-1, 2, 75]"
    ],
    [
        create_good_tree(1), 1,
        "[1, 3, 75][-1, 0, 100][4, -1, 50][0, 4, 25][3, 2, 0]"
    ],
    [
        create_good_tree(2), 4,
        "[-1, 2, 100][4, 3, 0][0, 4, 50][1, -1, 25][2, 1, 75]"
    ],
    [
        create_good_tree(2), 2,
        "[2, 1, 50][0, 4, 75][-1, 0, 100][4, -1, 25][1, 3, 0]"
    ],
])
def test_swap_elements(heap, swap_index, expected):
    heap.swap_elements(swap_index)
    output = print_heap_info(heap)
    assert output == expected


@pytest.mark.parametrize("inputs, expected", [
    [
        [5,20,3,9,2,10],
        "[3, 5, 20][5, 4, 9][4, -1, 10][-1, 0, 5][1, 2, 2][0, 1, 3]"
    ],
])
def test_insert_into_empty_heap(inputs, expected):
    heap = OrderedHeap()
    pos = -1
    for inp in inputs:
        pos = heap.insert(pos, inp)

    assert print_heap_info(heap) == expected
