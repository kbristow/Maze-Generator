from game import *
class MazeView (Game):
    """Main Game object that will contain the procedural maze visualisation"""
    
    def parse_map(self, maze, width, height):
        """Parses a text maze of given width and height.

        Args:
            maze: A dictionary of all the locations in the maze and what
                type of maze element is at the location. TODO: Probably should
                not be a dictionary.
            width: Maximum possible x location. Necessary because not all
                locations in the dictionary are populated.
            height: Maximum possible y location. Ditto reason for width.
        """
        tile_width = self.screen_width/width
        tile_height = self.screen_height/height
        for i in range(0, height):
            for j in range(0, width):
                if not maze[j].has_key(i):
                    tile = MazeTile(self)
                    tile.initialise()
                    tile.set_size(tile_width, tile_height)
                    tile.set_position((j*tile_width,i*tile_height))
                    self.add(tile)
                
        self.run()


class MazeTile (GameObject):
    """GameObject definition for an individual maze tile or wall."""

    def initialise(self):
        """Sets the image for the GameObject."""
        self.set_image("wall.png")
        return self
        
