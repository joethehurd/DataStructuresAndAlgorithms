from hashlib import new
from multiprocessing import Value
from operator import index
from tokenize import Double
import statistics

# Node - For Linked Lists, Doubly Linked Lists, and Stacks
#region
class Node:
      def __init__(self, value):
        # creates a new node
        self.value = value
        self.next = None
        self.prev = None
#endregion

# Linked Lists
#region

class LinkedList:    
    def __init__(self, value):
        # creates a newNode list as well as the first node
        newNode = Node(value)
        self.head = newNode
        self.tail = newNode
        self.length = 1        
    
    def Append(self,value):
        # creates a newNode node and adds that node to the end of list
        newNode = Node(value)
        if self.head is None: # checks if list is empty. achieves same result as if self.length == 0 (checking if is None is faster BUT checking self.length is safer/more reliable)
            self.head = newNode
            self.tail = newNode   
        else:
            self.tail.next = newNode
            self.tail = newNode
        self.length += 1
        return True # OPTIONAL, other functions that call this may require a boolean value   

    def Prepend(self,value):
        # creates a newNode node and adds that node to the beginning of list
        newNode = Node(value)
        if self.length == 0:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.next = self.head
            self.head = newNode
        self.length += 1
        return True # OPTIONAL, other functions that call this may require a boolean value
    
    def Pop(self):
        # extracts the last node value from a list and reduces the list size accordingly
        if self.length == 0:
            return None # by returning nothing, this basically cancels/breaks out of the function, so an else statement afterwards is unnecessary/implied
        temp = self.head
        preNode = self.head
        while(temp.next is not None):
            preNode = temp
            temp = temp.next
        self.tail = preNode
        self.tail.next = None     
        self.length -= 1
        if self.length == 0:
            self.head = None
            self.tail = None
        return temp 

    def PopFirst(self):
        if self.length == 0:
            return None
        temp = self.head
        self.head = self.head.next
        temp.next = None
        self.length -= 1
        if self.length == 0:
            self.tail = None
        return temp

    def Get(self, index):
        # gets/returns the node value specified by a specific index (does not extract/remove)
        if index < 0 or index >= self.length:
            return None
        temp = self.head
        for _ in range(index): # if the index counter isnt being used within the for loop, you are supposed to use an _ instead of an i
            temp = temp.next
        return temp

    def SetValue(self, index, value):
        temp = self.get(index)
        if temp is not None: # "if temp" is the same as saying "if temp is not None"...i currently prefer is not None for clarity, although if temp might be more efficient
            temp.value = value
            return True
        return False

    def Insert(self, index, value):
        if index < 0 or index > self.length:
            return False
        if index == 0:
            return self.Prepend(value) # this method uses the boolean value in prepend
        if index == self.length:
            return self.Append(value) # this method uses the boolean value in append
        newNode = Node(value)
        temp = self.get(index - 1)
        newNode.next = temp.next
        temp.next = newNode
        self.length += 1
        return True
  
    def Remove(self, index):
        if index < 0 or index >= self.length:
            return None
        if index == 0:
            return self.PopFirst()
        if index == self.length - 1:
            return self.Pop()
        prev = self.get(index - 1)
        temp = prev.next
        prev.next = temp.next
        temp.next = None
        self.length -= 1
        return temp

    def Reverse(self):
        temp = self.head
        self.head = self.tail
        self.tail = temp
        after = temp.next
        before = None
        for _ in range(self.length):
            after = temp.next
            temp.next = before
            before = temp
            temp = after

    def PrintList(self):
        # this function iterates through the linked list and prints each node value
        temp = self.head    
        while temp is not None:
            print(temp.value)
            temp = temp.next

#endregion

