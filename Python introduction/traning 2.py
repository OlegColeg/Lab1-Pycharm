input_str = input("Enter a string: ")
try:
    number = input_str.split()
    print(number)
    int_numbers = []
    for number in number:
        int_numbers.append(int(number))
except ValueError:
    print("Invalid input")
    exit()
print(int_numbers)
