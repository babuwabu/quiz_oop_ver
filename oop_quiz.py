import pygame
import sys


class QuizMaker:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Constants
        self.WIDTH = 800
        self.HEIGHT = 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (70, 150, 255)
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Lulu's Quiz Maker")
        self.clock = pygame.time.Clock()
        
        # Load resources
        self._load_resources()
        
        # Initialize state
        self.state = FileNameState(self)
        