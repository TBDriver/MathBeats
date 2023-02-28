import pygame

class inputBox:
    def __init__(self, rect: pygame.Rect = pygame.Rect(100, 100, 140, 32), font: str = ".\data\\ttf\\狮尾四季春-Regular.ttf", size: int = 18) -> None:
        """
        rect 传入矩形实体 传达输入框的位置和大小
        """
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')  # 未被选中的颜色
        self.color_active = pygame.Color('dodgerblue2')  # 被选中的颜色
        self.color = self.color_inactive  # 当前颜色，初始为未激活颜色
        self.active = False
        self.text = ''
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