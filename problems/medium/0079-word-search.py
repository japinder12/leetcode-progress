class Solution(object):
    def exist(self, board, word):
        """
        :type board: List[List[str]]
        :type word: str
        :rtype: bool
        """
        ROWS, COLS = len(board), len(board[0])

        def dfs(r, c, i):
            if i == len(word):
                return True
            if r < 0 or c < 0 or r >= ROWS or c >= COLS:
                return False
            if board[r][c] != word[i]:
                return False

            temp, board[r][c] = board[r][c], "#"
            found = (
                dfs(r+1, c, i+1) or 
                dfs(r-1, c, i+1) or 
                dfs(r, c+1, i+1) or 
                dfs(r, c-1, i+1)
                )
            board[r][c] = temp

            return found

        for r in range(ROWS):
            for c in range(COLS):
                if dfs(r, c, 0):
                    return True
        return False
    