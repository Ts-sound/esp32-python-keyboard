import collections

# msg_map = collections.OrderedDict(["",collections.deque()])

def NullFunc(msg = ""):
    print("run NullFunc msg ",msg)


sub_map = collections.OrderedDict([("",[NullFunc])])


def Publish(topic="",msg=""):
    try:
        print("run topic ",topic," sub func")
        subs = sub_map[topic]
        for s in subs:
            s(msg)
    except:
        print("Publish error")

def Subscribe(topic="",func=NullFunc):
    try:
        if topic in sub_map:
            sub_map[topic].append(func)
        else :
            sub_map[topic] = [func]
    except:
        print("Subscribe error")


def Test():
    Subscribe("aaa")
    Publish(msg="aaaaaaaaaaa")
    Publish(topic="aaa",msg="aaaaaaaaaaa")
