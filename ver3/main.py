import recognition
import sensing
import time


class PotData:
    nowData = {}
    # wantDate = {}   #ex) wantData = {'lux' = 5, 'ph' = 6.5}

    def dataSensing(self, factor, address):
        self.nowData[factor] = sensing.getData(address)

        return self.nowData[factor]


def main():
    while True:
        pot = PotData()
        address = recognition.check()
        pot = PotData()

        for factor in address:
            pot.dataSensing(factor, address[factor])

        for i in pot.nowData.keys():    #센싱값 출력 테스트
            print("%s %s %s" % (i, pot.nowData[i], pot.nowData[i]))

        time.sleep(5)  # 5초 주기로 반복


main()
