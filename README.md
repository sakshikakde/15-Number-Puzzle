# File Structure

project1_sakshi_kakde    

--Code     
----NumberPuzzle.ipynb     
----NumberPuzzle.py     

--Results      
----test1      
----test2    
----test3    
----test4    
----test5    

--README.md    

Inside the code structure, the python script is the final code. The python notebook is for development purpose.
# How to run code
1) Change the directory to the location where NumberPuzzle.py is located. Eg.
/home/sakshi/courses/ENPM661/proj1_sakshi_kakde/Code

2) Run the python script using  the command:       
python3 NumberPuzzle.py --PuzzleNumber 4 --InitState 1 6 2 3 9 5 7 4 0 10 11 8 13 14 15 12 --SaveFolderName /home/sakshi/courses/ENPM661/proj1_sakshi_kakde/Results/test5/

## parameters
1) PuzzleNumber: The size of the puzzle. Here, it is 4. But the code is generalized for any number of grids. Though, the tesing has been done only for size 3 and 4.

2) InitState: Inital state for the puzzle

3) SaveFolderName: folder path where you want to save the output .txt files

## Libraries used
numpy, timeit, argparse


# Output
The folders corresponding to test cases have been created. Each folder has
1) moves.txt: Describes the moves from start till end: eg. left, right
2) path.txt: List of puzzle state from start till end. Only the nodes on the path
3) parent_child_nodes.txt: this has three columns, parent node state, current node state, child node state


