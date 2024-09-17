Initialize:
Fringe F ← (s)
Cache C[start] ← (0, null),
C[n] ← null for n != start
flimit ← h(start)
found ← false

Repeat until found = true or F empty
    fmin ← ∞
    Iterate over nodes n ∈ F from left to right:
        (g, parent) ← C[n]
        f ← g + h(n)
        If f > flimit
            fmin ← min(f, fmin)
            continue
        If n = goal
        found ← true
        break
        
        Iterate over s ∈ successors(n) from right to left:
            gs ← g + cost(n, s)
            If C[s] != null
                (g′, parent) ← C[s]
            If gs ≥ g′
                continue
        If F contains s
Remove s from F
Insert s into F after n
C[s] ← (gs, n)
Remove n from F
flimit ← fmin
If found = true
Construct path from parent nodes in cache


(children(node) from right-to-left
fringe(x) from left-to-right)

Double-linked list.. so i have nodes in fringe and go through them from 0 with for node in fringe...
Then I throw children at the beginning of the list, 0? Then for next round i go from start again
to achieve this left-to-right, right-to-left, left-to-right? Worth a try, I need to limit the node loop.
