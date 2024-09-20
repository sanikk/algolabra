

class Node:
    def __init__(self, data=None, prev=None, nex=None):
        self.prev = prev
        self.next = nex
        self.data = data
    def remove(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev

class DLLIterator:
    def __init__(self, node: Node):
        self.current = node

    def __next__(self):
        if self.current:
            node = self.current
            self.current = node.next
            return node
        raise StopIteration

    def __iter__(self):
        return self

class DoubleLinkedList:
    def __init__(self, node=None):
        # if head set we're not empty
        self.head = node
        self.tail = self.head

    def add_to_begin(self, node):
        if self.head:
            self.head.prev = node
        node.next = self.head
        self.head = node
        if not self.tail:
            self.tail = node

    def add_data_to_begin(self, data):
        node = Node(data)
        self.add_to_begin(node)

    def remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

        if node == self.head:
            self.head = node.next
        if node == self.tail:
            self.tail = node.prev

    def __iter__(self):
        return DLLIterator(self.head)

if __name__=='__main__':
    dll = DoubleLinkedList()
    if dll.head:
        print("hep 1")
    dll.add_data_to_begin(1)

    if dll.head:
        print("hep 2")

    for i in range(9):
        dll.add_data_to_begin(i)

    for nro in dll:
        if nro.data == 5:
            dll.remove_node(nro)

    for nro in dll:
        print(nro.data)