import pygame as pg


class Timer:
    def __init__(self, frames, wait=100, frameindex=0, step=1,  # imagerect frames
                 looponce=False, wait_for_command=False, oscillating=False):
        self.frames = frames
        self.wait = wait
        self.frameindex = frameindex
        self.step = step
        self.looponce = looponce
        self.wait_for_command = wait_for_command
        self.oscillating = oscillating

        self.finished = False
        self.lastframe = len(frames) - 1 if step == 1 else 0
        self.last = None

    def frame_index(self):
        now = pg.time.get_ticks()
        if self.last is None:
            self.last = now
            self.frameindex = 0 if self.step == 1 else len(self.frames) - 1
            return 0
        elif self.wait_for_command: return self.frameindex
        elif not self.finished and now - self.last > self.wait:
            if self.looponce and self.frameindex + self.step >= self.lastframe:
                self.finished = True
            self.frameindex += self.step
            if self.oscillating:
                if self.frameindex >= self.lastframe or self.frameindex <= 0:
                    self.step *= -1
                if self.frameindex <= 0: self.frameindex = 0
                if self.frameindex >= self.lastframe: self.frameindex = self.lastframe
            else:
                self.frameindex %= len(self.frames)
            self.last = now
        return self.frameindex

    def advance_frame_index(self):
        if not self.wait_for_command or self.finished: return
        if self.looponce and self.frameindex >= self.lastframe: self.finished = True
        else:
            self.frameindex += self.step
            self.frameindex %= len(self.frames)
        self.last = pg.time.get_ticks()

    def reset(self):
        self.last = None
        self.finished = False

    def __str__(self): return 'Timer(frames=' + self.frames +\
                              ', wait=' + str(self.wait) + ', index=' + str(self.frameindex) + ')'

    def imagerect(self):
        return self.frames[self.frame_index()]


class TimerDict:
    def __init__(self, dict_frames, first_key, wait=100, looponce=False):
        self.dict_frames = dict_frames
        self.dict_timers = {}
        for k, v in self.dict_frames.items():
            self.dict_timers[k] = Timer(v)
        self.timer = self.dict_timers[first_key]
        self.key = first_key

    def switch_timer(self, key): self.key = key

    def getkey(self): return self.key

    def frame_index(self): return self.dict_timers[self.key].frame_index()

    def advance_frame_index(self): self.dict_timers[self.key].advance_frame_index()

    def reset(self): self.dict_timers[self.key].reset()

    def imagerect(self):
        timer = self.dict_timers[self.key]
        return timer.frames[timer.frame_index()]


class TimerDual:
    def __init__(self, frames1, frames2, wait1=100, wait2=100, waitBetween=300):
        self.timer1 = Timer(frames1, wait1)
        self.timer2 = Timer(frames2, wait2)
        self.waitBetween = waitBetween
        self.timer1_running = True
        self.timer = self.timer1
        self.frames = frames1
        self.frames1 = frames1
        self.frames2 = frames2
        self.last = pg.time.get_ticks()

    def frame_index(self):
        now = pg.time.get_ticks()
        if self.last is None:
            self.last = now
            return 0
        elif now - self.last > self.waitBetween:
            self.timer = self.timer2 if self.timer1_running else self.timer1
            self.frames = self.frames2 if self.timer1_running else self.frames1
            self.timer1_running = not self.timer1_running
            self.last = now
        return self.timer.frame_index()

    def reset(self):
        self.last = None
        self.timer1_running = False

    def imagerect(self):
        return self.frames[self.frame_index()]
