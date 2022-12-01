import pygame
pygame.mixer.init()
class playmain():
    
    def Play_Close_Sound(self):
        OpenCPlayer = pygame.mixer.Sound("./data/sound/" + "shutter_close.wav")
        OpenCPlayer.play()
        
    def Play_Open_Sound(self):
        OpenCPlayer = pygame.mixer.Sound("./data/sound/" + "shutter_open.wav")
        OpenCPlayer.play()
    
    def Play_Change_Sound(self):
        SoundPlayer = pygame.mixer.Sound("./data/sound/g_ui_btn_n.wav")
        SoundPlayer.play()
    
    def Play_Song_Confirm(self):
        SoundPlayer = pygame.mixer.Sound("./data/sound/song_confirm.wav")
        SoundPlayer.set_volume(4)
        SoundPlayer.play()
    
    def Play_Hit_Sound(self):
        SoundPlayer = pygame.mixer.Sound("./data/sound/arc.wav")
        SoundPlayer.play()
    
    def Play_Lost_Sound(self):
        SoundPlayer = pygame.mixer.Sound("./data/sound/g_ui_back.wav")
        SoundPlayer.play()
    
    def Play_Beat_Sound(self):
        SoundPlayer = pygame.mixer.Sound("./data/sound/tap.wav")
        SoundPlayer.set_volume(0.8)
        SoundPlayer.play()