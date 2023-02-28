# -*- coding:utf-8 -*-

from time import sleep, gmtime
from sys import exit
from mutagen.mp3 import MP3
import os, pygame, threading, json  # ,bezier
from InputRect import InputBox      # 输入框模块 灵感来自网络

pygame.init()
# 加载文件,存档与设置
try:
    os.mkdir(".\config")
except:
    pass
try:
    os.mkdir(".\data")
except:
    pass
try:
    os.mkdir(".\cache")
except:
    pass
with open(".\config\config.mb", "r+") as f:
    READ_CONFIG_DATA = f.read()  # 读取设置
    CONFIG_DATA = READ_CONFIG_DATA.split("\n")
with open(".\config\save.mb", "r+") as f:
    global Save_Time
    Save_Time = gmtime(os.path.getmtime(".\config\save.mb"))


# 加载歌曲
global Song_List
Song_List = []
Score_List = []
Songs = os.listdir(".\data\music")
for i in range(len(Songs)):  # 查找歌曲
    Song_List.append([])  # 增加一首歌的槽位
    with open(".\data\music\\" + Songs[i-1] + "\song.ini", encoding='utf-8') as f:
        for line in f:
            Song_List[i].append(line.strip())
    with open(".\data\music\\" + Songs[i-1] + ".\score.json", encoding="utf-8") as f:
        Score_List.append(json.load(f))
        print(Score_List)
        print(Song_List)

'''
| 歌曲信息 - song.ini
第1行: 歌曲名
第2行: 作者名
第3行: 铺师名
第4行: 歌曲难度
第5行:  BPM
========================================
| 铺面信息 - score
使用方法：
Score_List[谱面索引 -> int] -> 锁定歌曲
            [Note索引 -> str] -> 锁定音符
            [Note信息 -> int] -> 锁定信息
Note信息 对应:
0 字典   每拍间隔
1 字符串 题目
2 布尔值 正确与否
3 字符串 特殊动作
'''


