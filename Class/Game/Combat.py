import random
import math


class Combat:
    def __init__(self, game, player_pokemons, enemy_pokemon):
        self.game = game  # Game object
        self.__player_pokemon = player_pokemons[0]  # Pokemon object
        self.__enemy_pokemon = enemy_pokemon  # Enemy object
        self.__run_attempt = 0  # take note of the number of run attempt

        # Check who attack first
        self.attacker = self.check_who_attack_first()

        # self.turn()  # start the combat

    # ATTACK METHOD (return the damage)
    def attack(self, lvl, attack, attack_spe, attack_type, attack_category, power, enemy_defence, enemy_sp_defence, enemy_type):  # lvl(int), attack(int), attack_spe(int), attack_type(str), attack_category(str), power(int), enemy_defence(int), enemy_sp_defence(int), enemy_type(list)
        # check if the attack is effective (in multiple type of enemy)
        effectiveness = 1
        for ty in enemy_type:
            type_lower = ty.lower()
            effectiveness *= self.game.SETTINGS.type_chart[attack_type][type_lower]

        if attack_category == "physical":
            return math.floor(((((((2 * lvl / 5) + 2) * attack * power / enemy_defence) / 50 + 2) * effectiveness) * random.randint(217, 255)) / 255)  # physical attack
        elif attack_category == "special":
            return math.floor(((((((2 * lvl / 5) + 2) * attack_spe * power / enemy_sp_defence) / 50 + 2) * effectiveness) * random.randint(217, 255)) / 255)  # special attack
        else:
            return 0
            # TODO: STATUS ATTACK (ex: poison, sleep, etc...)

    # TURN METHOD (manage the turn)
    def turn(self):

        # ask the player what he want to do
        if self.attacker == self.__player_pokemon:
            print("What do you want to do ?")
            print("1. Attack")
            print("2. Switch")
            print("3. Bag")
            print("4. Run")
            choice = input("")

            # choice 1: attack | TODO: (ONLY FOR TEST IN TERMINAL - NOT FOR GUI VERSION DON'T FORGET TO REMOVE IT)
            if choice == "1":
                print("Which attack do you want to use ?")
                for i in range(0, len(self.__player_pokemon.get_moves())):
                    print(str(i + 1) + ". " + self.__player_pokemon.get_moves()[i]["name"])
                choice = input("")

                # Check if the choice is valid
                if choice.isdigit() and 0 < int(choice) <= len(self.__player_pokemon.get_moves()):
                    # Make the player attack
                    damage = self.attack(self.__player_pokemon.get_lvl(), self.__player_pokemon.get_attack(), self.__player_pokemon.get_sp_attack(),
                                         self.__player_pokemon.get_moves()[int(choice) - 1]["type"], self.__player_pokemon.get_moves()[int(choice) - 1]["category"], self.__player_pokemon.get_moves()[int(choice) - 1]["power"],
                                         self.__enemy_pokemon.get_defense(), self.__enemy_pokemon.get_sp_defense(), self.__enemy_pokemon.get_type())
                    self.__enemy_pokemon.take_damage(damage)
                    print(self.__player_pokemon.get_name() + " use " + self.__player_pokemon.get_moves()[int(choice) - 1]["name"] + " and deal " + str(damage) + " damage")
                    print(self.__enemy_pokemon.get_name() + " have " + str(self.__enemy_pokemon.get_hp()) + " hp left")
                else:
                    choice = None
                    self.turn()

            # choice 2: switch | TODO: (ONLY FOR TEST IN TERMINAL - NOT FOR GUI VERSION DON'T FORGET TO REMOVE IT)
            elif choice == "2":
                self.switch_pokemon()

            # choice 3: bag | TODO: (ONLY FOR TEST IN TERMINAL - NOT FOR GUI VERSION DON'T FORGET TO REMOVE IT)
            elif choice == "3":
                print("Bag")

            # choice 4: run | TODO: (ONLY FOR TEST IN TERMINAL - NOT FOR GUI VERSION DON'T FORGET TO REMOVE IT)
            elif choice == "4":
                if self.run():
                    # stop the combat
                    return
                else:
                    pass

            # check if the enemy is dead (if yes, end the combat else next turn)
            if self.__enemy_pokemon.is_alive():
                if self.attacker == self.__player_pokemon:
                    self.attacker = self.__enemy_pokemon
                else:
                    self.attacker = self.__player_pokemon
                self.turn()
            else:
                self.win()

        # Make the enemy attack
        else:
            print("Enemy turn")
            # make the enemy choose a random attack
            choice = random.randint(0, len(self.__enemy_pokemon.get_moves()) - 1)
            # Make the enemy attack
            damage = self.attack(self.__enemy_pokemon.get_lvl(), self.__enemy_pokemon.get_attack(), self.__enemy_pokemon.get_sp_attack(),
                                 self.__enemy_pokemon.get_moves()[choice]["type"], self.__enemy_pokemon.get_moves()[choice]["category"], self.__enemy_pokemon.get_moves()[choice]["power"],
                                 self.__player_pokemon.get_defense(), self.__player_pokemon.get_sp_defense(), self.__player_pokemon.get_type())
            self.__player_pokemon.take_damage(damage)
            print(self.__enemy_pokemon.get_name() + " use " + self.__enemy_pokemon.get_moves()[choice]["name"] + " and deal " + str(damage) + " damage")
            print(self.__player_pokemon.get_name() + " have " + str(self.__player_pokemon.get_hp()) + " hp left")

            # check if the player is dead (if yes, end the combat else next turn)
            if self.__player_pokemon.is_alive():
                if self.attacker == self.__player_pokemon:
                    self.attacker = self.__enemy_pokemon
                else:
                    self.attacker = self.__player_pokemon
                self.turn()
            else:
                print("You lose !")

    # check who attack first (player or enemy) and return the pokemon who attack first (random if same speed)
    def check_who_attack_first(self):
        if self.__player_pokemon.get_speed() > self.__enemy_pokemon.get_speed():
            return self.__player_pokemon
        elif self.__player_pokemon.get_speed() < self.__enemy_pokemon.get_speed():
            return self.__enemy_pokemon
        else:
            return random.choice([self.__player_pokemon, self.__enemy_pokemon])

    # Make the player choose a pokemon to switch
    def switch_pokemon(self):
        print("Which pokemon do you want to switch ?")
        for i in range(0, len(self.game.Player.get_pokemons())):
            print(str(i + 1) + ". " + self.game.Player.get_pokemons()[i].get_name())
        choice = input("")

        # Check if the choice is valid
        if choice.isdigit() and 0 < int(choice) <= len(self.game.Player.get_pokemons()):
            self.__player_pokemon = self.game.Player.get_pokemons()[int(choice) - 1]
            print("You switch to " + self.__player_pokemon.get_name())
        else:
            print("Invalid choice")
            self.switch_pokemon()

    # make player go out of combat (cant run if the enemy is a trainer)
    def run(self):
        ood_escape = (((self.__player_pokemon.get_speed() * 128) / self.__enemy_pokemon.get_speed()) + 30 * self.__run_attempt) % 256
        if ood_escape > random.randint(0, 255):
            print("You run away")
            return True
        else:
            print("You can't run away")
            self.__run_attempt += 1
            return False

    # function that calculate how much xp the player will get
    def calculate_xp(self):
        return math.floor(((self.__enemy_pokemon.get_lvl() * 2) + 10) / 250 * self.__enemy_pokemon.get_lvl()) + self.__enemy_pokemon.get_lvl() * 3

    # function that calculate how much money the player will get
    def calculate_money(self):
        return math.floor(self.__enemy_pokemon.get_lvl() * 1.5)

    # win the combat and give the player the reward
    def win(self):
        # give all players pokemon xp
        for pokemon in self.game.Player.get_pokemons():
            pokemon.add_xp(self.calculate_xp())
            pokemon.debug_all()

        # give the player money
        self.game.Player.add_money(self.calculate_money())

        print("You win !")
        print("You get " + str(self.calculate_xp()) + " xp and " + str(self.calculate_money()) + " money")

