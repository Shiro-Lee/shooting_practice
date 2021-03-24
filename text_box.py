import pygame


class TextBox:

    def __init__(self, screen, stats, start_game=None, *args):
        self.width, self.height = 300, 50
        self.text = ''
        self.font = pygame.font.SysFont('arial', 32)
        self.text_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.screen = screen
        self.stats = stats
        self.screen_rect = screen.get_rect()
        self.text_image, self.text_rect = None, None
        self.box_rect = None
        self.start_game = start_game
        self.length = 0
        self.max_length = 10    # 玩家id最长为10个字符
        self.args = args

        # 创建文本框的rect对象，并使其居中
        self.box_rect = pygame.Rect(0, 0, self.width, self.height)
        self.box_rect.center = self.screen_rect.center
        self.prep_text()

    def prep_text(self):
        self.text_image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.box_rect.center

    def draw_textbox(self):
        self.screen.fill(self.bg_color, self.box_rect)
        self.screen.blit(self.text_image, self.text_rect)

    def key_down(self, event):
        key = event.key
        if key == pygame.K_BACKSPACE:   # 退格键
            self.text = self.text[:-1]
            self.length -= 1
        elif key == pygame.K_RETURN:    # 回车键
            if self.start_game and self.text != '':   # 按下回车且输入玩家昵称不为空时开始游戏
                self.stats.player_name = self.text
                self.start_game(*self.args)
        elif event.unicode != '':   # 输入字符
            if self.length < self.max_length:
                char = event.unicode
                self.length += 1
                self.text += char