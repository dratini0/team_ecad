# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 12:33:08 2017

@author: Dylan
"""

import numpy as np
import random
import math
from time import sleep

renderer = None

class Player(object):
    
    def __init__(self, portrait, Player_MAX_HP, defence, accuracy, dodge, exp, Move_list):
        self.level = math.ceil(exp+0.1/100) -1
        self.Player_MAX_HP = Player_MAX_HP
        self.Player_HP = Player_MAX_HP
        self.Player_accuracy = accuracy
        self.Player_defence =defence #all incoming attacks attenuated by (1- this)
        self.Player_dodge = dodge # all accuracies of attacks are attenduated by this
        self.game_over = False
        self.Move_list = Move_list
        self.exp = exp
        self.justdodged = False
        
        
    def Player_take_hit(self, Move, Monster):
        """codes for how Player takes hits"""
        points_lost = 0
        if(random.uniform(0, 1) < Move.accuracy*Monster.accuracy*self.Player_dodge):
            #check if attack hits
            points_lost = (1-self.Player_defence)*Move.damage
            if(random.uniform(0,1)< Move.crit_chance):
                points_lost = points_lost*3
                renderer.battle_print("The attack took you by surprise!")
            # print("You take ", round(points_lost,3), " damage")
        else:
            renderer.battle_print("You dodged the attack!")
        self.Player_HP = self.Player_HP- points_lost
        if points_lost > 0:
            renderer.damage_self(max(self.Player_HP, 0))
        if self.Player_HP<=0:
            self.game_over = True
            self.Player_HP = 0
            renderer.battle_print("The room starts to go dark, as you collapse to the ground, blood seeping out")
            renderer.battle_print("through the cracks in your armour. Game Over")
            sleep(1)
            renderer.die_self()
            
    def Player_strike(self, Move, Monster):
        
        if Move.Move_type == "attack":
            renderer.battle_print("You try to ", Move.Move_name, " the ", Monster.name)
            Monster.take_hit(self, Move)
            
        if Move.Move_type == "run":
            # print("You try to escape")
            if (random.uniform(0,1)<0.25):
                renderer.battle_print("You made it away")
                Player.game_over = True #Change this so you run away rather than die
            else:
                renderer.battle_print("Damn, that thing is persistent")
        if Move.Move_type == "dodge":
            # print("You attempt to evade their next blow")
            if(random.uniform(0,1)<0.75):
                renderer.battle_print("You dodge the blow, and manage to whack them in the process")
                Monster.take_hit(self, Move)
                self.justdodged = True # sets bool so you evade next attack
            else:
                renderer.battle_print("You weren't quite quick enough")
                self.justdodged = False
        #OTHER ATTACK TYPES TO BE ADDED
      
        
class Move(object):
    """contains data on the different types of Move/attack"""
    def __init__(self, animation, Move_name, damage, accuracy, Move_type, crit_chance):
        self.animation = animation
        self.Move_name = Move_name
        self.damage = damage
        self.accuracy = accuracy
        self.Move_type = Move_type
        self.crit_chance= crit_chance
    

class Monster(object):
    """contains information about the Monster"""
    def __init__(self, portrait, name, maxhp, exp, defence, accuracy, dodge, Move_list):
        #Movelist is list of 3 value coupoles which contain Moves,  their probabilities, and their AP's
        self.name = name
        self.hp = maxhp # current hp
        self.maxhp = maxhp # max hp
        self.exp = exp
        self.defence = defence
        self.accuracy = accuracy
        self.portrait = portrait #image for battle mode
        self.Move_list = Move_list
        self.dodge = dodge
        self.alive = True
        
    def attack(self, Player):
         chosen_attack = np.random.choice([self.Move_list[0][0], self.Move_list[1][0], self.Move_list[2][0], self.Move_list[3][0]], p=[self.Move_list[0][1], self.Move_list[1][1], self.Move_list[2][1], self.Move_list[3][1]])
         #select attack based off prbabilities
         if chosen_attack.Move_type == "attack" and self.hp>0 and Player.justdodged == False:
             renderer.battle_print("The ", self.name, " attempts to ", chosen_attack.Move_name, " you!")
             Player.Player_take_hit(chosen_attack, self)
             #OTHER ATTACK TYPES TO BE ADDED
         if(Player.justdodged == True):
            Player.justdodged == False; #resests the just dodged bool so only 1 attack is missed
    def take_hit(self, Player, Move):
        """codes for how Monster takes hits"""
        points_lost = 0
        if(random.uniform(0, 1) < Move.accuracy*Player.Player_accuracy*self.dodge):
            #check if attack hits
            points_lost = (1-self.defence)*Move.damage
            if(random.uniform(0,1)< Move.crit_chance):
                points_lost = points_lost*3
                renderer.battle_print("The attack took the ", self.name, " by surprise!")
            # print("The ", self.name, " takes ", round(points_lost,3), " damage")
        else:
            renderer.battle_print("The ", self.name, " dodged the attack!")
        self.hp -= points_lost
        if points_lost > 0:
            renderer.damage_enemy(max(self.hp, 0))
        if self.hp<=0:
            self.alive = False
            self.hp =0 
            renderer.battle_print("You defeated the ", self.name)
            Player.exp += self.exp
            renderer.die_enemy()


Bite = Move("bite.png", "bite", 3, 0.8, "attack", 0.01)

Slash = Move("slash.png", "slash", 10, 0.9, "attack", 0.05)
Stab = Move("slash.png", "stab", 20, 0.5, "attack", 0.2)
Punch = Move("punch.png", "punch", 300 , 1, "attack", 0.5)

Run = Move("run.png", "run", 0 , 0, "run", 0)
Evade = Move("evade.png", "evade", 1, 1, "dodge", 0.01)

PLAYER = Player("Player.png", 100, 0.1, 0.9, 0.9, 0, [(Slash, 10), (Stab, 10), (Punch, 10), (Evade, 10)])

scratch = Move("","Scratch",5.0,0.6,"attack",0.005)
gnaw = Move("","Gnaw",7.0,0.4,"attack",0.0)
syntax_error = Move("","Syntax Error",3.0,0.8,"attack",0.02)
unfound_function = Move("","Could not find function",5.0,0.5,"attack",0.1)
bracket_expected = Move("","} Expected",10.0,0.2,"attack",0.005)
rapid_strike = Move("","Rapid Strikes",5.0,0.9,"attack",0.2)
energy_ball = Move("","Energy Ball",8.0,0.6,"attack",0.001)
bump = Move("","Bump",1.0,0.8,"attack",0.5)
googol_strikes = Move("","Googol Strikes",5.0,0.5,"attack",1.0)
fire_breath = Move("","Fire Breath",7.0,0.75,"attack",0.05)
tail_whip = Move("","Tail Whip",3.0,0.95,"attack",0.1)
mozilla_killa = Move("","Mozilla Killa",90.0,0.5,"attack",0.0)
chroma = Move("","Chroma",8.0,0.4,"attack",0.2)
laser_beam = Move("","Laser Beam",5.0,0.9,"attack",0.01)
razer_storm = Move("","Razer Storm",10.0,0.5,"attack",0.5)
suggestion = Move("","Suggestion",2.0,0.5,"attack",0.3)
glare = Move("","Glare",1.0,0.6,"attack",0.75)
is_this_a_letter = Move("","Is this a letter?",40.0,0.7,"attack",0.005)
lag_spike = Move("","Lag Spike",7.0,0.6,"attack",0.005)
obseletion = Move("","Obsoletion",30.0,0.5,"attack",0.1)
strum = Move("","Strum",0.0,1.0,"attack",0.0)

rat = Monster("rat.pbm","Rat",20,0,0.1,0.6,0.4,[(Bite,0.4),(scratch,0.2),(gnaw,0.4),(gnaw,0.0)])
bug = Monster("insect.pbm","B.U.G",50,0,0.3,0.8,0.2,[(syntax_error,0.25),(unfound_function,0.25),(bracket_expected,0.4),(Bite,0.1)])
chrome = Monster("ball.pbm","ChrDome",100,0,0.5,0.5,0.2,[(rapid_strike,0.25),(energy_ball,0.4),(bump,0.25),(googol_strikes,0.1)])
firefox = Monster("firefox.pbm","Firefox",100,0,0.3,0.7,0.6,[(fire_breath,0.4),(tail_whip,0.2),(scratch,0.3),(mozilla_killa,0.1)])
adder = Monster("deathadder.pbm","Adder",120,0,0.1,0.7,0.3,[(bump,0.2),(chroma,0.4),(laser_beam,0.3),(razer_storm,0.1)])
clippy = Monster("clippy.pbm","Nightmare",150,0,0.25,0.5,0.2,[(suggestion,0.4),(bump,0.2),(glare,0.3),(is_this_a_letter,0.1)])
explorer = Monster("explorer.pbm","Explorer",80,0,0.1,0.4,0.1,[(lag_spike,0.4),(scratch,0.2),(gnaw,0.3),(obseletion,0.1)])
harp = Monster("magicharp.pbm","MagicHarp",1000,0,0.5,0.9,0.5,[(strum,1.0),(scratch,0.0),(gnaw,0.0),(gnaw,0.0)])

def select_attack(Player):
    # print("")
    while(1>0):
        attack = renderer.battle_input("What will you do next? ")
        for mov in Player.Move_list:
            if mov[0].Move_name == attack:
                # renderer.battle_print("")
                return mov[0]
        else:
            # print("")
            renderer.battle_print("Invalid input. Possible actions:")
            renderer.battle_print(" ".join("{}. {} ".format(i + 1, move[0].Move_name) for i, move in enumerate(Player.Move_list)))

def fight(Player, monster, renderer_):

    global renderer
    renderer = renderer_
    renderer.start_battle(monster.name, monster.portrait, Player.Player_MAX_HP, Player.Player_HP, monster.maxhp, monster.hp)
    renderer.battle_print("A " + monster.name + " is heading straight for you!")
    while (Player.game_over != True and monster.hp >0):

        attack = select_attack(Player)
        PLAYER.Player_strike(attack, monster)

        # print(monster.name, " is left with a HP of ", round(monster.hp,3))
        monster.attack(Player)
        # print("Your HP is ", round(Player.Player_HP, 3))
        # print(" ")

    Player.game_over = False

    
    