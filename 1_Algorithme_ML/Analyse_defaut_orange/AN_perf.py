import time
import math
from datetime import datetime

def AN_pf(function):
        def inner1(*args, **kwargs):
                start =datetime.now()
                function(*args, **kwargs)
                processing_time =datetime.now()-start
                print(f'temps de traitement {function.__name__} :\n', processing_time)
        return inner1



'''import time
import math
 
# decorator to calculate duration
# taken by any function.
def calculate_time(func):
     
    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner1(*args, **kwargs):
 
        # storing time before function execution
        begin = time.time()
         
        func(*args, **kwargs)
 
        # storing time after function execution
        end = time.time()
        print("Total time taken in : ", func.__name__, end - begin)
 
    return inner1'''


'''import time
import math
from datetime import datetime

def AN_pf(function):
        start =datetime.now()
        function(*args, **kwargs)
        processing_time =datetime.now()-start
        print(f'temps de traitement {function} :\n', processing_time)'''


