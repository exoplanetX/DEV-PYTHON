# https://blog.csdn.net/qx3501332/article/details/105546208
# 原始对偶算法
class SetCoverPD(object):
    """ 基于Primal-Dual的近似算法求解Set Cover问题.
    """

    def __init__(self, m, sets, costs):
        """
        注意: 输出参数的数值必须是整数.
        :param m: 元素个数. 元素的编号从0开始, e.g. 0, 1, ..., m-1
        :param sets: 元素(下标)的集合, list of sets, e.g. [{0, 2}, {1, 2, 3, 6}, {3, 4, 5}, {2, 4, 6}]
        :param costs: 每个元素集合的cost, e.g. [2, 3, 4, 1]
        """
        self._m = m
        self._sets = sets
        self._costs = costs
        self._result = []  # 计算结果: 保存结果集合在sets中的编号
        self._y = [0] * self._m  # 对偶决策变量

    def solve(self):
        """
        Primal-Dual算法.
        """
        uncovered_elements = set(range(self._m))
        ub = max(self._costs)
        while uncovered_elements:
            # 如果存在未被覆盖的元素i, 通过二分查找y[i]的值使得它满足条件:
            # y(S)=c(S), for some S 包含元素i. (称S为tight set.)
            i = uncovered_elements.pop()
            tight_sets = self._binary_search(i, 0, ub)
            # 把关于i的所有tight sets添加到结果集
            for ts in tight_sets:
                uncovered_elements -= self._sets[ts]
                self._result.append(ts)

    def _is_some_set_satisfied(self, i):
        """ 给定i(已知y[i]), 判断是否存在集合S满足y(S)>=c(S),
        其中y(S)代表S中元素对应y值之和, c(S)代表集合S的cost.
        """
        for j in range(len(self._sets)):
            set_j = self._sets[j]
            if i not in set_j:
                continue
            sum_y = sum([self._y[k] for k in set_j])
            if sum_y >= self._costs[j]:
                return True
        return False

    def _binary_search(self, i, lb, ub):
        """
        用二分法查找y[i]使得y(S) = c(S) for some S (S称为tight set)
        :param i: 元素的下标
        :param lb: y_i的下界
        :param ub: y_i的上界
        :return: list of tight sets
        """
        if ub - lb <= 1:
            self._y[i] = ub
            return self._get_tight_sets(i)
        mid = (lb + ub) // 2
        self._y[i] = mid
        if not self._is_some_set_satisfied(i):
            return self._binary_search(i, mid, ub)
        else:
            return self._binary_search(i, lb, mid)

    def _get_tight_sets(self, i):
        """
        已知y[i], 找到所有tight sets(满足y(S)=c(S)).
        """
        tight_sets = []
        for j in range(len(self._sets)):
            set_j = self._sets[j]
            if i not in set_j:
                continue
            sum_y = sum([self._y[k] for k in set_j])
            if abs(sum_y - self._costs[j]) < 1e-6:
                tight_sets.append(j)

        return tight_sets

    def print_result(self):
        print("solution:", [self._sets[i] for i in self._result])
        print("total cost:", sum([self._costs[i] for i in self._result]))


if __name__ == '__main__':
    sc = SetCoverPD(9,  # m
                    [{0, 1}, {2, 5, 8}, {3, 5}, {4, 6}, {1, 2, 3, 4}, {6, 7, 8}],  # sets
                    [4, 2, 5, 7, 8, 1]  # costs
                    )
    sc.solve()
    sc.print_result()
