class Solution:
    def buildMatrix(self, k: int, rowConditions: list[list[int]], colConditions: list[list[int]]) -> list[list[int]]:
        def topological_order(conditions):
            successors = defaultdict(list)
            in_degrees = [0] * (k + 1)
            for before, after in conditions:
                successors[before].append(after)
                in_degrees[after] += 1

            ready = deque()
            for number in range(1, k + 1):
                if in_degrees[number] == 0:
                    ready.append(number)
            
            order = list()
            while ready:
                current = ready.popleft()
                order.append(current)
                for successor in successors[current]:
                    in_degrees[successor] -= 1
                    if in_degrees[successor] == 0:
                        ready.append(successor)

            return order if len(order) == k else list()

        row_order = topological_order(rowConditions)
        col_order = topological_order(colConditions)
        if not row_order or not col_order:
            return list()
        
        col_of_number = [0] * (k + 1)
        for col_index, number in enumerate(col_order):
            col_of_number[number] = col_index

        matrix = [[0] * k for _ in range(k)]
        for row_index, number in enumerate(row_order):
            matrix[row_index][col_of_number[number]] = number
        return matrix
        