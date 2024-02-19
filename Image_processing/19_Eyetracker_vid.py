import cv2 as cv
import numpy as np
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.FaceMeshModule import FaceMeshDetector

LEFT_EYE =[362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398]


detector = FaceDetector()
meshdetector = FaceMeshDetector(maxFaces=1)


cap = cv.VideoCapture("Videos/eye_tracker.mp4")
if (cap.isOpened()== False):
    print("Error opening video stream or file")

 
while(cap.isOpened()):
    ret, frame = cap.read()
    ret, frame2 = cap.read()
    if ret == True:
        face_img, bbox = detector.findFaces(frame)
        face_img, faces = meshdetector.findFaceMesh(frame)
        print(bbox)
        if bbox:
            center = bbox[0]["center"]   
            if faces:
                left_eye_points = np.array([[faces[0][p][0],faces[0][p][1]] for p in LEFT_EYE])
                #cv.fillPoly(face_img2, pts=[left_eye_points], color = 255)
                (ex,ey,ew,eh) = cv.boundingRect(left_eye_points)
                #cv.rectangle(face_img2, (ex,ey), (ex+ew,ey+eh), (255,255,255))
                eye_roi = frame2[ey:ey+eh, ex:ex+ew]
                eye_roi_gr = cv.cvtColor(eye_roi, cv.COLOR_BGR2GRAY)
                _, iris = cv.threshold(eye_roi_gr, 40, 255, cv.THRESH_BINARY_INV)
                contours, _ = cv.findContours(iris, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)

                if contours:
                    (ix,iy,iw,ih) = cv.boundingRect(contours[0])
                    ix_cntr, iy_centr = ix+int(iw/2) + ex, iy+int(ih/2)+ey
                    cv.circle(frame2, (ix_cntr, iy_centr), 5, (0,0,255), -1)

                    ix_cntr_e, iy_centr_e = ix+int(iw/2), iy+int(ih/2)

                    offset = 10
                    if ix_cntr_e > int(ew/2)+offset:
                        text = "right"
                    elif ix_cntr_e < int(ew/2)-offset:
                        text = "left"
                    else:
                        text = "center"

                    cv.putText(frame2, text, (100,100), cv.FONT_HERSHEY_PLAIN, 3, (0,60,0), 2)


        cv.imshow('frame2', frame2)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv.destroyAllWindows()