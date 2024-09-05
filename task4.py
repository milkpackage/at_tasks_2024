# a)Use a CountDownLatch to wait for a set of threads to complete before continuing execution in the main thread.
# b)Create your own custom class extended from another class, and make an object for it. 
# Use getSuperclass() to print out the name of the superclass of the class.
# Use getInterfaces() to print out the names of all the interfaces implemented by the class.
# c)Create a generic method that takes two parameters of any type, and returns the larger one using T extends Comparable<T> and compareTo().

import threading
import time
from typing import TypeVar, Callable

#CountDownLatch 
class CountDownLatch:
    def __init__(self, count: int):
        self.count = count
        self.condition = threading.Condition()

    def count_down(self):
        with self.condition:
            self.count -= 1
            if self.count == 0:
                self.condition.notify_all()

    def wait(self):
        with self.condition:
            while self.count > 0:
                self.condition.wait()

#function to simulate work in threads
def worker(latch: CountDownLatch):
    time.sleep(1)
    print(f"Thread {threading.current_thread().name} finished")
    latch.count_down()


class Transport:
    pass

#custom class extended from another class
class Car(Transport):
    pass

#getting superclass
def get_superclass(cls: type) -> str:
    return cls.__base__.__name__

#python doesn't have interfaces so i'm returning class
def get_interfaces(cls: type) -> list:
    return [base.__name__ for base in cls.__bases__ if base is not object]

#generic method
T = TypeVar('T')
def get_larger(a: T, b: T, key: Callable[[T], any] = lambda x: x) -> T:
    return a if key(a) > key(b) else b

if __name__ == "__main__":
    # a) Using CountDownLatch
    num_threads = 3
    latch = CountDownLatch(num_threads)
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(latch,))
        thread.start()
        threads.append(thread)

    print("Main thread waiting for all workers to finish...")
    latch.wait()
    print("All workers have finished!")

    #custom class and reflection-like operations
    car = Car()
    print(f"\nSuperclass of Car: {get_superclass(Car)}")
    print(f"Interfaces implemented by Car: {get_interfaces(Car)}")

    #testing generic method on integers

    a,b = 8,2 

    result = get_larger(a, b)
    print(f"\nLarger of {a} and {b} is: {result}")

    #testing generic method on strings
    
    str_data_a,str_data_b = "it", "step"

    result_str = get_larger(str_data_a, str_data_b)
    print(f"larger of {str_data_a} and {str_data_b} is: {result_str}")