class spaceIntersection():
    def spaceIntersection(self, db, im1, im2):
        self.im1 = im1
        self.im2 = im2
        self.db = db


    def getGeoLocation(self, matches, pts1, pts2):
        cx1, cy1, f1, R1, XYZ1s, _, miu1 = self.db.getInfo(self.im1)
        X1s, Y1s, Z1s = XYZ1s
        cx2, cy2, f2, R2, XYZ2s, _, miu2 = self.db.getInfo(self.im2)
        X2s, Y2s, Z2s = XYZ2s

        for match in matches:
            pt1 = pts1[match.queryIdx].pt
            pt2 = pts2[match.trainIdx].pt
            x1, y1 = self.pix2Dist(cx1,cy1,miu1,int(self.im1.shape[0]/2), int(self.im1.shape[1]/2),pt1[0], pt1[1])
            x2, y2 = self.pix2Dist(cx2, cy2, miu2, int(self.im2.shape[0] / 2), int(self.im2.shape[1] / 2), pt2[0], pt2[1])
            l11 = f1 * R1[0][0] + x1 * R1[0][2] # l1
            l12 = f2 * R2[0][0] + x2 * R2[0][2] # l1 for right image
            l21 = f1 * R1[1][0] + x1 * R1[1][2] # l2
            l22 = f2 * R2[1][0] + x2 * R2[1][2] # l2 for right image
            l31 = f1 * R1[2][0] + x1 * R1[2][2] # l3
            l31 = f2 * R2[2][0] + x2 * R2[2][2] # l3 for right image


    # def calculation(self, info1, info2):
    #     l11 =

    def pix2Dist(self, cx, cy, miu, mx, my, pix_x, pix_y):
        return abs((mx-pix_x)*miu+cx), abs((my-pix_y)*miu+cy)
