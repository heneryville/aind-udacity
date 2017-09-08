# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twin is an additional constraint.
It is actually a second order application of the only_choice rule.
That is you can eliminate a subset of N possibilities from other cells in a unit if there are N units that share the same possibilities and there are N of those possibilities.
In the case of only_choice, N = 1, meaning that if there is 1 cell in a unit, with 1 possibilities, we can eliminate that one from the other cells.
Naked twins is N = 2, meaning if there are 2 cells in a unit with 2 identical options, we can eliminate that from the other cells.
This hints that there should be a rule for "Naked triplets", "Naked quadruplets", etc. Though these are likely increasingly rare.

We can apply the constraint of naked twins to eliminiate possibilities from other cells. This reduction of possibilities can then be re-used in other constraints
to further reduce the problem space. Ultimately, search is used to guess and check otherwise un-reducible solutions
# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: The diagonal is just two an additional constraints on the problem.
We can add these as units to the other units, and apply all the other techniques to these constraints identically.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

