class Node:
    def __init__(self, data=None, prev=None, next=None):
        self.prev = prev
        self.next = next
        self.data = data

class DLLIterator:
    def __init__(self, node: Node):
        self.previous = Node(next=node)

    def __next__(self):
        if self.previous and self.previous.next:
            self.previous = self.previous.next
            return self.previous
        raise StopIteration

    def __iter__(self):
        return self

class DoubleLinkedList:
    def __init__(self, node=None, data=None):
        if data:
            node = Node(data=data)
        self.head = node

    def add_data_after_node(self, data, node):
        new_node = Node(prev=node, next=node.next, data=data)
        if node.next:
            next_node = node.next
            next_node.prev = new_node
        node.next = new_node

    def remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if self.head == node:
            self.head = node.next

    def remove_data(self, data):
        node = self.find_node_with_data(data)
        if node:
            self.remove_node(node)

    def find_node_with_data(self, data):
        for node in iter(self):
            if node.data == data:
                return node

    def __iter__(self):
        return DLLIterator(self.head)

if __name__=='__main__':
    dll = DoubleLinkedList(data=1)