# Doubly Linked Lists
#region
class DoublyLinkedList:
    def __init__(self, value):
        newNode = Node(value)
        self.head = newNode
        self.tail = newNode
        self.length = 1
    
    def PrintList(self):
        # iterate through the linked list and print each node value
        temp = self.head    
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def Append(self, value):
        newNode = Node(value)
        if self.length == 0: 
            self.head = newNode
            self.tail = newNode
        else:
            newNode.prev = self.tail
            self.tail.next = newNode           
            self.tail = newNode
        self.length += 1
        return True

    def Prepend(self, value):
        newNode = Node(value)
        if self.length == 0:
            self.head = newNode
            self.tail = newNode
        else:            
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode
        self.length += 1
        return True

    def Pop(self):
        if self.length == 0:
            return None
        temp = self.tail
        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            temp.prev = None
        self.length -= 1      
        return temp
           
    def PopFirst(self):
        if self.length == 0:
            return None
        temp = self.head
        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
            temp.next = None
        self.length -= 1
        return temp

    def Get(self, index):
        if index < 0 or index >= self.length:
            return None       
        if index < self.length / 2: # if specified index is in first half of list, count upwards. otherwise count backwards....for optimized efficiency
            temp = self.head
            for _ in range(index):                
                temp = temp.next                  
        else:
            temp = self.tail
            for _ in range(self.length - 1, index, -1):               
                temp = temp.prev                
        return temp

    def SetValue(self, index, value):
        temp = self.Get(index)
        if temp is not None:
            temp.value = value
            return True
        return False

    def Insert(self, index, value):
        if index < 0 or index > self.length:
            return False
        if index == 0:
            return self.Prepend(value)
        if index == self.length:
            return self.Append(value)
        newNode = Node(value)
        before = self.Get(index - 1)
        after = before.next
        newNode.prev = before
        newNode.next = after
        before.next = newNode
        after.prev = newNode
        self.length += 1
        return True

    def Remove(self, index):
        if index < 0 or index >= self.length:
            return False
        if index == 0:
            return self.PopFirst()
        if index == self.length - 1:
            return self.Pop()
        temp = self.Get(index)
        before = temp.prev # Option 1
        after = temp.next # Option 1
        before.next = after # Option 1...same as saying "temp.next.prev = temp.prev" without having to declare "before = temp.prev" above...this is easier to read though
        after.prev = before # Option 1...same as saying "temp.prev.next = temp.next" without having to declare "after = temp.next" above...this is easier to read though        
        #temp.next.prev = temp.prev # Option 2 ... less lines of code at the cost of readability
        #temp.prev.next = temp.next # Option 2 ... less lines of code at the cost of readability
        temp.next = None
        temp.prev = None
        self.length -= 1
        return temp
#endregion

# Stacks
#region
class Stack:
    # nodes (items) can only be inserted/extracted from the top
    # items can only be taken out when no other items are above them (First In Last Out)
    # self.head becomes self.top
    # self.length becomes self.height

    def __init__(self, value):
        newNode = Node(value)
        self.top = newNode
        self.height = 1

    def PrintStack(self):
        temp = self.top
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def Push(self, value):
        newNode = Node(value)
        if self.height == 0:
            self.top = newNode            
        else:            
            newNode.next = self.top            
            self.top = newNode
        self.height += 1
        return True

    def Pop(self):        
        if self.height == 0:
            return None
        temp = self.top
        if self.height == 1:
            self.top = None            
        else:
            self.top = self.top.next            
            temp.next = None
        self.height -= 1
        return temp
#endregion

# Queues
#region
# items are inserted at the right (aka tail) and extracted from the left (aka head)
# items must fully pass through the Queue to be taken out (First In First Out)
# self.head becomes self.first --- this is where items exit
# self.tail becomes self.last --- this is where items enter 
class Queue:

    def __init__(self, value):
        newNode = Node(value)
        self.first = newNode
        self.last = newNode
        self.length = 1

    def PrintQueue(self):
        temp = self.first
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def Enqueue(self, value):
        newNode = Node(value)
        if self.length == 0:
            self.first = newNode
            self.last = newNode
        else:
            self.last.next = newNode
            self.last = newNode
        self.length += 1

    def Dequeue(self):
        if self.length == 0:
            return None
        temp = self.first
        if self.length == 1:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next
            temp.next = None
        self.length -= 1
        return temp

