import heapq

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
heapq.heapify(data)
print(data)

heapq.heappush(data, 7)
print(data)

smallest = heapq.heappop(data)
print(smallest)


largest_elements = heapq.nlargest(2, data)
print(largest_elements)

smallest_elements = heapq.nsmallest(2, data)
print(smallest_elements)

heap1 = [1, 3, 5]
heap2 = [2, 4, 6]
merged_heap = list(heapq.merge(heap1, heap2))
print(merged_heap)

# Why Use heapq:
# Efficiency: Heaps provide efficient access to the smallest (or largest) element, making them suitable for priority queue applications.
# Priority Queue: Heaps are often used to implement priority queues, where elements are processed based on their priority.
# Efficient Sorting: If you need to find the N smallest or largest elements in a collection, using a heap is more efficient than sorting the entire collection.
# Space Efficiency: Heaps use less memory compared to sorting the entire collection, making them useful for large datasets.
# Dijkstra's Algorithm: Heaps are crucial for implementing algorithms like Dijkstra's shortest path algorithm.

class Task:
    def __init__(self, description, priority):
        self.description = description
        self.priority = priority

    def __lt__(self, other):
        # Custom comparison method for tasks based on priority
        return self.priority < other.priority


# Priority queue to store tasks
task_queue = []

# Adding tasks to the queue
tasks = [
    Task("Write report", 2),
    Task("Debug code", 1),
    Task("Test new feature", 3),
    Task("Attend meeting", 2),
    Task("Review pull requests", 1),
]

# Adding tasks to the priority queue
for task in tasks:
    heapq.heappush(task_queue, task)

# Processing tasks in order of priority
while task_queue:
    next_task = heapq.heappop(task_queue)
    print(f"Processing: {next_task.description}, Priority: {next_task.priority}")