class MathBeats():
    # 预处理
    def __returnSaveNone(self):
        '''返回空函数的函数,无实际意义'''
        def ___None():
            pass
        return ___None
    def __fontInit(self):
        '''字体路径初始化'''
        self.z准雅宋 = ".\\data\\ttf\\方正准雅宋简体.ttf"
        self.notoSansHansBold = ".\\data\\ttf\\NotoSansHans-Bold.otf"
        self.notoSansHansLight = ".\\data\\ttf\\NotoSansHans-Light.otf"
        self.notoSansHansRegular = ".\\data\\ttf\\NotoSansHans-Regular.otf"
        self.s狮尾四季春 = ".\\data\\ttf\\狮尾四季春-Regular.ttf"
    def __eventBusyOrNot(self, event: int):
        '''
        检测时间栈是否繁忙 返回0或1
        event为所排除的查询事件
        '''
        for i in self.eventStack:
            if i and i != event:
                return 1
        return 0
    def __loadingButtonID(self):
        self.buttonID = []     # 按钮ID初始化
        self.buttonID.append([(44, 62, 80), (44, 62, 80), (0, 0, 0)])  # 开始游戏按钮ID
        self.buttonID.append([(44, 62, 80), (44, 62, 80), (0, 0, 0)])  # 铺面制作按钮ID
        self.buttonID.append([(44, 62, 80), (44, 62, 80), (0, 0, 0)])  # 选择歌曲返回按钮ID
        # buttonID三个元素
        for i in range(len(Song_List)): # 歌曲buttonID
            self.buttonID.append([(44, 62, 80), (44, 62, 80), (0, 0, 0)])  # 歌曲开始按钮ID
        self.buttonID.append([(44, 62, 80), (44, 62, 80), (0, 0, 0)])  # 铺面制作ID
        self.buttonID.append([(44, 62, 80), (44, 62, 80), (0, 0, 0)])  # 继续制作ID
    def __loadingPictures(self):
        self.songFrame = pygame.transform.scale(pygame.image.load(".\\data\\img\\frame.png").convert_alpha(), (400, 400))
        self.Title_img = pygame.transform.scale(pygame.image.load(".\data\img\Title.png").convert_alpha(), (400, 400))
        self.Masks_img_1 = pygame.image.load(".\data\img\Mask1.png").convert_alpha()
        self.Masks_img_2 = pygame.image.load(".\data\img\Mask2.png").convert_alpha()
    def __init__(self):
        self.Main_Screen = pygame.display.set_mode(size=(1054, 600), flags=pygame.DOUBLEBUF, depth=32)
        self.gameState = "start"
        self.gameFPS = 180    # FPS
        self.gameTick = pygame.time.Clock()
        self.Antialias = True  # 抗锯齿
        self.LastM1 = 0
        self.LastM2 = 0
        self.eventStack = [0, 0, 0]  # 加载等待ID

        self.__fontInit()        # 文字封装初始化
        self.__loadingButtonID() # 按钮唯一ID初始化
        self.__loadingPictures() # 图片初始化
        pygame.font.init()       # 文字库初始化
        pygame.display.set_caption("Mathbeats")
        '''
        摆了 会用公式不知道怎么应用
        
        def Update_Smooth(self):
            # 模拟三次贝塞尔函数 用于进行平滑展示
            # 相当于css的ease
            # 遮罩层平滑   0.42, 0, 0.58, 1       较慢 ease-in-out
            # 自创滑块平滑 0.6, 0.65, 0.35, 0.94 较快
            self.Mask_Smooth   = bezier.Calculator_bezier(0.42, 0,    0.58, 1,    self.gameFPS)
            self.Slider_Smooth = bezier.Calculator_bezier(0.6,  0.65, 0.35, 0.94, self.gameFPS)
        '''

    # 过渡函数
    def _renderStartGame(self):
        # _renderStartGame作为加载时预处理的图像
        self.showAButton("开始游戏", 50, self.z准雅宋, (255, 255, 255), 420, 100,
                             self.Main_Screen, self.Antialias, 0, self.__returnSaveNone, self.buttonID[0][0])
        self.showAButton("谱面创作", 50, self.z准雅宋, (255, 255, 255), 420, 300,
                             self.Main_Screen, self.Antialias, 1, self.__returnSaveNone, self.buttonID[1][0])
    def _renderChosingGame(self):
        pass

    # 主界面
    def Start_Screen(self):
        keep_screen = True
        while keep_screen:
            self.Main_Screen.fill((34, 40, 49))
            # Load title image
            self.Main_Screen.blit(self.Title_img, (307, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.gameState = "play"  # 目前直接衔接到游玩系统
                    keep_screen = False
                    break  # 退出循环因为标题画面已关

            sleep(1/self.gameFPS)
            pygame.display.flip()  # 更新屏幕内容

    # 功能性函数
    def showAButton(self, text: int, size: str, font: str,
                    color: tuple, buttonX: int, buttonY: int, renderSurface: pygame.Surface,
                    antialias: bool, buttonID: int, functions,
                    backgroundColor: tuple = (255, 255, 255)):
        '''
        用于显示按钮
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
        buttonFont = pygame.font.Font(font, size)  # 加载字符
        renderedText = renderSurface.blit(buttonFont.render(text, antialias, color, backgroundColor), (buttonX, buttonY))  # 渲染文字
        textSize = pygame.font.Font.size(buttonFont, text)
        
        for event in pygame.event.get():
            if event.type == 1025 and renderedText.collidepoint(event.pos):
                functions()
            if event.type == 1024:
                # inTheButton = ((event.pos[0] >= buttonX) and (event.pos[0] <= buttonX + textSize[0])) and ((event.pos[1] >= buttonY) and (event.pos[1] <= buttonY + textSize[1]))
                if renderedText.collidepoint(event.pos): self.buttonID[buttonID][0] = self.buttonID[buttonID][2]   # 悬停事件
                else:           self.buttonID[buttonID][0] = self.buttonID[buttonID][1]
    def showAComboBox(self, options: list, strSize: int, boxSize: int, font: str,
                    color: tuple, boxX: int, boxY: int,
                    antialias: bool, renderSurface: pygame.Surface, tip: str, 
                    backgroundColor: tuple = (255, 255, 255)):
        '''
        用于显示按钮
        options: 选项文本      列表
        strSize: 文本大小      整型
        boxSize  下拉框大小    元组
        font: 使用字体路径     字符串
        color:文本颜色         元组    其中接受三个参数
        boxX&Y: 下拉框xy值    整型    用于按钮置放和悬停表现
        antialias: 抗锯齿与否  布尔值
        renderSurface: 作用Surface对象
        tip:     待选文字      字符串
        backgroundColor 背景色 元组
        '''
        boxFont = pygame.font.Font(font, strSize)
        self.showARect(boxX, boxY, boxSize[0], boxSize[1], color)
    def showARect(self, x: int, y: int, width: float, height: float, color: tuple):
        '''
        x    整型 Rectx值
        y    整型 Recty值
        width整型 宽度
        heigh整型 高度
        color元组 颜色Hex值
        '''
        pygame.draw.rect(self.Main_Screen, color, (pygame.Rect(x, y, width, height)))
    def beforeChangeTo(self, preFunction, *afterFunction):
        if afterFunction:
            pass
        else:
            def afterFunction():
                pass
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
            
            self.Main_Screen.blit(self.Masks_img_1,(Mask1_x,0))
            self.Main_Screen.blit(self.Masks_img_2,(Mask2_x,0))
            
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
                
            sleep(1/self.gameFPS)
            pygame.display.flip() #更新屏幕内容
        '''

        Mask1_x = -810
        Mask2_x = 880
        inWhile = True
        while inWhile:  # 不断尝试进行加载
            while (self.eventStack[0] and not (self.__eventBusyOrNot(self.eventStack[0]))):
                self.Main_Screen.fill((34, 40, 49))
                preFunction()
                if Mask1_x >= 0:
                    sleep(0.2)
                    self.LastM1 = Mask1_x
                    self.LastM2 = Mask2_x
                    inWhile = False
                    self.eventStack[0] = 0
                    break
                Mask1_x += 820/self.gameFPS
                Mask2_x -= 800/self.gameFPS
                
                self.Main_Screen.blit(self.Masks_img_1, (Mask1_x, 0))
                self.Main_Screen.blit(self.Masks_img_2, (Mask2_x, 0))
                sleep(1/self.gameFPS) # 限制FPS 每秒刷新self.gameFPS次 也就是每刷新一次等待1/self.gameFPS秒
                pygame.display.flip()  # 更新屏幕内容
        afterFunction()  
    def afterChangeTo(self, preFunction, *afterFunctions):
        if afterFunctions:
            pass
        else:
            def afterFunctions():
                pass
        Mask1_x = self.LastM1
        Mask2_x = self.LastM2
        inWhile = True
        while inWhile:
            while self.eventStack[1] and not (self.__eventBusyOrNot(self.eventStack[1])):
                self.Main_Screen.fill((34, 40, 49))
                preFunction()
                if Mask1_x <= -810:
                    inWhile = False
                    self.eventStack[1] = 0
                    break
                Mask1_x -= 820/self.gameFPS
                Mask2_x += 800/self.gameFPS

                self.Main_Screen.blit(self.Masks_img_1, (Mask1_x, 0))
                self.Main_Screen.blit(self.Masks_img_2, (Mask2_x, 0))

                sleep(1/self.gameFPS)
                pygame.display.flip()  # 更新屏幕内容
        afterFunctions()
    def selectSongReturnToTheMainScreen(self):
        '''
        # 6
        '''
        self.selectSongWhileLock = False
        self.mainScreenLock = True
        self.eventStack[0] = 1
        self.beforeChangeTo(self.__returnSaveNone)
        self.eventStack[1] = 1
        sleep(0.005)
        self.afterChangeTo(self._renderStartGame)
    def editorMainScreenReturnToTheMainScreen(self):
        self.mainScreenLock = True
        self.editorWhile = False
        self.eventStack[0] = 1
        self.beforeChangeTo(self._renderEditor)
        self.eventStack[1] = 1
        sleep(0.005)
        self.afterChangeTo(self._renderStartGame)
    
    # 界面
    def Main_Screen_(self):
        '''主界面'''
        self.mainScreenLock = True
        self.eventStack[0] = 1
        self.beforeChangeTo(self.__returnSaveNone)
        self.eventStack[1] = 1
        self.afterChangeTo(self._renderStartGame)

        while self.mainScreenLock:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()
                    
            self.Main_Screen.fill((34, 40, 49))
            self.showAButton("开始游戏", 50, self.z准雅宋, (255, 255, 255), 420, 100,
                             self.Main_Screen, self.Antialias, 0, self.selectSong, self.buttonID[0][0])
            
            self.showAButton("谱面创作", 50, self.z准雅宋, (255, 255, 255), 420, 300,
                             self.Main_Screen, self.Antialias, 1, self.editorMainScreen, self.buttonID[1][0])
            
            
            sleep(1/self.gameFPS)
            pygame.display.flip()
    def selectSong(self):
        '''歌曲选择'''
        self.mainScreenLock = False
        self.eventStack[0] = 1
        self.beforeChangeTo(self._renderStartGame)
        self.eventStack[1] = 1
        self.afterChangeTo(self._renderChosingGame)
        songFrame = pygame.transform.scale(pygame.image.load(".\\data\\img\\frame.png").convert_alpha(), (400, 400))
        self.selectSongWhileLock = True
        while self.selectSongWhileLock:
            self.Main_Screen.fill((34, 40, 49))
                
            for i in range(len(Song_List)):
                # 歌曲框
                self.Main_Screen.blit(songFrame, (320 * i, 100))
                
                # 歌曲标题
                if i == 0:
                    self.Main_Screen.blit((pygame.font.Font(self.z准雅宋, 35)).render(Song_List[i][0], self.Antialias, (202, 207, 210)), (125, 140))  # 渲染文字
                else:
                    self.Main_Screen.blit((pygame.font.Font(self.z准雅宋, 35)).render(Song_List[i][0], self.Antialias, (202, 207, 210)), (
                        110 * (i+1) + (pygame.font.Font.size(pygame.font.Font(self.z准雅宋, 35), Song_List[i-1][0]))[0], 140))  # 渲染文字
                    
                # 游玩按钮
                if i == 0 :
                    self.showAButton("  →  ", 35, self.notoSansHansBold, (202, 207, 210),
                                    180 # 300 * (i+1) - (pygame.font.Font.size(pygame.font.Font(self.z准雅宋, 35), "Start→"))[0]
                                    , 430, self.Main_Screen, self.Antialias, i+3, self.getIntoGame, self.buttonID[i+3][0])
                else:
                    self.showAButton("  →  ", 35, self.notoSansHansBold, (202, 207, 210),
                                    320 * (i+1) - 140 # 300 * (i+1) - (pygame.font.Font.size(pygame.font.Font(self.z准雅宋, 35), "Start→"))[0]
                                    , 430, self.Main_Screen, self.Antialias, i+3, self.getIntoGame, self.buttonID[i+3][0])
            
            # 返回
            self.showAButton(" ← ", 40, self.notoSansHansBold, (202, 207, 210), 20, 20, self.Main_Screen, self.Antialias, 2, self.selectSongReturnToTheMainScreen, self.buttonID[2][0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()
            sleep(1/self.gameFPS)
            pygame.display.update()

    # 铺面制作
    def _renderEditor(self):
        self.showAButton("新建谱面", 70, self.z准雅宋, (255, 255, 255), 100, 200, self.Main_Screen
                             , self.Antialias, len(Song_List) + 3, self.__returnSaveNone, self.buttonID[len(Song_List) + 3][0])
        self.showAButton("继续创作", 70, self.z准雅宋, (255, 255, 255), 100, 380, self.Main_Screen
                             , self.Antialias, len(Song_List) + 4, self.__returnSaveNone, self.buttonID[len(Song_List) + 4][0])
    def editorMainScreen(self):
        self.editorWhile = True
        self.mainScreenLock = False
        self.eventStack[0] = 1
        self.beforeChangeTo(self._renderStartGame)
        pygame.display.set_caption("Mathbeats 铺面制作器")
        self.eventStack[1] = 1
        self.afterChangeTo(self._renderEditor)
        
        while self.editorWhile:
            self.Main_Screen.fill((34, 40, 49))
            self.showAButton("新建谱面", 70, self.z准雅宋, (255, 255, 255), 100, 200, self.Main_Screen
                             , self.Antialias, len(Song_List) + 2, self.createNewScore, self.buttonID[len(Song_List) + 2][0])
            self.showAButton("继续创作", 70, self.z准雅宋, (255, 255, 255), 100, 380, self.Main_Screen
                             , self.Antialias, len(Song_List) + 3, self.continueWork, self.buttonID[len(Song_List) + 3][0])
            
            # 返回
            self.showAButton(" ← ", 40, self.notoSansHansBold, (202, 207, 210), 20, 20, self.Main_Screen, self.Antialias, 2, self.editorMainScreenReturnToTheMainScreen, self.buttonID[2][0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()
            sleep(1/self.gameFPS)
            pygame.display.update()
    def createNewScore(self):
        self.tempScore = {}
        self.editScore(self.tempScore,[None, None, None, None, None])
    def continueWork(self):
        pass
    def editScore(self,Score: dict,Inf: list):
        '''
        Score 铺面   字典
        Inf 歌曲信息 列表
            ->[name, author, geneticist, bpm, song]
            其中song为歌曲全路径
        '''
        self.editScoreWhile = True
        
        # 谱面信息参数未指定处理
        unknownInf = ["未命名歌曲", "未命名曲师", "未命名谱师", 200, ""]
        for i in range(len(Inf)):
            if Inf[i] == None:  Inf[i] = unknownInf[i]
        # 追加歌曲时长
        if Inf[4] == "":    Inf.append(30)
        else:               Inf.append(MP3(Inf[4]).info.length)
        
        # 输入框初始化
        beatInputBox = InputBox(pygame.Rect      (15, 160, 140, 32))
        beatPerSecInputBox = InputBox(pygame.Rect(15, 230, 140, 32))
        
        # 字体预载
        tipFont = pygame.font.Font(self.s狮尾四季春, 26)
        
        while self.editScoreWhile:
            self.Main_Screen.fill((34, 40, 49))
            # 歌曲进度条
            self.showARect(0, 0, 1054 ,130, (23, 76, 89))
            
            # 谱面制作组件
            beatInputBox.draw(self.Main_Screen)
            beatPerSecInputBox.draw(self.Main_Screen)
            
            # 提示文字
            self.Main_Screen.blit(tipFont.render("当前Note拍数", self.Antialias, (255, 255, 240)), (13, 125))
            self.Main_Screen.blit(tipFont.render("当前Note每拍间隔(ms)", self.Antialias, (255, 255, 240)), (13, 195))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()
                beatInputBox.dealEvent(event)  # 拍数
                beatPerSecInputBox.dealEvent(event)  # 每秒间隔
            
            # 获取信息
            beatInputBox.getText()
            beatPerSecInputBox.getText()
            sleep(1/self.gameFPS)
            pygame.display.flip()
        
    # 游玩
    def getIntoGame(self):
        '''
        你先别急
        如函数名
        '''
        pass
    
    
    
    # 基本函数
    def Keep_Flip(self):
        while True:
            # 游戏状态为 开始游戏
            if self.gameState == "start":
                self.Start_Screen()  # 进入开始屏幕的循环
            if self.gameState == "play":
                self.Main_Screen_()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()

            sleep(1/self.gameFPS)
            pygame.display.flip()  # 更新屏幕内容
    def start(self):
        self.Keep_Flip()


if __name__ == "__main__":
    SYSTEM_MAIN = MathBeats()
    SYSTEM_MAIN.start()
