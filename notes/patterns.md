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

## Stack (Valid Parentheses)
- Map closers to openers and verify stack empties at end.

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
