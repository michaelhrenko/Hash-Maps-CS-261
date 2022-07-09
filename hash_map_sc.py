# Name:         Michael Hrenko
# OSU Email:    hrenkom@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment:   6 - HashMap Implementation - Chaining
# Due Date:     06/03/2022
# Description:  This program makes use of a hash map (which 
#   is built upon a dynamic array and a single linked list) chaining 
#   for collision resolution using a singly linked list. Performs 
#   these various actions:
#   add a key/value pair (aka put), remove a key/value pair, clear 
#   all key/value pairs, resize the hash map, return the value for a
#   key (aka get), return all the keys (aka get keys), determine if
#   a key exists in the hash map, calculate the number of empty 
#   buckets and the table load for the hash map, and determines the
#   mode.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def get_hash_value(self, key: str) -> int:
        
        """ 
        - Calls the _hash_function method to determine the location in the 
            hash table.       
        - If hash value exceeds the capacity of the array, the new value is 
            the current value modulus the capacity.
        - Uses the hash function passed as a parameter to HashMap.
        - Returns an integer for the index in the array. 
        """ 

        hashValue = self._hash_function(key)

        return hashValue % self.get_capacity() 

    def get_hash_object(self, key: str) -> object:
        """
        - Returns the linked list object associated with the key.                    
        """

        return self._buckets[self.get_hash_value(key)]

    def put(self, key: str, value: object) -> None:
        
        """ 
        - Adds a key/value pair to the location determined by the hash function.
        - Given a key, first calls the get_hash_object method to get 
            the node associated with the hash location. Then calls the contains 
            method from LinkedList to determine if a node exists in the linked list.
        - If the key already exists, the new value replaces the existing value.
        - Else the passed key/value pair is added at the front of the linked list by 
            calling the insert method from LinkedList (this also increases the size 
            of the linked list by 1).
        - Returns None
        """

        hashObject = self.get_hash_object(key)
        linkedlistNode = hashObject.contains(key)

        if linkedlistNode and linkedlistNode.key == key:
            linkedlistNode.value = value
            return

        hashObject.insert(key, value)

        # The linked list size is increased when we call the insert method from 
        #   LinkedList. This increases the size of the hash map.
        self._size += 1

    def empty_buckets(self) -> int:
        """
        - Returns the number of empty buckets in the hash table.
        - A bucket is an index in the dynamic array.
        - Since the hash table is an array of linked lists, a bucket is considered 
            "empty" when it's size (determined by calling the length method from the 
            LinkedList class) is 0.
        """

        emptyBuckets = 0

        for i in range(self.get_capacity()):
            if self._buckets[i].length() == 0:
                emptyBuckets += 1

        return emptyBuckets

    def table_load(self) -> float:
        """
        - Returns load factor for the hash table defined as size / capacity.
        """

        return self.get_size() / self.get_capacity()

    def clear(self) -> None:
        """
        - Clears the contents of the hash map by initializing a new dynamic array
            object, and a new linked list object for each bucket in the array.
        - Updates the size, but not the capacity. 
        """

        self._buckets = DynamicArray()

        for i in range(self.get_capacity()):
            self._buckets.append(LinkedList())  
        
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        - Changes the capacity and clears the current hash table, then 
            rehashes all existing key/value pairs before inserting them 
            into the new table. 
        - If new_capacity is less than 1, this method does nothing.

        Steps:
        (1) Make a copy of the prior hash table. 
        (2) Update the capacity. 
        (3) Call the clear method to clear the contents of the hash map.
        (4) Loop through each bucket in the prior table. If a linked list 
            exists in a bucket, loop through each key in the linked list,
            rehashing and adding it to the new table by calling the put method.

        - The inner linked list loop utilizes the __iter__() method from LinkedList 
            and LinkedListIterator class which does all the iteration work. 
        - Returns: None
        """

        if new_capacity < 1:
            return

        priorArray = self._buckets
        priorArrayLength = self.get_capacity()

        self._capacity = new_capacity
        self.clear()

        for i in range(priorArrayLength):
            if priorArray[i].length() > 0:
                for node in priorArray[i]:
                    self.put(node.key, node.value)

    def get(self, key: str) -> int:
        """
        - Given a key, first calls the get_hash_object to get 
            the node associated with the hash location. Then calls
            the contains method from LinkedList to get the node
            associated with the desired key and returns it.       
        """

        hashObject = self.get_hash_object(key)
        linkedlistNode = hashObject.contains(key)

        if linkedlistNode is None:
            return
        
        return linkedlistNode.value

    def contains_key(self, key: str) -> bool:
        """
        - Given a key, first calls the get_hash_object to get 
            the node associated with the hash location. Then calls
            the contains method from LinkedList to determine if a 
            node exists in the hash table. 
        - Returns True if the node exists, otherwise returns False.       
        """

        hashObject = self.get_hash_object(key)

        if hashObject.contains(key) is None:
            return False
        
        return True

    def remove(self, key: str) -> None:
        """
        - Given a key, calls the remove method from LinkedList to remove 
            the node associated with the key.
        - Does nothing if the key doesn't exist in the hash table.             
        - Returns None.        
        """

        if not self.contains_key(key):
            return

        hashObject = self.get_hash_object(key)
        hashObject.remove(key)

        # The linked list size is decreased when we call the remove method from 
        #   LinkedList. This decreases the size of the hash map.
        self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        - Returns a dynamic array object with all the keys stored in the 
            hash table.
        - Similar to the resize_table method, it loops through each bucket 
            in the table. If a linked list exists in a bucket, it loops through 
            each key in the linked list, adding it to the output array by 
            calling the append method in DynamicArray.
        - The inner linked list loop utilizes the __iter__() method from LinkedList 
            and LinkedListIterator class which does all the iteration work. 
        """

        newArray = DynamicArray()

        for i in range(self.get_capacity()):
            if self._buckets[i].length() > 0:
                for node in self._buckets[i]:
                    newArray.append(node.key)

        return newArray

    def put_mode(self, key: str, value=1) -> None:

        """ 
        - Identical to the put method, except that when the key already
            exists in the hash table, it increases its value by 1.
        - Returns None
        """

        hashObject = self.get_hash_object(key)
        linkedlistNode = hashObject.contains(key)

        if linkedlistNode and linkedlistNode.key == key:
            linkedlistNode.value += 1
            return

        hashObject.insert(key, value)

        # The linked list size is increased when we call the insert method from 
        #   LinkedList. This increases the size of the hash map.
        self._size += 1
        
