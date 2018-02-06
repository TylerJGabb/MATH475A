script.py has the code which generates the polynomials for the given data duck.dat
it is invoked on the command line via:

    python3 script.py n

    where n is a number greater than 0 which is the degree
    of the fitted polynomial

script.m has the code which generates the same polynomials, but is in Matlab

cubicSpline.py is a program which generates a cubic spline between data points
provided in a .dat or .csv file.
It is invoked on the command line via

    python3 cubicSpline.py FILE

    where FILE is a file with 2 columns, corresponding to x and y values of a dataset
