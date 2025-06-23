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

class FileNameState(GameState):
    """State for entering the filename"""
    def __init__(self, game):
        super().__init__(game)
        self.filename = ""
    
    def handle_keydown(self, event):
        if event.key == pygame.K_RETURN and self.filename.strip():
            # Move to question input state
            self.game.change_state(QuestionInputState(self.game, self.filename.strip()))
        elif event.key == pygame.K_BACKSPACE:
            self.filename = self.filename[:-1]
        elif event.key == pygame.K_ESCAPE:
            return False  # Quit
        else:
            self.filename += event.unicode
        return True
    
    def render(self):
        self.game.draw_text("Enter filename (e.g. quiz.txt):", 40, 50, 
                           self.game.large_font, self.game.WHITE)
        self.game.draw_text(self.filename, 40, 100, self.game.font, self.game.BLUE)


class QuestionInputState(GameState):
    """State for inputting question and answers"""
    def __init__(self, game, filename):
        super().__init__(game)
        self.filename = filename
        self.labels = ["Question", "a)", "b)", "c)", "d)", "Correct Answer (a/b/c/d)"]
        self.inputs = [""] * len(self.labels)
        self.current_input = 0
    
    def handle_keydown(self, event):
        if event.key == pygame.K_RETURN:
            if self._validate_inputs():
                self._save_question()
                self.game.change_state(SavedMessageState(self.game, self.filename))
            else:
                print("Please fill all fields and enter a valid correct answer (a/b/c/d).")
        elif event.key == pygame.K_TAB:
            self.current_input = (self.current_input + 1) % len(self.inputs)
        elif event.key == pygame.K_BACKSPACE:
            self.inputs[self.current_input] = self.inputs[self.current_input][:-1]
        elif event.key == pygame.K_ESCAPE:
            return False  # Quit
        else:
            self.inputs[self.current_input] += event.unicode
        return True

    def _validate_inputs(self):
        """Validate that all inputs are filled and correct answer is valid"""
        return (all(self.inputs) and 
                self.inputs[5].lower() in ['a', 'b', 'c', 'd'])
    
    def _save_question(self):
        """Save the question to file"""
        QuestionSaver.save_question(self.filename, self.inputs)
    
    def render(self):
        self.game.draw_text("Enter your question and answers:", 40, 30, 
                           self.game.large_font, self.game.WHITE)
        
        for i, label in enumerate(self.labels):
            color = self.game.BLUE if i == self.current_input else self.game.WHITE
            self.game.draw_text(f"{label} {self.inputs[i]}", 40, 80 + i * 50, 
                               self.game.font, color)
        
        self.game.draw_text("ENTER = Save | TAB = Next | ESC = Quit", 40, 440, 
                           self.game.font, self.game.WHITE)


class SavedMessageState(GameState):
    """State showing saved message and asking for another question"""
    def __init__(self, game, filename):
        super().__init__(game)
        self.filename = filename
    
    def handle_keydown(self, event):
        if event.key == pygame.K_y:
            # Add another question
            self.game.change_state(QuestionInputState(self.game, self.filename))
        elif event.key == pygame.K_n:
            return False  # Quit
        return True
    
    def render(self):
        self.game.draw_text("Saved! Add another? (y/n)", 40, 500, 
                           self.game.large_font, self.game.WHITE)
        

class QuestionSaver:
    """Utility class for saving questions to file"""
    @staticmethod
    def save_question(filename, data):
        """Save a question and its answers to the specified file"""
        try:
            with open(filename, "a") as file:
                file.write("::QUESTION::\n")
                file.write(data[0] + "\n")
                file.write("a) " + data[1] + "\n")
                file.write("b) " + data[2] + "\n")
                file.write("c) " + data[3] + "\n")
                file.write("d) " + data[4] + "\n")
                file.write("ANSWER: " + data[5].lower() + "\n")
                file.write("::END::\n\n")
        except IOError as e:
            print(f"Error saving question: {e}")


def main():
    """Entry point of the application"""
    quiz_maker = QuizMaker()
    quiz_maker.run()


if __name__ == "__main__":
    main()