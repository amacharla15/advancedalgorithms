// CSCI 650 - Fall 2024
// Dynamic Array Class Skeleton
// Author: Carter Tillquist
#include <stdexcept>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <functional>
#include <unordered_map>
#include <string>
#include <chrono>
#include <vector>

class DynamicArray{
    private:
        int size;                     // the total number of elements in the array
        int capacity;                 // the total number of buckets in the array
        std::function<int(int)> grow; // a function specifying how to change capacity when size > capacity
        int *arr;                     // the underlying array

    public:
        /********************************************************************************
         * Default constructor                                                          *
         * The initial capacity of the array is 4                                       *
         * The initial grow function returns 2 times its argument (it doubles capacity) *
         ********************************************************************************/
        DynamicArray(){
            size = 0;
            capacity = 4;
            grow = [](int c){ return 2*c; };
            arr = new int[capacity];
        }

        /* Deconstructor */
        ~DynamicArray(){
            delete[] arr;
        }

        /* Getters */
        int getSize(){ return size; }
        int getCapacity(){ return capacity; }
        std::function<int(int)> getGrow(){ return grow; }


        /* Setter for the grow function */
        void setGrow(std::function<int(int)> g){ grow = g; }

        /*********************************************************************
         * Inserts a value at a given location in the array.                 *
         * A runtime error is thrown if the given location is out of bounds. *
         * @param int loc - the index at which to insert the new value       *
         * @param int val - the value to insert                              *
         *********************************************************************/
        void insert(int loc, int val){
            if (loc < 0 || loc > size){ throw std::runtime_error("index out of bounds"); }
            int newCap = capacity; //starting from current capacity and compute the capacity we need to accomodate one more element
            // Applying the growth policy until there is room for (size + 1) elements
            // Assuming that grow(newCap) will eventually return a strictly larger value
            while (size + 1 > newCap){
                newCap = grow(newCap);
            }
            // If capacity must increase, we allocate a new buffer and copy existing elements
            if (newCap != capacity){
                // Allocating the larger buffer.
                int *newArr = new int[newCap];
                // Copying over the current contents [0 to size-1].
                for (int i = 0; i < size; i++){
                    newArr[i] = arr[i];
                }
                // Releasing old storage and installing the new buffer
                delete[] arr;
                arr = newArr;
                capacity = newCap;
            }
            // Shifting elements in [loc .. size-1] one position to the right
            // to open a hole at index 'loc'. Iterating right-to-left to avoid overwriting and
            // if loc == size (append), this loop body never executes
            for (int i = size - 1; i >= loc; --i){
                arr[i + 1] = arr[i];
            }
            arr[loc] = val;
            size++;
            // YOUR CODE HERE
        }

        /****************************************
         * Adds a value at the end of the array *
         * @param int val - the value to add    *
         ****************************************/
        void push(int val){
            // YOUR CODE HERE
            // Ensuring there is enough space to append one more element
            // Starting by assuming current capacity is sufficient
            int newCap = capacity;
            // If tehre is no enough space for (size + 1) elements,
            // we repeatedly apply the growth policy until it is done
            // Assuming grow(newCap) eventually produces a strictly larger value
            while (size + 1 > newCap){
                newCap = grow(newCap);
            }
            // If we have computed a larger capacity, we then perform the resize:
            // by allocating new storage, copying existing elements, and swapping buffers.
            if (newCap != capacity){
                int *newArr = new int[newCap];
                // Copying the current contents [0 to size-1].
                for (int i = 0; i < size; i++){
                    newArr[i] = arr[i];
                }
                // Releasing old storage and installing the new buffer/capacity
                delete[] arr;
                arr = newArr;
                capacity = newCap;
            }
            arr[size] = val;
            size++;
        }

        /***********************************************************************************************
         * Remove an element from a specific location in the array. All elements to the right of       *
         * this location shift left. A runtime error is thrown is the given location is out of bounds. *
         * @param int loc - the index from which to remove an element                                  *
         * @return int - the value of the element being removed                                        *
         ***********************************************************************************************/
        int remove(int loc){
            // Checking if valid indexes are 0 .. size-1 (must remove an existing element)
            if (loc < 0 || loc >= size){ throw std::runtime_error("index out of bounds"); }
            // YOUR CODE HERE
            // Saving the value at 'loc' so we can return it after shifting
            int removed = arr[loc];
            // Shift left from loc+1 to end
            for (int i = loc + 1; i < size; ++i){
                arr[i - 1] = arr[i];
            }
            size--;
            return removed;
        }

        /*******************************************************
         * Remove the last element of the array.               *
         * @return int - the value of the element being popped *
         *******************************************************/
        int pop(){
            // YOUR CODE HERE
            // to check that cannot remove from an empty array.
            if (size == 0){ throw std::runtime_error("pop from empty array"); }
            //reading the last element and then decrementing size
            int v = arr[size - 1];
            size--;
            return v; // returning the popped value
        }

