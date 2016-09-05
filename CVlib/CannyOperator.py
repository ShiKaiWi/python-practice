import numpy as np
import pylab as plt
import mahotas as mh
import sys
sys.path.append('/home/kai/github-workspace/python-practice/CVlib/')
import GaussianFilter as GF

class CannyOperator(object):
    def __init__(self,img,threshold_H=None,threshold_L=None):
        self.img = mh.imread(img)
        self.M,self.N = self.img.shape
        self.imgsmooth = GF.GaussianFilter(img).filter()
        self.sobelx,self.sobely = self.createSobel()
        self.sobelmax = 0
        self.imgsobel = self.extractEdgesViaSobel()  
        self.trackmatrix = np.zeros((self.M,self.N))
    
    def createSobel(self):
        sobelx = np.array([-1.0,0,1,-2,0,2,-1,0,1])
        sobely = np.array([-1.0,-2,-1,0,0,0,1,2,1])
        sobelx = np.reshape(sobelx,(9,1))
        sobely = np.reshape(sobely,(9,1))
        return [sobelx,sobely]

    def sobelKernel(self,wind):
        x = np.sum(self.sobelx*wind[::-1])
        y = np.sum(self.sobely*wind[::-1])
        return np.sqrt(x*x+y*y)

    def extractEdgesViaSobel(self):
        imgsobel = np.zeros((self.M,self.N))
        for i in range(0,self.M):
            for j in range(0,self.N):
                if i<1 or j<1 or i>self.M-2 or j>self.N-2:
                    imgsobel[i][j] = 0
                    continue
                imgsobel[i][j] = self.sobelKernel(np.reshape(self.imgsmooth[i-1:i+2,j-1:j+2],(9,1)))
                self.sobelmax = max(imgsobel[i][j],self.sobelmax)
        return imgsobel

    def cannyOperation(self,threshold_HPercent=0.30,threshold_LPercent=0.20):
        self.threshold_H = self.sobelmax*threshold_HPercent
        self.threshold_L = self.sobelmax*threshold_LPercent
        for i  in range(0,self.M):
            for j in range(0,self.N):
                if self.trackmatrix[i][j]>0 or self.imgsobel[i][j]<self.threshold_H:continue
                self.track(self.imgsobel,i,j)
        return self.trackmatrix

    def track(self,imgx,tx,ty):
        if tx>self.M-1 or ty>self.N-1 or tx<0 or ty<0:
            return
        if self.trackmatrix[tx][ty]:return
        if imgx[tx][ty] < self.threshold_L:
            return
        self.trackmatrix[tx][ty] = 255
        self.track(imgx,tx+1,ty)
        self.track(imgx,tx,ty+1)

    def demo(self):
        # plt.imshow(self.imgsobel*255/self.sobelmax)
        # plt.gray()
        # plt.show()
        plt.imshow(255-self.cannyOperation())
        plt.gray()
        plt.show()
