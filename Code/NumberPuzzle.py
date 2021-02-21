import numpy as np
import timeit
import argparse


# Class to store the node info
# state: Current state of the node
# parent: The previous state of the node from where the current state is obtained
# move: The move that was performed on parent node to get the current state
class Node():
    def __init__(self, state, parent, move, cost): 

        self.state = state
        #self.goal = goal_state
        self.parent = parent
        self.move = move
        self.cost = cost
        
    def getState(self):
        return self.state
		
    def getParent(self):
        return self.parent
		
    def getMove(self):
	    return self.move
		
    def getCost(self):
        return self.cost

    def getFullPath(self):
        
        moves = []
        nodes = []
        current_node = self
        while(current_node.getMove() is not None):

            moves.append(current_node.getMove())
            nodes.append(current_node)
            current_node = current_node.getParent()

        nodes.append(current_node)
        moves.reverse()
        nodes.reverse()
        
        return moves, nodes

    def printStats(self):
        pass

# Func to get children in all possible directions: up, down, left, right
def getBranches(node, grid_size):

    moves = ["up", "down", "left", "right"]
    branches = []
    branches.append(Node(moveUp(node.getState(), grid_size), node, moves[0], node.getCost() + 1))
    branches.append(Node(moveDown(node.getState(), grid_size), node, moves[1], node.getCost() + 1))
    branches.append(Node(moveLeft(node.getState(), grid_size), node, moves[2], node.getCost() + 1))
    branches.append(Node(moveRight(node.getState(), grid_size), node, moves[3], node.getCost() + 1))

    #remove None nodes
    b = [branch for branch in branches if branch.getState() is not None]
            
    return b


# Func to move the blank tile up
def moveUp(state, grid_size):

    state_copy = state.copy()
    position = state_copy.index(0)

    num_rows = grid_size
 
    if position not in range(0, grid_size):
        #can move up
        #swap with the upper row
        tmp = state[position]
        state_copy[position] = state_copy[position - num_rows]
        state_copy[position - num_rows] = tmp
        return state_copy
    else:
        return None

# Func to move the blank tile down
def moveDown(state, grid_size):
    state_copy = state.copy()
    position = state_copy.index(0)

    num_cols = grid_size
    
    if position not in range(grid_size*(grid_size-1), grid_size*grid_size):
        #can move down
        #swap with the lower row
        tmp = state[position]
        state_copy[position] = state_copy[position + num_cols]
        state_copy[position + num_cols] = tmp
        return state_copy
    else:
        return None

# Func to move the blank tile right
def moveRight(state, grid_size):
    state_copy = state.copy()
    position = state_copy.index(0)

    #if position not in [2, 5, 8]:
    not_allowed = np.linspace(grid_size-1, grid_size*grid_size - 1, grid_size, dtype = int)
    if position not in not_allowed:
        #print(position)
        #can move right 
        #swap with the reft col
        tmp = state_copy[position]
        state_copy[position] = state_copy[position + 1]
        state_copy[position + 1] = tmp
        return state_copy
    else:
        return None

# Func to move the blank tile left
def moveLeft(state, grid_size):
    state_copy = state.copy()
    position = state_copy.index(0)
    #num_rows = 3 
    not_allowed = np.linspace(0, grid_size*(grid_size-1), grid_size, dtype = int)
    if position not in not_allowed:
        #can move left
        #swap with the left col
        tmp = state_copy[position]
        state_copy[position] = state_copy[position - 1]
        state_copy[position - 1] = tmp
        return state_copy
    else:
        return None


# Func to perform BFS search
def bfsSearch(init_state, goal_state, grid_size):

    nodes = list() #maintain a list of all possible states till the goal is reached
    visited_states = list() #maintain a list of all achieved states

    init_node = Node(init_state, 0, None, 0) #from input
    nodes.append(init_node)

    while(nodes):

        current_node = nodes.pop()
        visited_states.append(current_node.getState())
        
        #print("number of visited nodes: ", len(visited_states))

        if np.array_equal(current_node.getState(), goal_state):
            
            print("Goal Reached!")
            print("Total number of nodes explored:", len(visited_states))
            full_path, node_path = current_node.getFullPath()
            return full_path, node_path

        else:
            branches = getBranches(current_node, grid_size) #get chilren
            
            for branch in branches:
                branch_state = branch.getState()
                if branch_state not in visited_states: # check if achieved earlier
                    nodes.insert(0, branch) # if not, add to visted list


# Func to check solvablity
# if puzzle number is odd: eg. 3
# get inversion count. if even-> solvable, odd->not solvable

# if puzzle number is even: eg. 4
# get inversion count and location of 0 from bottom
# location of 0 from bottom is even AND inversion count is odd -> solvable
# location of 0 from bottom is odd AND inversion count is even -> solvable
  
