import pygame.font


class Button:
    """按钮类"""

    def __init__(self, screen, msg):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (180, 180, 180)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont('华文彩云', 40)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # 按钮文本
        self.msg = msg
        self.msg_image, self.msg_image_rect = None, None
        self.prep_msg()

    def prep_msg(self):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(self.msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制按钮"""
        # 绘制一个用颜色填充的圆角矩形按钮，再绘制文本
        pygame.draw.rect(self.screen, self.button_color, self.rect, border_radius=30)
        self.screen.blit(self.msg_image, self.msg_image_rect)
