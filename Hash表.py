class HashTable:
    def __init__(self, size):
        '''创建一个自定义大小的空表'''
        self.size = size
        self.slots = [None] * self.size
        self.data = [None] * self.size

    def put(self, key, data):
        '''设置键值对'''
        # 键item.key，值hashvalue，item.data可替换
        hashvalue = self.hashfunction(key, self.size)
        if self.slots[hashvalue] == None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = data
        else:
            if self.slots[hashvalue] == key:
                # 替换item.data
                self.data[hashvalue] = data
            else:
                # 寻找空槽或相同key值槽
                nextslot = self.rehash(hashvalue, self.size)
                while self.slots[nextslot] != None and \
                        self.slots[nextslot] != key:
                    nextslot = self.rehash(nextslot, self.size)
                if self.slots[nextslot] == None:
                    # 找到空槽直接占据
                    self.slots[nextslot] = key
                    self.data[nextslot] = data
                else:
                    # 找到同key槽，替换item.data
                    self.data[nextslot] = data  # replace

    def hashfunction(self, key, size):
        '''散列函数——求余法'''
        return key % size

    def rehash(self, oldhash, size):
        '''重散列函数——步长1的线性探索'''
        return (oldhash + 1) % size

    def get(self, key, position):
        '''递归实现Hash查找'''
        if self.slots[position] == key:
            return self.data[position]
        if self.slots[position] == None:
            return None
        position = self.rehash(position, self.size)
        return self.get(key, position)

    def __getitem__(self, key):
        '''重载索引'''
        start = self.hashfunction(key, self.size)
        return self.get(key, start)

    def __setitem__(self, key, data):
        '''重载下标赋值'''
        self.put(key, data)

if __name__ == '__main__':
    H = HashTable(11)
    H[54] = "cat"
    H[26] = "dog"
    H[93] = "lion"
    H[17] = "tiger"
    H[77] = "bird"
    H[31] = "cow"
    H[44] = "goat"
    H[55] = "pig"
    H[20] = "chicken"
    print(H.slots)
    print(H.data)
    print(H[20],H[17])
    H[20] = 'duck'
    print(H[20],H[99])