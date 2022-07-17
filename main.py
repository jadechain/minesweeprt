import pyautogui
import random
from time import sleep

miner_x, miner_y = 30, 16
width, height = 16, 16
global mines, mines_sign, mines_judge
global x_0, y_0


def game_init():
    # 初始脚本：初始化列表信息，寻找扫雷窗口，开始运行脚本
    global mines, mines_sign, mines_judge
    mines = []  # 存储未点开格子BOX信息的列表
    mines_sign = [-1 for _ in range(miner_x * miner_y)]  # 存储格子是否被点了的信息，0-8为雷的个数，-1为未点开，9为旗子, 10为雷
    mines_judge = [i for i in range(miner_x * miner_y)]  # 若某个格子已经得出结论，则删除该数的序号，以后无须再判断

    while True:
        minesweeper = pyautogui.locateOnScreen('minesweeper.png', confidence=0.99)
        if minesweeper:
            break
    for i in pyautogui.locateAllOnScreen('-1.png', grayscale=True):
        mines.append(i)
    global x_0, y_0
    x_0, y_0 = minesweeper.left, minesweeper.top  # 扫雷区域起始坐标
    click_luck(-1)  # 随机点机格子，直到点开一片


def run_game():
    game_init()
    # 脚本循环开始
    while True:
        pyautogui.moveTo(100, 100)
        get_nums()  # 读取扫雷窗口当前所有信息，大约耗时0.02秒
        a = get_mine_last()
        solve_a()
        solve_b()
        b = get_mine_last()
        if a == b:
            click_random()  # 若a方法和b方法均不能判断，即出现需要蒙的情况，则随机点一个
        if get_mine_last() == 99:
            for i in mines_judge:
                try:
                    if mines_judge[i] == -1:
                        click(i)
                except IndexError:
                    print('通关扫雷高级')
                    return


def get_mine_last(lei=9):
    # 获取当前窗口有多少颗雷，参数默认为 9 雷，其他数字代表窗口的数字
    mines_num = 0
    for num in mines_sign:
        if num == lei:
            mines_num += 1
    return mines_num


def solve_a():
    # 中心找空和找雷
    for index, num in enumerate(mines_sign):
        if index in mines_judge:
            if 0 < num < 9:
                booms, blank = 0, 0
                arr = check_8(index)
                if arr:
                    for index_ in arr:
                        if mines_sign[index_] == -1:
                            blank += 1
                        if mines_sign[index_] == 9:
                            booms += 1
                    if booms + blank == num:
                        for index_ in arr:
                            if mines_sign[index_] == -1:
                                click_right(index_)  # 找到是雷
                    elif booms == num and blank != 0:
                        click_mid(index)  # 中心的空格是空


def solve_b():
    # 重叠找空和找雷，需拆分为 找偏移九宫格、对比偏移九宫格空白格+雷格
    for index, num in enumerate(mines_sign):
        if index in mines_judge:
            if 0 < num < 9:
                booms_blank = get_blank_boom(index)  # 存储雷格子、空白格子的列表
                if not booms_blank:
                    continue
                arr_4 = check_4(index)  # arr为index的四个方向偏移序号列表
                for i in arr_4:
                    booms_blank_4 = get_blank_boom(i)  # 存储偏移格子的 雷格子、空白格子的列表
                    if not booms_blank_4:
                        continue
                    result = all(elem in booms_blank_4[1] for elem in booms_blank[1])  # 偏移空格列表包含中心空格列表
                    if result:
                        m = mines_sign[i] - len(booms_blank_4[0])  # 偏移剩余雷数
                        n = mines_sign[index] - len(booms_blank[0])  # 中心剩余雷数
                        if m == n:
                            # 如果 中心剩余雷数 == 偏移剩余雷数，则中心不重叠的地方都是空格
                            for elem in booms_blank_4[1]:
                                if elem not in booms_blank[1]:
                                    # print('重叠找空', elem)
                                    click(elem)
                        if (m - n) >= (len(booms_blank_4[1]) - len(booms_blank[1])) and m != n:
                            # 如果 偏移剩余雷数 - 中心剩余雷数 == 偏移空格数 - 中心空格数，则中心不重叠的地方都是雷
                            for elem in booms_blank_4[1]:
                                if elem not in booms_blank[1]:
                                    # print('重叠找雷', elem)
                                    click_right(elem)


def get_blank_boom(index):
    """得到index格子的周围8个格子中，雷格子、空白格子列表，不算已经点开的格子"""
    booms, blank = [], []
    arr_8 = check_8(index)
    if arr_8:
        for index_ in arr_8:
            if mines_sign[index_] == -1:
                blank.append(index_)
            if mines_sign[index_] == 9:
                booms.append(index_)
        if blank:
            return [booms, blank]
        else:
            return


def click_luck(temp):
    """随机从剩余没点开的格子中点击一个"""
    click_random()
    if len(mines_judge) < 430:
        return
    get_nums()
    temp_ = 0
    for sign in mines_sign:
        if sign == -1:
            temp_ += 1
    if temp - 1 == temp_:
        click_luck(temp_)


