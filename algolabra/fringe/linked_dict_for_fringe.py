from typing import Iterator


class Linknode:
    """
    There's a _link underneath and this could get confusing REALLY fast if you're working like that.

    The key is the value, the value is the key.
    """
    def __init__(self, value, left, right):
        self.left = left
        self.right = right
        self.value = value

class LinkedDictForFringe(dict):
    """
    Ok general cases can go in the other files.
    """
    def __init__(self, head):
        """
        not sure i need the nodes to know who they are.
        if i can get the keys from the
        :param head: key and value of head
        """
        super().__init__()

        self.head = None
        self.tail = None
        self[head] = head

    def _cut_links(self, linknode: Linknode):
        """
        Don't mess with iteration + this.

        Currently if the 'linknode' here is the current of an iterator, since this linknode's internal
        refs are untouched the iterator SHOULD continue to the next from this one, so things go smoothly.

        YMMV, Here be dragons, etc. And the current should never

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
            self.head = linknode.right

    def pop(self, key=None) -> None:
        """
        Removes key and value from dict and linkedlist.

        Should add a flag to supress exception here.

        :param key: if set removes key and linknode from dict
        :return: value if values flag set, None otherwise
        """
        if key:
            if key in self:
                linknode = self[key]
                self._remove_linknode(linknode)
                return linknode.value
            raise KeyError
        if self.tail:
            value = self.tail.value
            self._remove_linknode(self.tail)
            return value
        raise StopIteration


    def _remove_linknode(self, linknode: Linknode) -> Linknode:
        """
        removes entry by linknode reference. thought up for internals but not forced in anyway.

        :param linknode: Linknode object. quack quack.
        :return: the very same linknode object. maybe to bind to a local ref? if unused it should be collect very fast
            unless the value holds a lot of stuff.
        """
        self._cut_links(linknode)
        del self[linknode]
        return linknode

    def remove(self, key) -> None:
        """
        remove entry by key

        dict should give O(1) search time
        linkedlist structs, both the one under dict.keys(), and the one used here, should give O(1) removals with access
        to the links.

        Some caution and testing adviced.

        :param key: whatever is used as key
        :return: None
        """
        if key in self:
            self._cut_links(self[key])
            del self[key]

    def __iter__(self) -> Iterator:
        """

        :return: a suitable iterator for fringe search
        """
        return DelayedLinkedDictForFringeIterator(self)

    def __setitem__(self, key, value):
        """
        Slightly modified dict.__setitem__
        Also makes the dict record. With a Linknode.

        :param key:
        :param value:
        :return:
        """
        if key in self:
            linknode = self[key]
            self._cut_links(linknode)
            linknode.left = self.tail
            linknode.right = None
            linknode.value = value or key
        else:
            linknode = Linknode(value or key, self.tail, None)
        super().__setitem__(key, linknode)
        if not self.head:
            self.head = linknode
        if self.tail:
            self.tail.right = linknode
        self.tail = linknode

class DelayedLinkedDictForFringeIterator:
    """
    Suitable Iterator for Fringe

    """
    def __init__(self, mll: LinkedDictForFringe):
        self.mll = mll
        self.current_key = mll.head

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_key is None:
            raise StopIteration
        prev = self.current_key
        self.current_key = self.current_key.right
        return prev.value
