class Solution(object):
    def addBinary(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        out = []
        while i >= 0 or j >= 0 or carry:
            da = ord(a[i]) - 48 if i >= 0 else 0
            db = ord(b[j]) - 48 if j >= 0 else 0
            s = da + db + carry
            out.append(str(s & 1))
            carry = s >> 1
            i -= 1
            j -= 1
        return ''.join(reversed(out))
