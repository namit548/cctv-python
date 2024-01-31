import cv2 
import numpy as np

#web cam
#cap = cv2.VideoCapture('D:\\work\\cctv python\\cctv 1.0\\video.mp4')

cap = cv2.VideoCapture('D:\\personal\\cctv\\2023-08-29\\73863-76433.mp4')



min_width_react=80 #min widht reactangle
min_hieght_react=80 #min hight reactangle
count_line_position = 550



def center_handel(x,y,w,h):
    x1= int(w/2)
    y1= int(w/2)
    cy = y+y1
    cx = x+x1
    return cx,cy

detect = []#vehical detech karke list banega ki kitni aa gyi abhi tak
offset = 6#Allow erroe in pixel
counter =0


#intialize substrutor
#algo = cv2.bgsegm.createBackgroundSubtractorMOG2()
algo = cv2.createBackgroundSubtractorMOG2()

#(algo name can be change by) algorith hai ye vehical ka background suntract krega



while True:
    ret,frame1=cap.read()
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    
    # applying on each frame
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada = cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)#diltada can be change
    dilatada = cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernel)#diltada can be change
    CounterSahpe,h = cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

   # cv2.line(frame1,25,count_line_position,(1200,count_line_position),(225,127,0),3)
    cv2.line(frame1,(25, count_line_position),(1200,count_line_position), (225, 127, 0), 3)


    for(i,c) in enumerate(CounterSahpe):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>= min_width_react) and (h>= min_hieght_react)
        if not validate_counter:





            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h ),(0,255,0),2)#clor of boxes 

        cv2.putText(frame1,"VEHICLE COUNTER"+ str(counter),(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5) # vehicle box names        


        center = center_handel(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,4,(0,0,255),-1)


        for(x,y) in detect:
            if y<(count_line_position+offset) and y>(count_line_position-offset):
                counter+=1
            cv2.line(frame1,(25, count_line_position),(1200,count_line_position), (225, 127,255), 3)
            detect.remove((x,y))
            print("counter number :"+str(counter))

            cv2.putText(frame1,"VEHICLE COUNTER"+ str(counter),(450,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),5)        




#black in white image ke liye
    #cv2.imshow('detecher',dilatada )
    cv2.imshow('video original', frame1)

    if cv2.waitKey(1) == 13:
        break

cv2.destroyAllWindows()
cap.release()

