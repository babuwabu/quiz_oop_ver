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

    def draw_text(self, text, x, y, font, color=None):
        """Draw text on screen"""
        if color is None:
            color = self.BLACK
        text_surf = font.render(text, True, color)
        self.screen.blit(text_surf, (x, y))

    def change_state(self, new_state):
        """Change the current application state"""
        self.state = new_state

    def run(self):
        """Main game loop"""
        running = True
        while running:
            # Clear screen with background
            self.screen.blit(self.bg_image, (0, 0))
            
            # Handle events and update current state
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.state.handle_keydown(event):
                        running = False
            
            # Render current state
            self.state.render()
            
            pygame.display.flip()
            self.clock.tick(30)
        
        self.quit()

    def quit(self):
        """Clean up and quit"""
        pygame.quit()
        sys.exit()


class GameState:
    """Base class for all game states"""
    def __init__(self, game):
        self.game = game
    
    def handle_keydown(self, event):
        """Handle keydown events. Return False to quit the game."""
        return True
    
    def render(self):
        """Render the current state"""
        pass

