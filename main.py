"""主程序"""
import pygame
import asyncio
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from ship import Ship
from enemy import Enemy
from button import Button
import game_functions as gf

async def main():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    print(pygame)
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('飞机大战')
    
    # 创建一艘飞船
    ship = Ship(screen,ai_settings)
    enemy = Enemy(screen,ai_settings)
    # 创建一个管理游戏统计信息
    stats = GameStats(ai_settings)

    
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个用于存储敌机的编组
    aliens = Group()
    # 创建敌机群
    gf.create_fleet(screen,ai_settings,aliens,ship)

    
    clock = pygame.time.Clock()
    last_time = pygame.time.get_ticks()

    # 创建开始按钮
    play_button=Button(ai_settings,screen,'Play')
    # 创建向左按钮
    left_button=Button(ai_settings,screen,'<',80,160)
    left_button.msg_image_rect.centerx=50
    left_button.msg_image_rect.centery=600
    left_button.rect.centerx=50
    left_button.rect.centery=600

    # 创建向右按钮
    right_button=Button(ai_settings,screen,'>',80,160)
    right_button.msg_image_rect.centerx=screen.get_rect().width-50
    right_button.msg_image_rect.centery=600
    right_button.rect.centerx=screen.get_rect().width-50
    right_button.rect.centery=600

    
    # 开始游戏的主循环
    while True:
        current_time = pygame.time.get_ticks()
        # 监听键盘和鼠标事件
        gf.check_events(screen,ai_settings,ship,enemy,aliens,bullets,stats,play_button,left_button,right_button)
        if stats.game_active:
            ship.update()
            # enemy.update()
            # 子弹更新的操作
            gf.update_bullets(screen,ai_settings,ship,bullets,aliens)
            # 更新敌机
            gf.update_aliens(screen,ai_settings,ship,aliens,bullets,stats)
        
        # 每次循环时都重绘屏幕
        gf.update_screen(screen,ai_settings,ship,enemy,bullets,aliens,current_time,stats,play_button,left_button,right_button)


        # 更新状态
        last_time = current_time
    
        # 控制游戏循环的帧率
        clock.tick(60)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())