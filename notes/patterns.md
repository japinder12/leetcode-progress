# Patterns

Use this file to summarize common problem‑solving patterns and when to apply them.

## Hash Map Lookup (Two Sum)
- When: find complements/pairs quickly.
- Idea: store seen value → index; for each `x`, check `target-x`.
- Time: O(n); Space: O(n).

## Sliding Window (Longest Substring Without Repeating)
- When: contiguous subarrays/substrings with constraints.
- Template: maintain `left`, expand `right`, shrink while invalid.
- Tip: use set or last-index map; update best on each step.

## Two Pointers
- When: sorted arrays, pair sums, in‑place partitioning.
- Container With Most Water: move the pointer at the shorter line.
- 3Sum/4Sum: sort + dedupe + inner two‑pointer; skip duplicates carefully.

## Binary Search
- When: monotonic predicate, first/last true, search on answer

## Prefix/Suffix
- When: range sums, products, precompute to answer queries fast

## Linked Lists
- Use a dummy node to simplify head changes (merge, remove‑nth).
- Fast/slow pointers for nth‑from‑end; or two passes; or stack.
- Recursion works for merge; be mindful of recursion depth.

## Stack
- When: matching pairs, next greater/smaller, spans/ranges, histogram areas.

- Parentheses (Valid Parentheses): map closers→openers; stack should empty.
```py
def is_valid_parens(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch in pairs.values():
            st.append(ch)
        elif ch in pairs:
            if not st or st.pop() != pairs[ch]:
                return False
        # ignore other chars if present
    return not st
```

- Monotonic Stack (Next Greater Element): keep indices; pop while current breaks monotonicity.
```py
def next_greater_indices(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [-1] * n  # store index (or nums[i] if value desired)
    st = []         # indices with decreasing values on stack
    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            j = st.pop()
            res[j] = i
        st.append(i)
    return res
```

- Largest Rectangle in Histogram: store (start_index, height); extend start when popping.
```py
def largest_rectangle_area(heights: list[int]) -> int:
    st = []  # pairs: (start_index, height), heights increasing in stack
    best = 0
    for i, h in enumerate(heights + [0]):  # sentinel 0 to flush stack
        start = i
        while st and st[-1][1] > h:
            idx, hh = st.pop()
            best = max(best, hh * (i - idx))
            start = idx
        st.append((start, h))
    return best
```
Tips: choose increasing/decreasing based on "next greater/smaller"; store indices to compute distances; use a sentinel to flush remaining bars.

## Backtracking (Generate Parentheses)
- Build strings with counts of open/close used; only add `)` if `close < open`.

## Strings/Conversion
- Reverse Integer: reverse digits of `abs(x)`, reapply sign, clamp to 32‑bit.
- Palindrome Number: compare halves or reverse; avoid string where required.
- Roman ↔ Integer: greedy value–symbol pairs; handle IV, IX, XL, XC, CD, CM.

## Matrix Tricks
- Rotate Image: reverse rows, then transpose in place.

## Hashing/Grouping (Anagrams)
- Sorted key: simple; O(k log k) per string.
- Count vector (26): faster O(k) for lowercase inputs.

## Exponentiation by Squaring (Pow)
- Recurse/iterate on `n//2`; square base; multiply once if odd; handle negative `n`.

## Graphs
- BFS for shortest steps in unweighted graphs
- DFS for traversal/components/toposort (with cycle checks)

## Dynamic Programming
- Identify state, transition, base cases, and ordering
