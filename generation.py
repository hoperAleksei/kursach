import json
import random
import os.path


SQ_TYPE = ("Упорядоченная", "Из едениц", "Случайная", "Частичная", "Обратная")
SQ_DES = ("ord", "sing", "rnd", "par", "rvs")
# SQ_DES = ("ordered", "single", "random", "partial", "reverse")


class SortFile:
    def __init__(self, seq_type, count, name, sequence):
        self.type = seq_type
        self.sequence = sequence
        self.count = count
        self.name = name


class FileEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, SortFile):
            return {"__file__": True, "type": o.type, "count": o.count, "name": o.name, "sequence": o.sequence}
        else:
            super().default(self)


def decode_file(dct):
    seq_type = ""

    if "__file__" in dct:
        for i in range(len(SQ_DES)):
            if SQ_DES[i] == dct["type"]:
                seq_type = SQ_TYPE[i]
                break

        return SortFile(seq_type=seq_type, count=dct["count"], name=dct["name"], sequence=dct["sequence"])
    return dct


def generate_file(seq_type, count, folder):

    type_des = ""
    arr = []

    if seq_type == SQ_TYPE[0]:
        type_des = SQ_DES[0]
        arr = [i for i in range(count)]
    elif seq_type == SQ_TYPE[1]:
        type_des = SQ_DES[1]
        arr = [1] * count
    elif seq_type == SQ_TYPE[2]:
        type_des = SQ_DES[2]
        arr = [random.randint(0, count) for _ in range(count)]
    elif seq_type == SQ_TYPE[3]:
        type_des = SQ_DES[3]
        arr = [i if i < count / 2 else random.randint(int(count / 2), count) for i in range(count)]
    elif seq_type == SQ_TYPE[4]:
        type_des = SQ_DES[4]
        arr = [i for i in range(count - 1, -1, -1)]

    file_name = type_des + "_" + str(count) + ".sort"
    full_name = folder + "\\" + file_name

    if os.path.isfile(full_name):
        n = 1
        while os.path.isfile(full_name):
            file_name = type_des + "_" + str(count) + "(" + str(n) + ")" + ".sort"
            full_name = folder + "\\" + file_name
            n += 1

    sf = SortFile(type_des, count, file_name, arr)

    with open(full_name, "w", encoding="UTF-8") as file:
        json.dump(sf, file, cls=FileEncoder)

    # print(seq_type, count, folder)


def open_file(filename):
    if not os.path.isfile(filename):
        return None
    with open(filename, "r") as file:
        return json.load(file, object_hook=decode_file)


if __name__ == "__main__":
    generate_file("Упорядоченная", 1010, "./files/")

    ss = open_file("./files/ord_1000.sort")

    print(repr(ss.type), repr(ss.count), repr(ss.name), repr(ss.sequence))
