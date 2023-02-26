import pygame	 # 导入pygame库
comp = []	 # 储存组件


def init(size, title):	 # 初始化，明确窗口的大小和标题
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(title)
    return screen	# 返回screen后面用


def listening():	 # 监听鼠标事件
    x, y = pygame.mouse.get_pos()	 # 获取鼠标位置
    for m in comp:	 # 遍历组件
        if m[-1][0] <= x <= m[-1][0]+m[-1][2] and m[-1][1] <= y <= m[-1][3]+m[-1][1]:	 # 判断鼠标是否在组件上
            m[-2] = True
        else:
            m[-2] = False


def button(size, position, font, font_color, background,
           click_f_color, click_background, func, edge=5, width=0, title="Button"):	 # 添加按钮组件
    if_click = False
    crash_rect = [0, 0, 0, 0]	 # “碰撞体”，鼠标在这个范围算碰撞
    return ["bu", title, position, font, background, font_color,
            size, width, click_f_color, click_background, func, edge, if_click, crash_rect]


def label(size, position, font, font_color, background=0, title="Label",
          edge=5, width=0):	 # 标签组件
    if_click = False
    crash_rect = [0, 0, 0, 0]
    return ["la", title, position, font, background, font_color, size, width, edge, if_click, crash_rect]


def register_cp(way):	 # 注册组件
    comp.append(way)


def text_objects(text, font, color):	 # 定义文字
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def display(scr, com):	 # 显示组件
    for n in com:
        if n[0] == "bu":    # 如果是按钮
            if n[12]:   # 判断是否点击
                large_text = pygame.font.Font(n[3], n[6])
                text_surf, text_rect = text_objects(n[1], large_text, n[8])
                text_rect.center = n[2]
                pygame.draw.rect(scr, n[9], (text_rect.left - n[11],
                                             text_rect.top - n[11],
                                             text_rect.width + n[11] * 2,
                                             text_rect.height + n[11] * 2), n[7])
                scr.blit(text_surf, text_rect)	 # 把字刻在屏幕上
                n[13] = text_rect
            else:
                large_text = pygame.font.Font(n[3], n[6])
                text_surf, text_rect = text_objects(n[1], large_text, n[5])
                text_rect.center = n[2]
                pygame.draw.rect(scr, n[4], (text_rect.left-n[11],
                                             text_rect.top-n[11],
                                             text_rect.width+n[11]*2,
                                             text_rect.height+n[11]*2), n[7])
                scr.blit(text_surf, text_rect)
                n[13] = text_rect

        if n[0] == "la":    # 如果是标签 'freesansbold.ttf', 115
            large_text = pygame.font.Font(n[3], n[6])
            text_surf, text_rect = text_objects(n[1], large_text, n[5])
            text_rect.center = n[2]
            if n[4] != 0:
                pygame.draw.rect(scr, n[4], (text_rect.left-n[-3],
                                             text_rect.top-n[-3],
                                             text_rect.width+n[-3]*2,
                                             text_rect.height+n[-3]*2), n[-2])
            scr.blit(text_surf, text_rect)


def run(scr, background):	 # 主循环
    go_on = True
    while go_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:	 # 如果点击关闭窗口，则循环结束
                go_on = False
        scr.fill(background)	 # 设置屏幕背景色
        display(scr, comp)
        listening()
        pygame.display.update()	 # 更新屏幕