#endregion

# Node - For Trees (Binary Search Trees)
#region
class TreeNode:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

#endregion

# Trees (Binary Search Trees)
#region
# each parent node can have a max of 2 children......1 left and 1 right                         (45) --- Root, Parent
# the children to the left are always less than the highest parent node (aka the root)         /    \
# the children to the right are always greater than the root                                 30      60 --- Children, Parents
# child nodes can also be parents to subsequent nodes                                       /  \    /  \
# a node without any children is known as a leaf                                           20  40  50  70 --- Children, Leaves     
# trees cannot contain duplicate nodes

class BinarySearchTree:

    def __init__(self):        
        self.root = None

    def Insert(self, value):
        newNode = TreeNode(value)       
        if self.root is None:
            self.root = newNode
            return True 
        temp = self.root
        while (True):
            if newNode.value == temp.value: # checks to see if the new value is a duplicate...if it is a duplicate: returns False and does not insert anything to the tree
                return False
            if newNode.value < temp.value: #checks to see if node should be placed to left or right
                if temp.left is None:      #checks to see if a space is available for placement
                    temp.left = newNode
                    return True            
                else:                # this is called when the desired space is already taken
                    temp = temp.left # this relocates temp to the next node, and the loop will continue checking available spaces until one is found
            else:
                if temp.right is None:
                    temp.right = newNode
                    return True
                else:
                    temp = temp.right
        
    def Contains(self, value):   
        print("Desired Value = {}\n".format(value))
        temp = self.root
        while temp is not None:
            if value < temp.value:
                print("Moving Left")
                temp = temp.left
                print("Checking Node Value: {}\n".format(temp.value))
            elif value > temp.value:
                print("Moving Right")
                temp = temp.right
                print("Checking Node Value: {}\n".format(temp.value))
            else:
                print("Desired Value: {} == Node Value: {}".format(value, temp.value))
                return True 
        return False            

#endregion

# Hash Tables
#region
class HashTable:
    def __init__(self, size = 7):
        self.data_map = [None] * size
    
    def __hash(self, key):
        myHash = 0
        for letter in key:
            myHash = (myHash + ord(letter) * 23) % len(self.data_map)
        return myHash

    def PrintTable(self):
        for i, val in enumerate(self.data_map):
            print(i, ": ", val)

    def SetItem(self, key, value):
        index = self.__hash(key)
        if self.data_map[index] == None:
            self.data_map[index] = []
        self.data_map[index].append([key, value])

    def GetItem(self, key):
        index = self.__hash(key)
        if self.data_map[index] is not None:
            for i in range(len(self.data_map[index])):
                if self.data_map[index][i][0] == key:
                    return self.data_map[index][i][1]
        return None

    def Keys(self):
        allKeys = []
        for i in range(len(self.data_map)):
            if self.data_map[i] is not None:
                for j in range(len(self.data_map[i])):
                    allKeys.append(self.data_map[i][j][0])
        return allKeys

# INEFFICIENT Non-Hash Method: O(n)
def ItemInCommon1(listOne, listTwo):
    for i in listOne:
        for j in listTwo:
            if i == j:
                print("Common value = {}".format(j))
                return True
    print("No common values found")
    return False

# EFFICIENT Hash Method: O(1)
def ItemInCommon2(listOne, listTwo):
    myDict = {}
    for i in listOne:
        myDict[i] = True
    for j in listTwo:
        if j in myDict:
            print("Common value = {}".format(j))
            return True
    print("No common values found")
    return False

#endregion

