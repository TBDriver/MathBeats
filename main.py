# -*- coding:utf-8 -*-

import pygame.freetype
from sys import exit, argv
from clipboard import copy
from time import sleep, gmtime
from os import mkdir, path, listdir
from tkinter.messagebox import showinfo
import pygame, json, threading, webbrowser

from widgets import *
from scoreEditor import MathBeatsScoreEditor

pygame.init()
# 加载文件,存档与设置
for i in [".\config", ".\data", ".\cache", ".\data\img", ".\data\music", ".\data\sound", "\\ttf"]:
    if not path.isdir(i):
        mkdir(i)
with open(".\config\config.mb", "r+") as f:
    READ_CONFIG_DATA = f.read()  # 读取设置
    CONFIG_DATA = READ_CONFIG_DATA.split("\n")
with open(".\config\save.mb", "r+") as f:
    global Save_Time
    Save_Time = gmtime(path.getmtime(".\config\save.mb"))

# 加载歌曲
global Song_List
Song_List = []
Score_List = []
Songs = listdir(".\data\music")
for i in range(len(Songs)):  # 查找歌曲
    Song_List.append([])  # 增加一首歌的槽位
    with open(".\data\music\\" + Songs[i-1] + "\song.ini", encoding='utf-8') as f:
        for line in f:
            Song_List[i].append(line.strip())
    with open(".\data\music\\" + Songs[i-1] + ".\score.json", encoding="utf-8") as f:
        Score_List.append(json.load(f))
        
        

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
        self.notoSansHansRegular = ".\\data\\ttf\\NotoSansHans-Regular.otf"
        # self.notoSansHansLight = ".\\data\\ttf\\NotoSansHans-Light.otf"
        # self.s狮尾四季春 = ".\\data\\ttf\\狮尾四季春-Regular.ttf"
    def __eventBusyOrNot(self, event: int):
        '''
        检测时间栈是否繁忙 返回0或1
        event为所排除的查询事件
        '''
        for i in self.eventStack:
            if i and i != event:
                return 1
        return 0
    def __loadingPictures(self):
        self.songFrame = pygame.transform.scale(pygame.image.load(".\\data\\img\\frame.png").convert_alpha(), (400, 400))
        self.Title_img = pygame.transform.scale(pygame.image.load(".\data\img\Title.png").convert_alpha(), (400, 400))
        self.MathImg = pygame.transform.scale(pygame.image.load(".\data\img\Math.png").convert_alpha(), (400, 200))
        self.BeatsImg= pygame.transform.scale(pygame.image.load(".\data\img\Beats.png").convert_alpha(), (400, 200))
        self.songFrame = pygame.transform.scale(pygame.image.load(".\\data\\img\\frame.png").convert_alpha(), (400, 400))
        self.Mask = pygame.image.load(".\data\img\Mask.png").convert_alpha()
    def __offset(self):
        self.offset = [(0, 0), (0, 0, 0)]  # 偏移值
        '''
        [0]: 位置偏移       元组
        [1]: 色彩偏移       元组
        '''
    def __init__(self):
        self.Main_Screen = pygame.display.set_mode(size=(1054, 600), flags=pygame.DOUBLEBUF, depth=32)
        self.gameState = "start"
        self.gameFPS = 180    # FPS
        self.gameTick = pygame.time.Clock()
        self.Antialias = True  # 抗锯齿
        self.LastM1 = 0
        self.LastM2 = 0
        self.eventStack = [0, 0, 0]  # 加载等待ID
        self.version = "0.0.1"
        
        self.__fontInit()        # 文字封装初始化
        self.__loadingPictures() # 图片初始化
        self.__offset()          # 偏移值
        pygame.freetype.init()
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
        self.Main_Screen.blit(self.BeatsImg, self.BeatsImgDect)
        self.Main_Screen.blit(self.MathImg, self.MathImgDect)
        createButton("获取更新", 50, self.z准雅宋, (255, 255, 255), 420, 500,
                                self.Main_Screen, self.Antialias, self.checkUpdate)
        createButton("谱面创作", 50, self.z准雅宋, (255, 255, 255), 420, 400,
                                self.Main_Screen, self.Antialias, self.getIntoScoreEditor)
        createButton("开始游戏", 50, self.z准雅宋, (255, 255, 255), 420, 300,
                                self.Main_Screen, self.Antialias, self.selectSong)
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
        maskAlpha = 0
        inWhile = True
        while inWhile:  # 不断尝试进行加载
            while (self.eventStack[0] and not (self.__eventBusyOrNot(self.eventStack[0]))):
                self.Main_Screen.fill((34, 40, 49))
                preFunction()
                maskAlpha += 5
                self.Mask.set_alpha(maskAlpha)
                if maskAlpha >= 256:
                    sleep(0.2)
                    inWhile = False
                    self.eventStack[0] = 0
                    break
                self.Main_Screen.blit(self.Mask, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 卸载所有模块
                        pygame.quit()
                        # 终止程序，确保退出程序
                        exit()
                
                sleep(1/self.gameFPS) # 限制FPS 每秒刷新self.gameFPS次 也就是每刷新一次等待1/self.gameFPS秒
                pygame.display.flip()  # 更新屏幕内容
        afterFunction()  
    def afterChangeTo(self, preFunction, *afterFunctions):
        if afterFunctions:
            pass
        else:
            def afterFunctions():
                pass
        maskAlpha = 256
        inWhile = True
        while inWhile:
            while self.eventStack[1] and not (self.__eventBusyOrNot(self.eventStack[1])):
                self.Main_Screen.fill((34, 40, 49))
                preFunction()
                maskAlpha -= 5
                if maskAlpha <= 0:
                    inWhile = False
                    self.eventStack[1] = 0
                    break
                self.Mask.set_alpha(maskAlpha)
                self.Main_Screen.blit(self.Mask, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 卸载所有模块
                        pygame.quit()
                        # 终止程序，确保退出程序
                        exit()
                
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
    def selectSongReturnToPlayingSong(self):
        pass
    def getIntoScoreEditor(self):
        MBSE = MathBeatsScoreEditor(self.Antialias, (self.gameFPS, self.Main_Screen, self.eventStack), self.offset)
        MBSE.start()
    
    # 界面
    def Main_Screen_(self):
        '''主界面'''
        self.mainScreenLock = True
        self.MathImgDect = (-400, 0)
        self.BeatsImgDect = (1054, 0)
        
        self.eventStack[0] = 1
        self.beforeChangeTo(self.__returnSaveNone)
        self.eventStack[1] = 1
        self.afterChangeTo(self._renderStartGame)

        startGameButton = createButton("开始游戏", 50, self.z准雅宋, (255, 255, 255), 420, 300,
                                self.Main_Screen, self.Antialias, self.selectSong)
        scoreEditButton = createButton("谱面创作", 50, self.z准雅宋, (255, 255, 255), 420, 400,
                                self.Main_Screen, self.Antialias, self.getIntoScoreEditor)
        updateButton = createButton("获取更新", 50, self.z准雅宋, (255, 255, 255), 420, 500,
                                self.Main_Screen, self.Antialias, self.checkUpdate)
        mathXYmoving = [True, True]
        beatsXYmoving = [True, True]
        versionFont = pygame.font.Font(self.notoSansHansRegular, 20)
        while self.mainScreenLock:
            self.Main_Screen.fill((34, 40, 49))

            if mathXYmoving[0] or mathXYmoving[1]:
                if self.MathImgDect[0] >= 280:
                    mathXYmoving[0] = False
                if self.MathImgDect[1] >= 25:
                    mathXYmoving[1] = False
                if mathXYmoving[0]:
                    self.MathImgDect = (self.MathImgDect[0] + 5, self.MathImgDect[1])
                if mathXYmoving[1]:
                    self.MathImgDect = (self.MathImgDect[0], self.MathImgDect[1] + 1)
            if beatsXYmoving[0] or beatsXYmoving[1]:
                if self.BeatsImgDect[0] <= 450:
                    beatsXYmoving[0] = False
                if self.BeatsImgDect[1] >= 100:
                    beatsXYmoving[1] = False
                if beatsXYmoving[0]:
                    self.BeatsImgDect = (self.BeatsImgDect[0] - 5, self.BeatsImgDect[1])
                if beatsXYmoving[1]:
                    self.BeatsImgDect = (self.BeatsImgDect[0], self.BeatsImgDect[1] + 1)
            startGameButton.draw()
            scoreEditButton.draw()
            updateButton.draw()
            self.Main_Screen.blit(self.BeatsImg, self.BeatsImgDect)
            self.Main_Screen.blit(self.MathImg, self.MathImgDect)
            
            self.Main_Screen.blit(versionFont.render("Version " + self.version, self.Antialias, (255, 255, 240)), (10, 580))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()
                startGameButton.dealEvent(event)
                scoreEditButton.dealEvent(event)
                updateButton.dealEvent(event)
                
            sleep(1/self.gameFPS)
            pygame.display.flip()
    def selectSong(self):
        '''歌曲选择'''
        self.mainScreenLock = False
        self.eventStack[0] = 1
        self.beforeChangeTo(self._renderStartGame)
        self.eventStack[1] = 1
        self.afterChangeTo(self._renderChosingGame)
        self.selectSongWhileLock = True
        
        returnButton = createButton(" ← ", 40, self.notoSansHansBold, (202, 207, 210), 20, 20, self.Main_Screen, self.Antialias, self.selectSongReturnToTheMainScreen)
        self.selectButtonList = []
        for i in range(len(Song_List)):
            if i == 0:
                self.selectButtonList.append(createButton("  →  ", 35, self.notoSansHansBold, (202, 207, 210), 180, 430, self.Main_Screen, self.Antialias, self.getIntoGame))
            else:
                self.selectButtonList.append(createButton("  →  ", 35, self.notoSansHansBold, (202, 207, 210), 320 * (i+1) - 140, 430, self.Main_Screen, self.Antialias, self.getIntoGame))
        songTitle = pygame.font.Font(self.z准雅宋, 35)
        while self.selectSongWhileLock:
            self.Main_Screen.fill((34, 40, 49))
            
            for i in range(len(Song_List)):
                # 歌曲框
                self.Main_Screen.blit(self.songFrame, (320 * i, 100))
                # 歌曲标题
                if i == 0:
                    self.Main_Screen.blit(songTitle.render(Song_List[i][0], self.Antialias, (202, 207, 210)), (125, 140))  # 渲染文字
                else:
                    self.Main_Screen.blit(songTitle.render(Song_List[i][0], self.Antialias, (202, 207, 210)), (110 * (i+1) + (pygame.font.Font.size(songTitle, Song_List[i-1][0]))[0], 140))  # 渲染文字
                self.selectButtonList[i].draw()
            returnButton.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()
                for i in self.selectButtonList:
                    i.dealEvent(event)
                returnButton.dealEvent(event)
            
            sleep(1/self.gameFPS)
            pygame.display.flip()  # 更新屏幕内容
    def getIntoGame(self):
        for i in range(len(self.selectButtonList)):
            if (self.selectButtonList[i].renderedText).collidepoint(pygame.mouse.get_pos()):
                songIndex = i
        self.eventStack[0] = 1
        self.beforeChangeTo(self._renderStartGame)
        self.eventStack[1] = 1
        self.afterChangeTo(self._renderChosingGame)
        playingWhile = True
        with open(".\\data\\music\\" + Song_List[songIndex][0] + "\\score.json", "r", encoding="utf-8") as song:
            score = json.load(song)
        with open(".\\data\\music\\" + Song_List[songIndex][0] + "\\song.ini", "r", encoding="utf-8") as song:
            songInf = song.read().split("\n")
        # 谱面读取队列
        scoreHead = 0
        scoreTail = len(score)-1
        # 文本
        questionFont = pygame.font.Font(self.notoSansHansRegular, 32)
        def updateFonts():
            '''更新字体大小'''
            questionFont = pygame.font.Font(self.notoSansHansRegular, self.questionSurface.get_width())    
        updateFonts()
        while playingWhile:
            # 字体识别算法
            updateFonts()
            self.Main_Screen.blit(questionSurface)
    
    # 基本函数
    def Keep_Flip(self):
        while 1:
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
    def checkUpdate(self):
        '''检查更新'''
        webbrowser.open("https://tbdriver.lanzouo.com/b0382zldi")
        def temp(): 
            showinfo("密码提示", "文件夹密码为3inx\n已复制到粘贴板!")
        threading.Thread(target=temp).start()
        copy("3inx")
    
    def start(self):
        self.Keep_Flip()


if __name__ == "__main__":
    SYSTEM_MAIN = MathBeats()
    SYSTEM_MAIN.start()
