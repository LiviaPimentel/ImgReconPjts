from __future__ import print_function
import cv2
import numpy as np
import time




# Load Yolo
net = cv2.dnn.readNet("yolov3-tiny-obj_1000.weights", "yolov3-tiny-obj.cfg")
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

cap = cv2.VideoCapture(0)
font=cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id=0



while True:
    _,frame = cap.read()
    height,width,channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame,0.00392,(320,320),(0,0,0),True,crop = False)

    net.setInput(blob)
    outs = net.forward(outputlayers)

    class_ids=[]
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
  	    class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
 		center_x = int(detection[0]*width)
		center_y = int(detection[1]*height)
		w = int(detection[2]*width)
		h = int(detection[3]*height)

		x = int(center_x - w/2)
        
		y = int(center_y-h/2)
		boxes.append([x,y,w,h])

        	print(x)
        	print(y) 

		confidences.append(float(confidence))
		class_ids.append(class_id)
    
    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)

    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
	    label =str(classes[class_ids[i]])
	    confidence = confidences[i]
            color = colors[class_ids[i]]
	    cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
 	    cv2.putText(frame,label+""+str(round(confidence,2)),(x,y+30),font,1,(255,255,255),2)

    elapsed_time = time.time()-starting_time
    fps = frame_id/elapsed_time
    cv2.putText(frame,"FPS:"+str(round(fps,2)),(10,50),font,2,(0,0,0),1)

    cv2.imshow("Image",frame)
    key = cv2.waitKey(1)

    if key == 27:
        break;

cap.release()
cv2.destroyAllWindows()


    






