import msg_queue


def Func(msg=""):
    print("sub1 recv :",msg)

msg_queue.Subscribe("test",Func)
