import pygame
class Enemy():
    def __init__(self,screen,ai_settings):
        """初始化敌机并设置初始位置"""
        self.screen = screen
        self.ai_settings = ai_settings
        
        # 加载敌机图片并获取外接矩形
        self.image = pygame.image.load('images/enemy1.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        
        self.x=float(self.screen_rect.centerx)
        self.y=float(self.screen_rect.centery)
        
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        
    def update(self):
        if self.moving_up and self.rect.top > 0:
            self.y -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ai_settings.ship_speed_factor            
        if self.moving_left and self.rect.left > 0:
            self.x -= self.ai_settings.ship_speed_factor
        if self.moving_right and self.rect.right< self.screen_rect.right:
            self.x += self.ai_settings.ship_speed_factor
            
        # 根据self.center更新rect对象
        self.rect.centerx = self.x    
        self.rect.centery = self.y    
        
        
    def blitme(self):
        """在指定位置绘制敌机"""
        self.screen.blit(self.image, self.rect)