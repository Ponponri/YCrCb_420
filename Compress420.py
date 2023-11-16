import numpy as np

class Compress420:
    def __init__(self,img0):
        # Transform Matrix
        self.tr_bgr2ycrcb = np.array([[0.114,0.587,0.299],
                                      [-0.081,-0.419,0.5],
                                      [0.5,-0.331,-0.169]])
        # Inverse Transform Matrix
        self.tr_ycrcb2bgr = np.linalg.inv(self.tr_bgr2ycrcb)

        self.img0 = img0
        self.img0_444 = None
        self.img0_420 = None
        self.img_restore = None
        self.img_result = None

    
    def bgr_to_ycrcb444(self):
        # Convert Image from BGR to YCrCb 4:4:4
        h, w = self.img0.shape[:2]
        self.img0_444 = np.empty((h,w,3), dtype=np.float16)
        for i in range(h):
            for j in range(w):
                self.img0_444[i][j] = np.dot(self.img0[i][j],self.tr_bgr2ycrcb.T) + np.array([0,128,128])
        
        return self.img0_444

    def ycrcb444_to_420(self):
        # Compress the Image to YCrCb 4:2:0
        h, w = self.img0_444.shape[:2]
        h_420 = h//8
        w_420 = w//8
        self.img0_420 = np.empty((h_420,w_420,12,8), dtype=np.float16)
        for i in range(h_420):
            for j in range(w_420):
                for k in range(8):
                    for l in range(8):
                        self.img0_420[i,j,k,l] = self.img0_444[i*8+k,j*8+l,0]
                        if(k%2 == 0 and l%2 == 0):
                            self.img0_420[i,j,8+k//2,l//2] =  self.img0_444[i*8+k,j*8+l,1]
                            self.img0_420[i,j,8+k//2,4+l//2] = self.img0_444[i*8+k,j*8+l,2]
        
        return self.img0_420
    
    def ycrcb420_to_444(self):
        # Restore The Image
        h, w = self.img0_444.shape[:2]
        self.img_restore = np.empty((h,w,3), dtype=np.float16)
        for i in range(0,h,2):
            for j in range(0,w,2):
                self.img_restore[i,j,0] = self.img0_420[i//8,j//8,i%8,j%8]
                self.img_restore[i,j,1] = self.img0_420[i//8,j//8,8+(i%8)//2,(j%8)//2] 
                self.img_restore[i,j,2] = self.img0_420[i//8,j//8,8+(i%8)//2,(j%8)//2+4] 
        for i in range(1,h-1,2):
            for j in range(0,w,2):
                self.img_restore[i,j,0] = self.img0_420[i//8,j//8,i%8,j%8]
                self.img_restore[i,j,1] = (self.img_restore[i-1,j,1]+self.img_restore[i+1,j,1])/2
                self.img_restore[i,j,2] = (self.img_restore[i-1,j,2]+self.img_restore[i+1,j,2])/2

        for j in range(0,w,2):
            self.img_restore[h-1,j,0] = self.img0_420[(h-1)//8,j//8,(h-1)%8,j%8]
            self.img_restore[h-1,j,1] = self.img_restore[h-2,j,1]
            self.img_restore[h-1,j,2] = self.img_restore[h-2,j,2]

        for i in range(0,h):
            for j in range(1,w-1,2):
                self.img_restore[i,j,0] = self.img0_420[i//8,j//8,i%8,j%8]
                self.img_restore[i,j,1] = (self.img_restore[i,j-1,1]+self.img_restore[i,j+1,1])/2
                self.img_restore[i,j,2] = (self.img_restore[i,j-1,2]+self.img_restore[i,j+1,2])/2
            self.img_restore[i,j+2,0] = self.img0_420[i//8,(j+2)//8,i%8,(j+2)%8]
            self.img_restore[i,j+2,1] = self.img_restore[i,j+1,1]
            self.img_restore[i,j+2,2] = self.img_restore[i,j+1,2]

        return self.img_restore
    
    def ycrcb_to_bgr(self):
        # Convert Image from YCrCb to BGR
        h, w = self.img0_444.shape[:2]
        self.img_result = np.empty((h,w,3), dtype=np.uint8)
        for i in range(h):
            for j in range(w):
                self.img_result[i][j] = np.clip(np.dot(self.img_restore[i][j] + np.array([0,-128,-128]),self.tr_ycrcb2bgr.T),0,255)
        
        return self.img_result
    

