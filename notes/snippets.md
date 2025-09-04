# Snippets

Quick templates for common patterns seen in these problems.

## Sliding Window (no-repeat substring)
```
seen = {}
left = 0
best = 0
for right, ch in enumerate(s):
    if ch in seen and seen[ch] >= left:
        left = seen[ch] + 1
    seen[ch] = right
    best = max(best, right - left + 1)
return best
```

## Two Pointers (3Sum core)
```
nums.sort()
res = []
for i in range(len(nums)):
    if i and nums[i] == nums[i-1]:
        continue
    l, r = i+1, len(nums)-1
    while l < r:
        s = nums[i] + nums[l] + nums[r]
        if s < 0: l += 1
        elif s > 0: r -= 1
        else:
            res.append([nums[i], nums[l], nums[r]])
            l += 1
            while l < r and nums[l] == nums[l-1]:
                l += 1
return res
```

## Linked List (remove Nth from end)
```
dummy = ListNode(0, head)
fast = slow = dummy
for _ in range(n):
    fast = fast.next
while fast and fast.next:
    fast = fast.next
    slow = slow.next
slow.next = slow.next.next if slow.next else None
return dummy.next
```

## Backtracking (generate parentheses)
```
res = []
def dfs(cur, open_used, close_used):
    if open_used == n and close_used == n:
        res.append(cur); return
    if open_used < n: dfs(cur+'(', open_used+1, close_used)
    if close_used < open_used: dfs(cur+')', open_used, close_used+1)

dfs('', 0, 0)
return res
```

## Rotate Image (in-place)
```
matrix.reverse()
for i in range(len(matrix)):
    for j in range(i):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
```

## Fast Power (x^n)
```
if n < 0:
    x, n = 1/x, -n
res = 1
while n:
    if n & 1: res *= x
    x *= x
    n >>= 1
return res
```
