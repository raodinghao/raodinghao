import os
import time
import sys
import pyautogui
from PIL import ImageGrab
import numpy as np

def match(a,b):
    sum_a = 0
    sum_b = 0

    for i in a:
        flag1 = 0
        for j in i:
            if flag1 == 0:
                sum_a += j
                flag1+=1
                continue
            for k in j:
                sum_a += k
    for i in b:
        flag1 = 0
        for j in i:
            if flag1 == 0:
                sum_b += j
                flag1 += 1
                continue
            for k in j:
                sum_b += k
    # print('sum_a:{},sum_b:{}'.format(sum_a,sum_b))
    if sum_a > 3400:
        return True
    if abs(sum_a-sum_b)<50:
        return True
    else:return False


def parameter():
    #数字1-8表示雷数目，这里就写四个雷
    #weidianji 未被点击
    #wulei 无雷
    #boom 普通雷
    #boom_red 猜中的雷
    global rgba_weidianji
    global rgba_weidianji_2
    global rgba_weidianji_3
    global rgba_weidianji_4
    global rgba_weidianji_5
    global rgba_wulei
    global rgba_1
    global rgba_2
    global rgba_3
    global rgba_4
    global rgba_hongqi
    global rgba_boom
    global rgba_boom_red
    # rgba_weidianji = [(12,(255,255,255)),(132,(192,192,192))]
    # rgba_weidianji = [(31, (255, 255, 255)), (1, (235, 235, 235)), (14, (223, 223, 223)), (14, (215, 215, 215)), (196, (192, 192, 192))]
    # rgba_weidianji_2 = [(31, (255, 255, 255)), (14, (223, 223, 223)), (1, (236, 236, 236)), (14, (216, 216, 216)), (196, (192, 192, 192))]
    # rgba_weidianji_3 = [(31, (255, 255, 255)), (14, (223, 223, 223)), (14, (217, 217, 217)), (1, (236, 236, 236)), (196, (192, 192, 192))]
    # rgba_weidianji_4 =[(31, (255, 255, 255)), (14, (223, 223, 223)), (1, (236, 236, 236)), (14, (218, 218, 218)), (196, (192, 192, 192))]
    # rgba_weidianji_5 = [(1, (235, 235, 235)), (13, (223, 223, 223)), (13, (215, 215, 215)), (169, (192, 192, 192))]
    rgba_weidianji_5 = [(16, (192, 192, 192))]
    rgba_wulei = [(196, (192, 192, 192))]
    rgba_1 = [(2, (192, 192, 192)), (2, (134, 134, 211)), (1, (82, 82, 228)), (1, (58, 58, 236)), (1, (36, 36, 243)), (9, (0, 0, 255))]
    rgba_2 = [(1, (184, 189, 184)), (1, (171, 185, 171)), (1, (135, 173, 135)), (1, (15, 133, 15)), (5, (192, 192, 192)), (1, (155, 180, 155)), (1, (151, 178, 151)), (1, (121, 168, 121)), (1, (95, 160, 95)), (3, (0, 128, 0))]
    rgba_3 = [(3, (217, 115, 115)), (6, (255, 0, 0)), (2, (223, 96, 96)), (1, (205, 154, 154)), (4, (192, 192, 192))]
    rgba_4 = [(88,(192,192,192)),(56,(0,0,128))]
    rgba_hongqi = [(12,(255,255,255)),(17,(255,0,0)),(93,(192,192,192)),(22,(0,0,0))]
    rgba_boom= [(4,(255,255,255)),(66,(192,192,192)),(74,(0,0,0))]
    rgba_boom_red = [(4,(255,255,255)),(66,(255,0,0)),(74,(0,0,0))]
    global map
    map = [[-1 for i in range(9)]for j in range(9)]

def mapping_img(img,click):
    box_location = pyautogui.locateOnScreen(img)
    print(box_location)
    # center = pyautogui.center(box_location)
    if click == 'double':
        pyautogui.doubleClick(box_location)
    elif click == 'single':
        pyautogui.leftClick(box_location)
    else:
        print(box_location)
        return box_location
    time.sleep(0.5)



