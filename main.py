import cv2
import time
import os
import glob
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame=None
status_list=[]
count=1

def clean_folder():
    for file in glob.glob("images/*.png"):
        os.remove(file)

clean_thread=Thread(target=clean_folder)
try:
    while True:   
        status=0
        check, frame = video.read()

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gaussianed = cv2.GaussianBlur(gray_frame, (21,21), 0)

        if first_frame is None:
            first_frame = gaussianed

        delta_frame= cv2.absdiff(first_frame,gaussianed)

        thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
        dil_frame=cv2.dilate(thresh_frame,None,iterations=2)
        cv2.imshow("My video",dil_frame)

        contours,check=cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour)<5000:
                continue
            x,y, w,h=cv2.boundingRect(contour)
            rectange=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0))
            if rectange.any():
                status=1
                cv2.imwrite(f"images/{count}.png",frame)
                count=count+1
                all_image=glob.glob("images/*.png")
                index=int(len(all_image)/2)
                image_obj=all_image[index]

        status_list.append(status)
        status_list=status_list[-2:]

        if status_list[0]==1 and status_list[1]==0:
            email_thread=Thread(target=send_email,args=(image_obj,))
            email_thread.daemon = True
            email_thread.start()

        cv2.imshow("Video",frame)
        key = cv2.waitKey(1)  # waitKey requires an argument, 1 is the delay in milliseconds

        if key == ord("q"):
            break

except KeyboardInterrupt:
    print("Program interrupted by user")

finally:
    video.release()
    clean_thread.start()
    cv2.destroyAllWindows()  # destroyAllWindows is necessary to close all OpenCV windows