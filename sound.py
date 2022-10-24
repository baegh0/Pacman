import pygame as pg
import time

# from my last project, please update with new sounds here!

class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.3)
        startup_sound = pg.mixer.Sound('sounds/pacman_eatfruit.wav')
        levelup_sound = pg.mixer.Sound('sounds/pacman_eatfruit.wav')
        runningaway_sound = pg.mixer.Sound('sounds/pacman_intermission.wav')
        eating_sound = pg.mixer.Sound('sounds/pacman_chomp.wav')
        self.sounds = {'startup': startup_sound, 'levelup': levelup_sound, 'eating': eating_sound, 
                        'runningaway': runningaway_sound}

    def play_bg(self):
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()

    def eatingsfx(self): pg.mixer.Sound.play(self.sounds['eating'],)
    def startupsfx(self): pg.mixer.Sound.play(self.sounds['startup'])
    def runningawaysfx(self): pg.mixer.Sound.play(self.sounds['runningaway'])
    def levelupsfx(self): pg.mixer.Sound.play(self.sounds['levelup'])

    def gameover(self): 
        self.stop_bg() 
        pg.mixer.music.load('sounds/pacman_death.wav')