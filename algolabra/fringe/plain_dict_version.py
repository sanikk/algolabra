from typing import Iterator


class LinkNode:
    """
    Most structs have _link and this could get confusing REALLY fast if you're working like that.

    The key is the value, the value is the key.
    Something mabbe helpful for now so I can keep track of things.
    """
    def __init__(self, key, left, right):
        self.key = key
        self.left = left
        self.right = right

class MappedLinkedList(dict):
    """
    hmm let's try this out. keys are ordered now. but i'm traversing values..
    """
    def __init__(self, head=None, head_node=None, *args, **kwargs):
        """
        head can be head_node, i don't care.
        we link keys or values? version for both?
        best would be both in same packet.

        :param head:
        :param head_node:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, *kwargs)
        # ensin tyhmät tarkistukset
        if head:
            if not head_node:
                head_node = LinkNode(head, None, None)
            self[head] = head_node
        self.head = head_node
        self.tail = head_node

    def _cut_links(self, linknode: LinkNode):
        """
        If you change linknode.left,right to None iteration while this list
        changes will cause problems. Here be dragons.

        :param linknode:
        :return:
        """
        if linknode.left:
            linknode.left.right = linknode.right
        if linknode.right:
            linknode.right.left = linknode.left
        if self.tail == linknode:
            self.tail = linknode.left
        if self.head == linknode:
            self.head = linknode

    def pop(self, key=None, tail=True) -> LinkNode:
        if key:
            if key in self:
                linknode = self[key]
                self.remove_linknode(linknode)
                return linknode
            return None
        if tail:
            return self.remove_linknode(self.tail)
        return self.remove_linknode(self.head)

    def remove_linknode(self, linknode: LinkNode) -> LinkNode:
        self._cut_links(linknode)
        del self[linknode.key]
        return linknode

    def __iter__(self) -> Iterator:
        return DelayedMappedLinkedListIterator(self)


class DelayedMappedLinkedListIterator:
    def __init__(self, mll: MappedLinkedList):
        self.mll = mll
        self.current_key = mll.head

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_key is None:
            raise StopIteration
        prev = self.current_key
        self.current_key = self.current_key.right
        return prev