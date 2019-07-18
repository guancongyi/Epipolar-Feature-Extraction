import numpy as np
import database
import cv2

class rectification():
    def __init__(self, cx, cy, f, R, miu):
        self.f = f
        self.cx = cx
        self.cy = cy
        self.miu = miu
        self.a1, self.a2, self.a3 = R[0, 0], R[0, 1], R[0, 2]
        self.b1, self.b2, self.b3 = R[1, 0], R[1, 1], R[1, 2]
        self.c1, self.c2, self.c3 = R[2, 0], R[2, 1], R[2, 2]

    def getEpipolarImage(self, src):
        r, c = src.shape[:2]
        r_dst, c_dst = self.getResultImgSize((r,c))
        dst = np.zeros((r_dst, c_dst, 3), np.uint8)
        # resample
        for i in range(int(r_dst/8)-100, int(r_dst/8)+100):
            for j in range(int(c_dst/8)-100, int(c_dst/8)+100):
                # physical distance
                du, dv = self.pixToDist((r_dst/2, c_dst/2), (i, j), (0,0))
                dx, dy = self.uvToXy(du, dv)
                x, y = self.distToPix((r,c),(dx,dy),(self.cx,self.cy))
                if (x >= 0 and y >= 0) and (x < r and x < c):
                    print(i)
                    dst[i, j, 1] = src[x, y, 1]
                    dst[i, j, 2] = src[x, y, 2]
                    dst[i, j, 3] = src[x, y, 3]


        return dst



    # estimate the result image size by
    # estimating the original image's
    # left up corner and bottom right corner.
    def getResultImgSize(self, size):
        r, c = size
        x1, y1 = self.pixToDist((r / 2, c / 2), (0, 0), (self.cx, self.cy))
        x2, y2 = self.pixToDist((r / 2, c / 2), (r, c), (self.cx, self.cy))
        x3, y3 = self.pixToDist((r / 2, c / 2), (0, c), (self.cx, self.cy))
        x4, y4 = self.pixToDist((r / 2, c / 2), (r, 0), (self.cx, self.cy))

        # top left
        u1, v1 = self.xyToUv(x1, y1)
        # bottom right
        u2, v2 = self.xyToUv(x2, y2)
        u3, v3 = self.xyToUv(x3, y3)
        u4, v4 = self.xyToUv(x4, y4)

        us = [abs(u1), abs(u2), abs(u3), abs(u4)]
        vs = [abs(v1), abs(v2), abs(v3), abs(v4)]

        u = int((max(us)-min(us))/self.miu)
        v = int((max(vs)-min(vs))/self.miu)

        return (u, v)

    # function that convert u,v in parallel coordinate system to xy
    # in orginal coordinate system based on extrinsic parameters.
    def uvToXy(self, u, v):
        x = -self.f * (self.a1 * u + self.b1 * v - self.c1 * self.f) / (self.a3 * u + self.b3 * v - self.c3 * self.f)
        y = -self.f * (self.a2 * u + self.b2 * v - self.c2 * self.f) / (self.a3 * u + self.b3 * v - self.c3 * self.f)
        return (x,y)

    # On the other hand
    def xyToUv(self, x, y):
        A = np.array([[self.a3*x+self.a1*self.f, self.b3*x+self.b1*self.f],
                      [self.a3*y+self.a2*self.f, self.b3*y+self.b2*self.f]])
        b = np.array([[self.c1*self.f*self.f+self.c3*x*self.f],
                      [self.c2*self.f*self.f+self.c3*y*self.f]])

        Ainv = np.linalg.inv(A)
        reslt = np.dot(Ainv,b)
        return (reslt[0,0],reslt[1,0])

    # Convert pixel distance to physical distance on CCD
    def pixToDist(self, center, xy, cxy):
        mx, my = center
        x, y = xy
        cx, cy = cxy
        return ((mx - x) * self.miu + cx, (my - y) * self.miu + cy)

    # On the other hand
    def distToPix(self, center, dxy, cxy):
        dx, dy = dxy
        mx, my = center
        cx, cy = cxy
        return ( int(mx-((dx-cx)/self.miu)),int(my-((dy-cy)/self.miu)) )


if __name__ == '__main__':
    # get extrinsic from database
    im1 = 'E00224_40814-thred.jpg'
    im2 = 'E02814_43404-thred.jpg'

    db = database.DB('extrinsic.db')
    (R1, T1, XYZ1) = db.get_RT(im1)
    (R2, T2, XYZ2) = db.get_RT(im2)
    cx1 = -0.07302
    cy1 = -0.009029
    miu1 = 0.0046
    f1 = 40

    # find epipolar image by using epipolar rectification
    path1 = 'test/' + im1
    # path2 = 'test/' + im2
    img1 = cv2.imread(path1)

    obj1 = rectification(cx1,cy1,f1,R1,miu1)
    ret1 = obj1.getEpipolarImage(img1)

    cv2.imwrite('result.jpg', ret1)
    print('done')







