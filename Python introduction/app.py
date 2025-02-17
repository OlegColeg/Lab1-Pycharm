number=[]
while True:
    try:
        n = int(input("Enter a number: "))
        if n == 0:
            print("Nr 0 a fost introdus")
            break
        number.append(n)
    except ValueError:
        print("Introduceti un nr intreg")
        break
    print(number)
//primul code