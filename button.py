import pygame
class createButton():
    def __init__(self, text: int, size: str, font: str,
                color: tuple, buttonX: int, buttonY: int, renderSurface: pygame.Surface,
                antialias: bool, functions,
                inActiveColor: tuple = (44, 62, 80), activeColor: tuple = (0, 0, 0)):
        '''
        用于显示按钮
        text: 按钮文本         字符串
        size: 文本大小         整型
        font: 使用字体路径     字符串
        color:文本颜色         元组    其中接受三个参数
        buttonX&Y 按钮xy值     整型    用于按钮置放和悬停表现
        renderSurface: 作用Surface对象
        antialias: 抗锯齿与否  布尔值
        functions: 执行函数    函数    可选
        backgroundColor 背景颜色  列表嵌套元组
        '''
        self.text = text
        self.size = size
        self.font = font
        self.color = color
        self.buttonX = buttonX
        self.buttonY = buttonY
        self.renderSurface = renderSurface
        self.antialias = antialias
        self.functions = functions
        
        self.active = False
        self.backgroundColor = inActiveColor
        self.activeColor = activeColor
        self.inActiveColor = inActiveColor
        
    def draw(self):
        self.buttonFont = pygame.font.Font(self.font, self.size)  # 加载字符
        self.renderedText = self.renderSurface.blit(self.buttonFont.render(self.text, self.antialias, self.color, self.backgroundColor), (self.buttonX, self.buttonY))  # 渲染文字
        
    def dealEvent(self, event):
        if event.type == 1025 and self.renderedText.collidepoint(event.pos):
            print(self.functions)
            self.functions()
        if event.type == 1024:
            # inTheButton = ((event.pos[0] >= buttonX) and (event.pos[0] <= buttonX + textSize[0])) and ((event.pos[1] >= buttonY) and (event.pos[1] <= buttonY + textSize[1]))
            if self.renderedText.collidepoint(event.pos): 
                self.backgroundColor = self.activeColor
            else: 
                self.backgroundColor = self.inActiveColor