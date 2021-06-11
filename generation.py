import json
import random
import os.path


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
    sequence_type = ("Упорядоченная", "Из едениц", "Случайная", "Частичная", "Обратная")
    sequence_des = ("ordered", "single", "random", "partial", "reverse")

    seq_type = ""

    if "__file__" in dct:
        for i in range(len(sequence_des)):
            if sequence_des[i] == dct["type"]:
                seq_type = sequence_type[i]
                break

        return SortFile(seq_type=seq_type, count=dct["count"], name=dct["name"], sequence=dct["sequence"])
    return dct


def generate_file(seq_type, count, folder):
    sequence_type = ("Упорядоченная", "Из едениц", "Случайная", "Частичная", "Обратная")
    sequence_des = ("ordered", "single", "random", "partial", "reverse")

    type_des = ""
    arr = []

    if seq_type == sequence_type[0]:
        type_des = sequence_des[0]
        arr = [i for i in range(count)]
    elif seq_type == sequence_type[1]:
        type_des = sequence_des[1]
        arr = [1] * count
    elif seq_type == sequence_type[2]:
        type_des = sequence_des[2]
        arr = [random.randint(0, count) for i in range(count)]
    elif seq_type == sequence_type[3]:
        type_des = sequence_des[3]
        arr = [i if i < count / 2 else random.randint(int(count / 2), count) for i in range(count)]
    elif seq_type == sequence_type[4]:
        type_des = sequence_des[4]
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

    ss = open_file("./files/ordered_1010.sort")

    print(repr(ss.type), repr(ss.count), repr(ss.name), repr(ss.sequence))
