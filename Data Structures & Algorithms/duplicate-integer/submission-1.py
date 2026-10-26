class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
         uniqueValues = set()
         
         for num in nums:
            if num in uniqueValues:
                return True
            uniqueValues.add(num)
         return False