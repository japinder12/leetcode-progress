class MinStack(object):
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.stack = []
        self.min_stack = []
        self.min = float('inf')

    def push(self, val):
        """
        :type val: int
        :rtype: None
        """
        self.stack.append(val)
        if val <= self.min:
            self.min = val
            self.min_stack.append(val)

    def pop(self):
        """
        :rtype: None
        """
        x = self.stack.pop()
        if self.min_stack and x == self.min_stack[-1]:
            self.min_stack.pop()
        self.min = self.min_stack[-1] if self.min_stack else float('inf')

    def top(self):
        """
        :rtype: int
        """
        return self.stack[-1]

    def getMin(self):
        """
        :rtype: int
        """
        return self.min
    
