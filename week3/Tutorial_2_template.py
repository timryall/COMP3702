import sys
import time

from collections import deque
import matplotlib.pyplot as plt
import heapq




# Define the 4 possible actions in 8-puzzle
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

# mapping
MOVE_MAPPING = {
    0: "LEFT",
    1: "RIGHT",
    2: "UP",
    3: "DOWN"
}

# Define an EightPuzzle class
class EightPuzzle:

    def __init__(self, squares):
        self.squares = tuple(squares)

        idx = -1
        for i in range(len(self.squares)):
            if self.squares[i] == '_':
                idx = i
        self.idx = idx

        self.total_cost = 0

    def __eq__(self, obj):
        # required to test if this object is in a collection
        if obj is None:
            return False
        return self.squares == obj.squares

    def __hash__(self):
        # required to allow this object to be placed inside a hashtable (i.e. set/dict)
        return hash(self.squares)

    def move_left(self):
        new_squares = list(self.squares)
        new_squares[self.idx] = self.squares[self.idx-1]
        new_squares[self.idx-1] = self.squares[self.idx]
        return EightPuzzle(new_squares)

    def move_right(self):
        new_squares = list(self.squares)
        new_squares[self.idx] = self.squares[self.idx+1]
        new_squares[self.idx+1] = self.squares[self.idx]
        return EightPuzzle(new_squares)

    def move_up(self):
        new_squares = list(self.squares)
        new_squares[self.idx] = self.squares[self.idx-3]
        new_squares[self.idx-3] = self.squares[self.idx]
        return EightPuzzle(new_squares)

    def move_down(self):
        new_squares = list(self.squares)
        new_squares[self.idx] = self.squares[self.idx+3]
        new_squares[self.idx+3] = self.squares[self.idx]
        return EightPuzzle(new_squares)

    def get_successors(self):
        successors = []

        if self.idx % 3 > 0:
            successors.append(self.move_left())
        else:
            successors.append(None)

        if self.idx % 3 < 2:
            successors.append(self.move_right())
        else:
            successors.append(None)

        if self.idx // 3 > 0:
            successors.append(self.move_up())
        else:
            successors.append(None)

        if self.idx // 3 < 2:
            successors.append(self.move_down())
        else:
            successors.append(None)

        return successors

    def num_inversions(self):
        """ Write code here to calculate the number of inversions of self.squares"""
        n_inversions = 0
        return n_inversions

    def get_parity(self):
        """ Write code here to determine the parity of self.squares using your num_inversions method"""
        return 0

    def __str__(self):
        s = ""
        for c in self.squares:
            s += c
        return s
    
    def get_cost(self, action):
        if(action == 'U'):
            return 1
        elif(action == 'D'):
            return 2
        elif(action == 'L'):
            return 3
        elif(action == 'R'):
            return 4
        else:
            raise Exception("Invalid action: {}".format(self.action))
    
    # Override less than function for UCS
    def __lt__(self, other):
        return self.total_cost < other.total_cost


# Node representation
# This is the object that represents a path/node on the frontier container
# It usually holds the state, parent, action, path_cost (optional)
# class StateNode:

#     """ Write code here to implement a node representation for entries in the frontier container
#         You should have a constructor that sets the state (puzzle), parent, action (and optionally path_cost / num_steps)
#     """
#     def __init__(self, puzzle):
#         #TO DO: add required arguments for the node
#         self.puzzle = puzzle

#     # We add get_successors to our Node to abstract away the dependence on the environment class (EightPuzzle)
#     # and enable getting of a node's successors when running search
#     # Here, we should only return states that are valid
#     def get_successors(self):
#         #TO DO: implement the get_successors function
#         s = []
#         suc = self.puzzle.get_successors()

#         return s

#     def __eq__(self, obj):
#         return self.puzzle == obj.puzzle


def reconstruct_path(parent, move, end_state):
    path = []
    moves = []
    state = end_state
    while state is not None:
        path.append(state)
        moves.append(move[state])
        state = parent[state]
    path.reverse()
    moves.reverse()
    return path, moves[1:]  # skip first None move

