class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        if len(nums) == 1:
            return True
        if min(nums) == 1:
            return False

        largest_value = max(nums)

        smallest_prime_factor = list(range(largest_value + 1))
        candidate = 2
        while candidate * candidate <= largest_value:
            if smallest_prime_factor[candidate] == candidate:
                for multiple in range(candidate * candidate, largest_value + 1, candidate):
                    if smallest_prime_factor[multiple] == multiple:
                        smallest_prime_factor[multiple] = candidate
            candidate += 1

        parent = list(range(largest_value + 1))
        rank = [0] * (largest_value + 1)

        def find(prime):
            while parent[prime] != prime:
                parent[prime] = parent[parent[prime]]
                prime = parent[prime]
            return prime

        def union(first_prime, second_prime):
            first_root = find(first_prime)
            second_root = find(second_prime)
            if first_root == second_root:
                return
            if rank[first_root] < rank[second_root]:
                first_root, second_root = second_root, first_root
            parent[second_root] = first_root
            if rank[first_root] == rank[second_root]:
                rank[first_root] += 1

        for value in nums:
            anchor_prime = smallest_prime_factor[value]
            remaining = value
            while remaining > 1:
                prime = smallest_prime_factor[remaining]
                union(anchor_prime, prime)
                while remaining % prime == 0:
                    remaining //= prime

        shared_root = find(smallest_prime_factor[nums[0]])
        for value in nums:
            if find(smallest_prime_factor[value]) != shared_root:
                return False
        return True