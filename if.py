from astrologic import switcher
import time
from astrologic import no_recursion



@no_recursion
def wrecursion(counter):
    if counter != 900:
        return wrecursion(counter + 1)
    return counter


def recursion(counter):
    if counter != 900:
        return recursion(counter + 1)
    return counter



for k in range(1000):
    recursion(0)
