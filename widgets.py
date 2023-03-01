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
        self.buttonFont = pygame.font.Font(self.font, self.size)  # 加载字符
        
    def draw(self):
        self.renderedText = self.renderSurface.blit(self.buttonFont.render(self.text, self.antialias, self.color, self.backgroundColor), (self.buttonX, self.buttonY))  # 渲染文字
        
    def dealEvent(self, event):
        if event.type == 1025 and self.renderedText.collidepoint(event.pos):
            self.functions()
        if event.type == 1024:
            # inTheButton = ((event.pos[0] >= buttonX) and (event.pos[0] <= buttonX + textSize[0])) and ((event.pos[1] >= buttonY) and (event.pos[1] <= buttonY + textSize[1]))
            if self.renderedText.collidepoint(event.pos): 
                self.backgroundColor = self.activeColor
            else: 
                self.backgroundColor = self.inActiveColor

class inputBox():
    def __init__(self, rect: pygame.Rect = pygame.Rect(100, 100, 140, 32), font: str = ".\data\\ttf\\狮尾四季春-Regular.ttf", size: int = 18, textPlaceHolder = "") -> None:
        """
        rect 传入矩形实体 传达输入框的位置和大小
        """
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')  # 未被选中的颜色
        self.color_active = pygame.Color('dodgerblue2')  # 被选中的颜色
        self.color = self.color_inactive  # 当前颜色，初始为未激活颜色
        self.active = False
        self.text = textPlaceHolder
        self.done = False
        self.font = pygame.font.Font(font, size)

    def dealEvent(self, event: pygame.event.Event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(self.boxBody.collidepoint(event.pos)):  # 若按下鼠标且位置在文本框
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if(self.active) else self.color_inactive
        if(event.type == pygame.KEYDOWN):  # 键盘输入响应
            if(self.active):
                if(event.key == pygame.K_RETURN):
                    print(self.text)
                    # self.text=''
                elif(event.key == pygame.K_BACKSPACE):
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen: pygame.surface.Surface):
        txtSurface = self.font.render(
            self.text, True, self.color)  # 文字转换为图片
        width = max(200, txtSurface.get_width()+10)  # 当文字过长时，延长文本框
        self.boxBody.w = width
        screen.blit(txtSurface, (self.boxBody.x+5, self.boxBody.y+5))
        pygame.draw.rect(screen, self.color, self.boxBody, 2)    

    def getText(self):
        return self.text

class checkBox():
    def __init__(self, renderSurface: pygame.Surface, boxX: int, boxY: int, length = 20, frame = 2, frameColor = pygame.Color('lightskyblue3'), backgroundColor = (44, 62, 80)):
        self.renderSurface = renderSurface
        self.boxX = boxX
        self.boxY = boxY
        self.length = length
        self.frame = frame
        self.frameColor = frameColor
        self.backgroundColor = backgroundColor
        self.active = False
    
    def draw(self):
        self.outerRect = pygame.draw.rect(self.renderSurface, self.frameColor, pygame.Rect(self.boxX, self.boxY, self.length, self.length))
        if self.active:
            self.selectedRect = pygame.draw.rect(self.renderSurface, self.frameColor, pygame.Rect(self.boxX + self.frame, self.boxY + self.frame, self.length - 2*self.frame, self.length - 2*self.frame))
        else:
            self.insideRect = pygame.draw.rect(self.renderSurface, self.backgroundColor, pygame.Rect(self.boxX + self.frame, self.boxY + self.frame, self.length - 2*self.frame, self.length - 2*self.frame))
    
    def dealEvent(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(self.outerRect.collidepoint(event.pos)):  # 若按下鼠标且位置在文本框
                self.active = not self.active
            else:
                self.active = False
    
    def returnAcitve(self) -> bool:
        return self.active