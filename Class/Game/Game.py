from Pokemon import Pokemon  # Pokemon class
from Combat import Combat  # Combat class
from Player import Player  # Player class
from Settings import *  # Settings class


class Game:
    def __init__(self):
        # Init pygame #
        pg.init()

        # Init settings #
        self.SETTINGS = Settings()  # Settings class

        # init screen #
        pg.display.set_caption("Pokemon")
        self.screen = pg.display.set_mode(self.SETTINGS.WIN_RES)
        self.clock = pg.time.Clock()

        # Init classes #
        self.GAME = self  # Game class
        self.COLORS = Colors()  # Colors class
        self.SPRITES = Sprites()  # Sprites class
        self.GENERATE = Generate()  # Generate class
        self.Player = Player()  # Player class

        # Debug #
        self.Debug()

        # Game variables #
        self.game_state = "combat"  # Game state (menu, combat, etc)
        self.menu_state = "main"  # Menu state (main, pokemon, etc)
        self.COMBAT = None  # Combat class

    # Start combat function #
    def start_combat(self, pokemon, enemy):
        self.COMBAT = Combat(self.GAME, pokemon, enemy)

    # Debug function (for testing) don't forget to remove it before release #
    def Debug(self):

        print("Debug")

        # Debug Add pokemon
        self.Player.add_pokemons(Pokemon(self, 25, self.GENERATE.generate_IV(), 20, self.GENERATE.generate_nature(), 5, [35, 6], False))
        # self.Player.add_pokemons(Pokemon(self, 5, self.GENERATE.generate_IV(), 1, self.GENERATE.generate_nature(), 1, [1, 3, 6, 4], True))

        # Debug Level up pokemon
        # for i in range(1, 10):
        #     self.Player.get_pokemons()[0].level_up()

        # Debug Combat
        self.start_combat(self.Player.get_pokemons(), Pokemon(self, 2, self.GENERATE.generate_IV(), 1, self.GENERATE.generate_nature(), 5, [1], False))

    # Pygame Draw function #
    def draw(self):

        # Background #
        self.screen.blit(self.SPRITES.back_ground, (0, 0))

        # pokemon DEBUG DRAW | TODO: delete this #
        self.screen.blit(self.SPRITES.get_pokemon_sprite(4, "front"), (800, 70))
        self.screen.blit(self.SPRITES.get_pokemon_sprite(15, "back"), (250, 275))

        # Field #
        self.screen.blit(self.SPRITES.enemy_pokemon_status, (80, 50))
        self.screen.blit(self.SPRITES.player_pokemon_status, (720, 345))

        # Bottom UI #
        self.screen.blit(self.SPRITES.bottom_message_box, (0, 500))
        self.screen.blit(self.SPRITES.choice_box, (680, 500))
        self.screen.blit(self.SPRITES.choice_arrow, (715, 555))





        pg.display.flip()
        pg.display.update()

    # GAME LOOP #
    def run(self):
        while True:
            self.clock.tick(self.SETTINGS.FPS)
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()


# Create the game instance #
game = Game()
game.run()