        /*********************************************************************
         * Get the value in the array at a particular index.                 *
         * A runtime error is thrown if the given location is out of bounds. *
         * @param int loc - the index of the value to return                 *
         * @return int - the value of the element at the location            *
         *********************************************************************/
        int get(int loc){ 
            if (loc < 0 || loc >= size){ throw std::runtime_error("index out of bounds"); }
            return arr[loc];
        }

        /*********************************************************************
         * Set the value at a particular index in the array.                 *
         * A runtime error is thrown if the given location is out of bounds. *
         * @param int loc - the location to set                              *
         * @param int val - the value to add at the given location           *
         *********************************************************************/
        void set(int loc, int val){ 
            if (loc < 0 || loc >= size){ throw std::runtime_error("index out of bounds"); }
            arr[loc] = val;
        }

        /*********************************************
         * Print the elements of the array to stdout *
         *********************************************/
        void printArray(){
            for (int i = 0; i < size-1; i++){
                std::cout << arr[i] << " ";
            }
            if (size > 0){ std::cout << arr[size-1] << std::endl; }
        }
};

/*********************************************************************************************
 * Run timing experiments for dynamic arrays using different strategies to increase capacity *
 *********************************************************************************************/
void runExperiments(){
    srand(time(NULL));

    int repeats = 50;
    int numOps = 8200; //Depending on your machine, the number of operations may need to be increased or decreased
                       //The goal is to observe the beginnings of asymptotic behavior

    std::vector<std::function<int(int)>> growFuncs = {[](int c){ return 2*c; },
                                                      [](int c){ return c+1; },
                                                      [](int c){ return c+100; }};
    
    std::chrono::high_resolution_clock::time_point start;
    std::chrono::high_resolution_clock::time_point end;

    int count = 0;
    for (std::function<int(int)> func: growFuncs){ // for each way of increasing capacity
        std::cout << "Count " << count << std::endl;
        count++;
        for (int rep = 0; rep < repeats; rep++){ // run repeated experiments
            std::cout << "Repeat " << rep << std::endl;
            DynamicArray arr;
            arr.setGrow(func);
            for (int op = 0; op < numOps; op++){ // for each experiment, run some sequence of operations
                int val = rand() % 1000; // generate a random value if necessary
                start = std::chrono::high_resolution_clock::now();
                // perform and time some operation on the array
                // while you might change other parts of this function, this is a key location to add code 
                arr.push(val);
                end = std::chrono::high_resolution_clock::now();
                double elapsed = std::chrono::duration_cast<std::chrono::duration<double>>(end-start).count();
                std::cout << elapsed << " ";
            }
            std::cout << std::endl;
        }
    }
}

/**********************************************************
 * A simple main to interact with the Dynamic Array class *
 **********************************************************/
int main(){
    /* set to true to collect run time data and false to run a simple driver */
    if (false){
        runExperiments();
        return 0;
    }

    DynamicArray arr;
    int loc = 0;
    int val = -1;
    int count = 0;

    std::unordered_map<std::string, int> actionMap = {{"insert", 1}, {"push", 2}, {"remove", 3}, {"pop", 4},
                                                      {"get", 5}, {"set", 6}, {"size", 7}, {"capacity", 8},
                                                      {"setGrow", 9}, {"print", 10}};
    std::string action = "";
    std::cin >> action;
    while (action != "quit"){
        int act = actionMap[action];
        switch(act){
            case 1:
                std::cout << "INSERT" << std::endl;
                std::cin >> loc >> val;
                arr.insert(loc, val);
                break;
            case 2:
                std::cout << "PUSH" << std::endl;
                std::cin >> val;
                arr.push(val);
                break;
            case 3:
                std::cout << "REMOVE" << std::endl;
                std::cin >> loc;
                std::cout << arr.remove(loc) << std::endl;
                break;
            case 4:
                std::cout << "POP" << std::endl;
                std::cout << arr.pop() << std::endl;
                break;
            case 5:
                std::cout << "GET" << std::endl;
                std::cin >> loc;
                std::cout << arr.get(loc) << std::endl;
                break;
            case 6:
                std::cout << "SET" << std::endl;
                std::cin >> loc >> val;
                arr.set(loc, val);
                break;
            case 7:
                std::cout << "SIZE" << std::endl;
                std::cout << arr.getSize() << std::endl;
                break;
            case 8:
                std::cout << "CAPACITY" << std::endl;
                std::cout << arr.getCapacity() << std::endl;
                break;
            case 9:
                std::cout << "SETGROW" << std::endl;
                if (count % 2 == 0){ arr.setGrow([](int k){ return k+1; }); }
                else{ arr.setGrow([](int k){ return 2*k; }); }
                count++;
                break;
            case 10:
                std::cout << "PRINT" << std::endl;
                arr.printArray();
                break;
            default:
                std::cout << action << " is not a recognized action" << std::endl;
        }
        std::cin >> action;
    }
    return 0;
}
