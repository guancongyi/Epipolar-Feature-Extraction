import sys
import sqlite3
import numpy as np

# store the pose data in database
class DB():
    def __init__(self, dbPath):
        self.conn = sqlite3.connect(dbPath)
        self.cursor = self.conn.cursor()


    def create_table(self, name, items):
        s_ = ''
        for i in items:
            s_ = s_ + i + ','

        s = s_[:-1]
        cmd = 'CREATE TABLE ' + name + ' (' + s + ')'
        self.cursor.execute(cmd)

    def add_image(self, name, cx, cy, f, R=np.zeros((3,3)), XYZ=np.zeros(3), Euler=np.zeros(3)):
        self.cursor.execute(
            "INSERT INTO images VALUES (?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?)",
            (name, cx, cy, f, R[0,0], R[0,1], R[0,2],
                    R[1,0], R[1,1], R[1,2],
                    R[2,0], R[2,1], R[2,2],
                    XYZ[0], XYZ[1], XYZ[2], Euler[0], Euler[1], Euler[2]))

        self.conn.commit()

    def getInfo(self, name):
        temp = self.cursor.execute('SELECT * FROM images WHERE name = ?', (name, ))
        row = temp.fetchall()[0]
        cx, cy, f = row[1], row[2], row[3]
        R = np.array([[row[4], row[5], row[6]],
                      [row[7], row[8], row[9]],
                      [row[10], row[11], row[12]]])
        Euler = np.array([row[16], row[17], row[18]])
        XYZ = np.array([row[13], row[14], row[15]])
        return (R,Euler,XYZ)

    def close(self):
        self.conn.close()

