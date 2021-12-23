import util

tipIds = [4, 8, 12, 16, 20]


# 猪，牛，马，人， 鱼， 蝴蝶
# 草，山，树，花，蘑菇


# 鱼的静态识别逻辑：
#
#     手心向内：                      通过大拇指的y坐标在其他指尖y坐标之上来判读
#     判读手指是不是横着：             通过手指向量和(0,1)向量夹角是不是大概90度判断
#     手值是否伸展：                  左手：指尖的横坐标大于指节，右手反之。判断左右手通过大拇指在手心左边还是右边来判断
#
#     未进行判断：
#       手没张开也会识别成功，是否需要加上
#       距离的阈值和手离摄像头的距离相关，如果手离摄像头很近，有可能识别失败
def isFish(lmLists):
    print("isFish")
    angle_up_threshold = 110
    angle_down_threshold = 70

    if len(lmLists) != 1:
        return False

    lmList = lmLists[0]

    for id in (8, 12, 16, 20):
        if lmList[4][1] > lmList[id][1]:
            return False
        angle = util.vector_2d_angle((lmList[id][0] - lmList[id - 3][0], lmList[id][1] - lmList[id - 3][1]), (0, 1))
        if angle > angle_up_threshold or angle < angle_down_threshold:
            return False
        if (lmList[4][0] > lmList[0][0] and lmList[id][0] < lmList[id-2][0]) or \
                (lmList[4][0] < lmList[0][0] and lmList[id][0] > lmList[id-2][0]):
            return False

    return True


# 花的静态识别逻辑： 后续加上掌心向内的判断
#     单手，开始的时候所以手指指尖离中指很近，后面渐渐远离在中指。所有手指竖直向上的状态，
#
#     判别5根手指是不是合在一块：             其他手指离中指的距离小于阈值
#     判读手指是不是伸展向上：                指尖的y坐标大于指节的y坐标
#
#     未进行判断：
#       手没张开也会识别成功，是否需要加上
#       距离的阈值和手离摄像头的距离相关，如果手离摄像头很近，有可能识别失败
def isFlower(lmLists, isBegin):
    print("isFlower")
    mid_distance_threshold = 100
    edge_distance_threshold = 240
    if isBegin:
        mid_distance_threshold = 50
        edge_distance_threshold = 120

    if len(lmLists) != 1:
        return False

    lmList = lmLists[0]

    for id in (8, 12, 16, 20):
        if lmList[id][1] > lmList[id - 2][1]:
            return False

    print("flower distance: ", util.getDistance(lmList[8], lmList[12]), util.getDistance(lmList[12], lmList[16]),
          util.getDistance(lmList[12], lmList[20]), util.getDistance(lmList[12], lmList[4]))
    if util.getDistance(lmList[8], lmList[12]) > mid_distance_threshold or \
            util.getDistance(lmList[12], lmList[16]) > mid_distance_threshold or \
            util.getDistance(lmList[12], lmList[20]) > edge_distance_threshold or \
            util.getDistance(lmList[12], lmList[4]) > edge_distance_threshold:
        return False
    return True


def isMidFlower(lmLists):
    print("isMidFlower")
    mid_distance_threshold = 100
    edge_distance_threshold = 200
    if len(lmLists) != 1:
        return False

    lmList = lmLists[0]

    for id in (8, 12, 16, 20):
        if lmList[id][1] > lmList[id - 2][1]:
            return False

    print("flower distance: ", util.getDistance(lmList[8], lmList[12]), util.getDistance(lmList[12], lmList[16]),
          util.getDistance(lmList[12], lmList[20]), util.getDistance(lmList[12], lmList[4]))
    if util.getDistance(lmList[8], lmList[12]) > mid_distance_threshold or \
            util.getDistance(lmList[12], lmList[16]) > mid_distance_threshold or \
            util.getDistance(lmList[12], lmList[20]) > edge_distance_threshold or \
            util.getDistance(lmList[12], lmList[4]) > edge_distance_threshold:
        return False
    return True


