if __name__ == "__main__":
    from time import sleep,gmtime
    import os
    import random
    import play
    from colorama import init, Fore, Back
    init(autoreset=True)

    os.system("mode con:cols=120 lines=40")
    os.system("title MathBeats - [加载中~]")
    
    
    WaitingInfo = ['温馨提示：投喂主播可以获得金坷拉一吨',
                    '有时，失去理智何尝不是件好事呢',
                    '其实这个游戏的灵感来源于琪露诺（九章算术！）',
                    '是新游戏哦',
                    '哦我的上帝',
                    '嗨嗨嗨',
                    '特效写了挺久的，但是表现力真的太强啦',
                    '一二三四五六七',
                    '头发减少术！',
                    '我吃两碗',
                    '哼哼想什么呢',
                    '这个游戏会持续更新更多内容哦！没事就进入检查更新试试看吧！',
                    '这个游戏的想法来源是一款优秀的游戏《节奏医生》。']
    def WaitingForInfo(WaitingProgress,Choiced_Tip):
        '''
        用于缩小程序体积
        刻在DNA里的模块化
        
        Choiced_Tip:    Str,等待时的提示
        WatingProgress: Int ,加载阶段数,请注意总数为116,合理分配
        '''
        sleep(0.05)
        os.system('cls')    
        j=0              # 加载进度
        
        for i in range(39):
            if i == 0:
                print('================================================[ Loading Progress ]====================================================')
            elif i == 2 or i == 4 or i == 37:
                print('|======================================================================================================================|')
            elif i == 1:
                print('| ',end='')
                while (j<WaitingProgress):
                    print(Back.LIGHTGREEN_EX + '=',end='') # 此处共需要116个等号，需要平均分配
                    j+=1
                for i in range(116-WaitingProgress):
                    print(" ",end="")
                print(' |')
            elif i == 3:
                Random_Tips = Choiced_Tip
                print('| Tips: ' + Random_Tips,end="")
                for i in range(110-len(Random_Tips)*2):
                    print(" ",end="")
                print(" |")
            elif i == 13 or i == 19:
                print('|                                        ------------------------------------                                          |')
            elif i == 14 or i == 16 or i == 18:
                print('|                                        |                                  |                                          |')
            elif i == 15:
                print('|                                        |             加载中...            |                                          |')
            elif i == 17:
                print('|                                        |            Loading...            |                                          |')
            else:
                print('|                                                                                                                      |')


    Now_Tip = random.choice(WaitingInfo)
    WaitingForInfo(0,Now_Tip)
    WaitingForInfo(29,Now_Tip)
    # 加载模块
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"]=""
    import pygame,keyboard,random,requests,zipfile,threading


    WaitingForInfo(58,Now_Tip)
    #加载pygame
    import play
    playthings = play.playmain()
    global In_Title,In_BGM,BGMControler
    In_Title = True
    In_BGM = False
    BGMControler = True


    WaitingForInfo(87,Now_Tip)
    # 加载存档与设置
    # 存档文件夹
    try:    os.mkdir(".\config")
    except: pass
    try:    os.mkdir(".\data")
    except: pass
    try:    os.mkdir(".\cache")
    except: pass
    with open(".\config\config.mb","r+") as f:
        READ_CONFIG_DATA = f.read() # 读取设置
        CONFIG_DATA = READ_CONFIG_DATA.split("\n")
    with open(".\config\save.mb","r+") as f:
        global Save_Time
        Save_Time = gmtime(os.path.getmtime(".\config\save.mb"))
    
    
    Now_Tip = random.choice(WaitingInfo)
    WaitingForInfo(116,Now_Tip)
    # 加载歌曲
    global Song_List
    Song_List = []
    Score_List = []
    Songs = os.listdir(".\data\music")
    for i in range(len(Songs)): # 查找歌曲
        Song_List.append([]) # 增加一首歌的槽位
        Score_List.append([]) # 增加一首歌的铺面
        with open(".\data\music\\" + Songs[i-1] + "\song.ini",encoding='utf-8') as f:
            for line in f:
                Song_List[i].append(line.strip())
        with open(".\data\music\\" + Songs[i-1] + ".\score",encoding="utf-8") as f:
            Local_Operation = 0 # 当前读取铺面note
            for line in f:
                if line.strip() == "start":
                    # 开始读取铺面Local Note
                    Score_List[i].append([]) # 当前铺面第i-1个note
                elif line.strip() == "stop":
                    Local_Operation += 1 # 读取完成
                else:
                    Score_List[i][Local_Operation].append(line.strip()) # 谱堆 谱面 note
        
        sleep(0.02) # 缓一下   
    '''
    | 歌曲信息 - song.ini
    第12行: 歌曲名及所占字符数
    第34行: 作者名及所占字符数
    第56行: 铺师名及所占字符数
    第78行: 歌曲难度
    第9行:  BPM
========================================
    | 铺面信息 - score
    使用方法：
    Score_List[谱面索引][Note索引][操作]
    
    操作对应：
    0  开始时间(ms)
    1     题目
    2  题目所占字符      共6项
    3     结果
    4     拍数
    5  每拍时间(ms)
    '''
    
        
    def Continue_Play_Title():
        pygame.mixer.music.load("./data/sound/finale_start_loop.ogg")
        if pygame.mixer.music.get_busy() == True and In_Title == True:
            pygame.mixer.music.play(-1)
        global BGMControler
        while pygame.mixer.music.get_busy():
            continue
    def Play_Title_BGM():
        pygame.mixer.music.load("./data/sound/" + "finale_start_full.mp3")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()
        global BGMControler
        while BGMControler and In_Title:
            if pygame.mixer.music.get_busy() == False and In_Title == True:
                Continue_Play_Title()
            elif not pygame.mixer.music.get_busy() == True:
                continue
    def Play_BGM():
        pygame.mixer.music.load("./data/sound/" + "bgm_full.ogg")
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play()
        while BGMControler:
            if pygame.mixer.music.get_busy():
                continue
            else:
                break
        if In_BGM:
            Continue_Play_Title()
    def Check_and_Continue_BGM():
        if pygame.mixer.music.get_busy() == True:
            pass
        if pygame.mixer.music.get_busy() == False:
            thread = threading.Thread(target=Play_BGM)
            thread.start()
    
    class MathBeats_Main():
        def __init__(self):
            self.Title_Screen_ = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                     Math  Beats                                                      |',
    '|                                                      By 刘润东                                                       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '========================================================================================================================']
            self.Lanp = ['========================================================================================================================',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '========================================================================================================================']
            self.Coin = 0
            self.Version = "0.0.1"
            self.WaitingColor = [Fore.LIGHTWHITE_EX,Fore.LIGHTWHITE_EX,Fore.LIGHTWHITE_EX,Fore.LIGHTBLACK_EX,Fore.BLACK]
            self.LightColor = [Fore.BLACK,Fore.LIGHTBLACK_EX,Fore.WHITE,Fore.LIGHTWHITE_EX]
            
        def Refresh_Data(self):
            global Save_Time
            self.Main_Screen_ = ['===================================================[ Math Beats ]======================================================',
    '|                                     |     ' + Fore.YELLOW + '       ______         ' + Fore.LIGHTWHITE_EX + '                            |                        |',
    '|                                     |     ' + Fore.YELLOW + '      / _____)       保存进度               ' + Fore.LIGHTWHITE_EX + '      |                        |',
    '|                                     |     ' + Fore.YELLOW + '     ( (____   _____  _   _  _____        ' + Fore.LIGHTWHITE_EX + '        |                        |',
    '|                                     |     ' + Fore.YELLOW + '      \____ \ (____ || | | || ___ |        ' + Fore.LIGHTWHITE_EX + '       |                        |',
    '|                                     |     ' + Fore.YELLOW + '      _____) )/ ___ | \ V / | ____|       ' + Fore.LIGHTWHITE_EX + '        |                        |',
    '|                                     |     ' + Fore.YELLOW + '     (______/ \_____|  \_/  |_____)       ' + Fore.LIGHTWHITE_EX + '        |                        |',
    '|                                     |                                                       |                        |',
    '|----------------------------------------------------------------------------------------------------------------------|',
    '|                                        | ' + Fore.RED + '  ________  _________  ________  ________  _________    ' + Fore.LIGHTWHITE_EX + '   |                |',
    '|                                        | ' + Fore.RED + ' |\   ____\|\___   ___|\   __  \|\   __  \|\___   ___\  ' + Fore.LIGHTWHITE_EX + '   |                |',
    '|                                        |' + Fore.RED + '  \ \  \___|\|___ \  \_\ \  \|\  \ \  \|\  \|___ \  \_|  ' + Fore.LIGHTWHITE_EX + '   |                |',
    '|                                        | ' + Fore.RED + '  \ \_____  \   \ \  \ \ \   __  \ \   _  _\   \ \  \    ' + Fore.LIGHTWHITE_EX + '  |                |',
    '|                                        | ' + Fore.RED + '   \|____|\  \   \ \  \ \ \  \ \  \ \  \\\  \|   \ \  \   ' + Fore.LIGHTWHITE_EX + '  |                |',
    '|                                        | ' + Fore.RED + '     ____\_\  \   \ \__\ \ \__\ \__\ \__\\\ _\    \ \__\\  ' + Fore.LIGHTWHITE_EX + '  |                |',
    '|                                        | ' + Fore.RED + '    |\_________\   \|__|  \|__|\|__|\|__|\|__|    \|__|   ' + Fore.LIGHTWHITE_EX + ' |                |',
    '|                                        |  ' + Fore.RED + '    \|_________|                        开始旅途!        ' + Fore.LIGHTWHITE_EX + ' |                |',
    '|                                        |                                                            |                |',
    '|----------------------------------------------------------------------------------------------------------------------|',
    '|                                 | ____                    __                                  |                      |',
    '|                                 |/\  _`\                 /\ \__  __        继续游戏           |                      |',
    '|                                 |\ \ \/\_\    ___     ___\ \ ,_\/\_\    ___   __  __     __   |                      |',
    '|                                 | \ \ \/_/_  / __`\ /\' _ `\ \ \/\/\ \ /\' _ `\/\ \/\ \  /\'__`\ |                      |',
    '|                                 |  \ \ \L\ \/\ \L\ \/\ \/\ \ \ \_\ \ \/\ \/\ \ \ \_\ \/\  __/ |                      |',
    '|                                 |   \ \____/\ \____/\ \_\ \_\ \__\\\ \_\ \_\ \_\ \____/\ \____\|                      |',
    '|                                 |    \/___/  \/___/  \/_/\/_/\/__/ \/_/\/_/\/_/\/___/  \/____/|                      |',
    '|                                 |                                                             |                      |',
    '|                                 |            上个存档：{:04}年{:02}月{:>02}日{:>02}点{:02}分{:02}秒             |                      |'.format(Save_Time.tm_year,Save_Time.tm_mon,Save_Time.tm_mday,Save_Time.tm_hour,Save_Time.tm_min,Save_Time.tm_sec),
    '|                                 |  硬币数量：{:04}                                             |                      |'.format(self.Coin),
    '|                                 |                                                             |                      |',
    '|                                 |\                                                            |                      |',
    '|                                 | \                                                           |                      |',
    '|----------------------------------------------------------------------------------------------------------------------|',
    '|  _____        _  _              | ' + Back.LIGHTBLUE_EX + '检查更新 | Check Update' + Back.BLACK + '                            | ' + Back.BLUE + 'Update Log | 更新日志' + Back.BLACK + '         |',
    '| | ____|__  __(_)| |_    退出    |                                                    | Must connet to the Internet!  |',
    '| |  _|  \ \/ /| || __| --------> |                                                    | 需要联网使用~                 |',
    '| | |___  >  < | || |_            |------------------------------------------------------------------------------------|',
    '| |_____|/_/\_\|_| \__|           | Info:当前选中：                                                                    |',
    '====================================================[ 数据 ]============================================================'
    ]
            with open(".\config\save.mb","r+") as f:
                Save_Time = gmtime(os.path.getmtime(".\config\save.mb"))
            
            
        def Change_By_Fade_Effect(self,Turn_Str):
            self.Refresh_Data()
            thread = threading.Thread(target=playthings.Play_Close_Sound)
            thread.start()
            os.system("color 07")
            sleep(0.05)
            os.system("color 08")
            sleep(0.05)
            os.system("cls")
            sleep(1)
            # print(Turn_Str)
            for i in range(39):
                print(Turn_Str[i])
            os.system("color 08")
            sleep(0.05)
            thread = threading.Thread(target=playthings.Play_Open_Sound)
            thread.start()
            os.system("color 07")
            sleep(0.05)
        
        
        def Title_Screen(self):
            thread = threading.Thread(target=Play_Title_BGM)
            thread.start()
            os.system("title MathBeats")
            self.Refresh_Data()
            thread = threading.Thread(target=playthings.Play_Close_Sound)
            thread.start()
            os.system("color 07")
            sleep(0.1)
            os.system("color 08")
            sleep(0.1)
            os.system("cls")
            sleep(1)
            global Enter
            Enter = True
            global In_Title,In_BGM
            In_Title = True
            In_BGM = False
            sleep(0.5)
            Sentences = ['                                                   在这繁忙的世界上                                                              ',
                         '                                                     能够犒劳你的，                                                              ',
                         '                                                   可能不只是快乐...                                                             ',
                         '                                                    身为人类的一员，                                                             ',
                         '                                                     打击固然有，                                                                ',
                         '                                                      借力化力                                                                   ',
                         '                                                   才是此族的选择。                                                              ']
            os.system("cls")
            self.Skip_Intro = False
            print(" \n  Hold \"S\" to Skip | 长按\"S\"跳过\n\n\n\n\n\n\n\n\n")
            for i in range(len(Sentences)):
                if keyboard.is_pressed('s'):
                    self.Skip_Intro = True
                if self.Skip_Intro:
                    continue
                for color in self.LightColor:
                    if keyboard.is_pressed('s'):
                        self.Skip_Intro = True
                    if self.Skip_Intro:
                        continue
                    os.system("cls")
                    print(" \n  Hold \"S\" to Skip | 长按\"S\"跳过\n\n\n\n\n\n\n\n\n")
                    for j in range(i):
                        if keyboard.is_pressed('s'):
                            self.Skip_Intro = True
                        print(Sentences[j])
                    print(color + Sentences[i])
                    sleep(0.05)
                    if keyboard.is_pressed('s'):
                        self.Skip_Intro = True
                sleep(1.75)
                
            sleep(0.1167)
            os.system("cls")
            pygame.mixer.music.set_pos(16.2)
            for i in range(39):
                print(self.Title_Screen_[i])
            sleep(0.95)
            while(Enter):
                sleep(0.21)
                def Exit_While(x):
                    global Enter
                    Enter = False
                    global In_Title,In_BGM
                    In_Title = False
                    In_BGM = True
                self.Title_Screen_ = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                     ' + Fore.WHITE + 'Math  Beats' + Fore.LIGHTWHITE_EX + '                                                      |',
    '|                                                      By 刘润东                                                       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                    ' + Fore.LIGHTBLACK_EX + '按任意键开始游戏' + Fore.LIGHTWHITE_EX + '                                                  |',# 24here
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '========================================================================================================================']
                for j in range(len(self.WaitingColor)):
                    sleep(0.07)
                    os.system("cls")
                    for i in range(39):
                        if i == 23:
                            print('|                                                   ' + self.WaitingColor[j] + '按任意键开始游戏' + Fore.LIGHTWHITE_EX + '                                                   |')
                        else:
                            print(self.Title_Screen_[i])
                    keyboard.on_press(Exit_While)
            pygame.mixer.music.fadeout(1000)
            self.Refresh_Data()
            self.From_Title = True


        def Show_Main_Info(self,Info,longth,*Effect):
            '''
            longth计算方式:总字符数*2-非中文字符数
            '''
            longth = len(Info)*2 - longth
            Own_Effect = False
            try:
                if Effect:
                    Own_Effect = True
            except:
                pass
            self.Refresh_Data()
            if Own_Effect:
                os.system("color 07")
                sleep(0.1)
                os.system("color 08")
                sleep(0.1)
                os.system("cls")
                sleep(1)
            os.system('cls')
            for i in range(39):
                if i == 37:
                    print('| |_____|/_/\_\|_| \__|           | Info:' + Info,end='')
                    for j in range(77-longth):
                        print(" ",end="")
                    print(' |')
                else:
                    print(self.Main_Screen_[i])
            if Own_Effect:
                os.system("color 08")
                sleep(0.1)
                os.system("color 07")
                sleep(0.1)

        def Main_Screen(self):
            if self.From_Title:
                self.Refresh_Data()
                for i in range(39):
                    print(self.Main_Screen_[i])
                self.From_Title = False
            self.Main_Screen_Options_List = [[1,"保存进度",3],# 第一行
                                            [4,"开始游戏",6],# 第二行
                                            [7,"加载存档",9],# 第三行
                                            ["退出游戏","检查更新","更新日志"]] # 第四行
            global In_Title,BGMControler
            In_Title = False
            BGMControler = True
            
            self.Check_Main = True
            self.Locate_Main_Screen = [0,0] # 行，列
            self.User_Choice = "保存进度"
            def Get_Choice():
                return self.Main_Screen_Options_List[self.Locate_Main_Screen[0]][self.Locate_Main_Screen[1]]
            while(self.Check_Main):
                self.User_Choice = Get_Choice()
                if keyboard.is_pressed('up'):
                    Check_and_Continue_BGM()
                    thread = threading.Thread(target=playthings.Play_Change_Sound)
                    thread.start()
                    self.Show_Main_Info("当前选中：" + str(self.User_Choice),0)
                    if self.Locate_Main_Screen[0] == 0:
                        pass
                    elif self.Locate_Main_Screen[0] > 0:  # 大于0，也就是可以向上
                        self.Locate_Main_Screen[0] -= 1   # 向上操作
                        self.User_Choice = Get_Choice()
                    self.Show_Main_Info("当前选中：" + str(self.User_Choice),0)
                if keyboard.is_pressed('down'):
                    Check_and_Continue_BGM()
                    thread = threading.Thread(target=playthings.Play_Change_Sound)
                    thread.start()
                    if self.Locate_Main_Screen[0] == 3: # 最后一行即第四行
                        pass
                    elif self.Locate_Main_Screen[0] < 4:
                        self.Locate_Main_Screen[0] += 1
                    self.User_Choice = Get_Choice()
                    self.Show_Main_Info("当前选中：" + str(self.User_Choice),0)
                        
                if keyboard.is_pressed('left'):
                    Check_and_Continue_BGM()
                    if self.Locate_Main_Screen[1] == 0: # 第一列
                        pass
                    elif self.Locate_Main_Screen[1] > 0:
                        self.Locate_Main_Screen[1] -= 1
                    self.User_Choice = Get_Choice()
                    self.Show_Main_Info("当前选中：" + str(self.User_Choice),0)
                if keyboard.is_pressed('right'):
                    Check_and_Continue_BGM()
                    thread = threading.Thread(target=playthings.Play_Change_Sound)
                    thread.start()
                    if self.Locate_Main_Screen[1] == 2: # 第三列
                        pass
                    elif self.Locate_Main_Screen[1] < 3:
                        self.Locate_Main_Screen[1] += 1
                    self.User_Choice = Get_Choice()
                    self.Show_Main_Info("当前选中：" + str(self.User_Choice),0)
                
                if keyboard.is_pressed('enter'):
                    Check_and_Continue_BGM()
                    self.User_Choice = Get_Choice()
                    if self.User_Choice == "保存进度":
                        self.Save()
                    elif self.User_Choice == "加载存档":
                        self.Load()
                    elif self.User_Choice == "开始游戏":
                        self.Choose_Songs()
                    elif self.User_Choice == "检查更新":
                        self.Check_Update()
                    elif self.User_Choice == "退出游戏":
                        self.exit()
                    self.User_Choice = Get_Choice()
                    self.Show_Main_Info("当前选中：" + str(self.User_Choice),0)
                sleep(0.09)
        
        
        def Choose_Songs(self):
            
            # 歌曲特效
            self.Choose_Songs_Screen = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                       ---------------------------------------------------------------|',
    '|                                                      /                                                               |',
    '|                                                     /                                                                |',
    '|                                                    /                                                                 |',
    '|                                   -----------------------------------------------------------------------------------|',
    '|                                   \                                                                                  |',
    '|                                    \                                                                                 |',
    '|                                     \                                                                                |',
    '|  ----------------------\             \                                                                               |',
    '|   Located Song 选中歌曲 |--->         \                                                                              |',
    '|  ----------------------/               \                                                                             |',
    '|                                         \                                                                            |',
    '|                                          \                                                                           |',
    '|                                           \                                                                          |',
    '|                                            \                                                                         |',
    '|                                             \                                                                        |',
    '|                                              \_______________________________________________________________________|',
    '|                                                            \                                                         |',
    '|                                                             \                                                        |',
    '|                                                              \_______________________________________________________|',
    '|                                                                                                                      |',
    '| Press "0" to Exit | 按下0回到主页面                                                                                  |',
    '========================================================================================================================']
            self.Switch_Song_1 = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                       ---------------------------------------------------------------|',
    '|                                                      /                                                               |',
    '|                                                     /                                                                |',
    '|                                                    /                                                                 |',
    '|                                                   /                                                                  |',
    '|                                   -----------------------------------------------------------------------------------|',
    '|                                   \                                                                                  |',
    '|                                    \                                                                                 |',
    '|                                     \                                                                                |',
    '|                                      \                                                                               |',
    '|                                       \                                                                              |',
    '|                                        \                                                                             |',
    '|                                         \                                                                            |',
    '|                                          \                                                                           |',
    '|                                           \                                                                          |',
    '|                                            \                                                                         |',
    '|                                             \                                                                        |',
    '|                                              \_______________________________________________________________________|',
    '|                                                             \                                                        |',
    '|                                                              \_______________________________________________________|',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '========================================================================================================================']
            self.Switch_Song_2 = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                     -----------------------------------------------------------------|',
    '|                                                    /                                                                 |',
    '|                                                   /                                                                  |',
    '|                                                  /                                                                   |',
    '|                                                 /                                                                    |',
    '|                                                /                                                                     |',
    '|                                   -----------------------------------------------------------------------------------|',
    '|                                   \                                                                                  |',
    '|                                    \                                                                                 |',
    '|                                     \                                                                                |',
    '|                                      \                                                                               |',
    '|                                       \                                                                              |',
    '|                                        \                                                                             |',
    '|                                         \                                                                            |',
    '|                                          \                                                                           |',
    '|                                           \                                                                          |',
    '|                                            \                                                                         |',
    '|                                             \________________________________________________________________________|',
    '|                                                             \                                                        |',
    '|                                                              \_______________________________________________________|',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '========================================================================================================================']
            self.Switch_Song_3 = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                             -------------------------------------------------------------------------|',
    '|                                              \                                                                       |',
    '|                                               \                                                                      |',
    '|                                                \                                                                     |',
    '|                                                /                                                                     |',
    '|                                               /                                                                      |',
    '|                                              /                                                                       |',
    '|                                             /                                                                        |',
    '|                                            /                                                                         |',
    '|                                   -----------------------------------------------------------------------------------|',
    '|                                   \                                                                                  |',
    '|                                    \                                                                                 |',
    '|                                     \                                                                                |',
    '|                                      \                                                                               |',
    '|                                       \                                                                              |',
    '|                                        \                                                                             |',
    '|                                         \                                                                            |',
    '|                                          \                                                                           |',
    '|                                           \__________________________________________________________________________|',
    '|                                                              \_______________________________________________________|',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '========================================================================================================================']
            self.Switch_Song_4 = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                               -----------------------------------------------------------------------|',
    '|                                               \                                                                      |',
    '|                                                \                                                                     |',
    '|                                                 \                                                                    |',
    '|                                                  \                                                                   |',
    '|                                                   \                                                                  |',
    '|                                                    \                                                                 |',
    '|                                                    /                                                                 |',
    '|                                                   /                                                                  |',
    '|                                                  /                                                                   |',
    '|                                                 /                                                                    |',
    '|                                    ----------------------------------------------------------------------------------|',
    '|                                     \                                                                                |',
    '|                                      \                                                                               |',
    '|                                       \                                                                              |',
    '|                                        \                                                                             |',
    '|                                         \                                                                            |',
    '|                                          \                                                                           |',
    '|                                           \                                                                          |',
    '|                                            \_________________________________________________________________________|',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '========================================================================================================================']
            self.Switch_Song_5 = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                    ------------------------------------------------------------------|',
    '|                                               -----------------------------------------------------------------------|',
    '|                                               \                                                                      |',
    '|                                                \                                                                     |',
    '|                                                 \                                                                    |',
    '|                                                  \                                                                   |',
    '|                                                   \                                                                  |',
    '|                                                    \                                                                 |',
    '|                                                     \                                                                |',
    '|                                                      \                                                               |',
    '|                                                       \                                                              |',
    '|                                                       /                                                              |',
    '|                                                      /                                                               |',
    '|                                          ----------------------------------------------------------------------------|',
    '|                                          \                                                                           |',
    '|                                           \                                                                          |',
    '|                                            \                                                                         |',
    '|                                             \                                                                        |',
    '|                                              \                                                                       |',
    '|                                               \______________________________________________________________________|',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '========================================================================================================================']
            self.Switch_Song_6 = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                    ------------------------------------------------------------------|',
    '|                                                   /                                                                  |',
    '|                                           ---------------------------------------------------------------------------|',
    '|                                            \                                                                         |',
    '|                                             \                                                                        |',
    '|                                              \                                                                       |',
    '|                                               \                                                                      |',
    '|                                                \                                                                     |',
    '|                                                 \                                                                    |',
    '|                                                  \                                                                   |',
    '|                                                   \                                                                  |',
    '|                                                    \                                                                 |',
    '|                                                     \                                                                |',
    '|                                                      \                                                               |',
    '|                                               -----------------------------------------------------------------------|',
    '|                                               \                                                                      |',
    '|                                                \                                                                     |',
    '|                                                 \                                                                    |',
    '|                                                  \                                                                   |',
    '|                                                   \__________________________________________________________________|',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '========================================================================================================================']
            self.Switch_Song_7 = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                    ------------------------------------------------------------------|',
    '|                                                   /                                                                  |',
    '|                                                  /                                                                   |',
    '|                                          ----------------------------------------------------------------------------|',
    '|                                           \                                                                          |',
    '|                                            \                                                                         |',
    '|                                             \                                                                        |',
    '|                                              \                                                                       |',
    '|                                               \                                                                      |',
    '|                                                \                                                                     |',
    '|                                                 \                                                                    |',
    '|                                                  \                                                                   |',
    '|                                                   \                                                                  |',
    '|                                                    \                                                                 |',
    '|                                                     \                                                                |',
    '|                                                      ----------------------------------------------------------------|',
    '|                                                         \                                                            |',
    '|                                                          \                                                           |',
    '|                                                           \                                                          |',
    '|                                                            \_________________________________________________________|',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '========================================================================================================================']
            self.Switch_Song_8 = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                     -----------------------------------------------------------------|',
    '|                                                    /                                                                 |',
    '|                                                   /                                                                  |',
    '|                                                  /                                                                   |',
    '|                                   -----------------------------------------------------------------------------------|',
    '|                                    \                                                                                 |',
    '|                                     \                                                                                |',
    '|                                      \                                                                               |',
    '|                                       \                                                                              |',
    '|                                        \                                                                             |',
    '|                                         \                                                                            |',
    '|                                          \                                                                           |',
    '|                                           \                                                                          |',
    '|                                            \                                                                         |',
    '|                                             \                                                                        |',
    '|                                              \                                                                       |',
    '|                                              ------------------------------------------------------------------------|',
    '|                                                         \                                                            |',
    '|                                                          \                                                           |',
    '|                                                           \__________________________________________________________|',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '========================================================================================================================']
            self.Switch_Animation = [self.Choose_Songs_Screen,
                                     self.Switch_Song_1,
                                     self.Switch_Song_2,
                                     self.Switch_Song_3,
                                     self.Switch_Song_4,
                                     self.Switch_Song_5,
                                     self.Switch_Song_6,
                                     self.Switch_Song_7,
                                     self.Switch_Song_8,
                                     self.Choose_Songs_Screen]
            self.Change_By_Fade_Effect(self.Choose_Songs_Screen)
            
            def PrintChooseSong(Now_Song_Index):
                self.Choose_Songs_Screen = ['========================================================================================================================',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
    '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
    '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
    '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
    '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
    '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
    '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
    '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
    '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
    '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
    '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
    '|                                                                                                                      |',
    '|                                                                                                                      |',
    '|                                                       ---------------------------------------------------------------|',
    '|                                                      /                                                               |',
    '|                                                     /                                                                |',#18
    '|                                                    /                                                                 |',
    '|                                   -----------------------------------------------------------------------------------|',
    '|                                   \                                                                                  |',
    '|                                    \                                                                                 |',#22
    '|                                     \                                                                                |',
    '|  ----------------------\             \                                                                               |',
    '|   Located Song 选中歌曲 |--->         \                                                                              |',
    '|  ----------------------/               \                                                                             |',
    '|                                         \                                                                            |',
    '|                                          \                                                                           |',
    '|                                           \                                                                          |',
    '|                                            \                                                                         |',
    '|                                             \                                                                        |',
    '|                                              \_______________________________________________________________________|',
    '|                                                            \                                                         |',
    '|                                                             \                                                        |',#34
    '|                                                              \_______________________________________________________|',
    '|                                                                                                                      |',
    '| Press "0" to Exit | 按下0回到主页面                                                                                  |',
    '========================================================================================================================']
                for i in range(39):
                    if i == 18:
                        if Now_Song_Index == 0:
                            print("|                                                     /     " + Song_List[-1][0],end="")
                            for j in range(116-60-int(Song_List[-1][1])):
                                print(" ",end="")
                            print(" |")
                        else:
                            print('|                                                     /     ' + Song_List[Now_Song_Index-1][0],end='')
                            for j in range(116-60-int(Song_List[Now_Song_Index-1][1])):
                                print(" ",end="")
                            print(" |")
                    elif i == 22:
                        print("|                                    \         " + Song_List[Now_Song_Index][0],end="")
                        for j in range(116-47-int(Song_List[Now_Song_Index][1])):
                            print(" ",end="")
                        print(" |")
                    elif i == 34:
                        if Now_Song_Index == len(Song_List)-1:
                            print("|                                                             \   " + Song_List[Now_Song_Index-1][0],end="")
                            for j in range(116-66-int(Song_List[0][1])):
                                print(" ",end="")
                            print(" |")
                        else:
                            print("|                                                             \   " + Song_List[Now_Song_Index+1][0],end="")
                            for j in range(116-66-int(Song_List[Now_Song_Index+1][1])):
                                print(" ",end="")
                            print(" |")
                    else:
                        print(self.Choose_Songs_Screen[i])
                        
            self.Keep_Choose_Songs = True
            global In_BGM
            In_BGM = False
            self.Corect_Play = False
            
            os.system("cls")
            self.Located_Song = 0
            PrintChooseSong(self.Located_Song)
            # 经优化，此处不会出现长按持续增加现象
            while self.Keep_Choose_Songs:
                if keyboard.is_pressed('up'):
                    if self.Located_Song <= 0:
                        self.Located_Song = len(Song_List)-1
                    else:
                        self.Located_Song -= 1
                    for i in range(10):
                        os.system("cls")
                        for j in self.Switch_Animation[i]:
                            print(j)
                        sleep(0.02)
                    os.system("cls")
                    PrintChooseSong(self.Located_Song)
                if keyboard.is_pressed('down'):
                    if self.Located_Song >= len(Song_List)-1:
                        self.Located_Song = 0
                    else:
                        self.Located_Song += 1
                    for i in range(9,-1,-1):
                        os.system("cls")
                        for j in self.Switch_Animation[i]:
                            print(j)
                        sleep(0.02)
                    os.system("cls")
                    PrintChooseSong(self.Located_Song)
                if keyboard.is_pressed('enter'):
                    self.Start_Play(self.Located_Song)
                if keyboard.is_pressed('0'):
                    self.Change_By_Fade_Effect(self.Main_Screen_)
                    break
            if self.Corect_Play:
                self.Start_Play(self.Located_Song)
                    
        def Play_Song(self):
            pygame.mixer.music.load("./data/music/" + Songs[self.Located_Song] + "/music.mp3")
            pygame.mixer.music.set_volume(4)
            pygame.mixer.music.play()
        
        def Cal_HP(self,Volume,Level):
            Volume = int(Volume)
            Level = int(Level)
            if Volume < 400:
                Temp = 80/Volume + 0.2
            elif 400 <= Volume and Volume < 600:
                Temp = 32/Volume + 0.2
            elif Volume >= 600:
                Temp = 96/Volume + 0.08
            if Level >= 11:
                return Temp*0.8
            else:
                return Temp
        
        def Play_Beats(self):
            self.Local_beats = 0
            exit_it = False
            sleep(1)
            self.Able_to_Touch = True
            for i in range(5):
                if exit_it == True:
                  continue  
                elif pygame.mixer.music.get_busy():
                    while self.Keep_Playing:
                        for j in range(int(Score_List[self.Located_Song][self.Local_Note][4])):
                            # print("当前音符：" + str(self.Local_Note) + "\n当前节拍/s:" + str(60/int(Song_List[self.Located_Song][8])) + "节拍间隔：" + str(Score_List[self.Located_Song][len(Score_List[self.Located_Song])-1][0] - Score_List[self.Located_Song][self.Local_beats][0]))
                            self.Local_beats += 1
                            thread = threading.Thread(target=playthings.Play_Beat_Sound)
                            thread.start()
                            sleep(60/int(Score_List[self.Located_Song][self.Local_Note][6]))
                        # note间隔时间
                        if self.Local_Note >= int(len(Score_List[self.Located_Song]))-1:
                            exit_it = True
                            self.Able_to_Touch = False
                            break
                        else:
                            sleep(int(Score_List[self.Located_Song][self.Local_Note+1][0]) - int(Score_List[self.Located_Song][self.Local_Note][0]))
                        self.Local_Note += 1
                        self.Local_beats = 0
                    return
                sleep(0.01)
        
        def Start_Play(self,song_index):
            thread = threading.Thread(target=playthings.Play_Song_Confirm)
            thread.start()
            pygame.mixer.music.fadeout(400)
            global BGMControler
            BGMControler = False
            self.NowHP = 0 #Max100,1= = 2HP
            self.Play_Screen_1Track_Effect = ['========================================================================================================================',
                         '| Loading...                                                 HP [                                                  ]   |',#1
                         '|======================================================================================================================|',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',#4
                         '|                                                                                                                      |',
                         '|======================================================================================================================|',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                       ----- ----- ----- ----- ----- ----- -----                                      |',#19
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '|                                                                                                                      |',
                         '========================================================================================================================']
            self.Change_By_Fade_Effect(self.Play_Screen_1Track_Effect)  
            def Print_Refresh_Play_Screen():
                # 一次屏幕打印
                os.system("cls")
                for i in range(39):
                    if i == 1:
                        print('| ' + Fore.BLACK + Back.LIGHTWHITE_EX + '{}'.format(Song_List[song_index][0]) + Back.BLACK + Fore.WHITE + ' 音乐:{} 铺面:{} '.format(Song_List[song_index][2],Song_List[song_index][4]) + Fore.BLACK + Back.LIGHTRED_EX + ' Lv.{} '.format(Song_List[song_index][6]) + Fore.LIGHTWHITE_EX + Back.BLACK,end="")
                        for j in range(120-66-19-int(Song_List[song_index][1])-int(Song_List[song_index][3])-int(Song_List[song_index][5])-int(Song_List[song_index][7])):
                            print(" ",end="")
                        print("HP [",end="")
                        for k in range(int(self.NowHP/2)):
                            print("=",end="")
                        for l in range(int(50-self.NowHP/2)):
                            print(" ",end="")
                        print("]{:02} |".format(self.NowHP))
                    elif i == 4:
                        if self.Local_Note >= int(len(Score_List[self.Located_Song]))-1:
                            print('|          ' + Score_List[self.Located_Song][self.Local_Note-1][1],end="")
                            for m in range(120-11-2-int(Score_List[self.Located_Song][self.Local_Note-1][2])):
                                print(" ",end="")
                        else:
                            print('|          ' + Score_List[self.Located_Song][self.Local_Note][1],end="")
                            for m in range(120-11-2-int(Score_List[self.Located_Song][self.Local_Note][2])):
                                print(" ",end="")
                            
                        print(" |")
                    elif i == 19:
                        if self.Local_beats >= int((Score_List[self.Located_Song][self.Local_Note][4])):
                            print("|                                       ----- ----- ----- ----- ----- ----- " + Back.RED + Fore.BLACK + "--|--" + Back.BLACK + Fore.LIGHTWHITE_EX + "                                      |")
                        else:
                            if self.Local_beats == 0:
                                print("|                                       " + Back.RED + Fore.BLACK + "--|--" + Back.BLACK + Fore.LIGHTWHITE_EX + " ----- ----- ----- ----- ----- -----                                      |")
                            if self.Local_beats == 1:
                                print("|                                       ----- " + Back.RED + Fore.BLACK + "--|--" + Back.BLACK + Fore.LIGHTWHITE_EX + " ----- ----- ----- ----- -----                                      |")
                            if self.Local_beats == 2:
                                print("|                                       ----- ----- " + Back.RED + Fore.BLACK + "--|--" + Back.BLACK + Fore.LIGHTWHITE_EX + " ----- ----- ----- -----                                      |")
                            if self.Local_beats == 3:
                                print("|                                       ----- ----- ----- " + Back.RED + Fore.BLACK + "--|--" + Back.BLACK + Fore.LIGHTWHITE_EX + " ----- ----- -----                                      |")
                            if self.Local_beats == 4:
                                print("|                                       ----- ----- ----- ----- " + Back.RED + Fore.BLACK + "--|--" + Back.BLACK + Fore.LIGHTWHITE_EX + " ----- -----                                      |")
                            if self.Local_beats == 5:
                                print("|                                       ----- ----- ----- ----- ----- " + Back.RED + Fore.BLACK + "--|--" + Back.BLACK + Fore.LIGHTWHITE_EX + " -----                                      |")
                            if self.Local_beats == 6:
                                print("|                                       ----- ----- ----- ----- ----- ----- " + Back.RED + Fore.BLACK + "--|--" + Back.BLACK + Fore.LIGHTWHITE_EX + "                                      |")
                    else:
                        print(self.Play_Screen_1Track_Effect[i])
            
            sleep(1)
            self.Keep_Playing = True
            self.Local_Note = 0
            self.Local_Song_Note_HP = int(self.Cal_HP(len(Score_List[self.Located_Song]),Song_List[self.Located_Song][6]))
            self.Local_interval_time = int(Score_List[self.Located_Song][self.Local_Note][5])/1000
            self.Able_to_Touch = True
            
            Playing_Beats = False
            sleep(0.2)
            
            thread = threading.Thread(target=self.Play_Song)
            thread.start()
            global Note_Floating_Value
            Note_Floating_Value = float(Score_List[self.Located_Song][self.Local_Note][0])
            '''
            To do:
            分离打印和判断note
            '''
            
            
            
            while self.Keep_Playing:
                if keyboard.is_pressed("enter"):
                    if self.Able_to_Touch:
                        if self.Local_Note >= int(len(Score_List[self.Located_Song]))-1:
                            pass
                        else:
                            Note_Floating_Value = float(Score_List[self.Located_Song][self.Local_Note][0])
                        if Score_List[self.Located_Song][self.Local_Note][3] == "1":
                            # 判定Lost
                            if pygame.mixer.music.get_pos() + 200 >= Note_Floating_Value and pygame.mixer.music.get_pos() - 200 <= Note_Floating_Value:
                                # 判定Far
                                if pygame.mixer.music.get_pos() + 100 >= Note_Floating_Value and pygame.mixer.music.get_pos() - 100 <= Note_Floating_Value:
                                    if pygame.mixer.music.get_pos() + 50 >= Note_Floating_Value and pygame.mixer.music.get_pos() - 50 <= Note_Floating_Value:
                                        # Pure
                                        self.NowHP += self.Local_Song_Note_HP
                                        thread = threading.Thread(target=playthings.Play_Hit_Sound)
                                        thread.start()
                        else:
                            if self.NowHP >= 7:
                                self.NowHP -= 8
                            thread = threading.Thread(target=playthings.Play_Lost_Sound)
                            thread.start()
                if Playing_Beats == False:
                    thread2 = threading.Thread(target=self.Play_Beats)
                    thread2.start()
                    Playing_Beats = True
                if pygame.mixer.music.get_busy() == False:
                    self.Keep_Playing = False
                    sleep(1)
                Print_Refresh_Play_Screen()
                if self.Local_Note >= int(len(Score_List[self.Located_Song]))-1:
                    pass
                else:
                    self.Local_interval_time = int(Score_List[self.Located_Song][self.Local_Note][5])/1000
                sleep(0.075)
            
            # 检测通关与否并播放音频
            if self.NowHP == 100:
                pass
            
            
            # 回到界面
            Play_BGM()
            BGMControler = True
            thread1 = threading.Thread(target=Play_BGM)
            thread1.start()
                    
                    
        def Save(self):
            try:
                with open(".\config\save.mb","w+") as f:
                    f.write(str(self.Coin) + "\n")
                self.Refresh_Data()
                self.Show_Main_Info("存档成功！",0,True)
            except:
                self.Show_Main_Info("存档错误~可能是程序出了啥问题，重启一下吧！",1,True)
        
        def Load(self):
            try:
                global Save_Time
                with open(".\config\save.mb","r+") as f:
                    READ_SAVE_DATA = f.read()   # 读取存档
                    SAVE_DATA = READ_SAVE_DATA.split("\n")
                    Save_Time = gmtime(os.path.getmtime(".\config\save.mb"))
                    try:    self.Coin = SAVE_DATA[0]
                    except: self.Coin = 0
                self.Refresh_Data()
                self.Show_Main_Info("读取成功！",0,True)
            except:
                self.Show_Main_Info("读取错误~可能是程序出了啥问题，重启一下吧！",1,True)
        
        def Check_Update(self):
            self.DeadTime = 0
            if self.DeadTime == 3:
                self.Show_Main_Info("检查更新失败，请检查网络连接~",1,True)
                self.Refresh_Data()
                for i in range(39):
                    print(self.Main_Screen_[i])
            else:
                try:
                    self.Show_Main_Info("正在与神经取得连接...",3)
                    self.UpdateRequests = requests.get("http://tbdriver.ml/Version/MathBeats.zip",headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                                                                                                            "Accept-Encoding": "gzip, deflate",
                                                                                                            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                                                                                                            "Pragma": "no-cache",
                                                                                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56"})
                    with open(".\cache\download.zip",'wb') as f:
                        f.write(self.UpdateRequests.content)
                    with zipfile.ZipFile(".\cache\download.zip") as f:
                        f.extractall(path=".\cache")
                    with open(".\cache\MathBeats","r") as f:
                        self.New_Version = f.read()
                    if self.New_Version == self.Version:
                        self.Show_Main_Info("这个麦夫节拍是最新版本~",1,True)
                    else:
                        global In_BGM
                        In_BGM = False
                        self.Update_Screen = ['========================================================================================================================',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|       ___         ___      ___         ___                   ___         ___         ___      ___         ___        |',
        '|      /\__\       /\  \    /\  \       /\__\                 /\  \       /\  \       /\  \    /\  \       /\  \       |',
        '|     /::|  |     /::\  \   \:\  \     /:/  /                /::\  \     /::\  \     /::\  \   \:\  \     /::\  \      |',
        '|    /:|:|  |    /:/\:\  \   \:\  \   /:/__/                /:/\:\  \   /:/\:\  \   /:/\:\  \   \:\  \   /:/\ \  \     |',
        '|   /:/|:|__|__ /::\~\:\  \  /::\  \ /::\  \ ___           /::\~\:\__\ /::\~\:\  \ /::\~\:\  \  /::\  \ _\:\~\ \  \    |',
        '|  /:/ |::::\__/:/\:\ \:\__\/:/\:\__/:/\:\  /\__\         /:/\:\ \:|__/:/\:\ \:\__/:/\:\ \:\__\/:/\:\__/\ \:\ \ \__\\   |',
        '|  \/__/~~/:/  \/__\:\/:/  /:/  \/__\/__\:\/:/  /         \:\~\:\/:/  \:\~\:\ \/__\/__\:\/:/  /:/  \/__\:\ \:\ \/__/   |',
        '|        /:/  /     \::/  /:/  /         \::/  /           \:\ \::/  / \:\ \:\__\      \::/  /:/  /     \:\ \:\__\     |',
        '|       /:/  /      /:/  /\/__/          /:/  /             \:\/:/  /   \:\ \/__/      /:/  /\/__/       \:\/:/  /     |',
        '|      /:/  /      /:/  /               /:/  /               \::/__/     \:\__\       /:/  /              \::/  /      |',
        '|      \/__/       \/__/                \/__/                 ~~          \/__/       \/__/                \/__/       |',
        '|                                                                                                                      |',
        '|                                                   Math  Beats                                                        |',
        '|                                                  Version {}                                                       |'.format(self.Version),
        '|                                                                                                                      |',
        '|                                               发现新版本！是否更新？                                                 |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                              Y 好的~                                          N 不要!                                |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '|                                                                                                                      |',
        '========================================================================================================================']
                        self.Change_By_Fade_Effect(self.Update_Screen)
                        self.Check_Update_State = True
                        while(self.Check_Update_State):
                            if keyboard.is_pressed('y'):
                                pygame.mixer.music.fadeout(1000)
                                In_BGM = False
                                thread = threading.Thread(target=Play_Title_BGM)
                                thread.start()
                                self.Show_Main_Info("正在从神经取得信息...",3,True)
                                self.Download = requests.get("http://tbdriver.ml/File/MathBeats.zip", stream=True)
                                with open(".\cache\download.zip", "wb") as f:
                                    for chunk in self.Download.iter_content(chunk_size=1024):
                                        if chunk:
                                            f.write(chunk)
                                with zipfile.ZipFile(".\cache\download.zip","w") as f:
                                    f.extractall(path=".\cache")
                                    
                                    
                                pygame.mixer.music.fadeout(1000)
                                In_BGM = True
                                thread = threading.Thread(target=Play_BGM)
                                thread.start()
                            if keyboard.is_pressed('n'):
                                self.Change_By_Fade_Effect(self.Main_Screen_)
                                break
                except:
                    self.DeadTime += 1
                    self.Show_Main_Info("检查更新失败，正在重试...",3)
                    self.Check_Update()
        def UpdateLog(self):
            self.UpdateLogText_1 = []
        
        def start(self):
            self.Title_Screen()
            self.Refresh_Data()
            self.Change_By_Fade_Effect(self.Main_Screen_)
            thread = threading.Thread(target=Play_BGM)
            thread.start()
            self.Main_Screen()
            os.system("title MathBeats - [See You Next Time]")
        
        def exit(self):
            pygame.mixer.music.fadeout(500)
            self.Show_Main_Info("See You Next Time!",14)
            sleep(0.2)
            self.Check_Main = False
            global BGMControler
            BGMControler = False
            
    # X  X X XXX  X  X X XXXX(八分)  X XX XXXX  X X X X(四连音)
    System_Main = MathBeats_Main()
    System_Main.start()