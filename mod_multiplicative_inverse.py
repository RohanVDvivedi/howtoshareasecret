'''
    This code file is taken from https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
    And then it is modified to be used with this project.
'''

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return (0, False)
    else:
        return (x % m, True)