# Graphs
#region
# a Graph is a web of vertices that connect to other vertices via edges
# Graphs can be illustrated/constructed using Matrices or Adjacent Lists 
# Matrices store ALL relationships between vertices, and record connections that do AND do not exist
# Adjacent Lists only store relationships between vertices when a connection does exist
# For this example, an Adjacent List will be used (it is usually more efficient and better practice when managing a lot of data)
# Adjacent Lists store data using a Dictionary that contains a List of each relationship
# Vertices are stored as keys, Edges are stored as values that represent the other vertices the primary vertex key shares a relationship with
# ...(this is how relationships are illustrated...i.e., {'A':['B','C']}.........{'Vertex':['otherVertex','anotherVertex']}.........{Vertex:[Edges]}.........{Key:[Values]}

class Graph:
    
    def __init__(self):
        self.adjList = {} # this creates an empty dictionary that will hold the lists of vertices/edges

    def PrintGraph(self):
        for vertex in self.adjList:
            print(vertex, ':', self.adjList[vertex])

    def AddVertex(self, vertex):
        if vertex not in self.adjList.keys(): #if the vertex doesnt already exist, add it to the dictionary as a key
            self.adjList[vertex] = [] # this creates the key with an empty list (which will eventually store edges as relationships between vertices)
            return True
        return False

    def AddEdge(self, v1, v2):
        if v1 in self.adjList.keys() and v2 in self.adjList.keys(): # if both vertices (keys) exist, you can create an edge between them
            print("Creating edge between Vertex:{} and Vertex:{}".format(v1,v2))
            self.adjList[v1].append(v2) # this adds each vertex (aka key) to the other's list of edges (aka values) 
            self.adjList[v2].append(v1) # ibid...
            return True
        return False

    def RemoveEdge(self, v1, v2):
        if v1 in self.adjList.keys() and v2 in self.adjList.keys(): # if both vertices (keys) exist, you can remove the edge between them
            try: # this will attempt to remove the relationship between the two vertices, but will do nothing if that relationship doesnt exist
                print("Removing edge between Vertex:{} and Vertex:{}".format(v1,v2))
                self.adjList[v1].remove(v2)
                self.adjList[v2].remove(v1)
            except ValueError:              
                print("No edge was found between Vertex:{} and Vertex:{}".format(v1,v2))
                pass # this ignores the specific error that would occur if you try to remove a relationship that never existed
            return True
        return False

    def RemoveVertex(self, vertex):
        if vertex in self.adjList.keys():
            for otherVertex in self.adjList[vertex]:
                print("Removing Vertex:{} from list of Vertex:{}".format(vertex, otherVertex))
                self.adjList[otherVertex].remove(vertex)
            print("Removing Vertex:{} from Graph".format(vertex))
            del self.adjList[vertex]
            return True
        return False

#endregion

# Sorting Methods
#region

def BubbleSort(myList):
    print("Starting List: {}\n".format(myList))
    for i in range(len(myList) - 1, 0, -1):
        for j in range(i):            
            if myList[j] > myList[j+1]: # this determines if a larger number is before a smaller number and swaps them if so                         
                #print("Swapping {} with {}".format(myList[j], myList[j+1]))
                temp = myList[j] # temp saves the place of myList[j] so my myList[j] can be swapped with myList[j+1]
                myList[j] = myList[j+1]
                myList[j+1] = temp                
                #print("Current List = {}\n".format(myList))
    return myList




def SelectionSort(myList):
    print("Starting List: {}\n".format(myList))
    for i in range(len(myList) - 1):        
        minIndex = i
        for j in range(i+1, len(myList)):
            if myList[j] < myList[minIndex]:
                minIndex = j
        if i != minIndex:
            print("Swapping {} with {}".format(myList[i], myList[minIndex]))
            temp = myList[i]
            myList[i] = myList[minIndex]
            myList[minIndex] = temp
            print("Current List = {}\n".format(myList))
    return myList

def InsertionSort(myList):
    print("Starting List: {}\n".format(myList))
    for i in range(1, len(myList)):
        temp = myList[i]
        j = i-1
        while temp < myList[j] and j > -1:
            print("Swapping {} with {}".format(myList[j+1], myList[j]))
            myList[j+1] = myList[j]
            myList[j] = temp
            print("Current List = {}\n".format(myList))
            j -= 1
    return myList

