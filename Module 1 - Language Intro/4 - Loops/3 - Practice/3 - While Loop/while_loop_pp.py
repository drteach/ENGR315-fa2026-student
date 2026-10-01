# this will test your ability to write a while loop
# use the print() statement to determine whether your number is correct

# an example while loop is given below
a = 1
while a != 5:
    a = a + 1  # pay attention where the counter (this part of the loop) is located
    print("not 5 yet, but we're at " + str(a))

# now, move the counter to after the print statement
# notice how the value of a has changed in the print value,
# but remains the same in the actual value of a

# first, we're going to write the condition of a while loop
# this loop is going to multiply the variable x by 2 3 times
b = 0
x = 3
while b < 3:
    b += 1
    x = x * 2
print("the value of x is " + str(x))

# now, try and write the body of a while loop that should add a variable to itself 5 times
# when writing the code delete "break" - this is to prevent an infinite loop
c = 2
y = 0
while y < 5:
    c = c + c
    y = y + 1
print("the value of c is " + str(c))

# it's time to combine both of these concepts.
# write a loop entirely from scratch that prints out a statement 6 times
# the counter variable you will use is z

z = 0
while z < 6:
    print("This is iteration " + str(z + 1))
    z = z + 1