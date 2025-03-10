"""飞船相关"""
import pygame
class Ship():
    def __init__(self,screen,ai_settings):
        """初始化飞船并设置初始位置"""
        self.screen = screen
        self.ai_settings = ai_settings
        
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/player1.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.center = float(self.screen_rect.centerx)
        
        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # 移动标志
        self.moving_right = False
        self.moving_left = False

        # 射击间隔
        self.start_time_stamp = 0
        self.delta_time = 300 # 单位毫秒 时间差
        
    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        # 根据self.center更新rect对象
        self.rect.centerx = self.center
        
    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self): 
        """让飞船在屏幕上居中""" 
        self.center = self.screen_rect.centerx 