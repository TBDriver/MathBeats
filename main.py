if __name__ == "__main__":
    from time import sleep,gmtime
    from math import pow
    import os,pygame,random # ,bezier
    from sys import exit
    import threading
    pygame.init()
    
    # 加载文件
    # 加载存档与设置
    # 存档文件夹
    try:    os.mkdir(".\config")
    except: pass
    try:    os.mkdir(".\data")
    except: pass
    try:    os.mkdir(".\cache")
    except: pass
    with open(".\config\config.mb","r+") as f:
        READ_CONFIG_DATA = f.read() # 读取设置
        CONFIG_DATA = READ_CONFIG_DATA.split("\n")
    with open(".\config\save.mb","r+") as f:
        global Save_Time
        Save_Time = gmtime(os.path.getmtime(".\config\save.mb"))
    
    # 加载歌曲
    global Song_List
    Song_List = []
    Score_List = []
    Songs = os.listdir(".\data\music")
    for i in range(len(Songs)): # 查找歌曲
        Song_List.append([]) # 增加一首歌的槽位
        Score_List.append([]) # 增加一首歌的铺面
        with open(".\data\music\\" + Songs[i-1] + "\song.ini",encoding='utf-8') as f:
            for line in f:
                Song_List[i].append(line.strip())
        with open(".\data\music\\" + Songs[i-1] + ".\score",encoding="utf-8") as f:
            Local_Operation = 0 # 当前读取铺面note
            for line in f:
                if line.strip() == "start":
                    # 开始读取铺面Local Note
                    Score_List[i].append([]) # 当前铺面第i-1个note
                elif line.strip() == "stop":
                    Local_Operation += 1 # 读取完成
                else:
                    Score_List[i][Local_Operation].append(line.strip()) # 谱堆 谱面 note
        
    '''
    | 歌曲信息 - song.ini
    第12行: 歌曲名及所占字符数
    第34行: 作者名及所占字符数
    第56行: 铺师名及所占字符数
    第78行: 歌曲难度
    第9行:  BPM
========================================
    | 铺面信息 - score
    使用方法：
    Score_List[谱面索引][Note索引][操作]
    
    操作对应：
    0  开始时间(ms)
    1     题目
    2  题目所占字符      共6项
    3     结果
    4     拍数
    5  每拍时间(ms)
    '''
    
    
    class MathBeats():
        def __init_fonts(self):
            pygame.font.init() # 文字库初始化
            self.titleFont = pygame.font.Font(".\data\\ttf\\方正准雅宋简体.TTF",50)
            
            
            
        def __init__(self):
            self.Main_Screen = pygame.display.set_mode(size=(1054,600))
            self.Game_State = "start"
            self.Game_FPS = 120    # FPS
            self.Game_Tick = pygame.time.Clock()
            self.Antialias = False # 抗锯齿
            self.LastM1 = 0
            self.LastM2 = 0
            self.__init_fonts()  # 字体初始化
            pygame.display.set_caption("Mathbeats")
            # self.Update_Smooth()
        
        '''
        摆了 会用公式不知道怎么应用
        
        def Update_Smooth(self):
            # 模拟三次贝塞尔函数 用于进行平滑展示
            # 相当于css的ease
            # 遮罩层平滑   0.42, 0, 0.58, 1       较慢 ease-in-out
            # 自创滑块平滑 0.6, 0.65, 0.35, 0.94 较快
            self.Mask_Smooth   = bezier.Calculator_bezier(0.42, 0,    0.58, 1,    self.Game_FPS)
            self.Slider_Smooth = bezier.Calculator_bezier(0.6,  0.65, 0.35, 0.94, self.Game_FPS)
        '''
        
        def Start_Screen(self):
            keep_screen = True
            while keep_screen:
                self.Main_Screen.fill((34,40,49))
                # Load title image
                Title_img = pygame.transform.scale(pygame.image.load(".\data\img\Title.png"),(400,400))
                self.Main_Screen.blit(Title_img,(307,50))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        #卸载所有模块
                        pygame.quit()
                        #终止程序，确保退出程序
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.Game_State = "play" # 目前直接衔接到游玩系统
                        keep_screen = False
                        break # 退出循环因为标题画面已关    
                    
                self.Game_Tick.tick(self.Game_FPS)
                pygame.display.flip() #更新屏幕内容
        
        def Rendering(self):
            '''
            按照顺序渲染游戏
            防止出现顺序错误
            '''

            
            
        
        def beforeChangeTo(self):
            def __change_temp():
                # To do:减少时间 太慢了哈哈哈哈
                Masks_img_1 = pygame.image.load(".\data\img\Mask1.png")
                Masks_img_2 = pygame.image.load(".\data\img\Mask2.png")
                '''
                一个大坑,是类似于Arc的平滑移动
                
                sMask1_x = -670 # 基本值
                sMask2_x = 1736
                
                Mask1_x = -670
                Mask2_x = 1736
                temptick = 0
                Mask_state = "right"
                while True:
                    print("Mask1_x:" + str(Mask1_x))
                    print("Mask2_x:" + str(Mask2_x))
                    
                    self.Main_Screen.blit(Masks_img_1,(Mask1_x,0))
                    self.Main_Screen.blit(Masks_img_2,(Mask2_x,0))
                    
                    if Mask1_x >= 527:
                        Mask_state = "left"
                        temptick = 0         
                    if Mask_state == "right":
                        Mask1_x = Mask1_x + 670 * int(self.Mask_Smooth[temptick])
                        Mask2_x = sMask2_x * (1 - self.Mask_Smooth[temptick])
                        temptick += 1  
                    if Mask_state == "left":
                        print(self.Mask_Smooth)
                        Mask1_x = Mask1_x - 670 * self.Mask_Smooth[temptick]
                        Mask2_x = sMask2_x * (1 - self.Mask_Smooth[temptick])
                        temptick += 1
                        
                    self.Game_Tick.tick(self.Game_FPS)
                    pygame.display.flip() #更新屏幕内容
            '''
                
                Mask1_x = -810
                Mask2_x = 880
                while True:
                    self.Main_Screen.fill((34,40,49))
                    if Mask1_x >= 0:
                        sleep(0.2)
                        self.LastM1 = Mask1_x
                        self.LastM2 = Mask2_x
                        break
                    Mask1_x += 5
                    Mask2_x -= 5

                    
                    self.Main_Screen.blit(Masks_img_1,(Mask1_x,0))
                    self.Main_Screen.blit(Masks_img_2,(Mask2_x,0))
                    self.Game_Tick.tick(self.Game_FPS)
                    pygame.display.update() #更新屏幕内容
            _temp_thread = threading.Thread(target=__change_temp) # 多线程的原因是后台还得接着加载 不能耽误工作
            _temp_thread.start()    
        def afterChangeTo(self,pre_function):
            def __change_temp():
                sleep(0.2)
                Masks_img_1 = pygame.image.load(".\data\img\Mask1.png")
                Masks_img_2 = pygame.image.load(".\data\img\Mask2.png")
                Mask1_x = self.LastM1
                Mask2_x = self.LastM2
                
                while True:
                    
                    self.Main_Screen.fill((34,40,49))
                    pre_function()
                    if Mask1_x <= -810:
                        break
                    Mask1_x -= 5
                    Mask2_x += 5
                    
                    self.Main_Screen.blit(Masks_img_1,(Mask1_x,0))
                    self.Main_Screen.blit(Masks_img_2,(Mask2_x,0))
                    
                    self.Game_Tick.tick(self.Game_FPS)
                    pygame.display.update() #更新屏幕内容
                    
            _temp_thread = threading.Thread(target=__change_temp)
            _temp_thread.start()
            
        def Main_Screen(self):
            self.beforeChangeTo()
            sleep(3)
            def _render_start_game():
                # _render_start_game作为加载时预处理的图像
                self.Main_Screen.blit(self.titleFont.render("开始游戏", True, (255,255,255)),(200,200))
            
            
            
            self.afterChangeTo(_render_start_game)
            sleep(4)
            #startGame = 
            while True:
                self.Main_Screen.fill((34,40,49))
                
                titleFont = pygame.font.Font(".\\data\\ttf\\方正准雅宋简体.TTF",50)
                self.Main_Screen.blit(titleFont.render("开始游戏", True, (255,255,255)),(200,200))
                
                
                self.Game_Tick.tick(self.Game_FPS)
                pygame.display.update()
                
            
            #startGameRect = startGame.get_rect()
            #startGameRect.center = (300,200)
            #self.Main_Screen.blit(startGameRect)
            while True:
                pass
        
        
        def Keep_Flip(self):
            while True:
                # 游戏状态为 开始游戏 
                if self.Game_State == "start":
                    self.Start_Screen() # 进入开始屏幕的循环
                if self.Game_State == "play":
                    self.Main_Screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        #卸载所有模块
                        pygame.quit()
                        #终止程序，确保退出程序
                        exit()
                        
                self.Game_Tick.tick(self.Game_FPS)
                pygame.display.flip() #更新屏幕内容
                
                
        def start(self):
            self.Keep_Flip()
    SYSTEM_MAIN = MathBeats()
    SYSTEM_MAIN.start()