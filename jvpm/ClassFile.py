class ConstantInfo():
    def __init__(self):
        self.tag = 0
        self.info = []
        self.name_index = 0

class methodInfo():
    def __init__(self):
        self.value = 0

class ClassFile():
    def __init__(self):
        with open('Add.class', 'rb') as binary_file:
            self.data = binary_file.read()
        self.c_pool_table = []
        self.cpoolsize = 0
        self.interface_table = []
        self.method_table= []

    def get_magic(self):
        magic = ""
        for i in range(4):
            magic += format(self.data[i], '02X')
        return magic

    def get_minor(self):
        return self.data[4] + self.data[5]

    def get_major(self):
        return self.data[6] + self.data[7]

    def get_constant_pool_count(self):
        return self.data[8] + self.data[9]

    def create_c_pool(self):
        index_offset = 10
        switch = {
            3: 4,
            4: 4,
            5: 8,
            6: 8,
            7: 2,
            8: 2,
            9: 4,
            10: 4,
            11: 4,
            12: 4,
            15: 3,
            16: 2,
            18: 4
        }
        max = int(self.get_constant_pool_count()) - 1
        for i in range (0,max):
            thing = ConstantInfo()
            thing.tag = self.data[index_offset]
            index_offset += 1
            if thing.tag == 1:
                bytesNeeded = self.data[index_offset] + self.data[index_offset + 1]
                index_offset += 2
            else:
                bytesNeeded = switch.get(thing.tag)
            for x in range (0,bytesNeeded):
                thing.info.append(self.data[x + index_offset])
                index_offset += 1
            print("Constant #", i, " tag: ", thing.tag, " value: ", thing.info)
            self.c_pool_table.append(thing)
        self.cpoolsize = index_offset - 10
        return index_offset - 10

    def get_constant_pool_size(self):
        if(len(self.c_pool_table)!=self.get_constant_pool_count()-1):
            self.create_c_pool()
        return self.cpoolsize

    def get_flags(self):
        return self.data[10+self.get_constant_pool_size()] + self.data[self.get_constant_pool_size()+11]

    def get_this_class(self):
        return self.data[self.get_constant_pool_size()+12] + self.data[self.get_constant_pool_size()+13]

    def get_super_class(self):
        return self.data[self.get_constant_pool_size()+14] + self.data[self.get_constant_pool_size()+15]

    def get_interface_count(self):
        return self.data[self.get_constant_pool_size()+16] + self.data[self.get_constant_pool_size()+17]

    def create_interface(self):
        itable = [self.get_interface_count()]
        for i in range[0,len(itable)]:
            itable[i] = self.data[self.get_constant_pool_size() + 18 + i]
        self.interface_table = itable 

    def get_field_count(self):
        return self.data[18+self.get_constant_pool_size()+self.get_interface_count()] + self.data[19+self.get_constant_pool_size()+self.get_interface_count()]

    def create_field_table(self):
        '''dont wanna do'''
        return 
    
    def get_field_size(self):
        return self.get_field_count()*2

    def get_method_count(self):
        return self.data[20+self.get_constant_pool_size() + self.get_interface_count() + self.get_field_size()] + self.data[21+self.get_constant_pool_size() + self.get_interface_count() + self.get_field_size()]

    def create_method_table(self):
        mtable = methodInfo()
        count = 22+self.get_constant_pool_size() + self.get_interface_count() + self.get_field_size()
        for i in range(0, self.get_method_count()):
            print(self.data[count] + self.data[1+count])
            print(self.data[2+count] + self.data[3 + count])
            print(self.data[4+count] + self.data[5 + count])
            print(self.data[6+count] + self.data[7 + count])
            print(self.data[8 + count] + self.data[9 + count])  #code attribute
            print(self.data[10 + count] + self.data[11 + count] + self.data[12 + count] + self.data[13 + count])
            print(self.data[14 + count] + self.data[15 + count])
            print(self.data[16 + count] + self.data[17 + count])
            print(self.data[18 + count] + self.data[19 + count] + self.data[20 + count] + self.data[21 + count])
    


class OpCodes():
    def __init__(self):
        self.table = {0x00: self.not_implemented}

    def not_implemented(self):
        return 'not implemented'

    def interpret(self, value):
        return self.table[value]()

if '__main__' == __name__:
    java = ClassFile() #pragma: no cover
    print('magic: ', java.get_magic()) #pragma: no cover
    print('minor_version: ', java.get_minor()) #pragma: no cover
    print('major_version: ', java.get_major()) #pragma: no cover
    print('constant_pool_count: ', java.get_constant_pool_count()) #pragma: no cover
    print('interface count: ', java.get_interface_count())
    print('field count: ', java.get_field_count())
    print('method count: ', java.get_method_count())
    java.create_method_table()