import os
import secrets
import numpy

def create_secret() :
    # receive the number of bits in the 
    bits_in_secret = int(input("enter number of bits of the big secret (it must be a multiple of 4) to be generated : "))
    if(bits_in_secret % 4 != 0) :
        print("Error : the nuber of bits in the secret must be a multiple of 4\n")
        return
    print()

    # generate the big secret using the os.random
    big_secret = secrets.randbits(bits_in_secret)

    # print rhe big_secret
    print("your big secret (in hex) : " + hex(big_secret)[2:] + "\n")

    # get file name to save it to
    output_filename = input("enter filename to save the generated big secret : ")

    # write big secret to output file
    if(output_filename != "") :
        f = open(output_filename, "w")
        f.write(hex(big_secret)[2:])
        f.close()
        print()

    pass

def share_secret() :
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