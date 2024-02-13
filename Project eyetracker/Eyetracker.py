import cv2 as cv 
import numpy as np 
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.FaceMeshModule import FaceMeshDetector



detector = FaceDetector()
meshdetector = FaceMeshDetector(maxFaces=1)

face_img = cv.imread("f.jpg")

face_img , bbox = detector.findFaces(face_img)
face_img , faces = meshdetector.findFaceMesh(face_img)

cv.imshow('face_img' , face_img)
cv.waitKey(0)
cv.destroyAllWindows()