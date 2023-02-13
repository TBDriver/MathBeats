if __name__ == "__main__":
    from time import sleep,gmtime
    import os,pygame,random # ,bezier
    from sys import exit
    import threading
    import widgets
    pygame.init()
    Widgets = widgets.MathBeatsWidgets()
    
    
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
        def __returnPass(self):
            '''
            返回pass的函数,无实际意义
            '''
            def return_():
                pass
            return return_
        def __fontInit(self):
            # 字体简称
            self.z准雅宋 = ".\\data\\ttf\\方正准雅宋简体.ttf"
            self.notoSansHansBold = ".\\data\\ttf\\NotoSansHans-Bold.otf"
            self.notoSansHansLight = ".\\data\\ttf\\NotoSansHans-Light.otf"
            self.notoSansHansRegular = ".\\data\\ttf\\NotoSansHans-Regular.otf"
            
        def __init__(self):
            self.Main_Screen = pygame.display.set_mode(size=(1054,600))
            self.Game_State = "start"
            self.Game_FPS = 120    # FPS
            self.Game_Tick = pygame.time.Clock()
            self.Antialias = True # 抗锯齿
            self.LastM1 = 0
            self.LastM2 = 0
            
            self.buttonID = [] # 按钮ID初始化
            self.__fontInit()  # 文字封装初始化
            pygame.font.init() # 文字库初始化
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
        
        def showAButton(self, text: int, size: str, font: str, color: tuple, buttonX: int, buttonY: int, renderSurface: pygame.Surface, antialias: bool, buttonID: int, functions =__returnPass, backgroundColor: tuple = (255,255,255)):
            '''
            text: 按钮文本         字符串
            size: 文本大小         整型
            font: 使用字体路径     字符串
            color:文本颜色         元组    其中接受三个参数
            buttonX&Y 按钮xy值     整型    用于按钮置放和悬停表现
            antialias: 抗锯齿与否  布尔值
            buttonID: 按钮唯一ID   整型
            functions: 执行函数    函数    可选
            renderSurface: 作用Surface对象
            '''
            if not functions == self.__returnPass:
                functionToDo = functions
            else:
                def functionToDo():
                    pass
            
            buttonFont = pygame.font.Font(font,size) # 加载字符
            renderSurface.blit(buttonFont.render(text, antialias, color, backgroundColor), (buttonX,buttonY)) # 渲染文字

            
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN):
                    inTheButton = (event.pos[0] >= buttonX and event.pos[0] <= buttonX + (pygame.font.Font.size(buttonFont, text))[0]) and (event.pos[1] >= buttonY and event.pos[1] <= buttonY + (pygame.font.Font.size(buttonFont,text))[1])
                    if inTheButton: # 悬停事件
                        self.buttonID[buttonID][0] = self.buttonID[buttonID][2]
                    else:
                        self.buttonID[buttonID][0] = self.buttonID[buttonID][1]
                if event.type == pygame.MOUSEBUTTONUP and (event.pos[0] >= buttonX and event.pos[0] <= buttonX + (pygame.font.Font.size(buttonFont, text))[0]) and (event.pos[1] >= buttonY and event.pos[1] <= buttonY + (pygame.font.Font.size(buttonFont,text))[1]): # 按下按钮
                    functionToDo()
        
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
            
        def Main_Screen_(self):
            self.buttonID.append([(44, 62, 80), (44, 62, 80), (0, 0, 0)]) # 开始游戏按钮ID
            
            self.beforeChangeTo()
            sleep(2)
            def _render_start_game():
                # _render_start_game作为加载时预处理的图像
                self.showAButton("开始游戏", 50, self.z准雅宋, (255,255,255), 300, 300, self.Main_Screen, self.Antialias, 0, self.getIntoGame(0), self.buttonID[0][0])
            self.afterChangeTo(_render_start_game)
            sleep(2)
            
            
            while True:
                self.Main_Screen.fill((34,40,49))
                self.showAButton("开始游戏", 50, self.z准雅宋, (255,255,255), 300, 300, self.Main_Screen, self.Antialias, 0, self.getIntoGame(0), self.buttonID[0][0])
                self.Game_Tick.tick(self.Game_FPS)
                pygame.display.update()
                
            
            #startGameRect = startGame.get_rect()
            #startGameRect.center = (300,200)
            #self.Main_Screen.blit(startGameRect)
        
        def getIntoGame(self, songs):
            while True:
                

                self.Game_Tick.tick(self.Game_FPS)
                pygame.display.update()
            
            Score_List[songs]
            pass
        
        def Keep_Flip(self):
            while True:
                # 游戏状态为 开始游戏 
                if self.Game_State == "start":
                    self.Start_Screen() # 进入开始屏幕的循环
                if self.Game_State == "play":
                    self.Main_Screen_()
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
