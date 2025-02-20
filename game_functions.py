"""游戏处理相关"""
import sys
import pygame
from time import sleep 
from bullet import Bullet
from alien import Alien

def fire_bullet(screen,ai_settings,ship,bullets):
    """发射子弹"""
    new_bullet = Bullet(ai_settings,screen,ship)
    bullets.add(new_bullet)

def check_keydown_events(screen, ai_settings,  event, ship, enemy,bullets):
    """专门处理按下操作"""
    # 按下按钮
    if event.key == pygame.K_RIGHT:
        # 向右移动飞机
        ship.moving_right = True
        enemy.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向右移动飞机
        ship.moving_left = True
        enemy.moving_left = True
    elif event.key == pygame.K_UP:
        enemy.moving_up = True
    elif event.key == pygame.K_DOWN:
        enemy.moving_down = True
    elif event.key == pygame.K_SPACE:
        # 拿下空格创建一颗子弹
        fire_bullet(screen,ai_settings,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()
              
def check_keyup_events(event,ship,enemy):
    """专门处理松开操作"""
    # 松开按钮
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
        enemy.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
        enemy.moving_left = False
    elif event.key == pygame.K_UP:
        enemy.moving_up = False
    elif event.key == pygame.K_DOWN:
        enemy.moving_down = False

def check_play_button(screen,ai_settings,ship,aliens,bullets,stats,play_button,mouse_x,mouse_y): 
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active: 
         # 隐藏光标 
        pygame.mouse.set_visible(not stats.game_active) 
        # 重置游戏状态
        stats.game_active = True 
        stats.reset_stats()

        # 清空敌机和子弹
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，让飞船居中
        create_fleet(screen,ai_settings,aliens,ship)
        ship.center_ship()

def check_left_button(screen,ai_settings,ship,aliens,bullets,stats,left_button,mouse_x,mouse_y): 
    button_clicked = left_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        ship.moving_left = True
    else:
        ship.moving_left = False
def check_right_button(screen,ai_settings,ship,aliens,bullets,stats,right_button,mouse_x,mouse_y): 
    button_clicked = right_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        ship.moving_right = True
    else:
        ship.moving_right = False
          
def check_events(screen,ai_settings,ship,enemy,aliens,bullets,stats,play_button,left_button,right_button):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(screen,ai_settings,ship,aliens,bullets,stats,play_button,mouse_x,mouse_y)
            check_left_button(screen,ai_settings,ship,aliens,bullets,stats,left_button,mouse_x,mouse_y)
            check_right_button(screen,ai_settings,ship,aliens,bullets,stats,right_button,mouse_x,mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_left_button(screen,ai_settings,ship,aliens,bullets,stats,left_button,mouse_x,mouse_y)
            check_right_button(screen,ai_settings,ship,aliens,bullets,stats,right_button,mouse_x,mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(screen,ai_settings,  event, ship, enemy,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship,enemy)
            
def update_screen(screen,ai_settings,ship,enemy,bullets,aliens,current_time,stats,play_button,left_button,right_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 判断时间戳是否到达要求，达到要求发射子弹
    if (current_time-ship.start_time_stamp) > ship.delta_time:
        ship.start_time_stamp=current_time
        fire_bullet(screen,ai_settings,ship,bullets)
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 绘制飞船和外星人
    ship.blitme()
    # enemy.blitme()
    aliens.draw(screen)

    # 如果游戏处于非活动状态，就绘制开始游戏按钮
    if not stats.game_active:
        play_button.draw_button()
    else:
        left_button.draw_button()
        right_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()
   
def update_bullets(screen,ai_settings,ship,bullets,aliens):
    """更新子弹操作"""
    # 更新子弹位置
    bullets.update()
    check_bullet_alien_collisions(screen,ai_settings,ship,bullets,aliens)
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom<0:
            bullets.remove(bullet)
            
def check_bullet_alien_collisions(screen,ai_settings,ship,bullets,aliens):    
    """响应子弹和外星人的碰撞"""
    # 子弹编组和敌机编组 碰撞测试:如果碰撞 则两个都删除
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    # 如果敌机为空，则重新生成敌机
    if len(aliens) == 0:
        # 删除现有子弹并新建一群外星人
        bullets.empty()
        ai_settings.alien_speen_factor=ai_settings.alien_speen_factor + 0.5
        ai_settings.fleet_drop_speed=ai_settings.fleet_drop_speed + 0.5
        print(ai_settings.alien_speen_factor)
        print(ai_settings.fleet_drop_speed)
        create_fleet(screen,ai_settings,aliens,ship)
        
def get_number_aliens_x(ai_settings,alien_width):
    """获得每行最多可渲染敌机数"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    # 可绘制最大敌机数量
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可以容纳几行敌机"""
    available_space_y = (ai_settings.screen_height - (3*alien_height)-ship_height)
    number_rows = int(available_space_y / ( 5 * alien_height ) )
    return number_rows

def create_alien(screen,ai_settings,aliens,alien_number,number_rows):
    """绘制敌机"""
    alien = Alien(screen,ai_settings)
    alien_width = alien.rect.width
    # 创建一个外星人并将其加入当前行
    alien.x = alien_width + 2 * alien_width * alien_number 
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * number_rows
    aliens.add(alien)

def create_fleet(screen,ai_settings,aliens,ship):
    """绘制敌机群"""
    # 创建一个敌机，并计算一行可容纳多少个敌机
    alien = Alien(screen,ai_settings)
    # 敌机间距为敌机宽度
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    # 敌机行数
    number_rows= get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    # 居中的偏移量
    # outwidth = (ai_settings.screen_width - number_aliens_x * alien_width * 2 - alien_width)/2

     # 创建第一行外星人
    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(screen,ai_settings,aliens,alien_number,number_row)

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
        
def change_fleet_direction(ai_settings,aliens):
    """改变敌机方向，并下移"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *=-1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
 
    """响应被外星人撞到的飞船""" 
    if stats.ships_left > 0:
        # 将ships_left减1 
        stats.ships_left -= 1 
        # 清空外星人列表和子弹列表
        aliens.empty() 
        bullets.empty() 
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(screen,ai_settings,aliens,ship) 
        ship.center_ship() 
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        # 游戏结束，显示
        pygame.mouse.set_visible(not stats.game_active) 


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets): 
    """检查是否有外星人到达了屏幕底端""" 
    screen_rect = screen.get_rect() 
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom: 
            # 像飞船被撞到一样进行处理 
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets) 
            break 

def update_aliens(screen,ai_settings,ship,aliens,bullets,stats):
    """更新敌机位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)