import DynamicSign
import StaticSign

dynamicSigns = dict()
dynamicSigns["unKnow"] = DynamicSign.Sign()
dynamicSigns["hello"] = DynamicSign.HelloSign()
dynamicSigns["grass"] = DynamicSign.GrassSign()
dynamicSigns["mountain"] = DynamicSign.MountainSign()
dynamicSigns["tree"] = DynamicSign.TreeSign()
dynamicSigns["human"] = DynamicSign.HumanSign()
dynamicSigns["mushroom"] = DynamicSign.MushRoomSign()
dynamicSigns["flower"] = DynamicSign.FlowerSign()
dynamicSigns["fish"] = DynamicSign.FishSign()
dynamicSigns["cow"] = DynamicSign.CowSign()
dynamicSigns["pig"] = DynamicSign.PigSign()
dynamicSigns["horse"] = DynamicSign.HorseSign()
dynamicSigns["home"] = DynamicSign.HomeSign()


def getBeginSign(postions):
    i = -1
    for lmLists in postions:
        i = i+1
        # if StaticSign.isHello(lmLists):
        #     text = "hello"
        #     break
        if StaticSign.isHome(lmLists):
            text = "home"
            break
        elif StaticSign.isHorse(lmLists):
            text = "horse"
            break
        elif StaticSign.isPig(lmLists):
            text = "pig"
            break
        elif StaticSign.isCow(lmLists):
            text = "cow"
            break
        elif StaticSign.isFish(lmLists):
            text = "fish"
            break
        elif StaticSign.isFlower(lmLists, True):
            text = "flower"
            break
        elif StaticSign.isMushroom(lmLists):
            text = "mushroom"
            break
        elif StaticSign.isMountain(lmLists):
            text = "mountain"
            break
        elif StaticSign.isHuman(lmLists):
            text = "human"
            break
        elif StaticSign.isGrass(lmLists):
            text = "grass"
            break
        elif StaticSign.isTree(lmLists):
            text = "tree"
            break
        # elif StaticSign.isZero(lmLists):
        #     text = "0"
        #     break
        # elif StaticSign.isOne(lmLists):
        #     text = "1"
        #     break
        # elif StaticSign.isTow(lmLists):
        #     text = "2"
        #     break
        # elif StaticSign.isThree(lmLists):
        #     text = "3"
        #     break
        # elif StaticSign.isFour(lmLists):
        #     text = "4"
        #     break
        # elif StaticSign.isFive(lmLists):
        #     text = "5"
        #     break
        else:
            text = "unKnow"
    print("getBeginSign:", text)
    if text not in dynamicSigns:
        text = "unKnow"
    return dynamicSigns[text], postions[i:]


def judgeSign(postions):
    print("lenPostions: ", len(postions))
    # 判断第一个能识别出来的帧对应的哪个手势的起手式
    dynamic_ign, filt_postions = getBeginSign(postions)
    text = dynamic_ign.isTrue(filt_postions)
    return text