def refresh_map(start_x,start_y):
    global game_status
    game_status = -1
    for y in range(9):
        if game_status == -1:
            for x in range(9):
                # print('x:{},y"{}'.format(x,y))
                left = start_x + 20*x
                top = start_y + 20*y
                right = left + 20
                buttom = top + 20

                img0 = ImageGrab.grab((left,top,right,buttom))

                im1 = img0.crop([img0.size[0]/10*4,img0.size[1]/10*4,img0.size[0]*6/10,img0.size[1]*6/10,])
                # if y == 0 and x == 0: im1.show()

                color = im1.getcolors()

                if map[y][x] >=0: #如果已经被扫描或者无雷，就跳过
                    continue
                else:
                    if match(color,rgba_weidianji_5):#color == rgba_weidianji or color == rgba_weidianji_2 or color == rgba_weidianji_3 or color == rgba_weidianji_4 or
                        map[y][x] = -1
                        print(-1)
                    elif match(color,rgba_wulei):
                        map[y][x] = 0
                        print(0)
                    elif match(color,rgba_1):
                        map[y][x] = 1
                        print(1)
                    elif match(color ,rgba_2):
                         map[y][x] = 2
                         print(2)
                    elif match(color ,rgba_3):
                          map[y][x] = 3
                          print(3)
                    elif match( color,rgba_4):
                        map[y][x] = 4
                        print(4)
                    elif match(color,rgba_hongqi):
                        game_status = 1
                        break
                    elif match(color,rgba_boom) or match(color,rgba_boom_red):
                        game_status = 0
                        break
                    else:
                        print("无法识别图像")
                        im1.show()
                        print("坐标{}{}".format(y,x))
                        print('颜色{}'.format(color))
                        sys.exit()
        else: break

