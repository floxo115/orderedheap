from typing import List


class OrderedHeap():
    def __init__(self):
        self.array: List[OrderedHeapElement] = []

    def __len__(self):
        return len(self.array)

    def __repr__(self):
        s = f"<OrderedHeap [\n"
        for el in self.array:
            s += f"\t{el}\n"
        s += f"]>"
        return s

    @staticmethod
    def get_parent(pos: int):
        assert pos >= 0

        if pos == 0:
            return None
        if pos % 2 == 0:
            return (pos - 1) // 2
        else:
            return pos // 2

    @staticmethod
    def get_left_child(pos):
        assert pos >= 0
        return 2 * pos + 1

    def swap_elements(self, child_pos):
        # if pos_child is the root position raise a ValueError
        if child_pos == 0:
            raise ValueError("The root element can not be swapped with its parent!")

        parent_pos = OrderedHeap.get_parent(child_pos)
        parent = self.array[parent_pos]
        child = self.array[child_pos]

        # we have to check if the elements are in a neighbor
        # relationship and set the indexes according to it
        if parent.previous_idx == child_pos:
            parent.previous_idx = parent_pos
        elif parent.next_idx == child_pos:
            parent.next_idx = parent_pos

        if child.previous_idx == parent_pos:
            child.previous_idx = child_pos
        elif child.next_idx == parent_pos:
            child.next_idx = child_pos


        # we update the previous/next indices of neighbors if they are
        # not the parent/child itself (i.e. not already changed in previous step)
        if parent.previous_idx >= 0 and parent.previous_idx != parent_pos:
            self.array[parent.previous_idx].next_idx = child_pos
        if parent.next_idx >= 0 and parent.next_idx != parent_pos:
            self.array[parent.next_idx].previous_idx = child_pos

        if child.previous_idx >= 0 and child.previous_idx != child_pos:
            self.array[child.previous_idx].next_idx = parent_pos
        if child.next_idx >= 0 and child.next_idx != child_pos:
            self.array[child.next_idx].previous_idx = parent_pos

        # we swap the parent with the child inside the heap
        self.array[parent_pos], self.array[child_pos] = \
            self.array[child_pos], self.array[parent_pos]

        return parent_pos

    def insert(self, previous_idx:int, value: float, data = None):
        new_element = OrderedHeapElement(previous_idx, -1, value, data)

        self.array.append(new_element)

        if len(self) >= 1:
            self.array[previous_idx].next_idx = len(self)-1


        pos = len(self) - 1
        while pos != 0:
            parent_pos = OrderedHeap.get_parent(pos)
            parent = self.array[parent_pos]
            if parent >= new_element:
                break

            pos = self.swap_elements(pos)

        return pos


class OrderedHeapElement:
    def __init__(self, previous_idx: int, next_idx: int, value: float, data: any = None):
        self.previous_idx = previous_idx
        self.next_idx = next_idx
        self.value = value
        self.data = data

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __repr__(self):
        return f"<OrderedHeapElement [previous_idx: {self.previous_idx}, next_idx: {self.next_idx}, value: {self.value}]>"
