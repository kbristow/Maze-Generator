import random
from maze_view import *
class MazeGenerator():
    """Generates a random maze or dungeon in text format.

    Attributes:
        _CHANGE_PROBABILITY: How likely the path being generated is to change
            direction.
        width: how many tiles wide is the maze.
        height: how many tiles heigh is the maze.
        path_info: dictionary of all locations that contain a walkable tile.
    """

    _CHANGE_PROBABILITY = 0.2
    width = 0
    height = 0
    path_info = dict()

    def __init__(self, width, height, start_dir = "R", path_counter = -1, sources = 1):
        """Initialises the generator with the given configuration.

        Args:
            width: how many tiles wide the maze will be.
            height: how many tiles heigh the maze will be.
            start_dir: the default direction generated path will start moving in.
            path_counter: the number of moves a path will make before stopping.
            sources: number of path to create.
        """
        self.width = width
        self.height = height
        self.init_maze(width, height)
        
        for i in range(0,sources):  
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if path_counter == -1:
                path_counter = width*height*3/4

            new_dir = start_dir

            if start_dir == "Rand":
                new_dir = ["U", "D", "R", "L"][random.randint(0, 3)]

            self.create_path(x, y, new_dir, path_counter)
        self.draw_text_map(width, height)

    def create_path(self, x, y, starting_direction, max_path_depth):
        """Create a random path.

        Args:
            x: starting x location for random path.
            y: starting y location for random path.
            starting_direction: starting direction for the path.
            max_path_depth: maximum steps the path will take.
        """
        
        for count in range(0, max_path_depth):            
            new_direction = self.get_new_direction(starting_direction)
            new_x,new_y = self.process_direction(x, y, new_direction)
            self.path_info[new_x][new_y] = "-"
            
            starting_direction = new_direction
            x = new_x
            y = new_y


    def init_maze(self, width, height):
        """Initialises the mazes path_info dictionary."""

        for x in range(0, width):
            self.path_info[x] = dict()
    
    
    def get_new_direction(self, previous_direction):
        """Attempt to get a new direction. New direction will be at 90 degrees
        to previous direction."""
        change = (random.randint(0, 100)/100.0) < self._CHANGE_PROBABILITY
        if not change:
            return previous_direction
        else:
            new_directions = ["U","D"]
            if (previous_direction == "U" or previous_direction == "D"):
                new_directions = ["L","R"]
                
            direction = new_directions[random.randint(0,1)]
            return direction

    def process_direction(self, x, y, direction):
        new_x, new_y = x, y
        if direction == "U":
            new_y = max(0, y-1)
        elif direction == "D":
            new_y = min(self.height - 1, y + 1)
        elif direction == "L":
            new_x = max(0, x-1)
        elif direction == "R":
            new_x = min(self.width - 1, x + 1)
        
        return new_x,new_y
    
    def draw_text_map(self, width, height):
        for y in range(0, height):
            line = ""
            for x in range(0, width):
                if (self.path_info[x].has_key(y)):
                    line += self.path_info[x][y] + " "
                else:
                    line += "X "
            print line

    def draw_graphical_map(self):
        width = 1600
        height = 900
        maze_view = MazeView(width,height)
        maze_view.parse_map(self.path_info, self.width, self.height)