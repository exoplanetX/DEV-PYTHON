class TreeNode:
    def __init__(self, val):
        self.val=val
        self.left=None
        self.right=None

Input=[0]
tree=[0]
Input=Input+input().split()
cnt=1
for item in Input:
    tmp=TreeNode(item)
    tree.append(tmp)
for item in tree:
    if item.val=="null":
        continue
    if 2*cnt<=len(Input) and tree[2*cnt].val != "null":
        item.left=tree[2*cnt]
    if 2*cnt+1<=len(Input) and tree[2*cnt+1].val != "null":
        item.right=tree[2*cnt+1]
    cnt+=1