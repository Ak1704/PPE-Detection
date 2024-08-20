import os
from argparse import ArgumentParser,Namespace
import cv2
from ultralytics import YOLO
def make_infer(in_file_path,out_file_path,person_detect_model,ppe_model):
    for i in os.listdir(in_file_path):
        img = cv2.imread(f'{in_file_path}\{i}')
        res=infer(img,person_detect_model,ppe_model)
        cv2.imwrite(f'{out_file_path}\{i}',res)
def infer(img,person_weight,ppe_weight):
    classes = ["person",
               "hard-hat",
               "gloves",
               "mask",
               "boots",
               "glasses",
               "vest",
               "ppe-suit",
               "ear-protector",
               "safety-harness"]
    person_model = YOLO(person_weight)
    ppe_model = YOLO(ppe_weight)
    pred = person_model(img)
    for box in pred[0].boxes:
        x1, y1, x2, y2 = [
            round(x) for x in box.xyxy[0].tolist()
        ]
        crop_img = img[y1:y2,x1:x2]
        ppe_pred = ppe_model(crop_img)
        for b in ppe_pred[0].boxes:
            class_id = b.cls[0].item()
            xp1, yp1, xp2, yp2 = [
                round(x) for x in b.xyxy[0].tolist()
            ]
            if class_id==0:
                img = cv2.rectangle(img, (x1 + xp1, y1 + yp1), (x1 + xp2, y1 + yp2), (0, 0, 255), 1)
                cv2.putText(img, 'person', (x1 + xp2, y1 + yp1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                continue
            img = cv2.rectangle(img, (x1+xp1, y1+yp1), (x1+xp2,y1+yp2), (266, 0, 0), 2)
            class_id = int(b.cls[0].item())
            prob = round(b.conf[0].item(), 2)
            cv2.putText(img, f'{classes[class_id]}', (x1+xp1, y1+yp1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
            cv2.putText(img, f'{prob}', (x1+xp2, y1+yp1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
    return img
#make_infer("test-1","test","Weights/Person_detect/content/runs/detect/train/weights/best.pt","Weights/PPE_model/content/runs/detect/train4/weights/best.pt")
parser = ArgumentParser()
parser.add_argument('input_dir',help="Provide path to input directory",type=str)
parser.add_argument('output_dir',help="Provide path to output directory",type=str)
parser.add_argument('person_model',help="Provide path to person detection model",type=str)
parser.add_argument('ppe_model',help="Provide path to ppe detection model",type=str)
args: Namespace = parser.parse_args()
make_infer(args.input_dir,args.output_dir,args.person_model,args.ppe_model)