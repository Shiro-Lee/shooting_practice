import pygame

# 初始化混音器
pygame.mixer.init()

# 开火音效
fire_sound = pygame.mixer.Sound('sounds/fire.ogg')
# 护盾击破音效
shield_broken_sound = pygame.mixer.Sound('sounds/shield_broken.ogg')
# 靶机击破音效
target_broken_sound = pygame.mixer.Sound('sounds/target_broken.ogg')

# 背景音乐
pygame.mixer.music.load('sounds/bgm.wav')
