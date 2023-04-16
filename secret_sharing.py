import numpy

def create_secret() :
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
        print("0 -> creating a 4096 bit secret")
        print("1 -> share an already existing 4096 bit secret")
        print("2 -> reconstruct a 4096 bit secret from its portions")
        print("3 -> exit script")
        # take input option and jump to the task
        print()
        option = int(input("Enter integer option : "))
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