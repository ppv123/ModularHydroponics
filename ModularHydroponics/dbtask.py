import datetime
import sqlite3


class DBtask(object):
    def __init__(self, target):
        self.conn = sqlite3.connect(target)

    def insertcondition(self, **kwargs):

        try:
            cursor = self.conn.cursor()

            sql = 'insert into condition_plantconditions (plant_id, hum, lux, ph, temp, timestamp) values (?,?,?,?,?,?)'
            now = datetime.datetime.now()
            cursor.execute(sql, (kwargs.pop('plant_id', ''), kwargs.pop('hum', 0), kwargs.pop('lux', 0), kwargs.pop('ph',0), kwargs.pop('temp',0), now))
            self.conn.commit()

        except:
            print('insert error')

    def getfield(self):
        try:
            cur = self.conn.execute("select * from condition_plantconditions")
            field = list(map(lambda x: x[0], cur.description))

            return field

        except:
            pass

    def closeconn(self):
        self.conn.close()


if __name__ == '__main__':
    nowD = {'plant_id': 4, 'lux': 3.0, 'ph': 5.0, 'temp': 16.0, 'hum': 7.0}

    db = DBtask('../mandellion5/db.sqlite3')
    db.insertcondition(**nowD)
    db.closeconn()

