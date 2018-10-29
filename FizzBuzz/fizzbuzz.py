# Project FizzBuzz

# Print Fizz for multiple of 3
# Print Buzz for multiple of 5
# Print FizzBuzz for multiple of both

for i in range(1,101):
    if i%3==0 and i%5==0:
        print("FizzBuzz")
    elif i%3==0:
        print("Fizz")
    elif i%5==0:
        print("Buzz")
    else:
        print(i)