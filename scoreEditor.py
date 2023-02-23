from time import sleep
import pygame
pygame.init()

class MathBeatsScoreEditor:
    def __fontInit(self):
        pygame.font.init()
        # 字体简称
        self.z准雅宋 = ".\\data\\ttf\\方正准雅宋简体.ttf"
        self.notoSansHansBold = ".\\data\\ttf\\NotoSansHans-Bold.otf"
        self.notoSansHansLight = ".\\data\\ttf\\NotoSansHans-Light.otf"
        self.notoSansHansRegular = ".\\data\\ttf\\NotoSansHans-Regular.otf"
        
    def __init__(self):
        '''制谱器初始化'''
        self.MathBeatsScoreEditor = pygame.display.set_mode(size=(1054, 600))
        self.gameFPS = 200
        self.Antialias = True
        self.eventStack = [0, 0, 0]
        self.buttonID = []
        
        self.__fontInit()  # 字体路径初始化
        pygame.display.set_caption("Mathbeats 谱面制作器")
    
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
    
    
    def loadingScreen(self):
        self.buttonID.append([(44, 62, 80), (44, 62, 80), (0, 0, 0)])
        self.buttonID.append([(44, 62, 80), (44, 62, 80), (0, 0, 0)])
        while True:
            self.MathBeatsScoreEditor.fill((34, 40, 49))
            self.showAButton("新建谱面", 70, self.z准雅宋, (255, 255, 255), 100, 200, self.MathBeatsScoreEditor
                             , self.Antialias, 0, self.createNewScore, self.buttonID[0][0])
            self.showAButton("继续创作", 70, self.z准雅宋, (255, 255, 255), 100, 380, self.MathBeatsScoreEditor
                             , self.Antialias, 1, self.continueWork, self.buttonID[1][0])
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 卸载所有模块
                    pygame.quit()
                    # 终止程序，确保退出程序
                    exit()
            sleep(1/self.gameFPS)
            pygame.display.update()


    def continueWork(self):
        pass
    def createNewScore(self):
        pass
            
    def start(self):
        self.loadingScreen()

# ScoreEditor = MathBeatsScoreEditor()
# ScoreEditor.start()