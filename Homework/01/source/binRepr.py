'''
Author: Tyler J Gabb
NedID : TylerJGabb@email.arizona.edu

HOMEWORK 1 FOR Math475A

Write a code to read real numbers from a text file
and write strings out with their binary representation


No signed bit is used, if a negative sign comes in, ignore it
and throw it back in front of the base 10 representation
'''
import sys
import os
import math
from fractions import Fraction as Frac

'''
Converts a base 10 integer to a binary integer
'''
def bin_int(int_str):
    int_str = int_str.replace("-","")
    res = ""
    N = int(int_str)
    while(N > 0):
        res = str(N%2) + res
        N//=2
    return res

'''
Converts a base 10 floating point number to a binary
floating point number.
least significant bit is on either side of the decimal
'''
def bin_float(float_str):
    split_ = float_str.replace("-","").split('.')
    integ_part = bin_int(split_[0])

    numer_str = split_[1]
    denom_str = "1" + "0"*len(numer_str)
    N = int(numer_str)
    D = int(denom_str)

    F = Frac(N,D) #Automatically reduces fraction

    N = F.numerator #Pull back out
    D = F.denominator #recuced numer and denomm

    float_part = ""
    while(len(float_part) <= 10):
        if N < D:
            ret = "0"
            N*=2
        elif N > D:
            ret = "1"
            N = N - D
        elif N==D:
            float_part += "1"
            break
        float_part += ret

    return integ_part + '.' + float_part

'''
Takes file of base 10 integers each on a seperate line
Prints out their base-2 interpretation to sdtout, one line at a time
'''
def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python binRepr.py FILE")
        return

    file_ = open(args[0])
    real_str = file_.readline().strip()
    was_neg = False
    is_float = False

    while real_str:
        was_neg = real_str.startswith("-")
        is_float = "." in real_str
        result = bin_float(real_str) if is_float else bin_int(real_str)
        final = "-" + result if was_neg else result
        sys.stdout.write(real_str + '\t' + final + '\n')
        real_str = file_.readline().strip()
    return 1  

main()
