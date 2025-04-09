import random
import os
import time
import itertools
import select
import sys
class Weapon:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
class Shop_Item:
    def __init__(self, name, price, gems):
        self.name = name
        self.price = price
        self.gems = gems
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    def is_red(self):
        return self.suit in ["Hearts", "Diamonds"]
    
    def is_black(self):
        return self.suit in ["Clubs", "Spades"]
    
    def is_special(self):
        return self.rank in ["Jack", "Queen", "King"]
class Deck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)
        
    def draw_card(self):
        return self.cards.pop()
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        
    def add_card(self, card):
        self.cards.append(card)
        self.value += self.get_card_value(card)
        
    def get_card_value(self, card):
        if card.rank in ["Jack", "Queen", "King"]:
            return 10
        elif card.rank == "Ace":
            return 11
        else:
            return int(card.rank)
        
    def adjust_for_ace(self):
        for card in self.cards:
            if card.rank == "Ace" and self.value > 21:
                self.value -= 10

class Player:
    def __init__(self, name, weapons):
        self.name = name
        self.health = 100
        self.stamina = 100
        self.weapons = weapons
        self.selected_weapon = None
        self.last_attack_used = None
        self.damage_reduction = 0
        self.charge = False
        self.charged = False
        self.armour = 0
        self.armour_turn = -1
        self.bleeding = False
        self.next_attack_does_no_damage = False
        self.venom = False
        self.venom_turns = 0
        self.poison_turns = 0
        self.drowsy = False
        self.confusion = False
        self.confusion_turns = 0
        self.boomerang_hammer = False
        self.small_bleeding = False
        self.royal_guards_summoned = False
        self.sacred_sacrifice_turns = 0
        self.the_force = False
        self.the_force_turns = 0
        self.focus_energy_power = False
        self.paralysed = False
        self.electric_shower = False
        self.assassination_mode = False
        self.assassination_mode_turns = 0
        self.hand = Hand()
        self.is_bust = False
        self.card_throw = False
        self.jokercardpower = False
        self.jokercardpowerloseturn = False
        self.jokercardpowerturn = 0
        self.jokerdamage = 0
        self.machine_gun_reload = 0
        self.flashstun = False
        self.secondaryultimate = False
        self.mirror_move = False
        self.burned = False
        self.traps_placed = 0
        self.charging_blow_turn = 0
        self.undying_will = False
        self.rage = False
        self.become_rage = 0
        self.grounded = False
        self.daggers = 0
        self.big_dagger = 0
        self.dagger_pull = 0
        self.spear_stun = 0
        self.grounded_turn = 0
        self.earthquake_attack = False
        self.double_lightsaber_turns = 0
        self.double_lightsaber = False
        self.overdosetwo = False
        self.overdosethree = False
        self.poison = False
        self.poison_drug_turns = 0
        self.overdose_turn = False
        self.medium_bleeding = False
        self.nuke_turns = 0
        self.shadow_energy = False
        self.combo = 0
        self.previouscombo = 0
        self.previous_icicle_stack = 0
        self.shadow = False
        self.shuriken_assassination = False
        self.shuriken_assassination_turns = 0
        self.current_health = 100
        self.shadow_kill = False
        self.smokebombactivation = False
        self.smokebomb = 1
        self.smokebombspecialactivation = False
        self.smokebombturns = 0
        self.fiveleafcloverult = False
        self.tastetherainbowconstantdamage = False
        self.tastetherainbowturns = 0
        self.goldenpotdamage = 0
        self.ultimate_move = False
        self.shotgunpassive = False
        self.shotgunpassiveturns = 0
        self.thebushes = False
        self.amount_of_slaves = 0
        self.fields = False
        self.slavingpower = 0
        self.suffering = False
        self.successfulharrass = False
        self.fieldsturns = 0
        self.special_hammer = False
        self.constantspin = False
        self.constant_spin_turns = 0
        self.no_damage_reduction = False
        self.slippery_fields_turns1 = False
        self.slippery_fields_turns2 = False
        self.frostbite_counter = 0
        self.icicle_storm_stack = 0
        self.icicle_storm_damage = False
        self.frostbite_heal = False
        self.hyperthermia = False
        self.power_usage = 100
        self.power_restriction = False
        self.lord_used = False
        self.chained = False
        self.punishment = False
        self.angelic_aid = 1
        self.melee = ["Red LightSaber", "Berserker Axe", "Sword", "Hammer", "Electric Axe", "Big Sledgehammer", "Spear", "C10H15N"]

    def add_weapon(self, weapon):
        self.weapons.append(weapon)
        
    def select_starting_weapon(self):
        while True:
            for i, weapon in enumerate(self.weapons):
                print(f"{i+1}. {weapon.name}")
            try:
                weapon_choice = int(input()) - 1
                if weapon_choice < len(self.weapons):
                    self.selected_weapon = self.weapons.pop(weapon_choice)
                    print(f"{self.name} selected {self.selected_weapon.name}.")
                    return
                else:
                    print("Invalid choice. Please choose again.")
            except ValueError:
                print("Error: Invalid input. Please enter a number.")
    def __repr__(self):
        return f"{self.name}: {self.hand.cards}, Value: {self.hand.value}"
    def display_hand(self):
        print(f"{self.name}'s Hand:")
        for card in self.hand.cards:
            print(f"\t{card}")
        print(f"Total Value: {self.hand.value}")
    
    def clear_display(self):
        os.system('cls||clear')
        
    def play_card_turn(self, deck):
        while True:
            action = input(f"{self.name}, do you want to hit or stand? ")
            if action.lower() == "hit":
                self.hand.add_card(deck.draw_card())
                print(self)
                if self.hand.value > 21:
                    print(f"{self.name} busts!")
                    self.is_bust = True
                    break
            elif action.lower() == "stand":
                break
            else:
                print("Invalid input. Please try again.")
                
    def is_key_pressed(self):
      # Check if a key is pressed
      return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    def clear_line(self, length):
      sys.stdout.write('\r' + ' ' * length + '\r')
      sys.stdout.flush()

    def calculate_damage(self, last_number):
      base_damage = 30
      return base_damage - abs(5 - last_number) * 3

    def super_sniper_attack(self, other_player):
      numbers = itertools.cycle(range(1, 11))  
      last_number = 0
      stop_flag = False

      while not stop_flag:
          for i in range(10):
              last_number = next(numbers)

              sys.stdout.write(f"{last_number} ")
              sys.stdout.flush()

              time.sleep(0.05)
              self.clear_line(len(str(last_number)))  # Clear the last printed number

              if self.is_key_pressed():
                  user_input = sys.stdin.read(1).lower()
                  if user_input == 's':
                      stop_flag = True
                      break

          if last_number == 10:
              countdown_number = 9
              while countdown_number > 0 and not stop_flag:
                  sys.stdout.write(f"{countdown_number} ")
                  sys.stdout.flush()
                  time.sleep(0.05)
                  self.clear_line(len(str(countdown_number)))  # Clear the last printed countdown number
                  countdown_number -= 1

                  # Display the last number when 's' is pressed
                  if self.is_key_pressed():
                      user_input = sys.stdin.read(1).lower()
                      if user_input == 's':
                          stop_flag = True
                          last_number = countdown_number + 1
                          break

      print(f"\nLast number generated: {last_number}")
      damage = self.calculate_damage(last_number)
      print(f"Damage: {damage}")
      other_player.health -= damage
      print(f"{other_player.name} took {damage} damage!")
        
    def play_turn(self, other_player):
        shop_items = [
          Shop_Item("Money Per Turn Buff", 30, 0),
        ]
        special_shop_items = [
          Shop_Item("Punch Attack", 0, 5),
          Shop_Item("Kick Attack", 0, 5),
          Shop_Item("Sniper Attack", 0, 13),
          Shop_Item("Nuke", 0, 20)
        ]
        other_player.shadow_kill = False
        other_player.current_health = other_player.health
        other_player.next_attack_does_no_damage = False
        if self.selected_weapon is None:
            self.choose_weapon()
        if self.selected_weapon.name == "Sniper":
            self.stamina += 15
            if self.stamina > 100:
                self.stamina = 100
            print(f"Stamina: {self.stamina}")
        if self.selected_weapon.name == "Ice Wand":
          print(f"Icicle Storm Stack:{self.icicle_storm_stack}")
        if self.icicle_storm_stack <= self.previous_icicle_stack:
            self.icicle_storm_stack = 0
        self.previous_icicle_stack = self.icicle_storm_stack
        if self.combo <= self.previouscombo:
            self.combo = 0
        if self.selected_weapon.name == "Shuriken":
            print(f"Combo: {self.combo}")
        if self.selected_weapon.name == "Whip":
            print(f"Slaving Power: {self.slavingpower}")
        if self.shotgunpassive:
            self.shotgunpassive = False
            self.shotgunpassiveturns -= 3
        if self.selected_weapon.name == "Shotgun":
            self.shotgunpassiveturns += 1
        if self.shotgunpassiveturns >= 3:
            self.shotgunpassive = True
        self.previouscombo = self.combo
        if self.ultimate_move and self.fiveleafcloverult:
          self.ultimate_move = False
          self.fiveleafcloverult = False
        if self.selected_weapon.name == "Dagger" or "Assassination Dagger":
            self.dagger_pull += 1
        if self.selected_weapon.name == "Spear":
            self.spear_stun += 1
        if game.slippery_fields1 and self.name in ['Player 1(W1)','Player 1(W2)','Player 1(W3)', 'Player 1(W4)', 'Player 1(W5)']:
            self.slippery_fields_turns1 += 1
        if game.slippery_fields2 and self.name in ['Player 2(W1)','Player 2(W2)','Player 2(W3)', 'Player 2(W4)', 'Player 2(W5)']:
            self.slippery_fields_turns2 +=1
        if self.selected_weapon.name == "Red LightSaber" and not self.double_lightsaber:
            self.double_lightsaber_turns += 1
        if self.double_lightsaber_turns >= 7 and not self.double_lightsaber:
            self.double_lightsaber = True
            print(f"{self.name} entered double lightsaber mode")
        if self.frostbite_counter >= 1 and not self.frostbite_heal:
            self.frostbite_heal = True
            print(f"{self.name} is suffering from frostbite! {self.name} cannot heal up!")
        if self.frostbite_counter >= 5 and not self.hyperthermia:
            self.hyperthermia = True
            print(f"{self.name} is suffering from hyperthermia!")
        if self.power_usage < 15 and self.power_usage > -1:
            self.lord_used = True
            print("The Lord used all their power!")
            self.power_usage = -1
        if self.sacred_sacrifice_turns >= 2 and not self.lord_used:
            print(f"Lord Power: {self.power_usage}")
            lord_choice = input('The lord has responded to your sacrifice! What shall the lord do for you?(1. Holy Smite)PU:15 (2. Seraphic Punishment)PU:40 (3. Angelic Aid)PU:20 *Please enter NUMBER\n')
            if lord_choice == "1":
                damage = (4 * self.sacred_sacrifice_turns)
                other_player.health -= damage
                print(f"The lord used holy smite, dealing {damage} damage to {other_player.name}! This attack consumed 15% of the lord's power!")
                self.power_usage -= 15
                print(f"Lord Power: {self.power_usage}")
            elif lord_choice == "2":
                if self.punishment:
                    print("You already punished the opponent!")
                else:
                    lord_punishment = input(f'How should the lord punish {other_player.name}?(1. The Fields) (2. Power Restriction) (3. Chained Up)*Please enter NUMBER')
                    if lord_punishment == "1":
                        other_player.fields = True
                        print("The Lord sent the opponent to the fields to farm!")
                    if lord_punishment == "2":
                        other_player.power_restriction = True
                        print(f"The Lord restricted {other_player.name}'s power!")
                    if lord_punishment == "3":
                        other_player.selected_weapon.speed = 0
                        other_player.chained = True
                        print(f"The Lord chained up {other_player.name}, causing their speed to be 0! They will also take damage every turn!")
                    self.punishment = True
                    self.power_usage -= 40
                    print(f"Lord Power: {self.power_usage}")
            elif lord_choice == "2" and not self.power_usage < 40:
                print("The Lord doesn't have enough power for this attack!")
            elif lord_choice == "3":
                self.angelic_aid += 1
                print(f"The lord used angelic aid, causing an angel to strenghen {self.name}'s attacks and heal!")
                self.power_usage -= 20
                print(f"Lord Power: {self.power_usage}")
            elif lord_choice == "3" and not self.power_usage < 20:
                print("The Lord doesn't have enough power for this attack!")
        if self.boomerang_hammer:
            damage = random.randint(5, 8)
            self.health -= damage
            print(f"The {other_player.selected_weapon.name} comes back towards {other_player.name}, dealing {damage} damage!")
            self.boomerang_hammer = False
        if self.bleeding and not other_player.health <= 0:
            print(f"{self.name} takes 15 damage from bleeding!")
            damage = 15
            self.health -= damage
        if self.small_bleeding and not other_player.health <= 0:
            damage = 3
            self.health -= damage
            print(f"{self.name} takes {damage} damage from bleeding!")
        if self.medium_bleeding and not other_player.health <= 0:
            damage = 6
            self.health -= damage
            print(f"{self.name} takes {damage} damage from bleeding!")
        if other_player.electric_shower:
            damage = random.randint(3, 5)
            self.health -= damage
            print(f"The electric shower dealt {damage} damage!")
        if self.chained:
            damage = random.randint(4, 6)
            self.health -= damage
            print(f"{self.name} is chained up! The chains deal {damage} damage!")
        if other_player.venom:
            if other_player.venom_turns < 1:
                damage = 1
                other_player.health -= damage
                print(f"{other_player.name} takes {damage} damage from poison!")
                other_player.venom_turns += 1
            else:
                damage = 2 ** other_player.poison_turns
                other_player.health -= damage
                other_player.poison_turns += 1
                print(f"{other_player.name} takes {damage} damage from poison!")
        if self.poison:
            self.poison_drug_turns += 1
            damage = 4 * self.poison_drug_turns - 2
            self.health -= damage
            print(f"{self.name} takes {damage} damage from the C10H15N's poison!")
        if self.jokercardpowerturn >= 1:
            self.jokercardpower = True
        if self.card_throw:
            if self.jokercardpower:
                damage = random.randint(2, 3) + 7 * self.jokerdamage
                other_player.health -= damage
                print(f"{self.name} threw 10 more cards and dealt {damage} damage!")
            else:
                damage = random.randint(2, 3)
                other_player.health -= damage
                print(f"{self.name} threw 2 more cards and dealt {damage} damage!")  
        if self.tastetherainbowconstantdamage and self.tastetherainbowturns <= 7:
            self.tastetherainbowturns += 1
            damage = self.tastetherainbowturns
            other_player.health -= damage
            print(f"{other_player.name} took {damage} damage from the constant damage of taste the rainbow!")
        if self.the_force and not self.the_force_turns >= 4:
            if self.focus_energy_power:
                damage = random.randint(12, 17)
            else:
                damage = random.randint(9, 16)
            other_player.health -= damage
            print(f"{self.name} used the force and dealt {damage} damage!")
            return
        if other_player.the_force and not other_player.the_force_turns >= 4:
            print(f"{self.name} can't move because of {other_player.name} used the force!")
            other_player.the_force_turns += 1
            return
        if self.the_force_turns >= 4:
            print(f"{self.name} stopped using the force!")
            self.ultimate_move = True
            self.the_force = False
            self.the_force_turns -= 4
            return
        if other_player.assassination_mode and other_player.assassination_mode_turns > 2:
            print(f"{other_player.name} is no longer invisible!")
            other_player.assassination_mode = False
            other_player.assassination_mode_turns -= 3
            if other_player.special_hammer:
                other_player.selected_weapon.name = "Hammer"
            else:
                other_player.selected_weapon.name = "Dagger"
        if other_player.assassination_mode:
            print(f"{self.name} can't find {other_player.name} since they are invisible!")
            other_player.assassination_mode_turns += 1
            return
        if self.fields:
            self.fieldsturns += 1
        if self.fieldsturns < 6 and self.fields and not other_player.frostbite_heal:
            print(f"{self.name} is working in the fields!")
            heal = random.randint(2, 4)
            totalheal = heal + other_player.slavingpower + (2 * self.sacred_sacrifice_turns) // 2
            other_player.health += totalheal
            if other_player.health > 100:
                other_player.health = 100
            print(f"{self.name} farmed for {other_player.name} and helped them heal {totalheal} health!")
            if self.suffering:
                damage = random.randint(5, 7)
                self.health -= damage
                print(f"{self.name} is suffering from the whip and lost {damage} health!")
            if self.fieldsturns in [2, 4]:
                other_player.slavingpower += 1
                print(f"{self.name} is currently working too hard that they missed this turn!")
                return
        if self.fieldsturns >= 6:
            if other_player.selected_weapon.name in ["Whip", "Holy Bible"]:
                self.fields = False
                self.fieldsturns -= 6
        if self.lord_used:
            other_player.fields = False
        if self.jokercardpowerloseturn and self.jokercardpowerturn < 1:
            print(f"To perform the joker full power, {self.name} has to lose a turn!")
            self.jokercardpowerturn += 1
            return
        if not self.traps_placed == 0:
            damage = random.randint(8, 12)
            other_player.health -= damage
            print(f"{other_player.name} stepped into the trap! The trap dealt {damage} damage!")
            self.traps_placed -= 1
            print(f"Number of traps on the field: {self.traps_placed}")
        if self.hyperthermia:
            damage = self.frostbite_counter
            self.health -= damage
            print(f"{self.name} took {damage} damage due to hyperthermia!")
        if other_player.hyperthermia:
          damage = other_player.frostbite_counter
          other_player.health -= damage
          print(f"{other_player.name} took {damage} damage due to hyperthermia!")
        if other_player.slippery_fields_turns1 >= 6 and self.name in ['Player 2(W1)','Player 2(W2)','Player 2(W3)','Player 2(W4)','Player 2(W5)']:
          other_player.slippery_fields_turns1 -= 6
          print(f"{self.name} is frozen in the fields!")
          return
        if other_player.slippery_fields_turns2 >= 6 and self.name in ['Player 1(W1)','Player 1(W2)','Player 1(W3)','Player 1(W4)','Player 1(W5)']:
          other_player.slippery_fields_turns2 -= 6
          print(f"{self.name} is frozen in the fields!")
          return
        if other_player.shadow:
            print(f"{self.name} can't find {other_player.name}!")
            other_player.shadow = False
            other_player.shadow_kill = True
            return
        if self.drowsy:
            if random.randint(1, 10) <= 3:
                print(f"{self.name} was too drowsy and missed the attack! However, they shook the drowsiness off!")
                self.drowsy = False
                return
        if self.paralysed:
            if random.randint(1, 10) <= 2:
                print(f"{self.name} was paralysed and missed the attack!")
                return
        if other_player.spear_stun >= 4:
            self.flashstun = True
            other_player.spear_stun -= 4
            if self.frostbite_heal:
                heal = 0
            else:
                heal = random.randint(3, 5)
            other_player.health += heal
            print(f"{other_player.name} healed {heal} health because of the spear's passive!")
        if self.flashstun:
            print(f"{self.name} is stunned!")
            self.flashstun = False
            return
        if self.confusion:
            self.confusion_turns += 1
            if self.confusion_turns >= 2:
                print(f"{self.name} shook off their confusion!")
                self.confusion_turns -= 3
                self.confusion = False
            if random.randint(1, 10) < 3:
                damage = 5
                self.health -= damage
                print(f"{self.name} was confused and missed the attack, along with taking {damage} damage!")
                return
        if self.shuriken_assassination_turns >= 2:
            self.shuriken_assassination = False
        if self.shuriken_assassination and self.shuriken_assassination_turns < 2:
            if self.shuriken_assassination_turns == 0:
                damage = sum(random.randint(2, 3) for _ in range(5)) + self.combo
                self.combo += 5
                self.shuriken_assassination_turns += 1
                other_player.health -= damage
                print(f"{self.name} assasinated {other_player.name} and dealt {damage} damage!")
                return
            if self.shuriken_assassination_turns == 1:
                damage = sum(self.combo for _ in range(2))
                self.combo += 3
                self.shuriken_assassination_turns += 1
                other_player.health -= damage
                print(f"{self.name} used the finishing blow against {other_player.name} and dealt {damage} damage!")
                return
        if self.royal_guards_summoned:
            damage = 3 * random.randint(2, 6)
            other_player.health -= damage
            print(f"{self.name}'s royal guards dealt {damage} damage!")
        if self.selected_weapon.name == "Darts" and self.selected_weapon.speed > other_player.selected_weapon.speed:
            damage = random.randint(4, 6)
            other_player.health -= damage
            print(f"{other_player.name} lost {damage} from the Darts' passive!")
        if self.selected_weapon.name == "C10H15N":
            selfdamage = random.randint(2, 3)
            if not self.overdosetwo and not self.overdosethree and self.health > 0:
                damage = random.randint(6, 7)
                other_player.health -= damage
            else:
                damage = 0
            self.health -= selfdamage
            print(f"{self.name} took {selfdamage} damage, and {other_player.name} took {damage} damage from C10H15N's passive!")
        if self.selected_weapon.name == "C10H15N" and self.overdosetwo and self.health > 0:
            selfdamage = random.randint(8, 12)
            damage = random.randint(27, 33)
            self.health -= selfdamage
            other_player.health -= damage
            print(f"{self.name} took {selfdamage} damage, and {other_player.name} took {damage} damage from C10H15N's passive!")
        if self.health > 0 and self.selected_weapon.name == "Sword" and not self.frostbite_heal:
            heal = random.randint(5, 6)
            self.health += heal
            if self.health > 100:
                self.health = 100
            print(f"{self.name} healed {heal} health from the swords passive!")
        if other_player.selected_weapon.name == "Bomb" and not self.health < 0 and not other_player.health < 0:
            if self.name in ['Player 1(W1)','Player 1(W2)','Player 1(W3)','Player 1(W4)','Player 1(W5)']:
                damage = 1
                game.player1.health -= damage
                game.player3.health -= damage
                game.player5.health -= damage
                game.player7.health -= damage
                game.player9.health -= damage
                print(f"All of player 1's weapons took {damage} damage!")
                print("(passive)")
            elif self.name in ['Player 2(W1)','Player 2(W2)', 'Player 2(W3)', 'Player 2(W4)','Player 2(W5)']:
                damage = 1
                game.player2.health -= damage
                game.player4.health -= damage
                game.player6.health -= damage
                game.player8.health -= damage
                game.player10.health -= damage
                print(f"All of player 2's weapons took {damage} damage!")
                print("(passive)")
        if other_player.armour_turn < 3 and other_player.armour_turn >= 0:
            other_player.armour = 4
            other_player.armour_turn += 1
            if other_player.armour_turn >= 3:
                print(f"{other_player.name} regained their armour!")
                other_player.armour_turn = -1
                other_player.armour = 0
        if self.health <= 0 or other_player.health <= 0:
            return
        self.damage_reduction = 0
        self.attackopponent(other_player)
    def attackopponent(self, other_player):
        attacks = {}
        if self.selected_weapon.name == 'Hammer':
            attacks = {
                "Throw Hammer": self.throw_hammer_attack,
                "Spin Hammer": self.spin_hammer_attack,
                "Build": self.build
            }
        elif self.selected_weapon.name == 'Sword':
            attacks = {
                "Slash": self.slash_attack,
                "Charging blow": self.Charging_blow_attack,
                "Razor Wind": self.Razor_wind_attack
            }
        elif self.selected_weapon.name == 'Red LightSaber':
            attacks = {
                "Swing LightSaber": self.swing_attack,
                "Focus Energy": self.focus_energy,
                "The Force": self.the_force_attack,
            }
        elif self.selected_weapon.name == 'Bow':
            attacks = {
                "shoot": self.shoot_attack,
                "pierce": self.pierce_attack,
                "Bleeding arrow": self.bleeding_arrow_attack
            }
        elif self.selected_weapon.name == 'Sniper':
            attacks = {
                "Sniper shot": self.sniper_attack,
                "Da Bushes": self.the_bushes_effect,
                "Roll Back": self.roll_back_effect,
                "Brutality Training": self.brutality_training_attack
            }
        elif self.selected_weapon.name == 'Darts':
            attacks = {
                "Dart Attack": self.dart_attack,
                "Dart Flank": self.dart_flank_attack,
                "Poison Dart": self.poison_dart
            }
        elif self.selected_weapon.name == 'Holy Bible':
            attacks = {
                "Divine Judgment": self.divine_judgment_attack,
                "Sacred Sacrifice": self.sacred_sacrifice,
                "Consecreated Water": self.consecrated_water,
            }
        elif self.selected_weapon.name == 'Spear':
            attacks = {
                "Spear Slice": self.spear_slice_attack,
                "Spear Throw": self.spear_throw_attack,
                "Royal Guards": self.royal_guards,
            }
        elif self.selected_weapon.name == 'Electric Axe':
            attacks = {
                "Axe Throw": self.throw_hammer_attack,
                "Zap Attack": self.zap_attack,
                "Electric Arival": self.electric_arrival,
            }
        if self.selected_weapon.name == 'Dagger':
            attacks = {
                "Dagger Sharp Throw": self.sharp_throw_attack,
                "Dagger Multiple Throw": self.multiple_throw_attack,
                "Assassination": self.assassination,
            }
        elif self.selected_weapon.name == 'Assassination Dagger':
            attacks = {
                "Enhanced Dagger Sharp Throw": self.sharp_throw_attack,
                "Enhanced Dagger Multiple Throw": self.multiple_throw_attack,
                "Slicing Tornado": self.slicing_tornado_attack,
            }
        elif self.selected_weapon.name == 'Cards':
            attacks = {
                "Card throw attack": self.card_throw_attack,
                "Jokers Power": self.joker_power,
                "BJ Gamble": self.bj_gamble,
            }
        elif self.selected_weapon.name == 'Machine Gun':
            attacks = {
                "Shoot(1 round)": self.shoot_machine_gun_attack,
                "Reload": self.reload,
                "Hand Grenade": self.hand_grenade,
                "Rapid Fire": self.rapid_fire_attack,
            }
        elif self.selected_weapon.name == 'Mirror':
            attacks = {
                "Sun Reflect": self.sun_reflect_attack,
                "Glass Shard Attack": self.glass_shard_attack,
                "Reflect": self.reflect,
            }
        elif self.selected_weapon.name == 'Shotgun':
            attacks = {
                "Shotgun shoot": self.shotgun_shoot_attack,
                "Trap": self.trap,
                "Roll Foward": self.roll_forward,
            }
        elif self.selected_weapon.name == 'Big Sledgehammer' and not self.rage:
            attacks = {
                "Slam": self.slam_attack,
                "Swing": self.swing_sledgehammer_attack,
                "Rage Fill": self.rage_fill,
            }
        elif self.selected_weapon.name == 'Big Sledgehammer' and self.rage:
            attacks = {
                "Enchanced Slam": self.slam_attack,
                "Enchanced Swing": self.swing_sledgehammer_attack,
                "EarthQuake": self.earthquake,
            }
        elif self.selected_weapon.name == 'C10H15N':
            attacks = {
                "Incredible Punch": self.punch_attack,
                "Magnificent Kick": self.kick_attack,
                "Overdose": self.overdose,
            }
        elif self.selected_weapon.name == 'Bomb':
            attacks = {
                "Throw Bomb": self.throw_bomb,
                "Area Bomb attack": self.area_bomb_attack,
                "The Nuke": self.nuke,
            }
        elif self.selected_weapon.name == 'Berserker Axe' and not self.constantspin:
            attacks = {
                "Critical Slice": self.critical_slice,
                "Constant Spin": self.constant_spin,
                "Axe Slam": self.axe_slam,
            }
        elif self.selected_weapon.name == 'Berserker Axe' and self.constantspin:
            attacks = {
                "Constant Spin": self.constant_spin,
                "Stop": self.stop,
            }
        elif self.selected_weapon.name == 'Shuriken':
            attacks = {
                "Quick Stab": self.quick_stab_attack,
                "Shuriken Throw": self.shuriken_throw_attack,
                "Shadow Outburst": self.shadow_outburst,
                "Smoke Bomb": self.smoke_bomb,
                "Shadow Assassination": self.shadow_assassination
            }
        elif self.selected_weapon.name == 'Lucky Charms':
            attacks = {
                "Horseshoe Stomp": self.horseshoestompattack,
                "Taste The Rainbow": self.tastetherainbowattack,
                "Golden Pot": self.goldenpot,
                "5 Leaf Clover": self.fiveleafclover
            }
        elif self.selected_weapon.name == "Whip":
            attacks = {
                "Harass": self.harrass,
                "Whip Attack": self.whip_attack,
                "Slave Generator": self.slave_generator,
                "Sent to Fields": self.sent_to_fields,
            }
        elif self.selected_weapon.name == "Ice Wand":
            attacks = {
                "Icicle Storm": self.icicle_storm_attack,
                "Chilling Spell": self.chilling_spell_attack,
                "Slippery Field": self.slippery_fields,
            }
        elif self.selected_weapon.name == "Money":
            attacks = {
                "Invest": self.invest,
                "Gamble": self.gamble,
                "Spend": self.shop,
            }
        elif self.selected_weapon.name == "Poison Gas":
            attacks = {
                "Punch": self.punch_attack,
                "Kick": self.kick_attack,
                "Toxification": self.toxification,
            }
        if other_player.armour_turn >= 0 and other_player.bleeding:
            damage = random.randint(7, 9)
            other_player.health -= damage
            print(f"{self.name} dealt {damage} damage from the bow's passive!")
        if other_player.burned:
            damage = random.randint(2, 4)
            other_player.health -= damage
            print(f"{other_player.name} takes {damage} damage from burn!")
            if self.no_damage_reduction:
                print("The Damage Reduction is not active due to the axe slam!")
                self.no_damage_reduction = False
            else:
                self.damage_reduction += 2
 
        if self.selected_weapon.name == "Whip" and not self.slavingpower in [0, 1, 2]:
            if (self.health + 20) < self.current_health:
                self.slavingpower -= 3
                print(f"{self.name} lost 3 slaving power!")
        if self.successfulharrass:
            if self.no_damage_reduction:
                print("The Damage Reduction is not active due to the axe slam!")
                self.no_damage_reduction = False
            else:
                self.damage_reduction += 3
        if self.smokebombactivation:
            self.smokebombturns += 1
        if self.smokebombturns > 4:
            self.smokebombactivation = False
            self.smokebombspecialactivation = False
            self.smokebombturns = 0
            print(f"{self.name}'s smoke bomb is deactivated")
        if self.smokebombactivation and self.smokebombturns <= 3:
            if self.no_damage_reduction:
                print("The Damage Reduction is not active due to the axe slam!")
                self.no_damage_reduction = False
            else:
                self.damage_reduction += 3
        if self.smokebombspecialactivation:
            self.combo += 1
            damage = 3
            other_player.health -= 3
            print(f"{self.name} does 3 more damage because of the smoke bomb!")
        if self.selected_weapon.name == "Electric Axe" and self.current_health > self.health:
            damage = random.randint(3, 4)
            other_player.health -= damage
            print(f"{self.name} dealt {damage} reflection damage from the electric axe's passive!")
        if self.selected_weapon.name in ["Dagger", "Assassination Dagger"]:
            if self.dagger_pull >= 5:
                damage = 0 + self.daggers + (self.big_dagger * 5)
                other_player.health -= damage
                print(f"{self.name}'s daggers returned to them and dealt {damage} damage!(passive)")
                self.dagger_pull -= 5
                self.daggers = 0
                self.big_dagger = 0
        if self.grounded:
            self.grounded_turn += 1
        if self.grounded_turn >= 3:
            self.grounded = False
            print(f"{self.name} is no longer grounded!")
            self.grounded_turn -= 3
        if self.selected_weapon.name == 'Lucky Charms' and self.goldenpotdamage > 0:
          # Choose a random number between 1 and 5
          lucky_number = random.randint(1, 5)
          print(f"{self.name} activated Lucky Charms Passive! A random number between 1 and 5 has been chosen.")

          try:
              guess = int(input("Guess the lucky number (1-5): "))
              if 1 <= guess <= 5:
                  if lucky_number == guess:
                      damage = 5 * self.goldenpotdamage
                  elif abs(lucky_number - guess) == 1 and not guess == 3:
                      damage = 4 * self.goldenpotdamage
                  elif abs(lucky_number - guess) == 2 and not guess == 3:
                      damage = 3 * self.goldenpotdamage
                  elif abs(lucky_number - guess) == 3 and not guess == 3:
                      damage = 2 * self.goldenpotdamage
                  elif guess == 3 and lucky_number in (4, 2):
                      damage = 3 * self.goldenpotdamage
                  else:
                      damage = 1 * self.goldenpotdamage

                  print(f"Your guess: {guess}, Lucky Number: {lucky_number}, Damage: {damage}")
                  other_player.health -= damage
                  print(f"{other_player.name} took {damage} damage!")
              else:
                  print("Invalid guess. Please enter a number between 1 and 5.")
          except ValueError:
              print("Invalid input. Please enter a number.")
        if self.health <= 0 or other_player.health <= 0:
            return
        while True:
            for i, attack in enumerate(attacks.keys()):
                print(f"{i+1}. {attack}")
            try:
                attack_choice = int(input()) - 1
                if attack_choice < len(attacks):
                    attack_name = list(attacks.keys())[attack_choice]
                    attack_func = attacks[attack_name]
                    attack_func(other_player)
                    break
                else:
                    print("Invalid choice. Please choose again.")
            except ValueError:
                print("Error: Invalid input. Please enter a number.")
        if self.power_restriction:
          if other_player.no_damage_reduction:
              print("The Damage Reduction is not active due to the axe slam!")
              other_player.no_damage_reduction = False
          else:
              if other_player.current_health - other_player.health > 22:
                  other_player.health = other_player.current_health - 22
                  print(f"{other_player.name}'s punishment caused the damage of {self.name} do be reduced to 22!'")
    def damage(self, other_player, damage, damage_reduction, armour, charge):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return False
        
        if charge:
            self.charge = False
            print(f"({self.name} charged straight at the opponent(They have a long ranged weapon)!")
            print(f"({self.name} loses this turn)")
            return False
        if damage_reduction > 0:
            print(f"{other_player.name}'s damage reduction: {damage_reduction}")
        damage = damage + armour - damage_reduction
        if armour > 0:
            print(f"{other_player.name} will take extra damage this turn because they have no armour!")
        if damage < 0:
            damage = 0
        other_player.health -= damage 
        print(f"\n{other_player.name} takes {damage} damage from the attack!")
        if other_player.health < 0:
            other_player.health = 0
        return True
    def spin_hammer_attack(self, other_player):
        if self.grounded:
            print(f"{self.name} can't use spin attack if you are grounded!")
            return
        elif not self.charged and other_player.selected_weapon.name not in self.melee:
            self.charge = True
            self.charged = True
        damaged = self.damage(other_player, random.randint(11, 19), other_player.damage_reduction, other_player.armour, self.charge)
        if random.randint(1, 10) <= 8 and damaged and not other_player.confusion:
            other_player.confusion = True
            print(f"{other_player.name} is now confused!")
    
    def throw_hammer_attack(self, other_player):
        damaged = self.damage(other_player, random.randint(12, 14), other_player.damage_reduction, other_player.armour, self.charge)
        if damaged:
            other_player.boomerang_hammer = True
    
    def build(self, other_player):
        if self.ultimate_move:
            print("You already used your ultimate move!")
            return

        print("Type the weapon you want to build!")
        weapon_name = input().lower()
        valid_weapons = {
            "sword": "Sword", "spear": "Spear", "darts": "Darts", "bow": "Bow", "sniper": "Sniper",
            "red lightsaber": "Red LightSaber", "holy bible": "Holy Bible", "electric axe": "Electric Axe", "dagger": "Dagger",
            "cards": "Cards", "machine gun": "Machine Gun", "mirror": "Mirror", "shotgun": "Shotgun",
            "big sledgehammer": "Big Sledgehammer", "c10h15n": "C10H15N", "bomb": "Bomb", "shuriken": "Shuriken",
            "lucky charms": "Lucky Charms", "whip": "Whip", "berserker axe": "Berserker Axe", "ice wand": "Ice Wand", "money": "Money"
        }

        if weapon_name in valid_weapons:
            self.selected_weapon.name = valid_weapons[weapon_name]
            print(f"{self.name} built a {weapon_name}.")
            if self.next_attack_does_no_damage:
                self.next_attack_no_damage(other_player)
            self.attackopponent(other_player)
            self.selected_weapon.name = "Hammer"
            self.special_hammer = True
            print(f"{self.name} returned back to the hammer!")
            self.ultimate_move = True
        else:
            print("Invalid weapon name.")
            
    def slash_attack(self, other_player):
        if self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        elif not self.charged and other_player.selected_weapon.name not in self.melee:
            self.charge = True
            self.charged = True
        damaged = self.damage(other_player, random.randint(10, 15), other_player.damage_reduction, other_player.armour, self.charge)
    
    def Charging_blow_attack(self, other_player):
        if self.next_attack_does_no_damage == True:
            self.next_attack_no_damage(other_player)
        if self.charging_blow_turn == 0:
            print(f"{self.name} is charging power.")
            self.charging_blow_turn += 1
            return
        elif not self.charged and other_player.selected_weapon.name not in self.melee:
            self.charge = True
            self.charged = True
        damaged = self.damage(other_player, random.randint(31, 36), other_player.damage_reduction, other_player.armour, self.charge)
        if damaged:
            self.charging_blow_turn -= 1
    
    def Razor_wind_attack(self, other_player):
        if not self.ultimate_move:
            print(f"{self.name} used Razor wind, sending it towards the opponent!.")
            other_player.next_attack_does_no_damage = True
        else:
            print("You already used your ultimate move!")
            return
        self.ultimate_move = True
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
					
    def shoot_attack(self, other_player):
        self.damage(other_player, random.randint(8, 12), other_player.damage_reduction, other_player.armour, self.charge)
    
    def pierce_attack(self, other_player):
        damaged = self.damage(other_player, random.randint(4, 6), other_player.damage_reduction, other_player.armour, self.charge)
        if damaged and other_player.armour_turn == -1:
            print(f"It also removed {other_player.name}'s armour!")
            other_player.armour_turn = 0
    
    def bleeding_arrow_attack(self, other_player):
        if self.next_attack_does_no_damage :
            self.next_attack_no_damage(other_player)
        elif not self.ultimate_move and not self.next_attack_does_no_damage:
            print(f"{self.name} used for bleeding arrow attack! {other_player.name} is now bleeding!")
            other_player.bleeding = True
            self.ultimate_move = True
              
        else:
            print("You already used your ultimate move!")
    
    def sniper_attack(self, other_player):
        if not other_player.charged:
            damage = random.randint(18, 22)
        else:
            damage = 14
        self.damage(other_player, damage, other_player.damage_reduction, other_player.armour, self.charge)

    def the_bushes_effect(self, other_player):
        if self.thebushes:
            print("The bushes are already in affect!")
        elif self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        else:
            print(f"{self.name} used the bushes to hide themselves, causing them to have a 4 point damage reduction!")
            self.thebushes = True
            self.damage_reduction += 4
            if self.next_attack_does_no_damage:
                self.next_attack_no_damage(other_player)
    def roll_back_effect(self, other_player):
        if not self.ultimate_move and not other_player.royal_guards_summoned:
            other_player.charged = False
            self.damage(other_player, random.randint(20, 22), other_player.damage_reduction, other_player.armour, self.charge)
            self.ultimate_move = True
            print(f"{self.name} rolled back!")
        elif other_player.royal_guards_summoned or self.grounded:
            print(f"{self.name} can't use a dash or roll back skill if there are royal guards or grounded!")
        elif self.ultimate_move:
            print("You already used your ultimate move!")
    def brutality_training_attack(self, other_player):
        if self.next_attack_does_no_damage == True:
            self.next_attack_no_damage(other_player)
        if self.stamina < 50:
            print("You don't have enough stamina to use this move!")
            return
        print("Sniper attack starting...")
        self.super_sniper_attack(other_player)
        self.stamina -= 50
        print(f"{self.name} lost 50 stamina!")
            
    def dart_attack(self, other_player):
        self.damage(other_player, random.randint(7, 13), other_player.damage_reduction, other_player.armour, self.charge)
        
    def dart_flank_attack(self, other_player):
        damaged = self.damage(other_player, random.randint(4, 6), other_player.damage_reduction, other_player.armour, self.charge)
        if damaged and not other_player.drowsy:
            other_player.drowsy = True
            print(f"{self.name} sent a flank of darts, causing {other_player.name} to become drowsy!")
    
    def poison_dart(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
        elif not self.ultimate_move and not self.next_attack_does_no_damage:
            print(f"{self.name} sent a poison dart!")
            other_player.venom = True
            self.ultimate_move = True
        else:
            print("You already used your ultimate move!")
    def divine_judgment_attack(self, other_player):
        if self.health >= 44:
            damage = 10
        else:
            damage = (round(100 - self.health) / 2 - 18)
        if self.angelic_aid >= 2:
            angelic_damage = random.randint(1, 2)
            angel_damage = angelic_damage * self.angelic_aid
            self.health += angel_damage
            other_player.health -= angel_damage
            print(f"{self.name} called on Angelic Aid, dealing {angel_damage} extra damage and healing {angel_damage} health!")
        self.damage(other_player, damage, other_player.damage_reduction, other_player.armour, self.charge)

                
    def sacred_sacrifice(self, other_player):
        damage = 5
        self.health -= damage
        print(f"{self.name} sacrificed {damage} health!")
        self.sacred_sacrifice_turns += 1
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            
    def consecrated_water(self, other_player):
        if self.frostbite_heal:
            print(f"{self.name} cannot heal up due to frostbite!")
            return

        if not self.ultimate_move:
            heal = random.randint(17, 20)
            self.health += heal
            self.bleeding = self.venom = self.confusion = self.drowsy = self.small_bleeding = False
            self.paralysed = self.burned = self.poison = self.medium_bleeding = self.suffering = False

            print(f"{self.name} healed {heal} health, also removing all self-harming effects!")
            self.ultimate_move = True
            if self.health >= 100:
                self.health = 100
            if self.angelic_aid >= 2:
                heal = random.randint(2, 5) 
                total_heal = heal + (2 * self.angelic_aid)
                self.health += total_heal
                print(f"{self.name} healed an extra {total_heal} health due to the angelic aid!")
            if self.next_attack_does_no_damage:
                self.next_attack_no_damage(other_player)
        else:
            print("You already used your ultimate move!")
        
    def spear_slice_attack(self, other_player):
        if self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        elif not self.charged and other_player.selected_weapon.name not in self.melee:
            self.charge = True
            self.charged = True
        self.damage(other_player, random.randint(7, 12), other_player.damage_reduction, other_player.armour, self.charge)
            
    def spear_throw_attack(self, other_player):
        damaged = self.damage(other_player, random.randint(4, 8), other_player.damage_reduction, other_player.armour, self.charge)
        if random.randint(1, 10) <= 3 and damaged and not other_player.small_bleeding:
            print(f"{self.name} used spear throw and {other_player.name} is now bleeding!")
            other_player.small_bleeding = True
                
    def royal_guards(self, other_player):
        if self.grounded:
            print(f"{self.name} can't use summon royal guards if grounded!")
            return
        print(f"{self.name} summoned royal guards!")
        self.royal_guards_summoned = True
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)

    def swing_attack(self, other_player):
        if self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        elif self.focus_energy_power and not self.double_lightsaber:
            damage = random.randint(12, 16)
            speed = 70
        elif self.focus_energy_power and self.double_lightsaber:
            damage = random.randint(12, 16) + 8
            speed = 130
        elif self.double_lightsaber:
            damage = random.randint(6, 10) + 8
            speed = 50
        else:
            damage = random.randint(5, 9)
            speed = 30
        damaged = self.damage(other_player, damage, other_player.damage_reduction, other_player.armour, self.charge)
        if damaged:
            other_player.selected_weapon.speed = other_player.selected_weapon.speed - speed
            print(f"{self.name} used lightsaber swing attack, lowering {other_player.name}'s speed!")
            print(f"{other_player.name}'s speed:{other_player.selected_weapon.speed}")
        

    
    def focus_energy(self, other_player):
        self.focus_energy_power = True
        print(f"{self.name} used focus energy, increasing the chance of critical strikes! (Note: You can't stack this effect)")
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
    
    def the_force_attack(self, other_player):
        if not self.ultimate_move:
            self.the_force = True
            print(f"{self.name} used the force on {other_player.name}!")
            if self.next_attack_does_no_damage:
                self.next_attack_no_damage(other_player)
        else:
            print("You already used your ultimate move!")
    def zap_attack(self, other_player):
        if not self.charged and other_player.selected_weapon.name not in self.melee:
            self.charge = True
            self.charged = True
        damaged = self.damage(other_player, random.randint(7, 12), other_player.damage_reduction, other_player.armour, self.charge)
        if random.randint(1, 10) <= 5 and damaged and not other_player.paralysed:
            print(f"The zap attack also paralysed {other_player.name}!")
            other_player.paralysed = True
            other_player.selected_weapon.speed = int(other_player.selected_weapon.speed/2)
            print(f"{other_player.name}'s speed: {other_player.selected_weapon.speed}")
    def electric_arrival(self, other_player):
        if self.grounded:
            print(f"{self.name} can't use a dash or roll back skill if grounded!")
        elif self.ultimate_move:
            print("You already used your ultimate move!")
        else:
            self.charged = True
            self.damage(other_player, random.randint(20, 23), other_player.damage_reduction, other_player.armour, self.charge)
            self.electric_shower = True
            self.ultimate_move = True
            print(f"{self.name} jumped at {other_player.name}, creating a electric shower!")
    def sharp_throw_attack(self, other_player):
        if self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        elif self.assassination_mode:
            damage = random.randint(8, 15)
        else:
            damage = random.randint(5, 12)
        damaged = self.damage(other_player, damage, other_player.damage_reduction, other_player.armour, self.charge)
        if damage >= 12 and damaged and not other_player.small_bleeding:
            print(f"Critical Hit! {other_player.name} is now bleeding!")
            other_player.small_bleeding = True
        if self.assassination_mode and damaged:
            self.big_dagger += 1
            print(f"1 big dagger is stuck in {other_player.name}!")
        elif not self.assassination_mode and damaged:
            self.daggers += 1
            print(f"1 dagger is stuck in {other_player.name}!")
    def multiple_throw_attack(self, other_player):
        if self.assassination_mode:
            damage = 4 * random.randint(2, 4)
        else:
            damage = 4 * random.randint(1, 3)
        damaged = self.damage(other_player, damage, other_player.damage_reduction, other_player.armour, self.charge)
        if damaged:
            print(f"4 daggers are stuck in {other_player.name}!")
            self.daggers += 4
    def assassination(self, other_player):
        if self.ultimate_move:
            print("You already used your ultimate move!")
        elif self.grounded:
            print(f"{self.name} can't use a invisibility skill if grounded!")
        else:
            print(f"{self.name } used their assassination skills to turn invisible! {other_player.name} can no longer see them!")
            self.assassination_mode = True
            self.ultimate_move = True
            self.selected_weapon.name = "Assassination Dagger"
            if self.next_attack_does_no_damage:
                self.next_attack_no_damage(other_player)
        
    def slicing_tornado_attack(self, other_player):
        if self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        else:
            damaged = self.damage(other_player, 6 * random.randint(1, 3), other_player.damage_reduction, other_player.armour, self.charge)
            if damaged:
                self.daggers += 6
                print(f"6 daggers are stuck in {other_player.name}!")
    def card_throw_attack(self, other_player):
        damaged = self.damage(other_player, random.randint(6, 12), other_player.damage_reduction, other_player.armour, self.charge)
        if damaged:
            self.card_throw = True
    def joker_power(self, other_player):
        print(f"{self.name} used joker power! The continous damage of the card throw attack is increased!")
        self.jokercardpowerloseturn = True
        self.jokerdamage += 1
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
    def bj_gamble(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        if self.ultimate_move:
            print("You already used your ultimate move!")
            return
        self.deck = Deck()
        self.player1 = Player("Bj Player 1", [])
        self.player2 = Player("Bj Player 2", [])
        
        print("Welcome to Blackjack!")
        self.player1.hand.add_card(self.deck.draw_card())
        self.player2.hand.add_card(self.deck.draw_card())
        self.player1.hand.add_card(self.deck.draw_card())
        self.player2.hand.add_card(self.deck.draw_card())
        print(self.player1)
        
        both_stand = False
        
        while True:
            self.player1.play_card_turn(self.deck)
            if self.player1.is_bust:
                damage = random.randint(20, 25)
                other_player.health -= damage
                print(f"{self.player1.name} wins! That means the {self.name} deals {damage} damage!")
                break
            Player.clear_display(self)
            print(self.player2)
            self.player2.play_card_turn(self.deck)
            if self.player2.is_bust:
                damage = random.randint(40, 45)
                other_player.health -= damage
                print(f"{self.player2.name} wins! That means the {self.name} deals {damage} damage!")
                break
            if not self.player1.is_bust and not self.player2.is_bust:
                if self.player1.hand.value == self.player2.hand.value:
                    damage = random.randint(30, 35)
                    other_player.health -= damage
                    print(f"It's a tie! That means the {self.name} deals {damage} damage!")
                    break
                elif self.player1.hand.value > self.player2.hand.value:
                    damage = random.randint(40, 45)
                    other_player.health -= damage
                    print(f"{self.player1.name} wins! That means the {self.name} deals {damage} damage!")
                    break
                else:
                    damage = random.randint(20, 25)
                    other_player.health -= damage
                    print(f"{self.player2.name} wins! That means the {self.name} deals {damage} damage!")
                    break
            elif self.player1.hand.value != self.player2.hand.value:
                both_stand = True
            elif both_stand:
                damage = random.randint(30, 35)
                other_player.health -= damage
                print(f"It's a tie! That means the {self.name} deals {damage} damage!")
                break
                
        print("Game over.")
        print(self.player1)
        print(self.player2)
        self.ultimate_move = True
    def shoot_machine_gun_attack(self, other_player):
        if self.machine_gun_reload >= 2:
            print("You have no more bullets; You have to reload!")
            return
        damage = sum(random.randint(2, 5) for _ in range(6))
        damaged = self.damage(other_player, damage, other_player.damage_reduction, other_player.armour, self.charge)
        if damaged:
            self.machine_gun_reload += 1
    def reload(self, other_player):
        if self.machine_gun_reload >= 2:
            print("You reloaded your machine gun!")
            self.machine_gun_reload -= 2
        elif self.machine_gun_reload <= 2:
            print("Why would you reload the machine gun? Do it after you used machine gun regular attack 2 times!")
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
    def hand_grenade(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        if self.secondaryultimate:
            print("You don't have any more grenades!")
            return
        damage = random.randint(5, 10)
        other_player.health -= damage
        other_player.flashstun = True
        other_player.confusion = True
        self.secondaryultimate = True
        print(f"{self.name} used hand grenade and dealt {damage} damage, along with stunning & confusing {other_player.name}!")
    def rapid_fire_attack(self, other_player):
        if self.ultimate_move:
            print("You already used your ultimate move!")
            return
        if self.machine_gun_reload > 0:
            print("You need to have full ammo to use your ultimate move!")
            return
        damage = sum(random.randint(2, 4) for _ in range(12))
        damaged = self.damage(other_player, damage, other_player.damage_reduction, other_player.armour, self.charge)
        if damaged:
            print("[Note you have to reload after this]")
            self.machine_gun_reload = 2
    def sun_reflect_attack(self, other_player):
        damaged = self.damage(other_player, random.randint(5, 7), other_player.damage_reduction, other_player.armour, self.charge)
        if random.randint(1, 10) <= 5 and damaged and not other_player.burned:
            print(f"{other_player.name} is burned!")
            other_player.burned = True
    def glass_shard_attack(self, other_player):
        damaged = self.damage(other_player, random.randint(8, 11), other_player.damage_reduction, other_player.armour, self.charge)
        if random.randint(1, 10) >= 7 and damaged and not other_player.small_bleeding:
            print(f"{self.name} is also bleeding!")
            other_player.small_bleeding = True
    def reflect(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        if self.mirror_move:
            print("You already used your ultimate move!")
            return
        if self.current_health >= self.health:
            damage = (self.current_health - self.health)
            other_player.health -= damage
            self.health += damage
            print(f"{self.name} reflects {other_player.name} damage(NOT EFFECTS) and dealt {damage} damage!")
            self.mirror_move = True
        
    def shotgun_shoot_attack(self, other_player):
        if other_player.charge or self.ultimate_move or self.shotgunpassive:
            damage = random.randint(13, 18)
            if self.shotgunpassive and not self.ultimate_move or self.shotgunpassive and not other_player.charge:
                damage += 5 
        else:
            damage = random.randint(7, 12)
        damaged = self.damage(other_player, damage, other_player.damage_reduction, other_player.armour, False)
        if self.shotgunpassive and damaged:
            print(f"{self.name} dealt 5 more damage due to the shotgun passive!")
        if not self.traps_placed == 0 and damaged:
            damage = random.randint(8, 12)
            other_player.health -= damage
            print(f"{other_player.name} activated a trap! The trap dealt {damage} damage!")
            self.traps_placed -= 1
    
    def trap(self, other_player):
        print(f"{self.name} placed down three traps!")
        self.traps_placed += 3
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
    def roll_forward(self, other_player):
        if not self.ultimate_move and not other_player.royal_guards_summoned:
            self.ultimate_move = True
            print(f"{self.name} rolled forward!")
        elif other_player.royal_guards_summoned:
            print(f"{self.name} can't use a dash or roll skill if there are royal guards!")
        elif self.grounded:
            print(f"{self.name} can't use a dash or roll back skill if grounded!")
        elif self.ultimate_move:
            print("You already used your ultimate move!")
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
    def swing_sledgehammer_attack(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        elif self.rage:
            damage = random.randint(16, 21)
            other_player.health -= damage
            print(f"{self.name} used enchanced swing attack and dealt {damage} damage!")
            if random.randint(1, 10) <= 7:
                other_player.confusion = True
                print(f"{other_player.name} is now confused!")
            return
        damage = random.randint(10, 14)
        other_player.health -= damage
        print(f"{self.name} used swing attack and dealt {damage} damage!{self.name} gained 1 rage point!")
        self.become_rage += 1
        if random.randint(1, 10) <= 4:
            other_player.confusion = True
            print(f"{other_player.name} is now confused!")
    def slam_attack(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        elif self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        elif self.rage:
            damage = random.randint(22, 25)
            other_player.health -= damage
            print(f"{self.name} used enhanced slam attack and dealt {damage} damage!")
            other_player.grounded = True
            print(f"{other_player.name} is now grounded(or already is)! Some attacks can't be used if you are grounded!")
            return
        damage = random.randint(11, 15)
        other_player.health -= damage
        print(f"{self.name} used slam attack and dealt {damage} damage! {self.name} gained 1 rage point!")
        self.become_rage += 1
        other_player.grounded = True
        print(f"{other_player.name} is now grounded! Some attacks can't be used if you are grounded!")
    def rage_fill(self, other_player):
        if self.become_rage < 5:
            print(f"{self.name} gained 2 rage!")
            self.become_rage += 2
        elif self.become_rage >= 5 and not self.ultimate_move:
            print(f"{self.name} entered rage mode!")
            self.rage = True
        elif self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
    def earthquake(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damyage(other_player)
            return
        elif self.earthquake_attack:
            print("You already used your ultimate move!")
            return
        damage = sum(random.randint(11, 16) for _ in range(4))
        other_player.health -= damage
        print(f"{self.name} smash onto the ground, causing an earthquake and dealing {damage} damage!")
        self.earthquake_attack = True
    def punch_attack(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        elif self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        elif not self.charge and not other_player.selected_weapon.name in ["Red LightSaber", "Berserker Axe", "Spear", "Sword", "Electric Axe,", "C10H15N"]:
            self.charge = True
            print(f"({self.name} charged straight at the opponent(They have a long ranged weapon)!")
            print(f"({self.name} loses this turn)")
            return
        damage = random.randint(3, 5)
        other_player.health -= damage
        print(f"{self.name} punched the {other_player.name} and dealt {damage} damage!")
    def kick_attack(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        elif self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        elif not self.charge and not other_player.selected_weapon.name in ["Red LightSaber", "Berserker Axe", "Spear", "Sword", "Electric Axe,", "C10H15N"]:
            self.charge = True
            print(f"({self.name} charged straight at the opponent(They have a long ranged weapon)!")
            print(f"({self.name} loses this turn)")
            return
        damage = random.randint(2, 6)
        other_player.health -= damage
        print(f"{self.name} kicked the {other_player.name} and dealt {damage} damage!")
    def overdose(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        elif self.ultimate_move:
            print("You already used your ultimate move!")
            return
        elif not self.overdose_turn:
            print(f"{self.name} decides to overdose!")
            self.overdose_turn = True
            return
        player_overdose = input("What ultimate choice do you want to implement?(1. Driving Under the Influence 2. Massive Overdose 3. Peer pressure)")
        if player_overdose == "1":
            damage = random.randint(20, 26)
            selfdamage = 10
            self.health -= selfdamage
            other_player.health -= damage
            other_player.small_bleeding = True
            other_player.medium_bleeding = True
            self.charge = True
            print(f"{self.name} decided to drive under the influence, dealing {selfdamage} to the player, dealing {damage} damage to the opponent, getting close to the enemy, and causing the opponent to critically bleed!")
        elif player_overdose == "2":
            self.overdosetwo = True
            print(f"{self.name} consumed more C10H15N!")
        elif player_overdose == "3":
            other_player.overdosethree = True
            other_player.poison = True
            other_player.confusion = True
            print(f"{self.name} peer pressured {other_player.name} causing them to be poisoned and confused!")
        else:
            print("Nothing Happened!")
        self.ultimate_move = True
    def throw_bomb(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        damage = random.randint(9, 14)
        other_player.health -= damage
        print(f"{self.name} threw a bomb, dealing {damage} damage!")
    def area_bomb_attack(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        elif other_player.name in ['Player 1(W1)','Player 1(W2)','Player 1(W3)', 'Player1(W4)', 'Player1(W5)']:
            damage = random.randint(1, 3)
            game.player1.health -= damage
            game.player3.health -= damage
            game.player5.health -= damage
            game.player7.health -= damage
            game.player9.health -= damage
            print(f"{self.name} used area bomb attack!")
            print(f"All of player 1's weapons took {damage} damage!")
        elif other_player.name in ['Player 2(W1)','Player 2(W2)', 'Player 2(W3)', 'Player2(W4)', 'Player2(W5)']:
            damage = random.randint(1, 3)
            game.player2.health -= damage
            game.player4.health -= damage
            game.player6.health -= damage
            game.player8.health -= damage
            game.player10.health -= damage
            print(f"{self.name} used area bomb attack!")
            print(f"All of player 2's weapons took {damage} damage!")
    def nuke(self, other_player):
        if self.nuke_turns < 4:
            print(f"{self.name} is preparing the nuke!")
            self.nuke_turns += 1
            if self.next_attack_does_no_damage:
                self.next_attack_no_damage(other_player)
            return
        if self.ultimate_move:
            print("You already used your ultimate move!")
        elif other_player.name in ['Player 1(W1)','Player 1(W2)','Player 1(W3)', 'Player 1(W4)', 'Player 1(W5)']:
            damage = 17
            nukedamage = random.randint(20, 30)
            game.player1.health -= damage
            game.player3.health -= damage
            game.player5.health -= damage
            game.player7.health -= damage
            game.player9.health -= damage
            other_player.health -= nukedamage
            print(f"{self.name} used area bomb attack!")
            print(f"{game.player1.name} took {damage} damage!")
            print(f"{game.player3.name} took {damage} damage!")
            print(f"{game.player5.name} took {damage} damage!")
            print(f"{game.player7.name} took {damage} damage!")
            print(f"{game.player9.name} took {damage} damage!")
            print(f"{other_player.name} took an extra {nukedamage} damage!")
        elif other_player.name in ['Player 2(W1)','Player 2(W2)', 'Player 2(W3)', 'Player 2(W4)', 'Player 2(W5)']:
            damage = 17
            nukedamage = random.randint(20, 30)
            game.player2.health -= damage
            game.player4.health -= damage
            game.player6.health -= damage
            game.player8.health -= damage
            game.player10.health -= damage
            other_player.health -= nukedamage
            print(f"{self.name} used area bomb attack!")
            print(f"{game.player2.name} took {damage} damage!")
            print(f"{game.player4.name} took {damage} damage!")
            print(f"{game.player6.name} took {damage} damage!")
            print(f"{game.player8.name} took {damage} damage!")
            print(f"{game.player10.name} took {damage} damage!")
            print(f"{other_player.name} took an extra {nukedamage} damage!")
        self.ultimate_move = True
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
    def quick_stab_attack(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        elif self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        damage = random.randint(3, 7) + self.combo
        other_player.health -= damage
        print(f"{self.name} used quick stab attack and dealt {damage} damage!")
        self.combo += 1
        if self.shadow_energy:
            print(f"{self.name} teleported behind {other_player.name}!")
            self.shadow = True
            self.shadow_energy = False
    def shuriken_throw_attack(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        damage = random.randint(2, 5) + self.combo
        other_player.health -= damage
        print(f"{self.name} used shuriken throw attack and dealt {damage} damage!")
        self.combo += 3
        if self.shadow_energy:
            print(f"{self.name} teleported behind {other_player.name}!")
            self.shadow = True
            self.shadow_energy = False
    def shadow_outburst(self, other_player):
        if self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        print(f"{self.name} is charging shadow power!")
        self.shadow_energy = True
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
    def smoke_bomb(self, other_player):
        if self.smokebomb == 0:
            print("You don't have any smoke bombs left!")
            return
        print(f"{self.name} used smoke bomb and covered the battlefield with smoke!")
        self.smokebombactivation = True
        self.smokebomb -= 1
        if self.shadow_energy:
            print(f"{self.name} teleported behind {other_player.name}!")
            self.shadow = True
            self.shadow_energy = False
            self.smokebombspecialactivation = True
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
    def shadow_assassination(self, other_player):
        if not self.shadow_kill:
            print(f"{self.name} can't use shadow assassination in normal form!")
            return
        elif self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        elif self.ultimate_move:
            print("You already used your ultimate move!")
            return
        damage = sum(random.randint(2, 3) for _ in range(5)) + self.combo
        other_player.health -= damage
        print(f"{self.name}'s shuriken sliced through {other_player.name} and dealt {damage} damage!")
        self.shuriken_assassination = True
        self.combo += 5
        self.ultimate_move = True
        self.shadow_kill = False
        self.smokebomb += 1
    def horseshoestompattack(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        elif self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        damage = random.randint(6, 11)
        other_player.health -= damage
        print(f"{self.name} used horseshoe stomp attack and dealt {damage} damage!")
        if random.randint(1, 10) <= 2:
            other_player.grounded = True
            print(f"{other_player.name} is now grounded!")
        elif random.randint(1, 10) <= 2:
            other_player.confusion = True
            print(f"{other_player.name} is now confused!")
    def goldenpot(self, other_player):
        if self.goldenpotdamage < 1:
            print(f"{self.name} activated the passive!")
        else:  
            print(f"{self.name} added damage to the passive!")
        self.goldenpotdamage += 1
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
    def tastetherainbowattack(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        print(f"{self.name} used taste the rainbow, causing the opponent to lose health gradually!")
        self.tastetherainbowconstantdamage = True
    def fiveleafclover(self, other_player):
        if self.ultimate_move:
            print("You already used your ultimate move!")
        elif self.name in ['Player 1(W1)']:
            game.player3.fiveleafcloverult = True 
            print("The next weapon's ultimate move can be used twice due to the five-leaf clover!")
        elif self.name in ['Player 1(W2)']:
            game.player5.fiveleafcloverult = True 
            print("The next weapon's ultimate move can be used twice due to the five-leaf clover!")
        elif self.name in ['Player 1(W5)', 'Player 2(W5)']:
            print("Nothing Happened, because this is the last weapon!")
        elif self.name in ['Player 2(W1)']:
            game.player4.fiveleafcloverult = True 
            print("The next weapon's ultimate move can be used twice due to the five-leaf clover!")
        elif self.name in ['Player 2(W2)']:
            game.player6.fiveleafcloverult = True 
            print("The next weapon's ultimate move can be used twice due to the five-leaf clover!")
        elif self.name in ['Player 1(W3)']:
            game.player7.fiveleafcloverult = True 
            print("The next weapon's ultimate move can be used twice due to the five-leaf clover!")
        elif self.name in ['Player 2(W3)']:
            game.player8.fiveleafcloverult = True 
            print("The next weapon's ultimate move can be used twice due to the five-leaf clover!")
        elif self.name in ['Player 2(W4)']:
            game.player10.fiveleafcloverult = True 
            print("The next weapon's ultimate move can be used twice due to the five-leaf clover!")
        elif self.name in ['Player 1(W4)']:
            game.player9.fiveleafcloverult = True 
            print("The next weapon's ultimate move can be used twice due to the five-leaf clover!")
        self.ultimate_move = True
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
    def critical_slice(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        damage = random.randint(12, 16)
        if self.frostbite_heal:
            heal = 0
        else:
            heal = damage // 4
            self.health += heal
        other_player.health -= damage
        print(f"{self.name} used critical slice, dealing {damage} damage and healing {heal} health!")
        if damage == 16:
            other_player.flashstun = True
            print("The damage is so high that the enemy is now stunned!")
        if other_player.health <= 0 and self.selected_weapon.name == "Berserker Axe" and not self.frostbite_heal:
            self.health += 20
            print("The Berserker Axe defeated an enemy, so it healed 20 health!")
    def constant_spin(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
        elif self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        elif random.randint(1, 10) <= (10 - 2 * self.constant_spin_turns):
            notdamage = random.randint(6, 8)
            damage = notdamage * (1 + self.constant_spin_turns)
            if self.frostbite_heal:
                heal = 0
            else:
                heal = damage // 2
            other_player.health -= damage
            self.constant_spin_turns += 1
            self.health += heal
            print(f"{self.name} used constant spin attack, dealing {damage} damage healing {heal} health!")
            print(f"{self.name} is now stuck in constant spin attack!")
            self.constantspin = True
            if other_player.health < 0 and self.selected_weapon.name == "Berserker Axe" and not self.frostbite_heal:
                self.health += 20
                print("The Berserker Axe defeated an enemy, so it healed 20 health!")
        else: 
            print(f"{self.name} stopped spinning!")
            self.constantspin = False
            self.constant_spin_turns = 0
    def stop(self, other_player):
        print(f"{self.name} stopped spinning!")
        self.constantspin = False
        self.constant_spin_turns = 0
        self.attackopponent(other_player)
    def axe_slam(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
            return
        elif self.grounded:
            print(f"{self.name} can't use this attack if grounded!")
            return
        damage = random.randint(25, 35)
        other_player.health -= damage
        if self.frostbite_heal:
            heal = 0
        else:
            heal = damage // 5
            self.health  += heal
        other_player.grounded = True
        other_player.small_bleeding = True
        other_player.no_damage_reduction = True
        print(f"{self.name} slamed the axe, dealing {damage} damage, healing {heal} health, and causing the opponent to be bleeding and grounded!")
        print("This attack cannot be lowered by damage reduction!")
    def next_attack_no_damage(self, other_player):
        damage = 30
        self.health -= damage
        print(f"The razor wind dealt {damage} damage, and deflecting any attack!")
        self.next_attack_does_no_damage = False
        return
    def slave_generator(self, other_player):
        if self.amount_of_slaves < 6:
            print(f"{self.name} generated two slaves!")
            self.amount_of_slaves += 2
        else:
            print("You reached the max amount of slaves!")
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
    def harrass(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
        damage = random.randint(1, 3) 
        total_damage = (damage * self.amount_of_slaves) + self.slavingpower
        other_player.health -= total_damage
        print(f"{self.name} used harass, dealing {total_damage} damage and weakened the mentality of {other_player.name}!")
        print(f"{other_player.name}'s next attack does 3 less damage!")
        self.successfulharrass = True
    def whip_attack(self, other_player):
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
        self.slavingpower += 1
        damage = random.randint(11, 15)
        other_player.health -= damage
        print(f"{other_player.name} got whiped, losing {damage} health!")
        if other_player.fields:
            other_player.suffering = True
    def sent_to_fields(self, other_player):
        if self.amount_of_slaves < 3:
            print("You don't have enough slaves to sacrifise!")
        elif other_player.fields:
            print(f"{other_player.name} is already in the fields!")
        else:
            print(f"{self.name} sacrifised 3 slaves and sent {other_player.name} into the fields!")
            self.amount_of_slaves -= 3
            other_player.fields = True
            self.slavingpower += 1
        if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
    def icicle_storm_attack(self, other_player):
      if self.next_attack_does_no_damage:
            self.next_attack_no_damage(other_player)
      damage = random.randint(5, 7)
      total_damage = damage + self.icicle_storm_stack + (2 * other_player.frostbite_counter)
      other_player.health -= total_damage
      self.icicle_storm_stack += 3
      print(f"{self.name} summoned an icicle storm, dealing {total_damage} damage!")
    def chilling_spell_attack(self, other_player):
      if self.next_attack_does_no_damage:
        self.next_attack_no_damage(other_player)
      other_player.frostbite_counter += 1
      damage = random.randint(4, 6)
      other_player.health -= damage
      print(f"{self.name} used a chilling spell on {other_player.name}, dealing {damage} damage!")
    def slippery_fields(self, other_player):
      if self.name in ['Player 1(W1)','Player 1(W2)','Player 1(W3)', 'Player 1(W4)', 'Player 1(W5)']:
        game.slippery_fields1 = True
        print(f"{self.name} summoned a ice field!")
      if self.name in ['Player 2(W1)','Player 2(W2)','Player 2(W3)', 'Player 2(W4)', 'Player 2(W5)']:
        game.slippery_fields2 = True
        print(f"{self.name} summoned a ice field!")
      if self.next_attack_does_no_damage:
        self.next_attack_no_damage(other_player)
    def gamble(self, other_player):
      print("You enter the gambling state!")
      print("Choose your options:")
      options = {
        1: "Slot Machine",
        2: "Blackjack",
        3: "Roulette"
      }

      for key, value in options.items():
        print(f"{key}. {value}")
      
    def shop(self, other_player):
        print("HI")
    def toxification(self, other_player):
        other_player.confusion = other_player.drowsy = other_player.small_bleeding = other_player.suffering = True
        other_player.paralysed = other_player.burned = other_player.flashstun = True
        
class Game:
    def __init__(self):
        self.player1 = Player('Player 1(W1)', [])
        self.player2 = Player('Player 2(W1)', [])
        self.player3 = Player('Player 1(W2)', [])
        self.player4 = Player('Player 2(W2)', [])
        self.player5 = Player('Player 1(W3)', [])
        self.player6 = Player('Player 2(W3)', [])
        self.player7 = Player('Player 1(W4)', [])
        self.player8 = Player('Player 2(W4)', [])
        self.player9 = Player('Player 1(W5)', [])
        self.player10 = Player('Player 2(W5)', [])
        self.player11 = Player('Player 1(W6)', [])
        self.player12 = Player('Player 2(W6)', [])

    def ban_weapon(self, player, weapons):
        print(f"{player.name}, choose a weapon to ban:")
        for i, weapon in enumerate(weapons):
            print(f"{i+1}. {weapon.name}")
        ban_choice = None
        while ban_choice is None:
            try:
                ban_choice = int(input()) - 1
                if 0 <= ban_choice < len(weapons):
                    banned_weapon = weapons.pop(ban_choice)
                    print(f"{player.name} has banned the {banned_weapon.name}!")
                else:
                    print("Error: Invalid input. Please choose a number within the range of available weapons.")
                    ban_choice = None
            except ValueError:
                print("Error: Invalid input. Please enter a number.")

    def pick_weapon(self, player, weapons):
        print(f"{player.name}, choose a weapon:")
        for i, weapon in enumerate(weapons):
            print(f"{i + 1}. {weapon.name}")
        while True:
            try:
                weapon_choice = int(input()) - 1
                if 0 <= weapon_choice < len(weapons):
                    selected_weapon = weapons.pop(weapon_choice)
                    if player in [self.player1, self.player3, self.player5, self.player7,self.player9]:
                        self.player1.add_weapon(selected_weapon)
                    else:
                        self.player2.add_weapon(selected_weapon)
                    print(f"{player.name} has selected {selected_weapon.name}!")
                    break
                else:
                    print("Error: Invalid input. Please choose a number within the range of available weapons.")
            except ValueError:
                print("Error: Invalid input. Please enter a number.")

    def start_draft(self):
        weapons = [
            Weapon('Sword', 100),
            Weapon('Hammer', 280),
            Weapon('Dagger', 710),
            Weapon('Electric Axe', 80),
            Weapon('Bow', 400),
            Weapon('Spear', 450),
            Weapon('Sniper', 300),
            Weapon('Darts', 850),
            Weapon('Holy Bible', 570),
            Weapon('Red LightSaber', 520),
            Weapon('Cards', 900),
            Weapon('Machine Gun', 170),
            Weapon('Mirror', 670),
            Weapon('Shotgun', 320),
            Weapon('Big Sledgehammer', 20),
            Weapon('C10H15N', 930),
            Weapon('Bomb', 560),
            Weapon('Shuriken', 775),
            Weapon('Lucky Charms', 950),
            Weapon('Whip', 685),
            Weapon('Berserker Axe', 50),
            Weapon('Ice Wand', 535),
            Weapon('Money', 800),
            Weapon('Poison Gas', 1000)
            ]
        # Ban stage
        self.ban_weapon(self.player1, weapons)
        self.ban_weapon(self.player2, weapons)
        self.ban_weapon(self.player2, weapons)
        self.ban_weapon(self.player1, weapons)

        # Pick stage
        self.pick_weapon(self.player1, weapons)
        self.pick_weapon(self.player2, weapons)
        self.pick_weapon(self.player4, weapons)
        self.pick_weapon(self.player3, weapons)
        self.pick_weapon(self.player5, weapons)
        self.pick_weapon(self.player6, weapons)
        self.pick_weapon(self.player8, weapons)
        self.pick_weapon(self.player7, weapons)
        self.pick_weapon(self.player9, weapons)
        self.pick_weapon(self.player10, weapons)

    def play_game(self):
      print("Starting draft...")
      self.start_draft()
      print("Draft completed.")
      print(f"{self.player1.name}, choose your starting weapon:")
      
      while True:
          self.player1.select_starting_weapon()
          self.player2.select_starting_weapon()
          if self.player1.selected_weapon and self.player2.selected_weapon:
              break
      
      player1 = [self.player1, self.player3, self.player5]
      player2 = [self.player2, self.player4, self.player6]
      active_player1 = None
      active_player2 = None
      active_player3 = self.player11
      active_player4 = self.player12
      ultimate_move = False
      self.slippery_fields1 = False
      self.slippery_fields2 = False
      for player in player1:
          if self.player1.health > 0:
              active_player1 = self.player1
      for player in player2:
          if self.player2.health > 0:
              active_player2 = self.player2
      while True:
          if active_player1.selected_weapon.speed > active_player2.selected_weapon.speed and active_player1.health > 0 and active_player2.health > 0:
              print(f"{active_player1.name}: {active_player1.health} HP")
              print(f"{active_player2.name}: {active_player2.health} HP")
              print("------------------------------")
              active_player1.play_turn(active_player2)
              print(f"{active_player1.name}: {active_player1.health} HP")
              print(f"{active_player2.name}: {active_player2.health} HP")
              print("------------------------------")
              active_player2.play_turn(active_player1)
          if active_player2.selected_weapon.speed > active_player1.selected_weapon.speed and active_player1.health > 0 and active_player2.health > 0:
                print(f"{active_player1.name}: {active_player1.health} HP")
                print(f"{active_player2.name}: {active_player2.health} HP")
                print("------------------------------")
                active_player2.play_turn(active_player1)
                print(f"{active_player1.name}: {active_player1.health} HP")
                print(f"{active_player2.name}: {active_player2.health} HP")
                print("------------------------------")
                active_player1.play_turn(active_player2)
          elif active_player1.health <= 0:
            if active_player1.selected_weapon.name == "Holy Bible" and not active_player1.undying_will:
                  print(f"{active_player1.name} stays at 1 hp due to the Holy Bible's passive!")
                  active_player1.health = 1
                  active_player1.undying_will = True
                  if active_player1.selected_weapon.speed < active_player2.selected_weapon.speed:
                      active_player1.attackopponent(active_player2)
                  elif active_player1.selected_weapon.speed > active_player2.selected_weapon.speed:
                      active_player1.attackopponent(active_player2)
                      print(f"{active_player1.name}: {active_player1.health} HP")
                      print(f"{active_player2.name}: {active_player2.health} HP")
                      print("------------------------------")
                      if active_player2.health > 0:
                          active_player2.play_turn(active_player1)
            else:
                  print(f"{active_player1.name}'s weapon is destroyed!")
                  active_player3.weapons = active_player1.weapons
                  if not active_player1.traps_placed == 0:
                      active_player3.traps_placed = active_player1.traps_placed
                  if active_player1 == self.player9:
                    print(f"{self.player9.name}'s weapon is destroyed! This is a their final weapon, so they lose!")
                    print(f"{active_player2.name} Won!")
                    break
                  elif active_player1 == self.player7:
                    active_player1 = self.player9
                  elif active_player1 == self.player5:
                    active_player1 = self.player7
                  elif active_player1 == self.player3:
                    active_player1 = self.player5
                  elif active_player1 == self.player1:
                    active_player1 = self.player3
                  print(f"{active_player1.name}, choose your next weapon:")
                  active_player1.weapons = active_player3.weapons
                  active_player1.select_starting_weapon()
                  active_player1.traps_placed = active_player3.traps_placed
                  active_player3.traps_placed = 0
          elif active_player2.health <= 0:
            if active_player2.selected_weapon.name == "Holy Bible" and not active_player2.undying_will:
                  print(f"{active_player2.name} stays at 1 hp due to the Holy Bible's passive!")
                  active_player2.health = 1
                  active_player2.undying_will = True
                  if active_player2.selected_weapon.speed < active_player1.selected_weapon.speed:
                      active_player2.attackopponent(active_player1)
                  elif active_player2.selected_weapon.speed > active_player1.selected_weapon.speed:
                      active_player2.attackopponent(active_player1)
                      print(f"{active_player1.name}: {active_player1.health} HP")
                      print(f"{active_player2.name}: {active_player2.health} HP")
                      print("------------------------------")
                      if active_player1.health > 0:
                          active_player1.play_turn(active_player2)
            else:
                  print(f"{active_player2.name}'s weapon is destroyed!")
                  active_player4.weapons = active_player2.weapons
                  if not active_player2.traps_placed == 0:
                      active_player4.traps_placed = active_player2.traps_placed
                  if active_player2 == self.player10:
                    print(f"{self.player10.name}'s weapon is destroyed! This is a their final weapon, so they lose!")
                    print(f"{active_player1.name} Won!")
                    break
                  elif active_player2 == self.player8:
                    active_player2 = self.player10
                  elif active_player2 == self.player6:
                    active_player2 = self.player8
                  elif active_player2 == self.player4:
                    active_player2 = self.player6
                  elif active_player2 == self.player2:
                    active_player2 = self.player4
                  print(f"{active_player2.name}, choose your next weapon:")
                  active_player2.weapons = active_player4.weapons
                  active_player2.select_starting_weapon()
                  active_player2.traps_placed = active_player4.traps_placed
                  active_player4.traps_placed = 0
          
            
game = Game()
game.play_game()

'Shield', 310
'Grapple', 625















