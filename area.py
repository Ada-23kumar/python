from typing import List
def maxArea(height: List[int]) -> int:
    max_area = 0
    left = 0
    right = 0
    right = len(height) -1
    while left < right:
        max_area = max(max_area, (right - left) * min(height[left], height[right]))

        if height[left] <= height[right]:
            left += 1
        else:
            right -= 1

    return max_area

print(maxArea([1,8,6,2,5,4,8,3,7]))