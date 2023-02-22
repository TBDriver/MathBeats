# -*- coding:utf-8 -*-

from time import sleep, gmtime
import os
import pygame
import random
import json  # ,bezier
from sys import exit
import threading
import widgets
pygame.init()
Widgets = widgets.MathBeatsWidgets()


# 加载文件
# 加载存档与设置
# 存档文件夹
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
        '''
        返回6的函数,无实际意义
        '''
        def ___None():
            pass
        return ___None

    def __fontInit(self):
        # 字体简称
        self.z准雅宋 = ".\\data\\ttf\\方正准雅宋简体.ttf"
        self.notoSansHansBold = ".\\data\\ttf\\NotoSansHans-Bold.otf"
        self.notoSansHansLight = ".\\data\\ttf\\NotoSansHans-Light.otf"
        self.notoSansHansRegular = ".\\data\\ttf\\NotoSansHans-Regular.otf"

    def __revergeWhileLock(self):
        self.whileLock = not self.whileLock
        return self.__returnSaveNone

    def __eventBusyOrNot(self, event: int):
        '''
        检测时间栈是否繁忙 返回0或1
        event为所排除的查询事件
        '''
        for i in self.eventStack:
            if i and i != event:
                return 1
        return 0

    def __init__(self):
        self.Main_Screen = pygame.display.set_mode(size=(1054, 600))
        self.Game_State = "start"
        self.Game_FPS = 60    # FPS
        self.Game_Tick = pygame.time.Clock()
        self.Antialias = True  # 抗锯齿
        self.LastM1 = 0
        self.LastM2 = 0
        self.eventStack = [0, 0, 0]  # 加载等待ID

        self.buttonID = []  # 按钮ID初始化
        self.__fontInit()  # 文字封装初始化
        pygame.font.init()  # 文字库初始化
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

    # 过渡函数
    def _render_start_game(self):
        # _render_start_game作为加载时预处理的图像
        self.showAButton("开始游戏", 50, self.z准雅宋, (255, 255, 255), 300, 300,
                         self.Main_Screen, self.Antialias, 0, self.getIntoGame, self.buttonID[0][0], 0)

    def _render_chosing_game(self):
        pass

    # 主界面
    def Start_Screen(self):
        keep_screen = True
        while keep_screen:
            self.Main_Screen.fill((34, 40, 49))
            # Load title image
            Title_img = pygame.transform.scale(
                pygame.image.load(".\data\img\Title.png"), (400, 400))
            self.Main_Screen.blit(Title_img, (307, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.Game_State = "play"  # 目前直接衔接到游玩系统
                    keep_screen = False
                    break  # 退出循环因为标题画面已关

            self.Game_Tick.tick(self.Game_FPS)
            pygame.display.flip()  # 更新屏幕内容

    # 功能性函数
    def showAButton(self, text: int, size: str, font: str,
                    color: tuple, buttonX: int, buttonY: int, renderSurface: pygame.Surface,
                    antialias: bool, buttonID: int, functions,
                    backgroundColor: tuple = (255, 255, 255), songIndex: int = -1):
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
        songIndex: 歌曲索引
        '''
        buttonFont = pygame.font.Font(font, size)  # 加载字符
        renderSurface.blit(buttonFont.render(
            text, antialias, color, backgroundColor), (buttonX, buttonY))  # 渲染文字

        for event in pygame.event.get():
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN):
                inTheButton = (event.pos[0] >= buttonX and event.pos[0] <= buttonX + (pygame.font.Font.size(buttonFont, text))[0]) and (event.pos[1] >= buttonY and event.pos[1] <= buttonY + (pygame.font.Font.size(buttonFont, text))[1])
                if inTheButton:  # 悬停事件
                    self.buttonID[buttonID][0] = self.buttonID[buttonID][2]
                else:
                    self.buttonID[buttonID][0] = self.buttonID[buttonID][1]
            if event.type == pygame.MOUSEBUTTONUP and (event.pos[0] >= buttonX and event.pos[0] <= buttonX + (pygame.font.Font.size(buttonFont, text))[0]) and (event.pos[1] >= buttonY and event.pos[1] <= buttonY + (pygame.font.Font.size(buttonFont, text))[1]):  # 按下按钮
                functions()

    def beforeChangeTo(self, preFunction, *afterFunction):
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
                Mask1_x += 5
                Mask2_x -= 5
                self.Main_Screen.blit(Masks_img_1, (Mask1_x, 0))
                self.Main_Screen.blit(Masks_img_2, (Mask2_x, 0))
                self.Game_Tick.tick(self.Game_FPS)
                pygame.display.update()  # 更新屏幕内容
    def afterChangeTo(self, preFunction, *afterFunctions):
        if afterFunctions:
            pass
        else:
            def afterFunctions():
                pass
        sleep(0.2)
        Masks_img_1 = pygame.image.load(".\data\img\Mask1.png")
        Masks_img_2 = pygame.image.load(".\data\img\Mask2.png")
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
                Mask1_x -= 5
                Mask2_x += 5

                self.Main_Screen.blit(Masks_img_1, (Mask1_x, 0))
                self.Main_Screen.blit(Masks_img_2, (Mask2_x, 0))

                self.Game_Tick.tick(self.Game_FPS)
                pygame.display.update()  # 更新屏幕内容
        afterFunctions

    # 界面
    def Main_Screen_(self):
        self.mainScreenLock = False
        self.buttonID.append(
            [(44, 62, 80), (44, 62, 80), (0, 0, 0)])  # 开始游戏按钮ID
        self.eventStack[0] = 1
        self.beforeChangeTo(self.__returnSaveNone)
        self.eventStack[1] = 1
        self.afterChangeTo(self._render_start_game)
        # 以后填个坑
        # 这里一直用sleep守着不是个事
        # sleep会导致主程序未响应影响游玩

        while True:
            self.Main_Screen.fill((34, 40, 49))
            self.showAButton("开始游戏", 50, self.z准雅宋, (255, 255, 255), 300, 300,
                             self.Main_Screen, self.Antialias, 0, self.selectSong, self.buttonID[0][0])

            self.Game_Tick.tick(self.Game_FPS)
            pygame.display.update()

    def selectSong(self):
        self.mainGetIntoGameLock = False
        self.eventStack[0] = 1
        self.beforeChangeTo(self._render_start_game)
        self.eventStack[1] = 1
        self.afterChangeTo(self._render_chosing_game)

        while True:
            self.Main_Screen.fill((34, 40, 49))
            songFrame = pygame.transform.scale(
                pygame.image.load(".\\data\\img\\frame.png"), (400, 400))
            for i in range(len(Song_List)):
                # 歌曲框
                self.Main_Screen.blit(songFrame, (320 * i, 100))
                # 歌曲标题
                if i == 0:
                    self.Main_Screen.blit((pygame.font.Font(self.z准雅宋, 35)).render(
                        Song_List[i][0], self.Antialias, (202, 207, 210)), (125, 140))  # 渲染文字
                else:
                    self.Main_Screen.blit((pygame.font.Font(self.z准雅宋, 35)).render(Song_List[i][0], self.Antialias, (202, 207, 210)), (
                        110 * (i+1) + (pygame.font.Font.size(pygame.font.Font(self.z准雅宋, 35), Song_List[i-1][0]))[0], 140))  # 渲染文字
                # 游玩按钮
                self.buttonID.append([(44, 62, 80), (44, 62, 80), (0, 0, 0)])  # 开始游戏按钮ID
                if i == 0 :
                    self.showAButton("Start→", 35, self.z准雅宋, (202, 207, 210),
                                    170 # 300 * (i+1) - (pygame.font.Font.size(pygame.font.Font(self.z准雅宋, 35), "Start→"))[0]
                                    , 430
                                    , self.Main_Screen, self.Antialias, i+1, self.getIntoGame, self.buttonID[i+1][0])
                else:
                    self.showAButton("Start→", 35, self.z准雅宋, (202, 207, 210),
                                    320 * (i+1) - 150 # 300 * (i+1) - (pygame.font.Font.size(pygame.font.Font(self.z准雅宋, 35), "Start→"))[0]
                                    , 430
                                    , self.Main_Screen, self.Antialias, i+1, self.getIntoGame, self.buttonID[i+1][0])

            self.Game_Tick.tick(self.Game_FPS)
            pygame.display.update()

    def getIntoGame(self):
        '''
        你先别急
        如函数名
        '''
        pass

    def Keep_Flip(self):
        while True:
            # 游戏状态为 开始游戏
            if self.Game_State == "start":
                self.Start_Screen()  # 进入开始屏幕的循环
            if self.Game_State == "play":
                self.Main_Screen_()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()

            self.Game_Tick.tick(self.Game_FPS)
            pygame.display.flip()  # 更新屏幕内容

    def start(self):
        self.Keep_Flip()


if __name__ == "__main__":
    SYSTEM_MAIN = MathBeats()
    SYSTEM_MAIN.start()