myList = [24,20,26,17,16,11,13,14,14,21,35,30,31,33,27,37,38,49,42,40,40,38,48,44,36]

print(statistics.mean(BubbleSort(myList)))

#print("New List: {}\n".format(BubbleSort(myList)))
#print("New List: {}\n".format(SelectionSort(myList)))
#print("New List: {}\n".format(InsertionSort(myList)))

#endregion

# Merging Lists
#region 
def MergeLists(listOne,listTwo):
    # lists must be sorted before combining with this method
    print("Merging Lists: {} + {}\n".format(listOne, listTwo))
    combinedList = []
    i = 0
    j = 0
    while i < len(listOne) and j < len(listTwo):
        if listOne[i] < listTwo[j]:            
            combinedList.append(listOne[i])
            print("Adding {} to Combined List = {}".format(listOne[i], combinedList))
            i += 1
        else:            
            combinedList.append(listTwo[j])
            print("Adding {} to Combined List = {}".format(listTwo[j], combinedList))
            j += 1
    while i < len(listOne):         
         combinedList.append(listOne[i])
         print("Adding {} to Combined List = {}".format(listOne[i], combinedList))
         i += 1
    while j < len(listTwo):        
        combinedList.append(listTwo[j])
        print("Adding {} to Combined List = {}".format(listTwo[j], combinedList))
        j += 1   
    return combinedList

def MergeSort(myList):
    print("Calling MergeSort.......Current List = {}".format(myList))
    # recursive functions call on themselves (basically creating a loop), and must eventually break/return to avoid stack overflow
    # this function recursively splits a list into smaller chunks until each item becomes its own individual list
    # then those individual lists are recursively sorted and put back together using the MergeList function
    if len(myList) == 1: # once the list = 1 item, it is returned to the previously called MergeSort function, where it will be sorted and merged with the other list items       
        return myList    
    midIndex = int(len(myList) / 2) # splits the list into 2 halves from middle to left and middle to right       
    left = MergeSort(myList[:midIndex])     
    right = MergeSort(myList[midIndex:])      
    print("Left = {}......Right = {}".format(left, right))
    return MergeLists(left,right)

#print("\nNew List: {}\n".format(MergeLists(listOne, listTwo)))
#print("\nNew List: {}\n".format(MergeLists(SelectionSort(ulOne), BubbleSort(ulTwo)))) # this sorts two unordered lists and merges them into one ordered list
#mergedList = MergeSort(myList)
#print("\nNew List: {}\n".format(MergeSort(myList)))

#myList = ['D','G','A','O','Z','M']
#listOne = [1,2,7,8]
#listTwo = [3,4,5,6]
#ulOne = [2,8,1,7]
#ulTwo = [5,4,6,3]

#endregion

# Quick Sort
#region
def Swap(myList, indexOne, indexTwo):
    temp = myList[indexOne]
    myList[indexOne] = myList[indexTwo]
    myList[indexTwo] = temp

def Pivot(myList, pivotIndex, endIndex):
    swapIndex = pivotIndex
    for i in range(pivotIndex + 1, endIndex + 1):
        if myList[i] < myList[pivotIndex]:
            swapIndex += 1
            Swap(myList, swapIndex, i)
    Swap(myList, pivotIndex, swapIndex)
    return swapIndex

def QuickSortHelper(myList, left, right): # this method works as a standalone QuickSort, but it requires the user to pass the indices of the list each time
    if left < right:
        pivotIndex = Pivot(myList, left, right)
        QuickSortHelper(myList, left, pivotIndex - 1)
        QuickSortHelper(myList, pivotIndex + 1, right)
    return myList

def QuickSort(myList):
    return QuickSortHelper(myList, 0, len(myList) - 1) # this dynamically takes care of the indices so the user only has to pass the list

#myList = [4,6,1,7,3,2,5]
#print(QuickSort(myList))

#endregion