# 蘑菇的静态识别逻辑：
#     判别左手1，3，4，5手指是否为回收状态：   角度判读
#     判别右手是否张开拱起：                 指尖，最后一个指节和手心向量角度大于120度
#     判读左手是否顶着右手：                 左手指尖和右手食指指节距离小于50
#
#     未进行判断：
def isMushroom(lmLists):
    print("isMushroom")
    angle_threshold = 120
    distance_threshold = 180
    if len(lmLists) != 2:
        return False
    left_fingers = getFingerStatusByAngle(lmLists[0])
    # 大拇指的识别率太低率，暂时先把大拇指的判断去掉
    if not (left_fingers[1] == 1 and left_fingers[2] == 0 and left_fingers[3] == 0 and
            left_fingers[4] == 0):
        return False

    ids = (8, 12, 16, 20)
    for i in range(0, 4):
        angle_ = util.vector_2d_angle(
            ((int(lmLists[1][ids[i]][0]) - int(lmLists[1][ids[i] - 3][0])),
             (int(lmLists[1][ids[i]][1]) - int(lmLists[1][ids[i] - 3][1]))),
            ((int(lmLists[1][0][0]) - int(lmLists[1][ids[i] - 3][0])),
             (int(lmLists[1][0][1]) - int(lmLists[1][ids[i] - 3][1])))
        )
        if angle_ < angle_threshold:
            return False
    print("mushroom distance:", util.getDistance(lmLists[1][8], lmLists[0][6]))
    if not (util.getDistance(lmLists[0][8], lmLists[1][17]) < distance_threshold):
        return False

    return True


# 人的静态识别逻辑：
#     判读1，3，4，5手指是否为回收状态：      角度判读
#     判读两根食指角度是否大概90度：          向量角度判读
#     判读食指是接触：                      一食指指尖和另一食指指节距离小于阈值
#
#     未进行判断：
def isHuman(lmLists):
    print("isHuman")
    angle_up_threshold = 120
    angle_down_threshold = 60
    distance_threshold = 50
    if len(lmLists) != 2:
        return False
    left_fingers = getFingerStatusByAngle(lmLists[0])
    right_fingers = getFingerStatusByAngle(lmLists[1])
    if not (left_fingers[1] == 1 and left_fingers[2] == 0 and left_fingers[3] == 0 and
            left_fingers[4] == 0) or \
            not (right_fingers[1] == 1 and right_fingers[2] == 0 and right_fingers[3] == 0 and
                 right_fingers[4] == 0):
        return False
    # if not lmLists[0][4][0] < lmLists[0][3][0]:
    #     return False
    angle_ = util.vector_2d_angle(
        ((int(lmLists[0][5][0]) - int(lmLists[0][8][0])), (int(lmLists[0][5][1]) - int(lmLists[0][8][1]))),
        ((int(lmLists[1][5][0]) - int(lmLists[1][8][0])), (int(lmLists[1][5][1]) - int(lmLists[1][8][1])))
    )
    print("human angle:", angle_)
    if angle_ < angle_down_threshold or angle_ > angle_up_threshold:
        return False

    print("human distance:", util.getDistance(lmLists[1][8], lmLists[0][6]))
    if not (util.getDistance(lmLists[0][8], lmLists[1][6]) < distance_threshold or util.getDistance(lmLists[1][8],
                                                                                                    lmLists[0][6])):
        return False

    return True


# 树的静态识别逻辑：
#     判读3，4，5手指是否为回收状态：      角度判读
#     判读手是否横着：                通过5，9，13，17（手指最靠近手掌的四个关节点）点的x坐标是否相似
#     判读食指是否横着值：           通过食指的指尖的x坐标是否大雨指节的x坐标（左手，右手反之）
#
#     未进行判断：
#         拇指状态
#         手心朝向
def isTree(lmLists):
    if len(lmLists) != 2:
        return False
    if isSingleTree(lmLists[0], True) and isSingleTree(lmLists[1], False):
        return True
    else:
        return False