def bfs(initial, goal):
    """ Implement Breadth-First-Search Here"""
    # Define initial frontier
    frontier = deque([initial])
    reached = {initial}

    # Store parent and move
    parent = {initial: None}
    move = {initial: None}

    while frontier:  # while frontier not empty
        # Check node
        node = frontier.popleft()
        if node == goal:
            return reconstruct_path(parent, move, node)[1]

        for i, child in enumerate(node.get_successors()):
            if child is not None and child not in reached:
                frontier.append(child)
                reached.add(child)
                parent[child] = node
                move[child] = MOVE_MAPPING[i]

    print("BFS FAILED")
    return None


def dfs(initial, goal):
    """ Implement Depth-First-Search Here"""
    # Define initial frontier
    frontier = [initial]
    reached = {initial}

    # Store parent and move
    parent = {initial: None}
    move = {initial: None}

    while frontier:  # while frontier not empty
        # Check node
        node = frontier.pop()
        if node == goal:
            return reconstruct_path(parent, move, node)[1]

        for i, child in enumerate(node.get_successors()):
            if child is not None and child not in reached:
                frontier.append(child)
                reached.add(child)
                parent[child] = node
                move[child] = MOVE_MAPPING[i]

    print("DFS FAILED")
    return None


def ucs(initial, goal):
    """ Implement Depth-First-Search Here"""
    # Define initial frontier
    frontier = [initial]
    heapq.heapify(frontier)
    reached = {initial}

    # Store parent and move
    parent = {initial: None}
    move = {initial: None}

    while frontier:  # while frontier not empty
        # Check node
        node = heapq.heappop(frontier)
        if node == goal:
            return reconstruct_path(parent, move, node)[1]

        for i, child in enumerate(node.get_successors()):
            if child is not None and child not in reached:
                child.total_cost = child.total_cost + node.get_cost(MOVE_MAPPING[i][0])
                heapq.heappush(frontier, child)
                reached.add(child)
                parent[child] = node
                move[child] = MOVE_MAPPING[i]

    print("DFS FAILED")
    return None

def main(arglist):
    # Initial states to test
    p1_states = [
        "1348627_5",  # Easy
        "281_43765",  # Medium
        "281463_75",  # Harder
    ]


    p2_state = "1238_4765"  # Goal

    times_bfs = []
    depths_bfs = []
    times_dfs = []
    depths_dfs = []


    for p1_str in p1_states:
        p1 = EightPuzzle(p1_str)
        p2 = EightPuzzle(p2_state)
        
        # Check solvability
        if p1.get_parity() != p2.get_parity():
            print(f"{p1_str} -> No solution")
            times_bfs.append(None)
            depths_bfs.append(None)
            times_dfs.append(None)
            depths_dfs.append(None)
            continue
        
        # BFS timing
        t0 = time.time()
        for _ in range(5):  # repeat for stable timing
            actions_bfs = bfs(p1, p2)
        t_bfs = (time.time() - t0) / 5
        num_actions_bfs = len(actions_bfs)
        
        times_bfs.append(t_bfs)
        depths_bfs.append(num_actions_bfs)
        
        # DFS timing
        t0 = time.time()
        for _ in range(1):  # DFS may be slower, run once
            actions_dfs = ucs(p1, p2)
        t_dfs = (time.time() - t0)
        num_actions_dfs = len(actions_dfs)
        
        times_dfs.append(t_dfs)
        depths_dfs.append(num_actions_dfs)
        
        print(f"{p1_str} | BFS: {t_bfs:.4f}s ({num_actions_bfs} moves) | DFS: {t_dfs:.4f}s ({num_actions_dfs} moves)")

    # Plot BFS and DFS side-by-side with separate axes
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # BFS plot
    axes[0].plot(depths_bfs, times_bfs, marker='o', color='blue')
    axes[0].set_title("BFS: Time vs Solution Depth")
    axes[0].set_xlabel("Solution Depth (# of moves)")
    axes[0].set_ylabel("Time (seconds)")
    axes[0].grid(True)

    # DFS plot
    axes[1].plot(depths_dfs, times_dfs, marker='s', color='green')
    axes[1].set_title("DFS: Time vs Solution Depth")
    axes[1].set_xlabel("Solution Depth (# of moves)")
    axes[1].set_ylabel("Time (seconds)")
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main(sys.argv[1:])

