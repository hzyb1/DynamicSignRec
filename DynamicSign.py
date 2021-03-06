import util
import math
import StaticSign

# class DynamicSign
helloThreshold = 5

sign_contains_threshold = 0.7


class Sign:

    def isTrue(self, postions):
        return "unKnow"


class FishSign(Sign):

    def __init__(self):
        self.isLeft = True
        self.moves = []

    def isTrue(self, postions):
        count = 0
        self.isLeft = True
        self.moves = []
        for lmLists in postions:
            if StaticSign.isFish(lmLists):
                count = count + 1
                self.moves.append(lmLists[0][0])
                if lmLists[0][4][0] < lmLists[0][0][0]:
                    self.isLeft = False
        print(len(postions) * sign_contains_threshold, count)
        if len(postions) * sign_contains_threshold <= count and self.isRightMove():
            return "fish"
        else:
            return "unKnow"

    def isRightMove(self):
        if util.isHorizontalMove(self.moves, not self.isLeft):
            return True
        return False


class FlowerSign(Sign):

    def isTrue(self, postions):
        count = 0
        for lmLists in postions:
            if StaticSign.isFlower(lmLists, False):
                count = count + 1
        print(len(postions) * sign_contains_threshold, count)
        if len(postions) * sign_contains_threshold > count:
            return "unKnow"
        else:
            return "flower"


class MushRoomSign(Sign):

    def isTrue(self, postions):
        count = 0
        for lmLists in postions:
            if StaticSign.isMushroom(lmLists):
                count = count + 1
        print(len(postions) * sign_contains_threshold, count)
        if len(postions) * sign_contains_threshold > count:
            return "unKnow"
        else:
            return "mushroom"


class HumanSign(Sign):

    def isTrue(self, postions):
        count = 0
        for lmLists in postions:
            if StaticSign.isHuman(lmLists):
                count = count + 1
        print(len(postions) * sign_contains_threshold, count)
        if len(postions) * sign_contains_threshold > count:
            return "unKnow"
        else:
            return "human"


class HelloSign(Sign):

    def isTrue(self, postions):
        count = 0
        self.left_moves = []
        self.right_moves = []
        for lmLists in postions:
            if StaticSign.isHello(lmLists):
                self.left_moves.append(lmLists[0][0])
                self.right_moves.append(lmLists[1][0])
                count = count + 1
        print(len(postions) * sign_contains_threshold, count)
        if len(postions) * sign_contains_threshold > count:
            return "unKnow"
        if self.isRightMove():
            return "hello"

        return "unKnow"

    def isRightMove(self):
        if util.isLateralMove(self.right_moves) and util.isLateralMove(self.left_moves):
            return True
        return False


class GrassSign(Sign):

    def __init__(self):
        self.right_moves = []
        self.left_moves = []

    def isTrue(self, postions):
        print("grass is True?")
        self.right_moves = []
        self.left_moves = []
        count = 0
        for lmLists in postions:
            if StaticSign.isGrass(lmLists):
                self.left_moves.append(lmLists[0][0])
                self.right_moves.append(lmLists[1][0])
                count = count + 1
        print(len(postions) * sign_contains_threshold, count)
        if len(postions) * sign_contains_threshold > count:
            return "unKnow"
        if self.isRightMove():
            return "grass"

        return "unKnow"

    def isRightMove(self):
        if util.isVerticalMove(self.right_moves) and util.isVerticalMove(self.left_moves):
            return True
        return False


class MountainSign(Sign):

    def isTrue(self, postions):
        count = 0
        for lmLists in postions:
            if StaticSign.isMountain(lmLists):
                count = count + 1
        print(len(postions) * sign_contains_threshold, count)
        if len(postions) * sign_contains_threshold > count:
            return "unKnow"
        else:
            return "mountain"


class TreeSign(Sign):

    def __init__(self):
        self.right_moves = []
        self.left_moves = []

    def isTrue(self, postions):
        print("Tree is True?")
        count = 0
        self.right_moves = []
        self.left_moves = []
        for lmLists in postions:
            if StaticSign.isTree(lmLists):
                self.left_moves.append(lmLists[0][0])
                self.right_moves.append(lmLists[1][0])
                count = count + 1
        print(len(postions) * sign_contains_threshold, count)
        if len(postions) * sign_contains_threshold <= count and self.isRightMove():
            return "tree"
        return "unKnow"

    def isRightMove(self):
        if util.isVerticalUpMove(self.right_moves) and util.isVerticalUpMove(self.left_moves):
            return True
        return False
