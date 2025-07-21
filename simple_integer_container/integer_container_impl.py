from integer_container import IntegerContainer


class IntegerContainerImpl(IntegerContainer):

    def __init__(self):
        self.container = []

    def add(self, value: int) -> int:
        self.container.append(value)
        return len(self.container)

    def delete(self, value: int) -> bool:
        if value in self.container:
            self.container.remove(value)
            return True
        else:
            return False

    def get_median(self) -> int | None:
        length = len(self.container)
        if length == 0:
            return None
        sorted_container = sorted(self.container)
        center = length // 2
        if length % 2 == 1:
            return sorted_container[center]
        else:
            return sorted_container[center - 1]