def isSingleTree(lmList, isLeft):
    fingers = getFingerStatusByAngle(lmList)
    print("isSingleTree:", isLeft, lmList[8][0], lmList[6][0])
    if (fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0) and \
            ((isLeft and lmList[8][0] > lmList[6][0]) or (not isLeft and lmList[8][0] < lmList[6][0])) and \
            util.isHorizontal((lmList[5][0], lmList[9][0], lmList[13][0], lmList[17][0])):
        return True
    return False


def isMountain(lmLists):
    if len(lmLists) != 1:
        return False
    fingers = getFingerStatusByAngle(lmLists[0])
    if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        return True
    else:
        return False


"""
草的静态识别逻辑：
    判读是否只要食指张开：           角度判读
    判读食指是否竖着指：             通过食指关节点的x坐标是否相似
    判读食指是否横向张开：           通过食指的指尖的x坐标是否大雨指节的x坐标（左手，右手反之）

    未进行判读：
        手心朝向
        食指朝上
"""


def isGrass(lmLists):
    if len(lmLists) != 2:
        return False
    if isSingleGrass(lmLists[0]) and isSingleGrass(lmLists[1]):
        return True
    else:
        return False


def isSingleGrass(lmList):
    fingers = getFingerStatusByAngle(lmList)
    if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and \
            util.isHorizontal((lmList[8][0], lmList[7][0], lmList[6][0], lmList[5][0])):
        return True
    else:
        return False


def isHello(lmLists):
    if len(lmLists) != 2:
        return False
    if util.isOpen(lmLists[0], True) & util.isOpen(lmLists[1], False):
        return True
    else:
        return False


# def isOne(lmLists):
#     if len(lmLists) != 1:
#         return False
#     fingers = getFingerStatusByAngle(lmLists[0])
#     if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
#         return True
#     else:
#         return False
#
#
def isTow(lmLists):
    if len(lmLists) != 1:
        return False
    fingers = getFingerStatusByAngle(lmLists[0])
    if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
        return True
    else:
        return False
#
#
# def isThree(lmLists):
#     if len(lmLists) != 1:
#         return False
#     fingers = getFingerStatusByAngle(lmLists[0])
#     if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
#         return True
#     else:
#         return False
#
#
# def isFour(lmLists):
#     if len(lmLists) != 1:
#         return False
#     fingers = getFingerStatusByAngle(lmLists[0])
#     if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
#         return True
#     else:
#         return False
#
#
# def isFive(lmLists):
#     if len(lmLists) != 1:
#         return False
#     fingers = getFingerStatusByAngle(lmLists[0])
#     if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
#         return True
#     else:
#         return False
#
#
def isZero(lmLists):
    if len(lmLists) != 1:
        return False
    fingers = getFingerStatusByAngle(lmLists[0])
    if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        return True
    else:
        return False


def getFingerStatus(lmList):
    fingers = []
    if lmList[tipIds[0]][0] > lmList[tipIds[0] - 1][0]:
        fingers.append(1)
    else:
        fingers.append(0)
    for id in range(1, 5):
        if lmList[tipIds[id]][1] < lmList[tipIds[id] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers


def getFingerStatusByAngle(lmList):
    fingers = [-1, -1, -1, -1, -1]
    thr_angle = 65.
    thr_angle_thumb = 50.
    thr_angle_s = 49.
    angle_list = util.hand_angle(lmList)

    if angle_list[0] < thr_angle_s:
        fingers[0] = 1
    elif angle_list[0] > thr_angle_thumb:
        fingers[0] = 0

    for i in range(1, 5):
        if angle_list[i] < thr_angle_s:
            fingers[i] = 1
        elif angle_list[i] > thr_angle:
            fingers[i] = 0
    if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        print(angle_list)
        print(fingers)
        return fingers
    else:
        print(angle_list)
        print(fingers)
    return fingers
