import pygame
from os import path

# 初始化混音器
pygame.mixer.init()
dir_path = path.dirname(path.abspath(__file__))

# 开火音效
fire_sound = pygame.mixer.Sound(dir_path + r'\sounds\fire.wav')
# 护盾击破音效
shield_broken_sound = pygame.mixer.Sound(dir_path + r'\sounds\shield_broken.wav')
# 靶机击破音效
target_broken_sound = pygame.mixer.Sound(dir_path + r'\sounds\target_broken.wav')

# 背景音乐
pygame.mixer.music.load(dir_path + r'\sounds\bgm.wav')
