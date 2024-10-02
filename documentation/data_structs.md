# On the data structure for fringe

## The thoughts
So Ordered Dict seems nice. It remembers insert order out of the box, keys are a set. 
"Big-O running times for all methods are the same as regular dictionaries."

In python docs there is a nice bit of code to replace earlier insertions as 
[LastUpdatedOrderedDict](https://docs.python.org/3.12/library/collections.html#ordereddict-examples-and-recipes)
This looks like promising machinery.

```python
class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
```

The OrderedDict is made of _Link(object), which has prev and next in true "all python lists are linked lists" fashion.
I might try to use that for insertions.
```python
class _Link(object):
    __slots__ = 'prev', 'next', 'key', '__weakref__'
```
Actually making a working model using these would be outside the scope of this project. It would seem
that a decent implementation of a linked list with node tracking should be fast enough.

So linked list with built-in dict seemed a reasonable solution for now.

## The notes from fringe pdf

The data structure used by Fringe Search can be
thought of as two lists: one for the current iteration (now)
and one for the next iteration (later).

Initially the now list
starts off with the root node and the later list is empty.

The node at the
head of the now list (head) is examined and one of the following 
actions is taken:

1. If f (head) is greater than the threshold then head is
removed from now and placed at the end of later.
In other words, we do not need to consider head on
this iteration (we only visited head), so we save it for
consideration in the next iteration.

2. If f (head) is less or equal than the threshold then we
need to consider head’s children (expand head). Add
the children of head to the front of now. Node head
is discarded.

When an iteration completes and a goal has not been found,
then the search threshold is increased, the later linked list
becomes the now list, and later is set to empty.


## The fringe operations from pseudo code:
- Iterate over nodes n ∈ F from left to right
- If F contains s: Remove s from F
- Insert s into F after n
- Remove n from F

### + bool(fringe) for empty

## Sources
fringe pdf
https://docs.python.org/3.12/library/collections.html#ordereddict-examples-and-recipes
https://github.com/python/cpython/blob/main/Lib/collections/__init__.py