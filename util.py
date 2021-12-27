import math
import numpy as np

tipIds = [4, 8, 12, 16, 20]


def vector_2d_angle(v1, v2):
    """
        求解二维向量的角度
    """
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_


def hand_angle(hand_):
    """
        获取对应手相关向量的二维角度,根据角度确定手势
    """
    angle_list = []
    # ---------------------------- thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- ring 无名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
    )
    angle_list.append(angle_)
    return angle_list


def isOpen(lmList, isLeft):
    if len(lmList) != 0:
        # 判断是否手面正向摊开。
        if (isLeft and lmList[0][0] > lmList[4][0]) or (not isLeft and lmList[0][0] < lmList[4][0]):
            return False
        fingers = []
        if isLeft:
            if lmList[tipIds[0]][0] > lmList[tipIds[0] - 1][0]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if lmList[tipIds[0]][0] < lmList[tipIds[0] - 1][0]:
                fingers.append(1)
            else:
                fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][1] < lmList[tipIds[id] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        totalFingers = fingers.count(1)
    print(totalFingers)
    if totalFingers == 5:
        return True
    else:
        return False


# 横向反复移动
def isLateralMove(coordinates):
    if len(coordinates) < 3:
        return False
    xs = []
    ys = []
    for coordinate in coordinates:
        xs.append(coordinate[0])
        ys.append(coordinate[1])
    if overAndOver(xs) and isHorizontal(ys):
        return True
    return False


# 纵向反复移动
def isVerticalMove(coordinates):
    if len(coordinates) < 3:
        return False
    xs = []
    ys = []
    for coordinate in coordinates:
        xs.append(coordinate[0])
        ys.append(coordinate[1])
    if overAndOver(ys) and isHorizontal(xs):
        return True
    return False


# 纵向向上移动
def isVerticalUpMove(coordinates):
    if len(coordinates) < 3:
        return False
    xs = []
    ys = []
    for coordinate in coordinates:
        xs.append(coordinate[0])
        ys.append(coordinate[1])
    ys.reverse()
    if isUp(ys):
        return True
    return False


# 横向移动
def isHorizontalMove(coordinates, needReverse):
    print(needReverse)
    if len(coordinates) < 3:
        return False
    xs = []
    ys = []
    for coordinate in coordinates:
        xs.append(coordinate[0])
        ys.append(coordinate[1])
    if needReverse:
        xs.reverse()
    print("isHorizontalMove", isUp(xs), isHorizontal(ys))
    if isUp(xs) and isHorizontal(ys):
        return True
    return False


def getDistance(p1, p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    return math.sqrt((x ** 2) + (y ** 2))


def getMax(values):
    max_value = -1
    for value in values:
        if value > max_value:
            max_value = value
    return max_value


def getMin(values):
    min_value = 1 << 31
    for value in values:
        if value < min_value:
            min_value = value
    return min_value


def isStaticPoints(coordinates):
    if len(coordinates) < 3:
        return False
    xs = []
    ys = []
    for coordinate in coordinates:
        xs.append(coordinate[0])
        ys.append(coordinate[1])
    if isHorizontal(xs) and isHorizontal(ys):
        return True
    return False


def isHorizontal(values):
    threshold = 40

    arr_std_1 = np.std(values)
    print("std: ", arr_std_1)
    if arr_std_1 < threshold:
        return True
    return False


def overAndOver(values):
    threshold = 4
    count = 0
    dir = False
    if values[0] < values[1]:
        dir = True
    print(values)
    for i in range(1, len(values) - 1):
        if abs(values[i] - values[i + 1]) < threshold:
            continue
        if dir and values[i] > values[i + 1]:
            dir = False
            count = count + 1
            continue
        if not dir and values[i] < values[i + 1]:
            dir = True
            count = count + 1
    if count >= 2:
        return True
    return False


def isUp(values):
    count_threshold = 0.7
    up_count_threshold = 0.25
    equal_threshold = 4
    pre = values[0]
    equal_count = 0
    up_count = 0
    for i in range(1, len(values) - 1):
        if abs(pre - values[i]) <= equal_threshold:
            equal_count = equal_count + 1
        elif pre < values[i]:
            up_count = up_count + 1
        pre = values[i]
    # print("isHorizontalMove:", up_count, len(coordinates) * count_threshold)
    if up_count >= len(values) * up_count_threshold and up_count + equal_count >= len(
            values) * count_threshold:
        return True
    return False
