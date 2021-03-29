import pygame
from button import Button


class TextBox:
    """玩家名输入框"""

    def __init__(self, screen, stats, start_game=None, *args):
        self.width, self.height = 300, 50
        self.text = ''
        self.notice_text = 'Input your name:'
        self.text_font = pygame.font.SysFont('华文琥珀', 32)
        self.notice_text_font = pygame.font.SysFont('华文琥珀', 28)
        self.text_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.screen = screen
        self.stats = stats
        self.screen_rect = screen.get_rect()
        self.text_image, self.text_rect = None, None
        self.start_game = start_game
        self.length = 0
        self.max_length = 10    # 玩家id最长为10个字符
        self.args = args

        # 创建文本框的rect对象，并使其居中
        self.box_rect = pygame.Rect(0, 0, self.width, self.height)
        self.box_rect.center = self.screen_rect.center
        self.prep_text()

        # 创建开始按钮，放在文本框下方
        self.play_button = Button(screen, '- Play -')
        self.play_button.rect.centerx = self.box_rect.centerx
        self.play_button.rect.top = self.box_rect.bottom + 10
        self.play_button.prep_msg()

        # 提示输入玩家名，放在文本框上方
        self.notice_text_image = self.notice_text_font.render(self.notice_text, True, self.text_color, None)
        self.notice_text_rect = self.notice_text_image.get_rect()
        self.notice_text_rect.centerx = self.box_rect.centerx
        self.notice_text_rect.bottom = self.text_rect.top - 15

    def prep_text(self):
        """将输入玩家名转化为图像"""
        self.text_image = self.text_font.render(self.text, True, self.text_color, self.bg_color)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.box_rect.center

    def draw_text_box(self):
        """绘制玩家名输入框"""
        self.screen.blit(self.notice_text_image, self.notice_text_rect)
        if self.bg_color is not None:
            self.screen.fill(self.bg_color, self.box_rect)
        self.screen.blit(self.text_image, self.text_rect)

    def key_down(self, event):
        """响应按键"""
        key = event.key
        if key == pygame.K_BACKSPACE:   # 退格键
            self.text = self.text[:-1]
            self.length -= 1
        elif key == pygame.K_RETURN:    # 回车键
            if self.text != '':   # 按下回车且输入玩家昵称不为空时开始游戏
                self.stats.player_name = self.text
                self.start_game(*self.args)
        elif event.unicode != '':   # 输入字符
            if self.length < self.max_length:
                char = event.unicode
                self.length += 1
                self.text += char
