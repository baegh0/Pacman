import pygame as pg
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.4)

        start_screen = pg.mixer.Sound()
        level_up = pg.mixer.Sound()
        ghost_sound = pg.mixer.Sound()
        ghost_moving = pg.mixer.Sound() #runaway
        player_eating = pg.mixer.Sound()
        ghost_eating = pg.mixer.Sound()

        self.sounds = {'startup':start_screen, 'gameover': gameover_sound, 'ghost': ghost_sound, 'ghostmove':ghost_moving,
        'playereat':player_eating,'ghosteat':ghost_eating}

    def play_bg(self):
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()
    
    def gameover(self): 
        self.stop_bg() 
        pg.mixer.Sound.play(self.sounds['gameover'])
        self.play_bg()
        time.sleep(2.8)
