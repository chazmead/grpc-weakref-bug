import copy
from protobuf import message_pb2


class Obj:
    value = None

    def __init__(self, value):
        self.value = value


def get_obj():
    pb = message_pb2.TestMessage()
    obj = Obj(value=pb.value)
    return obj


def main():
    obj = get_obj()
    cp = copy.deepcopy(obj)
    print('No Weakref Issue here...')


if __name__ == '__main__':
    main()
