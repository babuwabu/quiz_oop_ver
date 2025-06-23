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
        
    def _load_resources(self):
        """Load all game resources"""
        try:
            # Load and play background music
            pygame.mixer.music.load("02. Title Theme.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            
            # Load background image
            self.bg_image = pygame.image.load("pixel forest.jpg")
            self.bg_image = pygame.transform.scale(self.bg_image, (self.WIDTH, self.HEIGHT))
            
            # Load fonts
            self.font = pygame.font.Font("PressStart2P-Regular.ttf", 18)
            self.large_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load resource - {e}")
            # Fallback to default font if custom font fails
            self.font = pygame.font.Font(None, 18)
            self.large_font = pygame.font.Font(None, 24)

