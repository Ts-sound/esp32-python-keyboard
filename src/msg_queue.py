import collections

# msg_map = collections.OrderedDict(["",collections.deque()])

def NullFunc(msg = ""):
    print("run NullFunc msg ",msg)


sub_map = collections.OrderedDict([("",[NullFunc])])


def Publish(topic="",msg=""):
    try:
        print("run topic ",topic," msg :",msg)
        subs = sub_map[topic]
        for s in subs:
            s(msg)
    except Exception as e:
        print("Publish error : ",e)

def Subscribe(topic="",func=NullFunc):
    try:
        if topic in sub_map:
            sub_map[topic].append(func)
        else :
            sub_map[topic] = [func]
        print(sub_map)
    except:
        print("Subscribe error")


def Test():
    Subscribe("aaa")
    Publish(msg="aaaaaaaaaaa")
    Publish(topic="aaa",msg="aaaaaaaaaaa")
