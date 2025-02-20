"""游戏设定相关"""
class Settings():
    """存储《外星人入侵》的所有设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 600
        self.screen_height = 800
        self.bg_color = (159, 159, 159)
       
        
        # 子弹设置
        self.bullet_speed_factor = 10 # 子弹速度
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        
        # 敌机设置
        # 左右移动速度
        self.alien_speen_factor = 1 # 敌机左右移动速度
        # 下落速度
        self.fleet_drop_speed = 20 # 敌机下落速度
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

        # 玩家设置
        # 玩家生命值
        self.ship_limit=3
        # 移动速度
        self.ship_speed_factor = 3 