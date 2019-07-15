import sys
import sqlite3
import numpy as np

# store the pose data in database
class DB():
    def __init__(self, dbPath):
        self.conn = sqlite3.connect(dbPath)
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE images (image_id, camera_id, qw, qx, qy, qz, tx, ty, tz, name)")

    def add_image(self, name, camera_id,prior_q=np.zeros(4), prior_t=np.zeros(3), image_id=None):
        self.c.execute(
            "INSERT INTO images VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (image_id, name, camera_id, prior_q[0], prior_q[1], prior_q[2],
             prior_q[3], prior_t[0], prior_t[1], prior_t[2]))

        self.conn.commit()

    def close(self):
        self.conn.close()




if __name__ == '__main__':
    dbPath = 'myDB.db'
    db = DB(dbPath)
    file = open('test.txt')
    count = 0
    for line_ in file.readlines():
        line = line_.split(' ')
        count+=1
        if line[0] != '#' and count%2 != 0:
            IMG_ID = int(line[0])
            Q = np.array([line[1], line[2], line[3], line[4]])
            T = np.array([line[5], line[6], line[7]])
            CAM_ID = int(line[8])
            NAME = line[9]
            db.add_image(NAME,CAM_ID,Q,T,IMG_ID)

    db.close()