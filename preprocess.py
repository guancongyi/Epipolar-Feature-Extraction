import numpy as np
import database
import math


# Calculates Rotation Matrix given euler angles.
def eulerAnglesToRotationMatrix(theta):
    R_x = np.array([[1, 0, 0],
                    [0, math.cos(theta[0]), -math.sin(theta[0])],
                    [0, math.sin(theta[0]), math.cos(theta[0])]
                    ])

    R_y = np.array([[math.cos(theta[1]), 0, math.sin(theta[1])],
                    [0, 1, 0],
                    [-math.sin(theta[1]), 0, math.cos(theta[1])]
                    ])

    R_z = np.array([[math.cos(theta[2]), -math.sin(theta[2]), 0],
                    [math.sin(theta[2]), math.cos(theta[2]), 0],
                    [0, 0, 1]
                    ])
    # Change direction if necessary
    R = np.dot(R_x, np.dot(R_y, R_z))

    return R

def parse(line):
    IMG_ID = line[0]
    # XYZ
    X,Y,Z = float(line[1]),float(line[2]),float(line[3])
    omega,phi,kappa = math.radians(float(line[4])),math.radians(float(line[5])),math.radians(float(line[6]))
    theta = (omega,phi,kappa)
    R = eulerAnglesToRotationMatrix(theta)

    return (IMG_ID, R, (X,Y,Z), theta)


if __name__ == '__main__':
    # initilize database
    db = database.DB('extrinsic.db')
    db.create_table('images', ['name','cx','cy','f', 'r11', 'r12', 'r13',
                               'r21', 'r22', 'r23',
                               'r31', 'r32', 'r33',
                               'omega', 'phi', 'kappa',
                               'Xs', 'Ys', 'Zs'])

    # Read in intrinsic and extrinsic parameters
    external = open('pix4d/test_calibrated_external_camera_parameters_wgs84.txt')

    '''Change ME'''
    ''''''''''''''''''
    ''''''''''''''''''
    cx = -0.05848851875596568217
    cy = -0.15072189195079516155
    f = 42.64141405461381850728

    # read extrinsic
    count = 1;
    for line_ in external.readlines():
        line = line_.split(' ')
        if count == 1:
            count = 0
            continue
        else:
            (img_name, R, XYZ, euler) = parse(line)
            db.add_image(img_name, cx , cy, f, R , euler, XYZ)


    db.close()