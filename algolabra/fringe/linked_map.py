from typing import Iterator



class Linknode:
    """
    There's a _link underneath and this could get confusing REALLY fast if you're working like that.

    The key is the value, the value is the key.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right



class LinkedMap(dict):
    """
    hmm let's try this out. keys are ordered now. but i'm traversing values..
    """
    def __init__(self, *args, **kwargs):
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
        self.head = None
        self.tail = None

    def _cut_links(self, linknode: Linknode):
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

    def pop(self, key=None, tail=True) -> None:
        """
        Removes key and value from dict and linkedlist.

        Tail has no meaning if key is given.

        Should add a flag to supress exception here.

        :param key: if set removes key and linknode from dict
        :param tail:
        :return: value if values flag set, None otherwise
        """
        if key:
            if key in self:
                linknode = self[key]
                self._remove_linknode(linknode)
                return None
            raise KeyError
        if tail and self.tail:
            self._remove_linknode(self.tail)
            return None
        # TODO flag for this?
        raise StopIteration


    def _remove_linknode(self, linknode: Linknode) -> Linknode:
        self._cut_links(linknode)
        del self[linknode]
        return linknode

    def remove(self, key) -> None:
        if key in self:
            self._cut_links(self[key])
            del self[key]

    def __iter__(self) -> Iterator:
        # if type == 'delayed':
        return DelayedLinkedMapIterator(self)
        # return iter(self.keys())
        pass
    # def __iter__(self, type=None) -> Iterator:
    #   if type == 'delayed':
    #       return DelayedLinkedMapIterator(self)
    #   return iter(self.keys())

    def __setitem__(self, key, value):
        if key in self:
            linknode = self[key]
            self._cut_links(linknode)
            linknode.left = self.tail
            linknode.right = None
        else:
            linknode = Linknode(self.tail, None)
        super().__setitem__(key, linknode)
        if not self.head:
            self.head = linknode
        if self.tail:
            self.tail.right = linknode
        self.tail = linknode

class DelayedLinkedMapIterator:
    def __init__(self, mll: LinkedMap):
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

if __name__=='__main__':
    # mll = MappedLinkedList()
    pass