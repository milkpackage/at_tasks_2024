# V5.
# Array Reverse: Write a Java program that takes an array of integers and reverses its elements. Your program should prompt the user to enter the array size and the elements of the array, and then output the reversed array.
# Make HashMap from the result array and perform the following operations: a) Add a key-value pair to the map; b) Remove a key-value pair from the map; c) Check if a key is in the map; d) Find the value associated with a given key; e) Print all the keys and values in the map;
# Make up the situation for ArrayIndexOutOfBoundsException. Catch it and display the explanation for your custom case.


#func to reverse array
def reverse_array(arr):
    return arr[::-1]

def main():
    #reversing array
    size = int(input("Enter the size of the array: "))
    arr = []
    for i in range(size):
        element = int(input(f"Enter element {i + 1}: "))
        arr.append(element)
        
    print("original array:", arr)
    reversed_arr = reverse_array(arr)
    print("reversed array:", reversed_arr)

    #hashmap creation
    hash_map = {str(i): val for i, val in enumerate(reversed_arr)}
        
    #add a key-value pair
    hash_map['new_key'] = 100
    print("adding 'new_key': 100 to the map")
        
    #remove a key-value pair
    if hash_map:
        removed_key, removed_value = hash_map.popitem()
        print(f"removed key-value pair: {removed_key}: {removed_value}")
        
    #key check
    key_to_check = '0'
    print(f"is '{key_to_check}' in the map? {key_to_check in hash_map}")
        
    #finding the value
    key_to_find = '1'
    value = hash_map.get(key_to_find, "Key not found")
    print(f"value associated with '{key_to_find}': {value}")
        
    # keys and values
    print("all keys and values in the map:")
    for key, value in hash_map.items():
        print(f"   {key}: {value}")

    #ArrayIndexOutOfBoundsException
    try:
        index = len(reversed_arr)
        value = reversed_arr[index]

    except IndexError as e:
        print(f"ArrayIndexOutOfBoundsException: {e}")


if __name__ == "__main__":
    main()