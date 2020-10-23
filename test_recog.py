import smbus  # 10.08 need test


def initI2C():
    address = {}

    for i in range(0, 2):
        for j in range(128):
            try:
                bus.write_byte(j, 0)
                address[j] = hex(j)
            except():
                pass

    for i in address.keys():
        print("%s %s" % (i, address[i]))


initI2C()
