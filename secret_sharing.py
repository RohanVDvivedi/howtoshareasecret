import os
import secrets
import struct
import numpy
import matrix_ops

def create_secret() :
    # receive the number of bits for the big secret
    bits_in_secret = int(input("enter number of bits of the big secret to be generated : "))
    print()

    # generate the big secret using the cryptographically secured random number generator
    big_secret = secrets.randbits(bits_in_secret)

    # print the big_secret
    print("your big secret (in hex) : " + hex(big_secret))
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

def read_hex_from_file(filename) :
    f = open(filename, "r")
    val = 0
    for c in f.read() :
        val = (val << 4)
        if(ord('0') <= ord(c) and ord(c) <= ord('9')) :
            val = (val | (ord(c)-ord('0')))
        elif(ord('a') <= ord(c) and ord(c) <= ord('f')) :
            val = (val | (ord(c)-ord('a')+10))
        elif(ord('A') <= ord(c) and ord(c) <= ord('F')) :
            val = (val | (ord(c)-ord('A')+10))
        else :
            print("Error: input file does not have a hex number")
            print()
            return (-1, False)
    f.close()
    return (val, True)

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
    big_secret = read_hex_from_file(big_secret_filename)
    if(big_secret[1] == False) :
        return
    big_secret = big_secret[0]

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

    print("next largest prime p = " + hex(p))
    print()

    # store coeffcients of polynomial in the increasing order of their order in the polynomial
    # i.e. coeff[0] * x^0 + coeff[1] * x^1 + coeff[2] * x^2 + coeff[3] * x^3 + ...
    coeff_of_polynomial = []
    coeff_of_polynomial.append(big_secret)
    for i in range(0, k-1) :
        coeff_of_polynomial.append(int(numpy.random.uniform() * p))
    
    # print the coeffcients
    print("printing polynomial that we selected : ")
    for i in range(0, len(coeff_of_polynomial)) :
        print(("  " if (i == 0) else "+ ") + "x ^ " + str(i) + " * " + str(hex(coeff_of_polynomial[i])))
    print()

    print("generating shared keys for the n individuals")
    print()

    # generating key for the n members
    shared_keys = {}
    for i in range(1, n+1) :
        key = 0
        for j in range(0, len(coeff_of_polynomial)) :
            key += ((i ** j) * coeff_of_polynomial[j])
        # key = key % p
        shared_keys[i] = key
    
    # printing shared keys
    print("printing shared keys :")
    print()
    for i,k in shared_keys.items() :
        print(str(i) + " : " + hex(k))
        print()
    
    print("saving shared keys with name as `"+ big_secret_filename +"_shared_<index>`")
    for i,k in shared_keys.items() :
        f = open(big_secret_filename + "_shared_" + str(i), "w")
        f.write(hex(k)[2:])
        f.close()

def solve_to_get_polynomial_coeffcients(shared_keys) :
    a = []
    b = []
    for i, k in shared_keys.items() :
        x = []
        for j in range(0, len(shared_keys)) :
            x.append(i ** j)
        a.append(x)
        b.append([k])

    a_inv = matrix_ops.getMatrixInverse(a, integral_inverse = False)
    if(a_inv[1] == False) :
        print("Error: couldn't find inverse of a desired matrix")
        print()
        return ([0], False)
    a_inv = a_inv[0]

    x = matrix_ops.getMatrixMultiplication(a_inv, b)

    x = matrix_ops.transposeMatrix(x)[0]

    return (x, True)

def reconstruct_secret() :
    # same as threshold k in the paper
    k = int(input("enter k - the number of individuals that must be present : "))
    print()

    shared_keys = {}
    for i in range(0, k) :
        rw = input("enter index and shared_key file name (space separated) : ")
        print()
        rw = rw.split(" ")
        index = int(rw[0])
        key = read_hex_from_file(rw[1])
        if(key[1] == False) :
            return
        key = key[0]
        if index in shared_keys :
            print("Error: invalid keys")
            return
        shared_keys[index] = key

    # printing shared keys
    print("printing shared keys read :")
    print()
    for i,k in shared_keys.items() :
        print(str(i) + " : " + hex(k))
        print()

    print("attempting to solve and get coeffcients of the polynomial")
    coeff_of_polynomial = solve_to_get_polynomial_coeffcients(shared_keys)
    if(coeff_of_polynomial[1] == False) :
        print("Error: as described above")
        print()
        return
    coeff_of_polynomial = coeff_of_polynomial[0]

    # print the coeffcients
    print("printing polynomial that we got : ")
    for i in range(0, len(coeff_of_polynomial)) :
        print(("  " if (i == 0) else "+ ") + "x ^ " + str(i) + " * " + str(hex(coeff_of_polynomial[i])))
    print()

    # print the big secret key
    big_secret = coeff_of_polynomial[0]
    if(big_secret < 0) :
        print("Error: we computed your big secret as a negativ value")
        print()
        return
    print("your big secret is : " + hex(big_secret))
    print()

    # get file name to save it to
    output_filename = input("enter filename to save the revealed big secret : ")
    print()

    if(output_filename != "") :
        # write big secret to output file
        f = open(output_filename, "w")
        f.write(hex(big_secret)[2:])
        f.close()
    else :
        print("filename empty - hence nothing saved")
        print()

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