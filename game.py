import pygame, sys
from pygame.locals import *

class Game ():
    """A basic game template which can be extended for quick and simple game
    creation.
 
    The game template provides simple mechanisms for creating, controlling
    and deleting GameObject's. This could be improved to add more complex
    features if necessary.

    Attributes:
        game_objects: list of all GameObject's in the scene
        game_objects_for_removal: list of all GameObject's that will be
            removed at the end of the step.
        game_objects_for_adding: list of all GameObject's that will be added
            at the end of the step.
        sprite_group: contains all GameObject's that need to be drawn in the scene.
        FPS: how many frames per second the game should run at.
        clock: the game clock.
        screen: instance of pygame display.
        running: whether the game is in progress or not.
        screen_width: width dimension of the screen.
        screen_height: height dimension of the screen.
    """
    game_objects = []
    game_objects_for_removal = []
    game_objects_for_adding = []
    sprite_group = pygame.sprite.RenderPlain(game_objects)
    FPS = 30
    clock = None
    screen = None
    running = True
    screen_width = 0
    screen_height = 0

    def __init__ (self, width, height):
        """Initialise a Game object with the given screen dimensions"""

        self.screen_width = width
        self.screen_height = height
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        self.initialise()

    def initialise(self):
        """Objects that inherit from Game should override this to 
        initialise the scene.
        """
        return

    def run (self):
        """Starts the main game loop. The loop runs an update for
        all GameObject's then draws all visible GameObject's
        """

        while self.running:
            delta_time = self.clock.tick(self.FPS)
            self.update(delta_time)
            self.draw()
            for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_ESCAPE:
                    self.running=False # quit the game

        pygame.quit()#Better method than just sys.exit
        sys.exit()

    def update(self, dT):
        """All GameObject logical GameObject's in the scene will have
        their update function called in this step. All GameObject's
        that should be removed are then removed. All GameObject's that
        should be added are added.

        Args:
            dT: The delta time between the last frame and this one.
        """
        
        for game_obj in self.game_objects:
            game_obj.update(dT)

        for game_obj in self.game_objects_for_removal:
            self.game_objects.remove(game_obj)

        for game_obj in self.game_objects_for_adding:
            self.game_objects.append(game_obj)

        self.game_objects_for_removal = []
        self.game_objects_for_adding = []

    def draw(self):
        """Draws all the visible GameObject's, I.E. those in the sprite_group
        list.
        """

        self.screen.fill((0,0,0))
        self.sprite_group.draw(self.screen)
        pygame.display.flip()

    def remove(self, game_obj):
        """Add the given GameObject to the list for scene deletion."""
        self.game_objects_for_removal.append(game_obj)

    def add(self, game_obj):
        """Add the given GameObject to the list for scene addition."""
        self.game_objects_for_adding.append(game_obj)

    def add_drawable(self, gameObject):
        """Add a GameObject to the list for GameObject's that need
        to be drawn.
        """
        if not self.sprite_group.has(gameObject):
            self.sprite_group.add(gameObject)

        
class GameObject(pygame.sprite.Sprite):
    """The main class used to create actors in a Game scene.

    Acts as a wrapper around the pygame Sprite class that can
    be inherited from to attach logic to Sprite objects in the scene.

    Attributes:
        game_ref: a reference to the Game objects that the GameObject is
            contained in.
        modules: list containing references to functions that the user wishes
            to act upon the GameObject in the update function call.
        current_delta_time: holds the current delta time so that module
            functions can access it if they require.
        drawable: should the GameObject be drawn
    """

    game_ref = None

    modules = []

    current_delta_time = 0

    drawable = True

    def __init__ (self, game):
        """Initialise the GameObject with the given Game as its parent."""

        pygame.sprite.Sprite.__init__(self)
        self.game_ref = game
        self.initialise()

    def initialise(self):
        """Should be overriden in children classes to initialise themselves."""
        return
    
    def update(self, dT):
        """Will run all the module functions in the modules list. The module
        functions should update the GameObject's postion/velocity/rotation/etc.

        Args:
            dT: the delta time between the last frame and the current one.
        """

        current_delta_time = dT
        for module in self.modules:
            module(self)


    def remove(self):
        """Will queue the GameObject to be removed from the Game."""
        game_ref.remove(self)

    def set_image(self, image_URL, bkg = None):
        """Sets the image for the GameObject.

        Args:
            image_URL: url to the image file.
            bkg: the background transparency colour for the image. The default
                is white.
        """

        self.image = self.image = pygame.image.load(image_URL).convert()
        if not bkg == None:
            # Set our transparent color
            self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        if self.drawable:
            self.set_drawable()

    def set_position(self, position):
        """Set the x,y position of the GameObject.

        Args:
            position: a 2 element tuple in the form (x,y)
        """

        self.position = position
        if (self.rect):
            self.rect.x = position[0]
            self.rect.y = position[1]

    def set_drawable(self, do_draw = True):
        """If do_draw is True, the GameObject will be added to the list of
        GameObject's that must be drawn in the scene. TODO: do_draw=False
        should remove the GameObject from the drawable scene objects list.
        """

        self.drawable = do_draw
        if do_draw == True:
            self.game_ref.add_drawable(self)

    def set_size(self, width, height):
        """Scale the GameObject's image to a given width and height."""
        
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        
