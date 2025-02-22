import cv2
import numpy as np

#obtener capas de salida
def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    #print("layer names ",layer_names)
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    
image = cv2.imread("ciudadcongestion.jpg")

Height = image.shape[0]
Width = image.shape[1]
scale = 0.00392

classes = "coco.names"

with open(classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]#class List
    #print(classes)
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
weights = "yolov3.weights" 
config = "yolov3.cfg"

net = cv2.dnn.readNet(weights, config)

blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

net.setInput(blob)

outs = net.forward(get_output_layers(net))
#print(len(outs))#3 class tuple
print(outs)#3

class_ids = []
confidences = []
boxes = []
conf_threshold = 0.5
nms_threshold = 0.4

for out in outs:
    
    for detection in out:
        print(len(detection))#85
        scores = detection[5:]
        class_id = np.argmax(scores)#devuelve el indice(num int) del valor mas alto en la estructura
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])

#supression non maximun
indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

for i in indices:
    try:
        box = boxes[i]
    except:
        i = i[0]
        box = boxes[i]
    
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

cv2.imshow("object detection", image)
cv2.waitKey()
    
#cv2.imwrite("object-detection.jpg", image)
cv2.destroyAllWindows()