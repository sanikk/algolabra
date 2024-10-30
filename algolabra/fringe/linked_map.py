class Node:
    def __init__(self, value, left, right):
        """
        Node struct.
        Node needs to know it's value during iteration.
        """
        self.value = value
        self.left = left
        self.right = right

class LinkedMap(dict):
    """
    Simple Linked Map structure for Fringe Search.

    Iterator goes over dict values.
    The dict values are Nodes. Actual payload is in node.value, (x,y) here.
    (x,y) is also the dict key for faster lookups from the linked list.

    remove: O(1) dict lookup, O(1) remove through dict lookup and links, O(1) remove through links

    iterate: O(m) where m is the number of nodes actually iterated. 0 <= m <= n if heuristics are not faulty.
        Iterator does not know about size, it does not know about the mass of nodes before it. It just knows __next__.

    add_tail: O(1) dict check, O(1) dict lookup OR simple but costly __init__ operation, O(1) ops to set fields
    """
    def __init__(self, start):
        super().__init__()
        node = Node(start, None, None)
        self[start] = node

        self.head = node
        self.tail = node


    def add_tail(self, key):
        """
        no checks for missing head. if head has been removed we are not here.
        """
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
        """
        no checks. this is only used for node after adding children.
        """
        self._cut_links(self.pop(key))


    def _cut_links(self, node: Node):
        """
        cuts a node loose from its neighbors, and connects the neighbors.
        also sets head/tail.
        """
        if node.left:
            node.left.right = node.right
        if node.right:
            node.right.left = node.left

        if self.tail == node:
            self.tail = node.left
        if self.head == node:
            self.head = node.right

    def __iter__(self):
        """
        iterator with a dummy first node, and slightly modified iteration order.
        curr.next is resolved on __next__, so when the last node on fringe is handled,
        the iterator moves onto its children.

        For live linkedlists. If you MIGHT delete current before __next__ check and re-check the logic.
        """
        curr = Node(None,None,self.head)
        while curr:
            curr = curr.right
            if curr:
                yield curr.value
