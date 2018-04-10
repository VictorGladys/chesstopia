import pygame

class Game:
    def __init__(self, size):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Chesstopia")
        self.clock = pygame.time.Clock()
        self.isPlaying = True
        self.colors = {"w": (255, 255, 255), "r": (255, 0, 0)}

    def start(self):
        while(self.isPlaying):
            for event in pygame.event.get():    #a user gave input
                if event.type == pygame.QUIT:   # If user clicked close
                    self.isPlaying = False      # Flag that we are done so we exit this loop
            self.screen.fill(self.colors["w"])

            # The you can draw different shapes and lines or add text to your background stage.
            pygame.draw.rect(self.screen, self.colors["r"], [55, 200, 100, 70], 0)

            # draw
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self.clock.tick(60)

    def quit(self):
        pygame.quit()

def main():
    game = Game((700,500))
    game.start()
    game.quit()

if __name__ == "__main__":
    main()
