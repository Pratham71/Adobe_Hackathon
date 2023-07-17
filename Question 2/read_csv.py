import csv


def read_csv():
    f = []
    with open("input/q2/transactions.csv") as file:
        lines = csv.reader(file)
        counter = 0
        for line in lines:
            line.insert(0, counter)
            f.append(line)
            counter += 1
    return f


if __name__ == "__main__":
    print(read_csv())
