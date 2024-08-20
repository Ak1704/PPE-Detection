import os
from argparse import ArgumentParser,Namespace
import xml.etree.ElementTree as ET
classes=["person",
"hard-hat",
"gloves",
"mask",
"glasses",
"boots",
"vest",
"ppe-suit",
"ear-protector",
"safety-harness"]
def read_text_file(file_path):
    with open(file_path, 'r') as f:
        print(f.read())
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(in_file_name,in_file_path,out_path):
    in_file = open(in_file_path)
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    with open(f'{out_path}\{in_file_name.rstrip(".xml")}.txt', 'w') as out_file:
        for obj in root.iter('object'):
            #difficult = obj.find('difficult').text
            cls = obj.find('name').text
            #if cls not in classes or int(difficult)==1:
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w,h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
parser = ArgumentParser()
parser.add_argument('input_dir',help="Provide path to input directory",type=str)
parser.add_argument('output_dir',help="Provide path to output directory",type=str)
args: Namespace = parser.parse_args()
path=args.input_dir
out_path = args.output_dir
for file in os.listdir(path):
    file_path = f"{path}\{file}"
    convert_annotation(file,file_path,out_path)