def checkSolvablity(init_state, grid_size):

    num = grid_size*grid_size
    inversion_count = 0

    
    for n in range(1, num):
        current_num = init_state[n]

        for m in range(n, num):
            if current_num > init_state[m]:
                if init_state[m] is not 0:
                    inversion_count = inversion_count + 1
    print("Inversion count = ", inversion_count)

    if (grid_size % 2) == 1: #odd
        if inversion_count % 2 == 0:
            print("The puzzle is solvable!")
            return True
        else:
            print("The puzzle is not solvable!")
            return False

    if (grid_size % 2) == 0: #even
        position = init_state.index(0)
        even_indexes = []
        for r in range(0, grid_size, 2):
            for c in range(0, grid_size):
                even_indexes.append(c + r*grid_size)
        print("Check if 0 is located at any of these: ", even_indexes)
        
        if position in even_indexes:
            if inversion_count % 2 == 1:
                print("The puzzle is solvable!")
                return True

            else:
                print("The puzzle is not solvable!")
                return False
        
        elif position not in even_indexes:
            if inversion_count % 2 == 0:
                print("The puzzle is solvable!")
                return True

            else:
                print("The puzzle is not solvable!")
                return False

        else:
            print("The puzzle is not solvable!")
            return False

# func to store the path into a .txt file
def storePath2Txtfile(path, node_path, file_names, grid_size):
    path_file_name = file_names[0]
    node_file_name = file_names[1]
    parent_child_file_name = file_names[2]

    path_file = open(path_file_name, 'w')
    path_file.writelines("%s\n" % move for move in path)

    node_file = open(node_file_name, 'w')
    node_file.writelines("%s\n" % formatting(node.getState(), grid_size) for node in node_path)

    parent_child_file = open(parent_child_file_name, 'w')
    for i in range(len(node_path)-1):
        if i is 0:
            parent_child_file.writelines("NA\t")
            parent_child_file.writelines("|\t")
            parent_child_file.writelines("%s\t" % formatting(node_path[i].getState(), grid_size))
            parent_child_file.writelines("|\t")
            parent_child_file.writelines("%s\n" % formatting(node_path[i+1].getState(), grid_size))
        else:

            parent_child_file.writelines("%s\t" % formatting(node_path[i].getParent().getState(), grid_size))
            parent_child_file.writelines("|\t")
            parent_child_file.writelines("%s\t" % formatting(node_path[i].getState(), grid_size))
            parent_child_file.writelines("|\t")
            parent_child_file.writelines("%s\n" % formatting(node_path[i+1].getState(), grid_size))

    parent_child_file.close()
    path_file.close()
    node_file.close()
    


# Since the derisred order of numbers in .txt file is different that what I used
# this is a simple function to achive the same
def formatting(state, grid_size):
    state_copy = np.array(state.copy())
    state_copy = state_copy.reshape(grid_size, grid_size)
    state_copy = state_copy.transpose()
    state_copy = state_copy.reshape(-1)
    state_copy = np.array2string(state_copy, separator=' ')
    return state_copy[1: -1]


def main():

    Parser = argparse.ArgumentParser()
    Parser.add_argument("--PuzzleNumber", default = 4, type=int, help = 'Grid size for the puzzle')
    Parser.add_argument("--InitState", nargs='+', type=int, default= '0 2 3 4 1 5 7 8 9 6 11 12 13 10 14 15', help = 'init state for the puzzle')
    Parser.add_argument('--SaveFolderName', default='/home/sakshi/courses/ENPM661/proj1_sakshi_kakde/Results/test1/', help='Base path of project1 where the results will be saved, Default:/home/sakshi/courses/ENPM661/proj1_sakshi_kakde/Results/test1')
    
    Args = Parser.parse_args()
    grid_size = Args.PuzzleNumber
    save_folder_name = Args.SaveFolderName
    init_state = Args.InitState
    init_state = list(init_state)
    
    file_names = []
    file_names.append(save_folder_name + "moves.txt")
    file_names.append(save_folder_name + "path.txt")
    file_names.append(save_folder_name + "parent_child_nodes.txt")
    

    grid_size = int(grid_size)
    print("The puzzle grid size is ", grid_size, "x", grid_size)
    initial_state = init_state
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

    print("initial state is: ", initial_state)
    print("goal state is: ", goal_state)
    print("solving ....")

    if(checkSolvablity(initial_state, grid_size)):
        start = timeit.default_timer()
        path, node_path = bfsSearch(initial_state, goal_state, grid_size)
        stop = timeit.default_timer()
        print("Time required: ", stop - start)
        print("storing it to file ...")
        storePath2Txtfile(path, node_path, file_names, grid_size)
        print(path)


if __name__ == "__main__":
    main()





