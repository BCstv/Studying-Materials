# Variables Are Not Boxes

# Python variables are like reference variables, labels with names attached to objects.
a = [1, 2, 3]
b = a
a.append(4)
print(b)

# Therefore, the b = a statement does not copy the contents of box a into box b. It attaches the label b to the object
# that already has the label a
