#CS325 HW3 / Ju

import heapq 

class Node:
    def __init__(self, count, children):
        self.count    = count
        self.children = children
        
    def is_leaf(self):
        return False
        
    def __lt__(self, other):
        return self.count < other.count

    def __eq__(self, other):
        return self.count == other.count
        
class LeafNode(Node):
    def __init__(self, symbol, count):
        super().__init__(count, [])
        self.symbol = symbol
        
    def is_leaf(self):
        return True

class HuffmanCode:
    def __init__(self, F):
        self.C = dict()
        self.T = None
        self.cost = 0
        self.average_cost = 0
        
        # Construct priority queue
        heap = []
        for symbol, count in F.items():
            heap.append(LeafNode(symbol, count))

        heapq.heapify(heap)
        while len(heap) > 1:
            n1 = heapq.heappop(heap)
            n2 = heapq.heappop(heap)
            new_count = n1.count + n2.count
            new_children = [n1, n2]
            new_node = Node(new_count, new_children)
            heapq.heappush(heap, new_node)
            
            #Define T
            self.T = heap[0]
            
            self.generate_codes(self.T, "")
        
    def generate_codes(self, node, code):
        if node.is_leaf():                   
            # Set the value of C for the symbol of code 
            self.C[node.symbol] = code  
            #Define cost and average cost
            self.cost += node.count * len(code)
            self.average_cost = self.cost / sum(F.values())
        else:
            self.generate_codes(node.children[0], code + "0")
            self.generate_codes(node.children[1], code + "1")
    
    def encode(self, m):
        encode_m = ""
        for char in m:
            encode_m += self.C[char]

        return encode_m
            
    def decode(self, c):
        decode_c = ""
        node = self.T
        for bit in c:
            if bit == "0":
                node = node.children[0]
            else:
                node = node.children[1]
            if node.is_leaf():
                decode_c += node.symbol
                node = self.T
        return decode_c
        
            
    def get_cost(self):
        
        return self.cost
            
    def get_average_cost(self):
        
        return self.average_cost
        
def get_frequencies(s):

    F = dict()
    
    for char in s:
        if not(char in F):
            F[char] = 1
        else:
            F[char] += 1
            
    return F
    
def get_frequencies_from_file(file_name):
    
    f = open(file_name, "r")
    s = f.read()
    f.close()

    return get_frequencies(s)


F = get_frequencies_from_file(r"C:\Users\jujud\Desktop\CS325\HW3\cs325-w23-homework3-gettysburg-address.txt")

huffman_code = HuffmanCode(F)

print(F)
print("Encoded output: ", huffman_code.encode("go beavers"))
print("Decoded output: ", huffman_code.decode("10010100011110010100111111001000111101011111001100010011110111000001110001"))
print("Cost: ", huffman_code.get_cost())
print("Average Cost: ", huffman_code.get_average_cost())

