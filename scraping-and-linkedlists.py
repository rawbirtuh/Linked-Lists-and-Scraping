import urllib.request    #this loads a library you will need.  Put this line at the top of your file.

def readHtml(toDoList):
    response = urllib.request.urlopen("http://research.cs.queensu.ca/home/cords2/todo.txt")
    html = response.readline()
    toDoList = None

    while len(html) != 0:
        data = html.decode("utf-8").split(',')
        #print ("This is the input", data)
        data[1] = int(data[1])
        toDoList = addToHead(toDoList,data)
        html = response.readline()
    
    return toDoList

def addToHead(linkedList, value):
    newnode = {}
    newnode["data"] = value
    #set the next pointer of this new node to the head of the list, linkedList
    #newnode is now the head of the list, so we return this node (which is
    #connected to the rest of the list
    newnode["next"] = linkedList
    return newnode

def insertBefore(linkedList, ptr, value):
    #My version of addtoMiddle since we know the ptr we want to add it before.
    #Create a new node for the information to add to the linkedList
    node = {}
    node['data'] = value

    #This pointer will keep moving on until the value after ptr2 matches the ptr from sortLists.
    #Create a new pointer that points to the head of the list
    ptr2 = linkedList

    if ptr == ptr2:
        linkedList = addToHead(linkedList, value)
        return linkedList
        
    while ptr2['next'] != ptr:
        ptr2 = ptr2['next']

    #Connect the ptr2 to the node
    ptr2['next'] = node
    node['next'] = ptr
    return linkedList


'''
Prints the list.  We need to visit each node and print the data.  We cannot just print
the list using a print statement!!!  If you do, you will see a big mess.
'''
def printList(linkedList):
    ptr = linkedList
    while ptr != None:
        print(ptr['data'], "->", end="")
        ptr = ptr['next']
    print("None")

#INPUT: The toDoList linked list and the task to be added
#OUTPUT: The newTask placed in the toDoList 
def sortAdd(toDoList, newTask):
    #Start the pointer at the head
    ptr = toDoList

    #If the list is empty, just add whatever value
    if ptr == None:
        return addToHead(toDoList, newTask)

    #If the value after the pointer is none, this will not be triggered. When it only has one value, this won't be triggered.
    #Now, we want to give that a second check in case the value the pointer is at is being checked.

    #This function is checking if the 'time to finish' from the linked list is more than the 'time to finish' of the newTask
    while ptr['next'] != None:
        if ptr['data'][1] > newTask[1]:
            #Place the newTask before the pointer if the 'time to finish' from the pointer is more than the 'time to finish' of the newTask.
            return insertBefore(toDoList, ptr, newTask)
        
        elif ptr['data'][1] == newTask[1]:
            
            if ptr['data'][0] > newTask[0]:
                
                return insertBefore(toDoList, ptr, newTask)
        ptr = ptr['next']

    #Force check to see if the ptr exactly is over the newTask
    if ptr['data'][1] > newTask[1]:
        return insertBefore(toDoList, ptr, newTask)

    #If it hasn't been returned yet, create a new node that'll be the new end in case the newTask is higher than everything.
    node = {}
    node['data'] = newTask
    node['next'] = None
    ptr['next'] = node
    return toDoList
#INPUT: The two linkedList to move pointers around.
#The instruction carrying the taskDone in it (with a little formatting).
#OUTPUT: The didItList head without 'taskDone' and didItList with 'taskDone' in it.
def doToDid(toDoList,didItList, taskDone):

    taskDone.remove(taskDone[0])
    toDoPTR = toDoList
    didItPTR = didItList
    #Move the pointer to where the 'taskDone' is.
    if toDoPTR['data'][0] == taskDone[0]:
        print("The first value matches!")
    while toDoPTR != None:

        if toDoPTR['next'] == None:
            print("Ok")
            #return toDoList, didItList
        else:
            if toDoPTR['next']['data'][0] == taskDone[0]:
                printList(toDoPTR)
                #if next next is none then toDoPTR['next'] is the last value
                #This means that toDoPTR['next'] should now point to none
            
                if toDoPTR['next']['next'] == None:
                    if didItList != None:
                        toDoPTR['next']['next'] = didItList
                        toDoPTR['next'] = None
                        printList(didItList)
                        printList(toDoList)
                    else:
                        toDoPTR['next']['next'] = didItList
                        didItList = toDoPTR['next']
                        toDoPTR['next'] = None
                        printList(didItList)
                        printList(toDoList)
                else:
                    #I can't change the toDoList at toDoPTR['next'] to toDoPTR['next']['next']
                    didItPTR = toDoPTR['next']
                    pass

                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    


        toDoPTR = toDoPTR['next']
        
        

#INPUT: The toDoList and the command from before since it has all the info we need
#OUTPUT: The head of the toDoList with the new task added.
def addToDo(linkedList, instruction):

    #A little formatting before calling our sortAdd function. This removes the command
    instruction.remove(instruction[0])
    linkedList = sortAdd(linkedList, instruction)
    return linkedList

#INPUT: None
#OUTPUT: The commands in the form of a list of lists to be read out by driveDriver
def readDriver():

    response = urllib.request.urlopen("http://research.cs.queensu.ca/home/cords2/driver.txt")
    html = response.readline()
    data = []
    while len(html) != 0 and html != "":

        
        html = response.readline()
        
        data.append(html.decode("utf-8").split(','))

    return data


#INPUT: The two linked lists
#OUTPUT: All the commands finished
def driveDriver(toDoList, didItList):
    instructions = readDriver()
    for eachCom in instructions:
        if eachCom[0] == "PrintDidIt\n":
            print("Printing DidIt List. . .")
            printList(didItList)
        elif eachCom[0] == "ExecuteTask\n":
            print("The task", eachCom[1], "was done by", eachCom[2])
        elif eachCom[0] == "PrintToDo\n":
            print("Printing ToDo List. . .")
            printList(toDoList)
        elif eachCom[0] == "AddTask": #Turn into an integer to compare the integers from toDoList
            print("Adding Task:", eachCom[1])
            eachCom[2] = int(eachCom[2])
            toDoList = addToDo(toDoList, eachCom)
            printList(toDoList)
        else:
            print(eachCom[0],"That ain't no command I ever heard of")


    
def main():
    #creating empty lists
    toDoList = None
    toDoList = readHtml(toDoList)
    didItList = None
    driveDriver(toDoList, didItList)
main()

