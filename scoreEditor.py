import pygame, os
from widgets import *
from time import sleep, strftime
from mutagen.mp3 import MP3
import json

class MathBeatsScoreEditor:
    def __fontInit(self):
        '''字体路径初始化'''
        self.z准雅宋 = ".\\data\\ttf\\方正准雅宋简体.ttf"
        self.notoSansHansBold = ".\\data\\ttf\\NotoSansHans-Bold.otf"
        self.notoSansHansRegular = ".\\data\\ttf\\NotoSansHans-Regular.otf"
        # self.notoSansHansLight = ".\\data\\ttf\\NotoSansHans-Light.otf"
        # self.s狮尾四季春 = ".\\data\\ttf\\狮尾四季春-Regular.ttf"
    def __loadingPictures(self):
        self.songFrame = pygame.transform.scale(pygame.image.load(".\\data\\img\\frame.png").convert_alpha(), (400, 400))
        self.Title_img = pygame.transform.scale(pygame.image.load(".\data\img\Title.png").convert_alpha(), (400, 400))
        self.MathImg = pygame.transform.scale(pygame.image.load(".\data\img\Math.png").convert_alpha(), (400, 200))
        self.BeatsImg= pygame.transform.scale(pygame.image.load(".\data\img\Beats.png").convert_alpha(), (400, 200))
        self.Mask = pygame.image.load(".\data\img\Mask.png").convert_alpha()
    def __eventBusyOrNot(self, event: int):
        '''
        检测时间栈是否繁忙 返回0或1
        event为所排除的查询事件
        '''
        for i in self.eventStack:
            if i and i != event:
                return 1
        return 0
    def __returnSaveNone(self):
        '''返回空函数的函数,无实际意义'''
        def ___None():
            pass
        return ___None
    def __init__(self, Antialias, parameter, offset):
        self.gameFPS = parameter[0]     # 继承FPS
        self.Main_Screen = parameter[1] # 继承作用Surface对象
        self.Antialias = Antialias      # 继承抗锯齿
        self.eventStack = parameter[2]  # 继承等待ID
        self.offset = offset            # 继承偏差值
        self.__fontInit()           # 字体初始化
        self.__loadingPictures()    # 图片加载
        self.MathImgDect = (280, 25)
        self.BeatsImgDect = (449, 100)
        pygame.display.set_caption("Mathbeats 铺面制作器")
    
    # 功能函数
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
    def showARect(self, x: int, y: int, width: float, height: float, color: tuple):
        '''
        x    整型 Rectx值
        y    整型 Recty值
        width整型 宽度
        heigh整型 高度
        color元组 颜色Hex值
        '''
        pygame.draw.rect(self.Main_Screen, color, (pygame.Rect(x, y, width, height)))
    def editorMainScreenReturnToTheMainScreen(self):
        self.mainScreenLock = True
        self.editorWhile = False
        self.eventStack[0] = 1
        self.beforeChangeTo(self._renderEditor)
        self.eventStack[1] = 1
        sleep(0.005)
        pygame.display.set_caption("Mathbeats")
        self.afterChangeTo(self._renderStartGame)
    def ediorReturnToTheEditorMainScreen(self):
        self.editScoreWhile = False
        self.editorWhile = True
        pygame.display.set_caption("Mathbeats")
        
    
    # 预加载函数
    def _renderEditor(self):
        pass
        '''
        self.returnButton.draw()
        self.createNewScoreButton.draw()
        self.continueWorkButton.draw()
        '''
    def _renderStartGame(self):
        # _renderStartGame作为加载时预处理的图像
        self.Main_Screen.blit(self.BeatsImg, self.BeatsImgDect)
        self.Main_Screen.blit(self.MathImg, self.MathImgDect)
        createButton("获取更新", 50, self.z准雅宋, (255, 255, 255), 420, 500,
                                self.Main_Screen, self.Antialias, self.__returnSaveNone)
        createButton("谱面创作", 50, self.z准雅宋, (255, 255, 255), 420, 400,
                                self.Main_Screen, self.Antialias, self.__returnSaveNone)
        createButton("开始游戏", 50, self.z准雅宋, (255, 255, 255), 420, 300,
                                self.Main_Screen, self.Antialias, self.__returnSaveNone)
    
    # 铺面制作
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
        self.editScore(self.tempScore,[None, None, None, None, None, None])
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
        unknownInf = ["未命名歌曲", "未命名曲师", "未命名谱师", "未指定难度 ", "200", "歌曲路径", "3000"]
        localSongInf = ["未命名歌曲", "未命名曲师", "未命名谱师", "未指定难度", "200", "歌曲路径", "3000"]
        for i in range(len(Inf)):
            if Inf[i] == None:  Inf[i] = unknownInf[i]
        if Inf[5] != "歌曲路径" and os.path.isfile(Inf[5]): # 检测是否是正常歌曲文件
            Inf[4] = (MP3(Inf[5]).info.length*1000)
        else:
            Inf[4] = "3000"
        for i in range(len(Inf)):
            localSongInf[i] = Inf[i]
        # 基础变量
        global changeInfActive, localTick, duration
        localTick = 0 # 单位毫秒
        localNoteInf = [["每拍停顿时间"], "题目", "正确与否", "特效ID", ["无音效BeatID"], "拍后间隔"]
        changeInfActive = False
        # 函数-创建或应用Note
        eachNoteTick = []  # 每拍时长以及当前时长
        duration = 0     # 总时长
        def calculatorDuration():
            for i in range(len(Score["note"])):     # i遍历谱面中每一个Note
                localNoteTick = 0
                for j in range(len(Score["note"][i])): # j遍历Note中的每个信息
                    if j == 0:
                        for k in range(len(Score["note"][i][0])): # 遍历每拍间隔
                            localNoteTick += int(Score["note"][i][0][k])
                    if j == 5:
                        localNoteTick += int(Score["note"][i][5])
            global duration
            duration += localNoteTick
            eachNoteTick.append([localNoteTick, duration])
        def createNote():
            if len(Score["note"]) > 2: # 检测谱面是否有note
                for i in range(len(Score["note"])): # 遍历每一个note
                    if localTick < int(eachNoteTick[i][1]) and localTick >  int(eachNoteTick[i-1][1]):
                        # 如果当前时长大于这个note所在的时长且小于上一个note的时长
                        # 也就是在上下两个note之间 不用担心会重复执行因为情况只会出现一次
                        print(i)
                        Score["note"].append(localNoteInf) 
                        # 处理此前note时长
                        calculatorDuration()
                        print(eachNoteTick)
                        print(duration)
                        print(Score)
            else: # 没有就不用管啦
                Score["note"].append(localNoteInf)
                calculatorDuration()
                print(eachNoteTick)
                print(duration)
                print(Score)
                
        # 函数-更改歌曲信息
        def changeInf():
            # 外边框
            pygame.draw.rect(self.Main_Screen, (38, 55, 70), pygame.Rect(300, 100, 450, 400))
            songNameInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("曲名:", self.Antialias, (255, 255, 240)), (320, 120))
            composerInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("曲师:", self.Antialias, (255, 255, 240)), (320, 160))
            geneticistNameInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("谱师:", self.Antialias, (255, 255, 240)), (320, 200))
            BPMInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("难度:", self.Antialias, (255, 255, 240)), (320, 240))
            songInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("BPM:", self.Antialias, (255, 255, 240)), (320, 280))
            difficultyInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont2.render("歌曲路径:", self.Antialias, (255, 255, 240)), (310, 325))
            inReverseChangeInfButton.draw()
            saveSongInfButton.draw()
        # 函数-改变信息编辑栏状态
        def reverseChangeInfBool():
            global changeInfActive
            changeInfActive = not changeInfActive
        # 函数-保存歌曲信息
        def saveSongInfData():
            if changeInfActive:
                for i in range(len(changeInfEvents)):
                    if type(changeInfEvents[i]) != createButton:
                        localSongInf[i] = changeInfEvents[i].getText()
                if os.path.isfile(localSongInf[5]):
                    localSongInf[6] = MP3(localSongInf[5]).info.length * 1000
                global chooseLengthRect
                chooseLengthRect = dragLine(self.Main_Screen, 10, 10, 200, 10, int(localSongInf[6]), (255, 255, 255), (0, 0, 0))
                saveSongData()
        def saveSongData():
            # 创建文件夹
            try:    os.mkdir(".\\data\\music\\" + localSongInf[0])
            except: pass
            # 写入音乐文件
            with open(localSongInf[5], "rb") as musicFile:
                tempMusic = musicFile.read()
                with open(".\\data\\music\\" + localSongInf[0] + "\\music.mp3", "wb+") as file:
                    file.write(tempMusic)
            # 写入配置文件
            with open(".\\data\\music\\" + localSongInf[0] + "\\song.ini", "w+", encoding="utf-8") as file:
                for i in range(len(localSongInf)):
                    file.write(str(localSongInf[i]) + "\n")
            # 写入谱面文件
            with open(".\\data\\music\\" + localSongInf[0] + "\\score.json", "w+", encoding="utf-8") as file:
                json.dump(Score, file)
        # 输入框初始化
        beatPerSecInputBox = inputBox(pygame.Rect (15, 150, 140, 32), textPlaceHolder="200 200 200 200 200 200") # 每拍间隔
        noSoundBeatInputBox = inputBox(pygame.Rect(15, 210, 140, 32))                               # 无音效note
        timeAfterBeatInputBox = inputBox(pygame.Rect  (15, 270, 140, 32), textPlaceHolder="200")    # 拍后间隔
        questionInputBox = inputBox(pygame.Rect  (1054-202, 210, 140, 32), textPlaceHolder="7^2=49")# 问题
        specInputBox = inputBox(pygame.Rect(1054-202, 150, 140, 32), textPlaceHolder="0")
        # 信息
        songNameInputBox = inputBox(pygame.Rect(380, 120, 140, 32), textPlaceHolder=Inf[0])         # 歌曲名
        composerInputBox = inputBox(pygame.Rect(380, 160, 140, 32) , textPlaceHolder="未命名曲师")   # 曲师
        geneticistNameInputBox = inputBox(pygame.Rect(380, 200, 140, 32), textPlaceHolder="未命名谱师")# 谱师
        difficultyInputBox = inputBox(pygame.Rect(380, 240, 140, 32), textPlaceHolder="0")          # 难度
        BPMInputBox = inputBox(pygame.Rect(380, 280, 140, 32), textPlaceHolder="200")               # BPM
        songInputBox = inputBox(pygame.Rect(380, 320, 140, 32), textPlaceHolder="")                 # 歌曲路径
        # 按钮初始化
        returnButton = createButton(" → ", 40, self.notoSansHansBold, (178, 202, 210), 900, 30, self.Main_Screen, self.Antialias, self.ediorReturnToTheEditorMainScreen)
        createNoteButton = createButton("在当前位置创建或应用Note", 26, self.z准雅宋, (255, 240, 240), 1054/2-120, 560, self.Main_Screen, self.Antialias, createNote)
        changeSongInfButton = createButton("更改歌曲信息", 26, self.z准雅宋, (255, 255, 240), 1054 - 300, 560, self.Main_Screen, self.Antialias, reverseChangeInfBool)
        inReverseChangeInfButton = createButton(" → ", 40, self.notoSansHansBold, (178, 202, 210), 675, 115, self.Main_Screen, self.Antialias, reverseChangeInfBool)
        saveSongInfButton = createButton("保存谱面于根目录\\data\\music中", 35, self.z准雅宋, (255, 255, 240), 500, 450, self.Main_Screen, self.Antialias, saveSongInfData)
        # 复选框初始化
        checkIfCheckBox = checkBox(self.Main_Screen, 1054-52, 250, 50, 3, True)
        # 拖拽Rect初始化
        global chooseLengthRect
        chooseLengthRect = dragLine(self.Main_Screen, 10, 10, 200, 10, int(localSongInf[6]), (255, 255, 255), (0, 0, 0))
        # 字体预载
        tipFont = pygame.font.Font(self.z准雅宋, 20)
        tipFont2 = pygame.font.Font(self.z准雅宋, 16)
        changeInfEvents = [songNameInputBox, composerInputBox, geneticistNameInputBox, difficultyInputBox, BPMInputBox, songInputBox, inReverseChangeInfButton, saveSongInfButton]
        
        while self.editScoreWhile:
            self.Main_Screen.fill((34, 40, 49))
            # 显示Note
            
            
            
            
            
            # 歌曲进度条
            self.showARect(0, 0, 1054 ,130, (23, 76, 89))
            
            # 输入框
            beatPerSecInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("当前Note每节拍间隔(ms)", self.Antialias, (255, 255, 240)), (13, 128))
            
            noSoundBeatInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("无音效的节拍(第几个)", self.Antialias, (255, 255, 240)), (13, 184))

            timeAfterBeatInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("拍后间隔(ms)", self.Antialias, (255, 255, 240)), (13, 236))
            
            specInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("特效选择(1~9)", self.Antialias, (255, 255, 240)), (1054-134, 128))

            questionInputBox.draw(self.Main_Screen)
            self.Main_Screen.blit(tipFont.render("Note对应问题", self.Antialias, (255, 255, 240)), (1054-128, 184))
            
            # 按钮
            createNoteButton.draw()
            changeSongInfButton.draw()
            returnButton.draw()
            
            # 复选框
            checkIfCheckBox.draw()
            self.Main_Screen.blit(tipFont.render("正确与否:", self.Antialias, (255, 255, 240)), (1054-148, 256))
            
            # 拖拽条
            chooseLengthRect.draw()
            localTick = chooseLengthRect.getText()

            # 是否更改信息
            if changeInfActive:
                changeInf()
                

            # 更新Note信息
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
                returnButton.dealEvent(event)
                # 复选框更新事件
                checkIfCheckBox.dealEvent(event)
                # 拖拽Rect更新事件
                chooseLengthRect.dealEvent(event)
                if changeInfActive:
                    for i in range(len(changeInfEvents)):
                        changeInfEvents[i].dealEvent(event)
                
            sleep(1/self.gameFPS)
            pygame.display.flip()
    
    def start(self):
        self.editorMainScreen()