def printf():
    for i, j in enumerate(mines_sign):
        if (i + 1) % 30 == 0:
            print('%2d' % j, end=',\n')
        else:
            print('%2d' % j, end=',')


def click_random():
    while True:
        index = random.randint(0, 480)
        if index in mines_judge:
            if mines_sign[index] == -1:
                print('无法判断，随机点啦！ %3d' % index)
                click(index)
                return


def click_right(index):
    pyautogui.rightClick(mines[index].left + 8, mines[index].top + 8, _pause=False)
    if index in mines_judge:
        mines_judge.remove(index)
    # print('mine 删除 %3d' % index)
    mines_sign[index] = 9


def click_mid(index):
    pyautogui.middleClick(mines[index].left + 8, mines[index].top + 8, _pause=False)
    mines_judge.remove(index)
    # print('mid 删除 %3d' % index)


def click(index):
    # print('left', index)
    pyautogui.click(mines[index].left + 8, mines[index].top + 8, _pause=False)
    if pyautogui.locateOnScreen('10.png', grayscale=True):
        print('BOOM!')
        # sys.exit()
        sleep(1)
        pyautogui.click(mines[15].left + 8, mines[0].top - 32)
        sleep(1)
        run_game()


def check_8(index):
    """
    返回第index个格子，周围8个格子中，空白格子+雷格子序号的列表
    若第index个格子周围只有标记出的雷，没有空格子，说明该格子无须再判断，返回None
    """
    if index not in mines_judge:
        return
    i, j = index // miner_x, index % miner_x
    up = [1, 0][i == 0]
    down = [2, 1][i == miner_y - 1]
    left = [1, 0][j == 0]
    right = [2, 1][j == miner_x - 1]
    grid_8 = []
    for x in range(i - up, i + down):
        for y in range(j - left, j + right):
            if x != i or y != j:
                grid_8.append(x * miner_x + y)
    temp = []
    booms = 0
    for i in grid_8:
        if mines_sign[i] >= 0 and mines_sign[i] != 9:
            temp.append(i)
    for tem in temp:
        grid_8.remove(tem)

    for i in grid_8:
        if mines_sign[i] == 9:
            booms += 1
    if booms == mines_sign[index] and len(grid_8) == mines_sign[index]:
        mines_judge.remove(index)
        # print('judge 删除 %3d' % index)
        return
    elif booms == mines_sign[index] and len(grid_8) != mines_sign[index]:
        click_mid(index)
        return
    else:
        return grid_8


def check_4(index):
    """
    返回第index个格子，上下左右8个格子中，空白格子+雷格子序号的列表
    若第index个格子周围只有标记出的雷，没有空格子，说明该格子无须再判断，返回None
    """
    if index not in mines_judge:
        return
    grid_4 = [index - miner_x, index - 1, index + 1, index + miner_x]
    temp = []
    if index % 30 == 0:
        grid_4.remove(index - 1)
    if (index + 1) % 30 == 0:
        grid_4.remove(index + 1)
    if 0 <= index <= 29:
        grid_4.remove(index - miner_x)
    if 450 <= index <= 479:
        grid_4.remove(index + miner_x)
    for m in grid_4:
        if mines_sign[m] == 0:
            temp.append(m)
        if mines_sign[m] == -1:
            temp.append(m)
        if mines_sign[m] == 9:
            temp.append(m)
    for m in temp:
        grid_4.remove(m)
    return grid_4


def get_nums():
    screenshot = pyautogui.screenshot(region=(x_0, y_0, 480, 256))
    for index in mines_judge:
        x, y = index // miner_x, index % miner_x
        pix = screenshot.getpixel((y * 16 + 10, x * 16 + 12))
        if pix == (192, 192, 192):
            pix_0 = screenshot.getpixel((y * 16, x * 16))
            if pix_0 == (255, 255, 255):
                mines_sign[index] = -1
                continue
            elif pix_0 == (128, 128, 128):
                mines_sign[index] = 0
                continue
        elif pix == (0, 0, 255):
            mines_sign[index] = 1
            continue
        elif pix == (0, 128, 0):
            mines_sign[index] = 2
            continue
        elif pix == (255, 0, 0):
            mines_sign[index] = 3
            continue
        elif pix == (0, 0, 128):
            mines_sign[index] = 4
            continue
        elif pix == (128, 0, 0):
            mines_sign[index] = 5
            continue
        elif pix == (0, 128, 0):
            mines_sign[index] = 6
            continue
        elif pix == (0, 0, 0):
            pix_7 = screenshot.getpixel((y * 16 + 7, x * 16 + 7))
            if pix_7 == (255, 0, 0):
                mines_sign[index] = 9
                continue
            elif pix_7 == (255, 255, 255):
                mines_sign[index] = 10
                continue
            elif pix_7 == (192, 192, 192):
                mines_sign[index] = 7
                continue
        elif pix == (128, 128, 128):
            mines_sign[index] = 8
            continue


if __name__ == '__main__':
    run_game()
