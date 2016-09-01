# pythonMonteCarloPi
# Calculate Pi in Python using the Monte Carlo Method
Recall from elementary geometry that the area of the unit circle (the circle of radius 1) is pi.  We calculate pi by using Ulam's Monte Carlo method to calculate the area of the unit circle.  For more information on the Monte Carlo method, the Wikipedia article, as of this date, is good:  https://en.wikipedia.org/wiki/Monte_Carlo_method . 

Our algorithm uses the Python standard library random number generator, random.  Python random uses a Mersenne Twister algorithm to generate pseudorandom numbers.  The Mersenne Twister is a good algorithm for our purposes.

I wrote the smaller program, pi.py, for a friend who is learning to program in Python and who won a contest for memorizing pi to sixty digits.  

I wrote the longer program to show what a "more professional" program might look like, with documentation and parallel calculations.  In reality, which sort of program an actual professional programmer might produce would depend upon context:  A programmer producing a library to be used and maintained by other programmers, perhaps for many years, would be more likely to add documentation and additional features (such as parallelization).  For a programmer piecing together data analysis for a report, creating code that is likely to be run only by people the programmer knows (or, more likely, only by the programmer), additional documentation would probably be overkill, and the parallelization might very well be overkill too.     
## pi.py
### usage
```
python pi.py [optional argument]
```
The optional argument must be an integer or things will eventually fail.  The optional argument is the number of iterations to run for the Monte Carlo method.  If you do not specify the number of iterations, the system will use `1000000`.

## pi_parallel.py
The number of iterations run is user-adjustable.  The more iterations 
run, the more accurate the result will be.

The number of processes to be used is also user adjustable.  Using more
or fewer processes will not affect the result, but will change 
performance characteristics.
### usage
```
python pi_parallel.py [optional arguments]
```
The first argument is the number of iterations to run -- make it a positive integer.  If no first argument is given a default of `1000000` is used.

The second argument is the number of CPU cores to use, which should be a positive integer.  If no argument is given, then the value returned by `max(1, multiprocessing.cpu_count() - 1)` is used (that is, one less than the number of cores seen by the python interpreter is used).
