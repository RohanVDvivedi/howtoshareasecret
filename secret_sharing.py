import os
import secrets
import struct
import numpy

def create_secret() :
    # receive the number of bits for the big secret
    bits_in_secret = int(input("enter number of bits of the big secret to be generated : "))
    print()

    # generate the big secret using the cryptographically secured random number generator
    big_secret = secrets.randbits(bits_in_secret)

    # print the big_secret
    print("your big secret (in hex) : " + hex(big_secret)[2:])
    print()

    # get file name to save it to
    output_filename = input("enter filename to save the generated big secret : ")
    print()

    if(output_filename == "") :
        print("Error: file name must not be empty")
        print()
        return

    # write big secret to output file
    f = open(output_filename, "w")
    f.write(hex(big_secret)[2:])
    f.close()

    pass

def is_prime(x):
    for j in range(2,int(x**0.5)+1):
        if (x%j==0):
            return False
    return True

def next_prime(x):
    while(True) :
        x = x + 1
        if(is_prime(x)) :
            return x

def share_secret() :
    # receive the number of bits for the big secret
    bits_in_secret = int(input("enter number of bits of the big secret to be shared : "))
    print()

    # get the big secret file name
    big_secret_filename = input("enter filename to get the big secret : ")
    print()

    if(big_secret_filename == '') :
        print("Error: file name must not be empty")
        print()
        return

    # read the big secret from the file
    f = open(big_secret_filename, "r")
    big_secret = 0
    for c in f.read() :
        big_secret = (big_secret << 4)
        if(ord('0') <= ord(c) and ord(c) <= ord('9')) :
            big_secret = (big_secret | (ord(c)-ord('0')))
        elif(ord('a') <= ord(c) and ord(c) <= ord('f')) :
            big_secret = (big_secret | (ord(c)-ord('a')+10))
        elif(ord('A') <= ord(c) and ord(c) <= ord('F')) :
            big_secret = (big_secret | (ord(c)-ord('A')+10))
        else :
            print("Error: input file not a hex number")
            print()
            return
    f.close()

    print("big secret read : " + hex(big_secret))
    print()

    # same as n in the paper
    n = int(input("enter n - the number of individuals to be shared with : "))
    print()

    # same as threshold k in the paper
    k = int(input("enter k - the number of individuals that must be present : "))
    print()

    print("finding prime number bigger than both n and big secret")
    print()

    p = next_prime(max(n, big_secret))

    print("next largest prime p = " + hex(p)[2:])
    print()

    # store coeffcients of polynomial in the increasing order of their order in the polynomial
    # i.e. coeff[0] * x^0 + coeff[1] * x^1 + coeff[2] * x^2 + coeff[3] * x^3 + ...
    coeff_of_polynomial = []
    coeff_of_polynomial.append(big_secret)
    for i in range(0, k-1) :
        coeff_of_polynomial.append(int(numpy.random.uniform() * p))
    
    print("printing polynomial that we selected : ")
    for i in range(0, len(coeff_of_polynomial)) :
        print(("  " if (i == 0) else "+ ") + "x ^ " + str(i) + " * " + str(hex(coeff_of_polynomial[i])))
    print()

    pass

def reconstruct_secret() :
    pass

def main():
    exit_called = False
    while not exit_called :
        # print intro and options
        print("Please select one of the following tasks that this script is meant to perform :")
        print("0 -> create a big secret number")
        print("1 -> share an already existing big secret to n individuals")
        print("2 -> reconstruct the big secret from any of its k ( <= n ) individual parts")
        print("3 -> exit script")
        # take input option and jump to the task
        print()
        option = int(input("enter integer option : "))
        print()

        if(option == 0) :
            create_secret()
        elif(option == 1) :
            share_secret()
        elif(option == 2) :
            reconstruct_secret()
        elif(option == 3) :
            exit_called = True
        else :
            print("Error: option you select must be in the list")

        print("\n")

if __name__ == "__main__" :
    main()