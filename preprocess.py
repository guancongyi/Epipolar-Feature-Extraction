import numpy as np
import database

def parse(line):
    IMG_ID = int(line[0])
    # qw qx qy qz
    qw,qx,qy,qz = float(line[1]),float(line[2]),float(line[3]),float(line[4])
    tx,ty,tz = float(line[5]),float(line[6]),float(line[7])

    Q = np.array([qw, qx, qy, qz])
    T = np.array([tx, ty, tz])
    R = np.array([[1 - 2 * qy * qy - 2 * qz * qz, 2 * qx * qy - 2 * qz * qw, 2 * qx * qz + 2 * qy * qw],
                  [2 * qx * qy + 2 * qz * qw, 1 - 2 * qx * qx - 2 * qz * qz, 2 * qy * qz - 2 * qx * qw],
                  [2 * qx * qz - 2 * qy * qw, 2 * qy * qz + 2 * qx * qw, 1 - 2 * qx * qx - 2 * qy * qy]])
    XYZ = np.dot(-R.T, T)
    CAM_ID = int(line[8])
    NAME = line[9]

    return (NAME, R, T, XYZ)


if __name__ == '__main__':
    # initilize database
    db = database.DB('extrinsic.db')
    db.create_table('images', ['name', 'r11', 'r12', 'r13',
                               'r21', 'r22', 'r23',
                               'r31', 'r32', 'r33',
                               't11', 't12', 't13',
                               'Xs', 'Ys', 'Zs'])

    # read quaternion and translation matrix
    # store them in database
    file = open('test/tianjin_E.txt')
    count = 0
    for line_ in file.readlines():
        line = line_.split(' ')
        count+=1
        if line[0] != '#' and count%2 != 0:
            (img_name, R, T, XYZ )= parse(line)
            name = img_name[:-1]
            db.add_image(name,R,T,XYZ)


    db.close()