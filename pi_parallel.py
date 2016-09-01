from random import uniform as uniform
import sys
import multiprocessing as mp
import timeit


"""
Recall from elementary geometry that the area of the unit circle (the
circle of radius 1) is pi.  We calculate pi by using Ulam's Monte Carlo 
method to calculate the area of the unit circle.  For more information on 
the Monte Carlo method, the Wikipedia article, as of this date, is good: 
https://en.wikipedia.org/wiki/Monte_Carlo_method . 

Our algorithm uses the Python standard library random number 
generator, random.  Python random uses a Mersenne Twister algorithm 
to generate pseudorandom numbers.  The Mersenne Twister is a good 
algorithm for our purposes.

The number of iterations run is user-adjustable.  The more iterations 
run, the more accurate the result will be.

The number of processes to be used is also user adjustable.  Using more
or fewer processes will not affect the result, but will change 
performance characteristics.
"""


def count_is_in_cirle(iteration_count):
    """
    We count the number of random points from the unit square, running 
    from -1 to 1 (inclusive, horizontally and vertically), that also fall 
    in the unit circle.  That value is returned.

    iteration_count is the number of iterations that are run.
    
    Our algorithm uses the Python standard library random number 
    generator, random.  See the module docs.
    """
    # We are using the map-reduce pattern here.  Per usual Python style, 
    # we use a generator (lazy list comprehension) instead of map(), and 
    # sum() instead of a reduce() on addition.  Thus, we create a 
    # generator with the result (1 or 0) for each iteration, then sum up 
    # the results contained in the generator.
    #
    # Our algorithm:  For each of a given number of iterations, determine 
    # if a random point in the [-1, 1] square is in the unit circle or 
    # not.  If it is in the circle, it contributes 1 to a sum, the total 
    # number of randompoints in the unit circle.  
    def one_if_in_circle(x, y):
        """
        Given a coordinate, x, y, we return 1 if the coordinate is in the
        unit circle; otherwise, we return 0.  Points on the circle are 
        considered in the circle.
        """
        return 1 if (x*x + y*y) <= 1 else 0

    return (sum( 
        (one_if_in_circle(uniform(-1.0, 1.0), uniform(-1.0, 1.0)) 
            for i in range(iteration_count)) ))


def calc_pi(iteration_count, cores_usage):
    """
    We calculate pi using Ulam's Monte Carlo method.  See the module 
    documentation.  The calculated value of pi is returned.

    We use a process pool to offer the option of spreading the 
    calculation across more then one core.

    iteration_count is the number of iterations that are run.
    cores_usage is the number of processes to use.
    """
    # We're using a multiprocessing pool here, to take advantage of 
    # multi-core CPUs.

    # Calculate stuff for the pool.
    pool_size = cores_usage
    iterations_per_process = iteration_count // pool_size
    work_list = [iterations_per_process] * pool_size
    work_list[0] += iteration_count % pool_size

    # Set up the pool.
    calc_pool = mp.Pool(pool_size)

    # Use the pool to obtain random points in the unit circle.
    # We'll let the system determine the chunk size.
    in_circle_total = sum(calc_pool.map(
            count_is_in_cirle, 
            work_list))
    
    # Finish the calculation.  in_circle_total, divided by the total 
    # number of iterations, is the area of the unit circle 
    # relative to the [-1, 1] square.  Multiply by 4, which is the area 
    # of the [-1, 1] square, to get the area of the unit circle.
    # .NOTE. If you modify this program to run in Python 2.7, remember
    # to modify this calculation to use floating point division (or 
    # import division from future).
    return 4 * in_circle_total / iteration_count
   

def calc_pi_and_time_it_too(count, cores_usage):
    """
    This is like calling calc_pi, but it also returns the elapsed time 
    in a tuple:
    (calculated value of pi, elapsed time).

    iteration_count is the number of iterations that are run.
    cores_usage is the number of processes to use.
    """
    # Q. Why is this so complicated?
    # A. The way Python handles time is inconsistent.  Rather than fixing
    # that problem, the powers that be in the Python world created
    # a new standard library class, Timeit, to workaround the problem
    # that they should have fixed.  However, Timeit is poorly designed,
    # so we have to jump through some hoops to get it to do what we
    # want it to do which is time a function call that returns a result
    # without also timing I/O.
    
    result = 0
    def wrapper():
        nonlocal result
        result = calc_pi(count, cores_usage)  
    etim = timeit.timeit(wrapper, number=1)
    return (result, etim)


if __name__ == "__main__":
    """
    The first argument is the number of iterations to run -- make it a 
    positive integer.  If no first argument is given a default of 1000000 
    is used.

    The second argument is the number of CPU cores to use, which should
    be a positive integer.  If no argument is given, then the value 
    returned by max(1, multiprocessing.cpu_count() - 1) is used.
    """
    count = int(sys.argv[1]) if (sys.argv and 2 <= len(sys.argv)) else 1000000
    cores_usage = (int(sys.argv[2]) if (sys.argv and 3 <= len(sys.argv)) 
        else max(1, mp.cpu_count() - 1))
    
    (result, etim) = calc_pi_and_time_it_too(count, cores_usage)
    print("PI ({}): {}".format(count, result))  
    print("     elapsed ({}): {}".format(cores_usage, etim));
    