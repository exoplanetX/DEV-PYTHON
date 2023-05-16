"""
给定一个二叉树，按中序遍历
"""
class Solution(object):
    result_list = []
    # 构造
    def __init__(self, value=None, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

    # 遍历
    def mid_order(self,root):
        if root is None:
            return
        self.mid_order(root.left)
        Solution.result_list.append(root.value)
        self.mid_order(root.right)
        
a=Solution()
b=Solution()
c=Solution()

a.value=10
b.value=20
c.value=30

a.left=b
a.right=c

a.mid_order(a)
print(Solution.result_list)