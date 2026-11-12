class Solution:
    def combinationSum4(self, nums: list[int], target: int) -> int:
        ways = [0] * (target + 1)
        ways[0] = 1
        for current_sum in range(1, target + 1):
            for number in nums:
                if number <= current_sum:
                    ways[current_sum] += ways[current_sum - number]
        return ways[target]