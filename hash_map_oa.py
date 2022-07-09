# Name:         Michael Hrenko
# OSU Email:    hrenkom@oregonstate.edu
# Course:       CS261 - Data Structures
# Assignment:   6 - HashMap Implementation - Open Addressing
# Due Date:     06/03/2022
# Description:  This program makes use of a hash map (which 
#   is built upon a dynamic array) using open addressing with 
#   quadratic probing for collision resolution. It performs these 
#   various actions: add a key/value pair (aka put), remove a 
#   key/value pair, clear all key/value pairs, resize the hash map, 
#   return the value for a key (aka get), return all the keys (aka 
#   get keys), determine if a key exists in the hash map, and 
#   calculate the number of empty buckets, and the table load for 
#   the hash map. 


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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

    def get_hash_value(self, key: str, iter: int) -> int:
        
        """ 
        - Calls the _hash_function method to determine the location in the 
            hash table.
        - Applies the quadratic probing approach, using the parameter called
            iter.     
        - If hash value exceeds the capacity of the array, the new value is 
            the current value modulus the capacity.
        - The _hash_function method Uses the hash function passed as a parameter 
            to HashMap.
        - Returns an integer for the index in the array. 
        """     
        
        hashValue = self._hash_function(key)

        return (hashValue + iter ** 2) % self.get_capacity() 

    def put(self, key: str, value: object) -> None:

        """ 
        - Adds a key/value HashEntry object to the location determined by the hash 
            function.
        - Steps below...

        (1) If the load factor is at least 0.5, it calls resize_table to double the
            capacity and copy the prior the rehashed HashEntry objects into the 
            larger array (without the tombstones).
        (2) Calls HashEntry to get the new hash object.
        (3) Initializes the insert index by calling get_hash_value with the value 
            of 0 for the iter parameter. 
        (4) If the key already exists at the location, or the key is a tombstone,
            the new value replaces the existing value.
        (5) Else if the location already has a key, but it's not equal to the passed 
            key, it calls get_hash_value again, but with an iter parameter that's
            incremented by 1.
        (6) If no empty location can be found, and the number of times we run the loop 
            exceeds the capacity, indicating the loop is repeating, it returns None. 
        (7) If the location is empty, it adds the HashEntry object here and increases
            the size.
            

        - Returns None
        """

        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity() * 2)

        newHashObject = HashEntry(key, value)
        
        iter = 0
        index = self.get_hash_value(key, iter)
        currHashObject = self._buckets[index]

        loopCounter = 1

        while currHashObject: 
            if currHashObject.key == key or currHashObject.is_tombstone:
                
                # Only increase the size for this when it's a tombstone because
                #   we decreased the size when the key was removed earlier. 
                if currHashObject.is_tombstone:
                    self._size += 1

                self._buckets[index] = newHashObject
                return

            iter += 1
            index = self.get_hash_value(key, iter)
            currHashObject = self._buckets[index]

            loopCounter += 1
            if loopCounter > self.get_capacity():
                return

        self._buckets[index] = newHashObject
        self._size += 1

    def table_load(self) -> float:
        """
        - Returns load factor for the hash table defined as size / capacity.
        - The size does not include tombstones.        
        """

        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        - Returns the number of empty buckets in the hash table as defined
            by capacity minus size.
        - The size does not include tombstones.
        """
        return self.get_capacity() - self.get_size()

    def resize_table(self, new_capacity: int) -> None:
        """
        - Changes the capacity and clears the current hash table, then 
            rehashes all existing key/value pairs (not including tombstones)
            before inserting each HashEntry object into the new table. 
        - If new_capacity is less than 1, or new_capacity is less than the 
            size, this method does nothing.

        Steps:
        (1) Make a copy of the prior hash table.
        (2) Initialize the new capacity.  
        (3) Call the clear method to clear the contents of the hash map.
        (4) Loop through each bucket in the prior table, rehashing and adding 
            the HashEntry object to the new table (not including tombstones)
            by calling the put method.

        - Returns: None
        """
 
        if new_capacity < 1 or new_capacity < self.get_size():
            return

        priorArray = self._buckets
        priorArrayLength = self.get_capacity()

        self._capacity = new_capacity
        self.clear()

        for i in range(priorArrayLength):
            priorHashObject = priorArray[i]
            if priorHashObject and not priorHashObject.is_tombstone:
                self.put(priorHashObject.key, priorHashObject.value)
                
    def get(self, key: str) -> int:
        """
        - Given a key, returns the value associated with the key. 
        - Calls get_hash_value repeatedly to find the location of the key.
        - Since we may have needed to call get_hash_value several times when 
            seeking to insert the key (each time increasing the iter value)
            to find an open location, we do the same here until we find a 
            the key.
        - If the key is not in the hash map, as indicated by (1) the key 
            exists in the array, but it's a tombstone or (2) the number of
            times we run the loop equals the capacity, indicating the loop
            is repeating or every bucket was checked, and the key doesn't 
            exist in the array, it returns None.
        """

        iter = 0
        index = self.get_hash_value(key, iter)
        currHashObject = self._buckets[index]

        loopCounter = 1

        while currHashObject and loopCounter <= self.get_capacity():
            
            if currHashObject.key == key:
                if currHashObject.is_tombstone:
                    return
                return currHashObject.value

            iter += 1
            index = self.get_hash_value(key, iter)
            currHashObject = self._buckets[index]
            
            loopCounter += 1

    def contains_key(self, key: str) -> bool:
        
        """
        - Given a key, calls the get method to see if the key exists in
            the table, 
        - Returns True if the key exists, otherwise returns False.       
        """

        if self.get(key) is None:
            return False

        return True

    def remove(self, key: str) -> None:
        """
        - Given a key, it removes the key/value by setting it's 
            is_tombstone value to True and reducing the size by 1.
        - Calls get_hash_value repeatedly to find the location of the key.
        - Since we may have needed to call get_hash_value several times when 
            seeking to insert the key (each time increasing the iter value)
            to find an open location, we do the same here until we find a 
            the key.
        - If the key is not in the hash map, as indicated by (1) the key 
            exists in the array, but it's a tombstone or (2) the number of
            times we run the loop equals the capacity, indicating the loop
            is repeating or every bucket was checked, and the key doesn't 
            exist in the array, it returns None. 
        - Returns None. 
        """

        iter = 0
        index = self.get_hash_value(key, iter)
        currHashObject = self._buckets[index]

        loopCounter = 1

        while currHashObject and loopCounter <= self.get_capacity():

            if currHashObject.key == key:
                if not currHashObject.is_tombstone:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
                return
                  
            iter += 1
            index = self.get_hash_value(key, iter)
            currHashObject = self._buckets[index]

            loopCounter += 1

    def clear(self) -> None:
        """
        - Clears the contents of the hash map by initializing a new dynamic 
            array object. 
        - Doesn't change the capacity.
        - Returns: None
        """
    
        self._buckets = DynamicArray()

        for i in range(self.get_capacity()):
            self._buckets.append(None)

        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        - Returns a dynamic array object with all the keys stored in the 
            hash table that are not tombstones.
        """

        newArray = DynamicArray()

        for i in range(self.get_capacity()):         
            currHashObject = self._buckets[i]
            if currHashObject and not currHashObject.is_tombstone:
                newArray.append(currHashObject.key)

        return newArray


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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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