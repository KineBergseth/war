# Create a new empty queue
class Queue:
    def __init__(self, owner):
        self.owner = owner
        self.items = []

    # Return a boolean value indicating whether or not the queue is empty
    def is_empty(self):
        return self.items == []

    # Adds the given item to the back of the queue
    def enqueue(self, item):
        self.items.insert(0, item)

    # Removes and returns the front item of the queue
    def dequeue(self):
        return self.items.pop()

    # Returns the number of items in the queue
    def size(self):
        return len(self.items)