def clickmap(start_x,start_y):
    if np.sum(map) == -81:       #第一次点击，选择x=0，y=0位置
        pyautogui.leftClick(start_x+10,start_y+10)
        pyautogui.moveTo(start_x,start_y-200)
    else:
        #查找周围的8个点，并且标记可以确定的雷，标记为-2
        for y in range(9):
            for x in range(9):
                #处理左上角的点
                if x == 0 and y == 0:
                    left = 0
                    right = map[y][x+1]
                    top = 0
                    top_left = 0
                    top_right = 0
                    buttom = map[y+1][x]
                    buttom_left = 0
                    buttom_right = map[y+1][x+1]

                #处理右上角的点
                elif y == 0 and x == 8:
                    left = map[y][x-1]
                    right = 0
                    top = 0
                    top_left = 0
                    top_right = 0
                    buttom = map[y+1][x]
                    buttom_left = map[y+1][x-1]
                    buttom_right = 0
                #处理上边
                elif y == 0 and x > 0 and x < 8:
                    left = map[y][x-1]
                    right = map[y][x+1]
                    top = 0
                    top_left = 0
                    top_right = 0
                    buttom = map[y+1][x]
                    buttom_left = map[y+1][x-1]
                    buttom_right = map[y+1][x+1]
                #处理左边
                elif x == 0 and y >0 and y < 8:
                    left = 0
                    right = map[y][x + 1]
                    top = map[y - 1][x]
                    top_left = 0
                    top_right = map[y - 1][x + 1]
                    buttom = map[y + 1][x]
                    buttom_left = 0
                    buttom_right = map[y + 1][x + 1]
                #处理右边
                elif x == 8 and y > 1 and y < 8:
                    left = map[y][x - 1]
                    right = 0
                    top = map[y - 1][x]
                    top_left = map[y - 1][x - 1]
                    top_right = 0
                    buttom = map[y + 1][x]
                    buttom_left = map[y] + 1[x - 1]
                    buttom_right = 0
                #处理左下角
                elif y == 8 and x == 0:
                    left = 0
                    right = map[y][x + 1]
                    top = map[y - 1][x]
                    top_left = 0
                    top_right = map[y - 1][x + 1]
                    buttom = 0
                    buttom_left = 0
                    buttom_right = 0
                #处理右下角
                elif x == 8 and y == 8:
                    left = map[y][x - 1]
                    right = 0
                    top = map[y - 1][x]
                    top_left = map[y - 1][x - 1]
                    top_right = 0
                    buttom = 0
                    buttom_left = 0
                    buttom_right = 0
                #处理下边
                elif y == 8 and x > 0 and x < 8:
                    left = map[y][x - 1]
                    right = map[y][x + 1]
                    top = map[y - 1][x]
                    top_left = map[y - 1][x - 1]
                    top_right = map[y - 1][x + 1]
                    buttom = 0
                    buttom_left = 0
                    buttom_right = 0
                else:
                    left = map[y][x-1]
                    right = map[y][x + 1]
                    top = map[y-1][x]
                    top_left = map[y-1][x - 1]
                    top_right = map[y-1][x + 1]
                    buttom = map[y + 1][x]
                    buttom_left = map[y+1][x - 1]
                    buttom_right = map[y + 1][x + 1]

                #将八个点存入列表
                ar_8 = [left,right,top,top_left,top_right,buttom,buttom_left,buttom_right]

                #找出所有可以确定雷，标记为-2
                if map[y][x] > 0:
                    total = 0
                    for i in ar_8:
                        if i == -1 or i == -2: total+=1
                    if total == map[y][x]:
                        if ar_8[0] == -1: map[y][x-1]=-2
                        if ar_8[1] == -1: map[y][x + 1] = -2
                        if ar_8[2] == -1: map[y-1][x] = -2
                        if ar_8[3] == -1: map[y][x - 1] = -2
                        if ar_8[4] == -1: map[y-1][x - 1] = -2
                        if ar_8[5] == -1: map[y-1][x + 1] = -2
                        if ar_8[6] == -1: map[y + 1][x] = -2
                        if ar_8[7] == -1: map[y+1][x - 1] = -2
                        if ar_8[8] == -1: map[y + 1][x + 1] = -2

                #找出所有安全点
                for y in range(9):
                    for x in range(9):

                        # 处理左上角的点
                        if x == 0 and y == 0:
                            left = 0
                            right = map[y][x + 1]
                            top = 0
                            top_left = 0
                            top_right = 0
                            buttom = map[y + 1][x]
                            buttom_left = 0
                            buttom_right = map[y + 1][x + 1]

                        # 处理右上角的点
                        elif y == 0 and x == 8:
                            left = map[y][x - 1]
                            right = 0
                            top = 0
                            top_left = 0
                            top_right = 0
                            buttom = map[y + 1][x]
                            buttom_left = map[y + 1][x - 1]
                            buttom_right = 0
                        # 处理上边
                        elif y == 0 and x > 0 and x < 8:
                            left = map[y][x - 1]
                            right = map[y][x + 1]
                            top = 0
                            top_left = 0
                            top_right = 0
                            buttom = map[y + 1][x]
                            buttom_left = map[y + 1][x - 1]
                            buttom_right = map[y + 1][x + 1]
                        # 处理左边
                        elif x == 0 and y > 0 and y < 8:
                            left = 0
                            right = map[y][x + 1]
                            top = map[y - 1][x]
                            top_left = 0
                            top_right = map[y - 1][x + 1]
                            buttom = map[y + 1][x]
                            buttom_left = 0
                            buttom_right = map[y + 1][x + 1]
                        # 处理右边
                        elif x == 8 and y > 0 and y < 8:
                            left = map[y][x - 1]
                            right = 0
                            top = map[y - 1][x]
                            top_left = map[y - 1][x - 1]
                            top_right = 0
                            buttom = map[y + 1][x]
                            buttom_left = map[y+1][x - 1]
                            buttom_right = 0
                        # 处理左下角
                        elif y == 8 and x == 0:
                            left = 0
                            right = map[y][x + 1]
                            top = map[y - 1][x]
                            top_left = 0
                            top_right = map[y - 1][x + 1]
                            buttom = 0
                            buttom_left = 0
                            buttom_right = 0
                        # 处理右下角
                        elif x == 8 and y == 8:
                            left = map[y][x - 1]
                            right = 0
                            top = map[y - 1][x]
                            top_left = map[y - 1][x - 1]
                            top_right = 0
                            buttom = 0
                            buttom_left = 0
                            buttom_right = 0
                        # 处理下边
                        elif y == 8 and x > 0 and x < 8:
                            left = map[y][x - 1]
                            right = map[y][x + 1]
                            top = map[y - 1][x]
                            top_left = map[y - 1][x - 1]
                            top_right = map[y - 1][x + 1]
                            buttom = 0
                            buttom_left = 0
                            buttom_right = 0
                        else:
                            # print('y2:{},x2:{}'.format(y, x))
                            left = map[y][x - 1]
                            right = map[y][x + 1]
                            top = map[y - 1][x]
                            top_left = map[y - 1][x - 1]
                            top_right = map[y - 1][x + 1]
                            buttom = map[y + 1][x]
                            buttom_left = map[y + 1][x - 1]
                            buttom_right = map[y + 1][x + 1]
                        ar_8 = [left, right, top, top_left, top_right, buttom, buttom_left, buttom_right]
                        # 找出所有可以确定安全点，标记为-3
                        if map[y][x] > 0:
                            total = 0
                            for i in ar_8:
                                if i == -2: total += 1
                            if total == map[y][x]:
                                if ar_8[0] == -1: map[y][x - 1] = -3
                                if ar_8[1] == -1: map[y][x + 1] = -3
                                if ar_8[2] == -1: map[y - 1][x] = -3
                                if ar_8[3] == -1: map[y][x - 1] = -3
                                if ar_8[4] == -1: map[y - 1][x - 1] = -3
                                if ar_8[5] == -1: map[y - 1][x + 1] = -3
                                if ar_8[6] == -1: map[y + 1][x] = -3
                                if ar_8[7] == -1: map[y + 1][x - 1] = -3
                                if ar_8[8] == -1: map[y + 1][x + 1] = -3
        #点掉所有安全点
        cnt_safe = 0
        for y in range(9):
            for x in range(9):
                if map[y][x] == -3:
                    cnt_safe+=1
                    print('safe x:{}, y:{}'.format(x+1,y+1))
                    pyautogui.leftClick(start_x + x *20+10,start_y + y*20+10)
                    pyautogui.moveTo(start_x,start_y-200)

        #假如没有安全点，就从点左上角开始找到第一个未点击的点
        if cnt_safe == 0:
            flag = 0
            for y in range(9):
                if flag == 1: break
                for x in range(9):
                    if map[y][x] == -1:
                        flag = 1
                        print('have to x:{}, y:{}'.format(x + 1, y + 1))
                        pyautogui.leftClick(start_x + x * 20 + 10, start_y + y * 20 + 10)
                        pyautogui.moveTo(start_x, start_y - 200)
                        break








def main():
    #切换到图片目录下
    os.chdir('D:/python全栈/项目/扫雷/img')
    print(os.getcwd())      #打印当前路径

    mapping_img('shibie.png','double')        #在桌面识别到扫雷程序，并且双击打开


    #定位到9*9表盘,180*180，每个20*20
    # desk_location = list(mapping_img('form.png', ''))
    # print(desk_location)
    desk_location = pyautogui.locateOnScreen('form.png')
    print(desk_location)
    # center = pyautogui.center(box_location)
    # pyautogui.doubleClick(desk_location)

    # start_x = desk_location[0]
    # start_y = desk_location[1]

    parameter() #初始环境变量
    # cnt = 0
    # while True:
    #     cnt+=1
    #     print('----------{}-----------'.format(cnt))
    #     refresh_map(start_x,start_y)
    #     print(map)
    #     if game_status == 0:
    #         print('失败了')
    #     if game_status == 1:
    #         print('过关')
    #     clickmap(start_x,start_y)

if __name__=='__main__':
    main()