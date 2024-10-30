class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

class LinkedDict(dict):
    def __init__(self, start):
        super().__init__()
        node = Node(start, None, None)
        self[start] = node

        self.head = node
        self.tail = node


    def add_tail(self, key):
        if key in self:
            node = self[key]
            self._cut_links(node)
            node.left = self.tail
            node.right = None
        else:
            node = Node(key, self.tail, None)
            self[key] = node
        if self.tail:
            self.tail.right = node
        self.tail = node

    def remove(self, key):
        self._cut_links(self.pop(key))


    def _cut_links(self, node: Node):
        if node.left:
            node.left.right = node.right
        if node.right:
            node.right.left = node.left

        if self.tail == node:
            self.tail = node.left
        if self.head == node:
            self.head = node.right

    def __iter__(self):
        curr = Node(None,None,self.head)
        while curr:
            curr = curr.right
            if curr:
                yield curr.value
