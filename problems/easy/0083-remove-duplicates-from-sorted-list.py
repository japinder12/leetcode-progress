# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution(object):
    def deleteDuplicates(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        cur = head
        while cur:
            nxt = cur.next
            while nxt and nxt.val == cur.val:
                nxt = nxt.next
            cur.next = nxt
            cur = nxt
        return head
