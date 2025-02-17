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
    if not number:
        print("Lista este goala")
    else:
        number.sort()
        print("Lista ordonata crescator: ", number)
        print("Elementul minim: ", number[0])
        print("Elementul minim: ", min(number))
        print("Elementul minim: ", number[-1])
        print("Elementul minim: ", max(number))
        print("Elementul minim: ", sum(number))
        print("Media Aritmetica: ",
              sum(number) / len(number)
        print("Total elemente: ", len(number))