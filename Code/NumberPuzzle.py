# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import timeit
import argparse


# %%
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


# %%
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


# %%
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


# %%
def bfsSearch(init_state, goal_state, grid_size):

    nodes = list()
    visited_states = list()

    init_node = Node(init_state, 0, None, 0)
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
            branches = getBranches(current_node, grid_size) 
            
            for branch in branches:
                branch_state = branch.getState()
                if branch_state not in visited_states:
                    nodes.insert(0, branch)
  


# %%
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
    


# %%
def formatting(state, grid_size):
    state_copy = np.array(state.copy())
    state_copy = state_copy.reshape(grid_size, grid_size)
    state_copy = state_copy.transpose()
    state_copy = state_copy.reshape(-1)
    state_copy = np.array2string(state_copy, separator=' ')
    return state_copy[1: -1]

class store_as_array(argparse._StoreAction):
    def __call__(self, parser, namespace, values, option_string=None):
        values = np.array(values)
        return super().__call__(parser, namespace, values, option_string)

# %%
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

    start = timeit.default_timer()
    path, node_path = bfsSearch(initial_state, goal_state, grid_size)
    stop = timeit.default_timer()
    print("Time required: ", stop - start)
    print("storing it to file ...")
    storePath2Txtfile(path, node_path, file_names, grid_size)
    print(path)


# %%
if __name__ == "__main__":
    main()


# %%



