class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        nums_checker = set()

        for num in nums:
            if num in nums_checker:
                return True
            else:
                nums_checker.add(num)
        return False
         