def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    - Given a dynamic array, returns a dynamic array object with the 
        modes and the mode count in a tuple. 

    Steps:
    (1) Create a new hash map to store the keys/values.
    (2) Create a new dynamic array to store the modes and their count.
    (3) Call the put_mode method to put all the keys into the in the hash 
        map, where each key's value is the number of times the key occurs 
        in the array.
    (4) Get the unique list of keys. This is needed because the HashMap 
        needs keys for the methods we are using here. 
    (5) Initialize the mode count to 0. 
    (6) Pass each unique key in the list from step #4 to the get method which
        returns the total count the key occurs in the array. If this count
        if greater than the current mode count, update the mode count to this
        value.
    (7) Repeat step #6 except that we append the key to the new dynamic array
        when it's count equals the mode count.   

    - Time complexity O(n) 

    - Alternative approaches were sought, but this produced the most consistent
        linear time complexity when measured over samples of 100k + 200k +...+
        1M.
    """

    map = HashMap(da.length() // 3, hash_function_1)

    newArray = DynamicArray()

    for i in range(da.length()):
        map.put_mode(da[i])

    keysArray = map.get_keys()
    keysArrayLength = keysArray.length()

    modeCount = 0
    for i in range(keysArrayLength):
        currCount = map.get(keysArray[i])
        if currCount > modeCount:
            modeCount = currCount
    
    for j in range(keysArrayLength):
        currCount = map.get(keysArray[j])
        if currCount == modeCount:
            newArray.append(keysArray[j])  

    return (newArray, modeCount)

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
