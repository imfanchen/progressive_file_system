# Requirements

Your task is to implement a simple container of integer numbers. Plan your design according to the level specifications below:

Level 1: Container should support adding and removing numbers.  
Level 2: Container should support getting the median of the numbers stored in it.  
To move to the next level, you need to pass all the tests at this level when submitting the solution.

### Level 1  
Container should support adding and removing numbers.

`add(self, number: int) -> int` — Should add the specified integer `value` to the container and return the number of integers in the container after the addition.

`delete(self, number: int) -> bool` — should attempt to remove the specified integer `value` from the container. If the `value` is present in the container, remove it and return `True`, otherwise, return `False`.

### Level 2  
Container should support calculating the median of the numbers stored in it.

`get_median(self) -> int | None` — should return the median integer: the integer in the middle of the sequence after all integers stored in the container are sorted in ascending order. If the length of the sequence is even, the leftmost integer from the two middle integers should be returned. If the container is empty, this method should return `None`.

#### Examples

| Query           | Explanation                                                         |
|-----------------|---------------------------------------------------------------------|
| get_median()    | returns None; container state: []                                   |
| add(5)          | returns 1; container state: [5]                                     |
| add(10)         | returns 2; container state: [5, 10]                                 |
| add(1)          | returns 3; container state: [5, 10, 1]                              |
| get_median()    | returns 5; sorted sequence of container numbers is: [1, 5, 10]      |
| add(4)          | returns 4; container state: [5, 10, 1, 4]                           |
| get_median()    | returns 4; sorted sequence of container numbers is: [1, 4, 5, 10]   |
| delete(1)       | returns True; container state: [5, 10, 4]                           |
| get_median()    | returns 5; sorted sequence of container numbers is: [4, 5, 10]      |
