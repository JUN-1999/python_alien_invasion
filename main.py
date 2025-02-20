"""主程序"""
import pygame
import asyncio
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from ship import Ship
from enemy import Enemy
import game_functions as gf

async def main():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    print(pygame)
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    print(dir(screen))
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
    
    # 开始游戏的主循环
    while True:
        # 监听键盘和鼠标事件
        gf.check_events(screen,ai_settings,ship,enemy,bullets)
        ship.update()
        # enemy.update()
        # 子弹更新的操作
        gf.update_bullets(screen,ai_settings,ship,bullets,aliens)
        # 更新敌机
        gf.update_aliens(screen,ai_settings,ship,aliens,bullets,stats)
        # 每次循环时都重绘屏幕
        gf.update_screen(screen,ai_settings,ship,enemy,bullets,aliens)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())