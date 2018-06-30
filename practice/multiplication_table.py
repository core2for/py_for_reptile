def multiplication_table():
    for row in range(1, 10):
        for col in range(1, row+1):
            print("{0}*{1}={2}".format(row, col, row*col), end=' ')
        print()


if __name__ == "__main__":
    multiplication_table()