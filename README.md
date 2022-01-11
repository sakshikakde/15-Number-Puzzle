

# Problem 
Solve the 15-Puzzle starting from the given initial state. The final state is [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]       

       
       
![alt](https://sandipanweb.files.wordpress.com/2017/03/sol06.gif?w=676)
# File structure
    .
    ├── Code
    |  ├── NumberPuzzle.ipynb     
    |  ├── NumberPuzzle.py  
    ├── Results
    |  ├── test1
    |  ├── test2
    |  ├── test3
    |  ├── test4
    |  ├── test5
    ├── README.md


# How to run code
- Change the directory to the root location 
- Run the following command:       
``` python3 Code/NumberPuzzle.py --PuzzleNumber 4 --InitState 1 6 2 3 9 5 7 4 0 10 11 8 13 14 15 12 --SaveFolderName ./Results/test5/ ```

## Parameters
- PuzzleNumber: The size of the puzzle. Here, it is 4. But the code is generalized for any number of grids. Though, the tesing has been done only for size 3 and 4.
- InitState: Inital state for the puzzle
- SaveFolderName: folder path where you want to save the output .txt files

# Results
The folders corresponding to test cases have been created. Each folder has
- moves.txt: Describes the moves from start till end: eg. left, right
- path.txt: List of puzzle state from start till end. Only the nodes on the path
- parent_child_nodes.txt: this has three columns, parent node state, current node state, child node state


