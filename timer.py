import pygame as pg


class Timer:
  def __init__(self, image_list, start_index=0, delay=100, is_loop=True): 
    self.image_list = image_list
    self.delay = delay 
    self.is_loop = is_loop
    self.last_time_switched = pg.time.get_ticks()
    self.frames = len(image_list)
    self.index = start_index if start_index < len(image_list) - 1 else 0
    self.start_index = start_index
    
  def next_frame(self): 
    now = pg.time.get_ticks()
    if now - self.last_time_switched > self.delay:
      self.index += 1
      if self.is_loop: self.index %= self.frames
      self.last_time_switched = now

  def is_expired(self):
    return not self.is_loop and self.index >= len(self.image_list) - 1

  def image(self): 
    self.next_frame()
    return self.image_list[self.index]

  def reset(self):
    self.index = self.start_index if self.start_index < len(self.image_list) - 1 else 0

    