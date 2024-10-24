class Node:
    def __init__(self, x, y, left, right):
        self.x = x
        self.y = y
        self.left = left
        self.right = right

class DLLIterator:
    def __init__(self, node: Node):
        self.current = Node(None, None, None, node)

    def __next__(self):
        if self.current and self.current.right:
            self.current = self.current.right
            return self.current
        raise StopIteration

    def __iter__(self):
        return self

class MyDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)

    def move_to_end(self, k):
        self[k] = self.pop(k)

class DoubleLinkedList:
    def __init__(self, node):
        self.head = node
        self.tail = node
        self.on_fringe = {(node.x, node.y): node}

    def add_tail(self, x, y):
        tup = (x, y)
        old_node = self.on_fringe.pop(tup, None)
        if old_node is not None:
            self.on_fringe[tup] = old_node
            if self.tail == old_node:
                return
            self.move_node_to_end(old_node)
            return
        child = Node(x, y, self.tail, None)
        self.tail.right = child
        self.tail = child
        self.on_fringe[tup] = child

    def bookkeep(self, child):
        bookkeeping = self.on_fringe.pop((child.x, child.y), None)
        if bookkeeping:
            self.remove_node(bookkeeping)
        self.on_fringe[(child.x, child.y)] = child

    def move_node_to_end(self, node):
        if node.left:
            node.left.right = node.right
        if node.right:
            node.right.left = node.left
        if self.head == node:
            self.head = node.right
        #now it's loose
        self.tail.right = node
        node.left = self.tail
        self.tail = node
        node.right = None

    def remove_node(self, node):
        if node.left:
            node.left.right = node.right
        if node.right:
            node.right.left = node.left
        if self.head == node:
            self.head = node.right
        if self.tail == node:
            self.tail = node.left
        self.on_fringe.pop((node.x, node.y), None)


    def find_node(self, x, y):
        return self.on_fringe.get((x,y), None)

    def __iter__(self):
        """
        Returns iterator and duck types this as iterable.
        :return:
        """
        return DLLIterator(self.head)

    def __bool__(self):
        if self.head is None:
            return False
        return True
