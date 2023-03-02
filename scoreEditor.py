import pygame
from widgets import *
from time import sleep
from mutagen.mp3 import MP3

class MathBeatsScoreEditor:
    def __fontInit(self):
        '''字体路径初始化'''
        self.z准雅宋 = ".\\data\\ttf\\方正准雅宋简体.ttf"
        self.notoSansHansBold = ".\\data\\ttf\\NotoSansHans-Bold.otf"
        self.notoSansHansLight = ".\\data\\ttf\\NotoSansHans-Light.otf"
        self.notoSansHansRegular = ".\\data\\ttf\\NotoSansHans-Regular.otf"
        self.s狮尾四季春 = ".\\data\\ttf\\狮尾四季春-Regular.ttf"
    def __loadingPictures(self):
        self.songFrame = pygame.transform.scale(pygame.image.load(".\\data\\img\\frame.png").convert_alpha(), (400, 400))
        self.Title_img = pygame.transform.scale(pygame.image.load(".\data\img\Title.png").convert_alpha(), (400, 400))
        self.Masks_img_1 = pygame.image.load(".\data\img\Mask1.png").convert_alpha()
        self.Masks_img_2 = pygame.image.load(".\data\img\Mask2.png").convert_alpha()
    def __eventBusyOrNot(self, event: int):
        '''
        检测时间栈是否繁忙 返回0或1
        event为所排除的查询事件
        '''
        for i in self.eventStack:
            if i and i != event:
                return 1
        return 0
    def __init__(self, Antialias, parameter):
        self.gameFPS = parameter[0]
        self.Main_Screen = parameter[1]
        self.Antialias = Antialias
        self.eventStack = parameter[2]  # 加载等待ID
        self.__fontInit()
        self.__loadingPictures()
    def __returnSaveNone(self):
        '''返回空函数的函数,无实际意义'''
        def ___None():
            pass
        return ___None
    
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
                Mask1_x += 820/self.gameFPS + 2
                Mask2_x -= 800/self.gameFPS + 2
                
                self.Main_Screen.blit(self.Masks_img_1, (Mask1_x, 0))
                self.Main_Screen.blit(self.Masks_img_2, (Mask2_x, 0))

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
                Mask1_x -= 820/self.gameFPS + 2
                Mask2_x += 800/self.gameFPS + 2

                self.Main_Screen.blit(self.Masks_img_1, (Mask1_x, 0))
                self.Main_Screen.blit(self.Masks_img_2, (Mask2_x, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # 卸载所有模块
                        pygame.quit()
                        # 终止程序，确保退出程序
                        exit()
                
                sleep(1/self.gameFPS)
                pygame.display.flip()  # 更新屏幕内容
        afterFunctions()
    
    # 铺面制作
    def _renderEditor(self):
        pass
        '''
        self.returnButton.draw()
        self.createNewScoreButton.draw()
        self.continueWorkButton.draw()
        '''
    def _renderStartGame(self):
        # _renderStartGame作为加载时预处理的图像
        (createButton("开始游戏", 50, self.z准雅宋, (255, 255, 255), 420, 100,
                             self.Main_Screen, self.Antialias, self.__returnSaveNone)).draw()
        (createButton("谱面创作", 50, self.z准雅宋, (255, 255, 255), 420, 300,
                             self.Main_Screen, self.Antialias, self.__returnSaveNone)).draw()
    def showARect(self, x: int, y: int, width: float, height: float, color: tuple):
        '''
        x    整型 Rectx值
        y    整型 Recty值
        width整型 宽度
        heigh整型 高度
        color元组 颜色Hex值
        '''
        pygame.draw.rect(self.Main_Screen, color, (pygame.Rect(x, y, width, height)))
    
    def editorMainScreen(self):
        self.eventStack[0] = 1
        self.beforeChangeTo(self._renderStartGame)
        
        self.returnButton = createButton(" ← ", 40, self.notoSansHansBold, (202, 207, 210), 20, 20, self.Main_Screen, self.Antialias, self.editorMainScreenReturnToTheMainScreen)
        self.createNewScoreButton = createButton("新建谱面", 70, self.z准雅宋, (255, 255, 255), 100, 200, self.Main_Screen
                             , self.Antialias, self.createNewScore)
        self.continueWorkButton = createButton("继续创作", 70, self.z准雅宋, (255, 255, 255), 100, 380, self.Main_Screen
                             , self.Antialias, self.continueWork)

        self.editorWhile = True
        self.mainScreenLock = False
        pygame.display.set_caption("Mathbeats 铺面制作器")
        
        self.eventStack[1] = 1
        self.afterChangeTo(self._renderEditor)
        
        while self.editorWhile:
            self.Main_Screen.fill((34, 40, 49))

            self.returnButton.draw()
            self.createNewScoreButton.draw()
            self.continueWorkButton.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()
                
                self.returnButton.dealEvent(event)
                self.createNewScoreButton.dealEvent(event)
                self.continueWorkButton.dealEvent(event)
                
            sleep(1/self.gameFPS)
            pygame.display.update()
    def createNewScore(self):
        self.tempScore = {
            "note": []
        }
        self.editScore(self.tempScore,[None, None, None, None, None])
    def continueWork(self):
        pass
    def editScore(self,Score: dict,Inf: list):
        '''
        Score 铺面   字典
        Inf 歌曲信息 列表
            ->[name, author, geneticist, bpm, song]s
            其中song为歌曲全路径
        '''
        self.editScoreWhile = True
        
        # 谱面信息参数未指定处理
        unknownInf = ["未命名歌曲", "未命名曲师", "未命名谱师", 200, "0:30"]
        for i in range(len(Inf)):
            if Inf[i] == None:  Inf[i] = unknownInf[i]
        # 追加歌曲时长
        if Inf[4] == "":    Inf.append(30)
        else:               Inf.append(MP3(Inf[4]).info.length)
        # 函数-创建或应用Note
        def createNote():
            eachNoteTick = []  # 每拍时长以及当前时长
            localNoteTick = 0  # 当前note时长
            duratation = 0     # 总时长
            # 判断Score中Note数量
            if len(Score["note"]) != 0:                 # 有其他Note时
                
                # 处理此前note时长
                for i in range(len(Score["note"])):     # i遍历谱面中每一个Note
                    eachNoteTick.append([])
                    localNoteTick = 0
                    for j in range(len(Score["note"][i])): # j遍历Note中的每个信息
                        for k in range(len(Score["note"][i][0])): # 遍历每拍间隔
                            localNoteTick += int(Score["note"][i][0][k])
                        localNoteTick += int(Score["note"][i][5])
                    duratation += localNoteTick
                    eachNoteTick[i].append(localNoteTick)
                    eachNoteTick[i].append(duratation)
                print(eachNoteTick)
                print(duratation)
                # Todo 根据当前时长增加note
                Score["note"].append(localNoteInf)
                
            else: # 是首个Note
                Score["note"].append([]) # 增加Note
                Score["note"][0] = localNoteInf
            print(Score)
            
            
            
            '''
            if len(Score["note"]) != 0:
                for i in range(len(Score["note"])):
                    # 目前i=note数量
                    for j in Score["note"][i][0]:
                        # 进行时间累加
                        localNoteTick += j
                        localNoteTick += Score["note"][i][4]
                        
                    if localNoteTick == localTick:            # 当选中时间点为Note开始时间点时
                        Score["note"][i] = localNoteInf       # 对当前Note信息进行覆盖
                    else:
                        Score["note"][i] = localNoteInf # 增加Note
            else:
                Score["note"][0] = localNoteTick
            '''
        # 函数-更改歌曲信息
        def changeInf():
            # 外边框
            pygame.draw.rect(self.Main_Screen, (38, 55, 70), pygame.Rect(300, 100, 450, 400))
            songNameInputBox.draw(self.Main_Screen)
            composerInputBox.draw(self.Main_Screen)
            geneticistNameInputBox.draw(self.Main_Screen)
            inReverseChangeInfButton.draw()
        # 函数-改变信息编辑栏状态
        def reverseChangeInfBool():
            global changeInfActive
            changeInfActive = not changeInfActive
        # 输入框初始化
        beatPerSecInputBox = inputBox(pygame.Rect (15, 150, 140, 32), textPlaceHolder="200 200 200 200 200 200") # 每拍间隔
        noSoundBeatInputBox = inputBox(pygame.Rect(15, 210, 140, 32))                               # 无音效note
        timeAfterBeatInputBox = inputBox(pygame.Rect  (15, 270, 140, 32), textPlaceHolder="200")    # 拍后间隔
        questionInputBox = inputBox(pygame.Rect  (1054-202, 210, 140, 32), textPlaceHolder="7^2=49")# 问题
        specInputBox = inputBox(pygame.Rect(1054-202, 150, 140, 32), textPlaceHolder="0")
        # 特效
        songNameInputBox = inputBox(pygame.Rect(320, 120, 140, 32), textPlaceHolder=Inf[0])       # 歌曲名
        composerInputBox = inputBox(pygame.Rect(320, 160, 140, 32) , textPlaceHolder="未命名曲师")   # 曲师
        geneticistNameInputBox = inputBox(pygame.Rect(320, 200, 140, 32), textPlaceHolder="未命名谱师")# 谱师
        difficultyInputBox = inputBox(pygame.Rect(320, 240, 140, 32), textPlaceHolder="")
        # 按钮初始化
        createNoteButton = createButton("在当前位置创建或应用Note", 26, self.z准雅宋, (255, 240, 240), 1054/2-120, 560, self.Main_Screen, self.Antialias, createNote)
        changeSongInfButton = createButton("更改歌曲信息", 26, self.z准雅宋, (255, 255, 240), 1054 - 300, 560, self.Main_Screen, self.Antialias, reverseChangeInfBool)
        inReverseChangeInfButton = createButton(" → ", 40, self.notoSansHansBold, (178, 202, 210), 675, 115, self.Main_Screen, self.Antialias, reverseChangeInfBool)
        # 复选框初始化
        checkIfCheckBox = checkBox(self.Main_Screen, 1054-52, 250, 50, 3)
        # 字体预载
        tipFont = pygame.font.Font(self.s狮尾四季春, 20)
        # 基础变量
        global changeInfActive
        localTick = 0 # 单位毫秒
        localNoteInf = [["每拍停顿时间"], "题目", "正确与否", "特效ID", ["无音效BeatID"], "拍后间隔"]
        localSongInf = ["未命名歌曲", "未命名曲师", "未命名谱师", "未指定难度"]
        changeInfActive = False
        changeInfEvents = [songNameInputBox, composerInputBox, geneticistNameInputBox, inReverseChangeInfButton]
        
        
        while self.editScoreWhile:
            self.Main_Screen.fill((34, 40, 49))
            # 歌曲进度条
            self.showARect(0, 0, 1054 ,130, (23, 76, 89))
            
            # 输入框
            beatPerSecInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("当前Note每节拍间隔(ms)", self.Antialias, (255, 255, 240)), (13, 128))
            
            noSoundBeatInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("无音效的节拍(第几个)", self.Antialias, (255, 255, 240)), (13, 184))

            timeAfterBeatInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("拍后间隔(ms)", self.Antialias, (255, 255, 240)), (13, 235))
            
            specInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("特效选择(1~9)", self.Antialias, (255, 255, 240)), (1054-134, 128))

            questionInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("Note对应问题", self.Antialias, (255, 255, 240)), (1054-128, 184))
            
            # 按钮
            createNoteButton.draw()
            changeSongInfButton.draw()
            
            # 复选框
            checkIfCheckBox.draw()
            
            # 是否更改信息
            if changeInfActive:
                changeInf()
                

            # 更新信息
            # 每拍间隔
            localNoteInf[0] = beatPerSecInputBox.getText().split()
            # Note问题
            localNoteInf[1] = questionInputBox.getText()
            # 问题对错
            localNoteInf[2] = checkIfCheckBox.returnAcitve()
            # 特效
            localNoteInf[3] = specInputBox.getText()
            # 无音效节拍
            localNoteInf[4] = noSoundBeatInputBox.getText().split()
            # 拍后间隔
            localNoteInf[5] = timeAfterBeatInputBox.getText()
            
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()

                # 输入框更新事件
                beatPerSecInputBox.dealEvent(event)   # 每秒间隔
                noSoundBeatInputBox.dealEvent(event)  # 无音效Note
                timeAfterBeatInputBox.dealEvent(event)# 拍后间隔
                specInputBox.dealEvent(event)         # 特效
                questionInputBox.dealEvent(event)     # 问题
                try:    inReverseChangeInfButton.dealEvent(event)
                except: pass
                # 按钮更新事件
                createNoteButton.dealEvent(event)     # 应用Note
                changeSongInfButton.dealEvent(event)
                # 复选框更新事件
                checkIfCheckBox.dealEvent(event)
                
                
                if changeInfActive:
                    for i in changeInfEvents:
                        i.dealEvent(event)
                

            sleep(1/self.gameFPS)
            pygame.display.flip()