from time import sleep

import pygame


class Service(object):

    def __init__(self):
        pygame.mixer.init()
        self.value = 0.5

    def play_music(self, music_path):
        try:
            print(music_path)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()
            return True
        except Exception as ex:
            return False

    def stop_music(self):
        pygame.mixer.music.stop()

    def suspend_music(self):
        pygame.mixer.music.pause()

    def UNsuspend_music(self):
        pygame.mixer.music.unpause()

    def volume_up(self):
        self.value += 0.1
        if self.value >= 1:
            self.value = 1
        pygame.mixer.music.set_volume(self.value)
        print("音量:", self.value)

    def volume_Down(self):
        self.value -= 0.1
        if self.value <= 0:
            self.value = 0
        pygame.mixer.music.set_volume(self.value)
        print("音量:", self.value)

    def mute_music(self):
        pygame.mixer.music.set_volume(0)

    def UNmute_music(self):
        pygame.mixer.music.set_volume(self.value)


if __name__ == "__main__":
    pass
    # service = Service()
    # print(service.play_music("cache/阿冷 - 春风吹.jh"))
    # sleep(30)