from vision.ssd.vgg_ssd import create_vgg_ssd, create_vgg_ssd_predictor
from vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
from vision.ssd.mobilenetv1_ssd_lite import create_mobilenetv1_ssd_lite, create_mobilenetv1_ssd_lite_predictor
from vision.ssd.squeezenet_ssd_lite import create_squeezenet_ssd_lite, create_squeezenet_ssd_lite_predictor
from vision.ssd.mobilenet_v2_ssd_lite import create_mobilenetv2_ssd_lite, create_mobilenetv2_ssd_lite_predictor
from vision.utils.misc import Timer
import cv2
import sys
import numpy as np
import socket
from contextlib import closing



if len(sys.argv) < 4:
    print('Usage: python run_ssd_example.py <net type>  <model path> <label path> [video file]')
    # net_type = "mb1-ssd"
    # model_path = "models/mobilenet-v1-ssd-mp-0_675.pth"
    # label_path = "models/voc-model-labels.txt.1"
    net_type = "vgg16-ssd"
    model_path = "models/vgg16-ssd-mp-0_7726.pth"
    label_path = "models/voc-model-labels.txt.1"
else:
    net_type = sys.argv[1]
    model_path = sys.argv[2]
    label_path = sys.argv[3]

if len(sys.argv) >= 5:
    cap = cv2.VideoCapture(sys.argv[4])  # capture from file
else:
    cap = cv2.VideoCapture(0)   # capture from camera
    cap.set(3, 1920)
    cap.set(4, 1080)

class_names = [name.strip() for name in open(label_path).readlines()]
num_classes = len(class_names)


if net_type == 'vgg16-ssd':
    net = create_vgg_ssd(len(class_names), is_test=True)
elif net_type == 'mb1-ssd':
    net = create_mobilenetv1_ssd(len(class_names), is_test=True)
elif net_type == 'mb1-ssd-lite':
    net = create_mobilenetv1_ssd_lite(len(class_names), is_test=True)
elif net_type == 'mb2-ssd-lite':
    net = create_mobilenetv2_ssd_lite(len(class_names), is_test=True)
elif net_type == 'sq-ssd-lite':
    net = create_squeezenet_ssd_lite(len(class_names), is_test=True)
else:
    print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
    sys.exit(1)
net.load(model_path)

if net_type == 'vgg16-ssd':
    predictor = create_vgg_ssd_predictor(net, candidate_size=200)
elif net_type == 'mb1-ssd':
    predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)
elif net_type == 'mb1-ssd-lite':
    predictor = create_mobilenetv1_ssd_lite_predictor(net, candidate_size=200)
elif net_type == 'mb2-ssd-lite':
    predictor = create_mobilenetv2_ssd_lite_predictor(net, candidate_size=200)
elif net_type == 'sq-ssd-lite':
    predictor = create_squeezenet_ssd_lite_predictor(net, candidate_size=200)
else:
    print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
    sys.exit(1)

host_name = "192.168.0.80" # destination
port_name = 16384
buffer_size = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
size = "0"
with closing(sock):
    sock.bind((host_name, port_name))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        bin_data = bytes()

        timer = Timer()
        while True:
            while True:
                buf = conn.recv(buffer_size)
                if b'__end__' in buf:
                    conn.send(b'givemesize')
                    size_bin = conn.recv(buffer_size)
                    conn.send(b'break')
                    try:
                        img = np.frombuffer(bin_data, dtype=np.uint8).reshape(np.frombuffer(size_bin, dtype=np.int))
                        bin_data = b""
                        buf = b""
                        print(np.frombuffer(size_bin, dtype=np.int))
                        break
                    except Exception as e:
                        bin_data = b""
                        buf = b""
                        print(e)
                bin_data += buf
            orig_image = img
            # orig_image = cv2.flip(orig_image, 1)

            if orig_image is None:
                continue
            image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
            timer.start()
            boxes, labels, probs = predictor.predict(image, 10, 0.3)
            interval = timer.end()
            print('Time: {:.2f}s, Detect Objects: {:d}.'.format(interval, labels.size(0)))
            for i in range(boxes.size(0)):
                box = boxes[i, :]
                label = f"{class_names[labels[i]]}: {probs[i]:.2f}"
                # print(box)
                # print(label)
                cv2.rectangle(orig_image, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 4)

                cv2.putText(orig_image, label,
                            (box[0]+20, box[1]+40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,  # font scale
                            (255, 0, 255),
                            2)  # line type
            # cv2.imshow('annotated', orig_image)
            cv2.imshow('annotated', cv2.resize(orig_image, dsize=(600, 800)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
