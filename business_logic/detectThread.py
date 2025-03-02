import threading

import argparse
import time
from pathlib import Path
import os

from cv2 import imshow, waitKey, imwrite, VideoWriter, VideoWriter_fourcc, CAP_PROP_FPS, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT
from torch import load, zeros, from_numpy, no_grad, tensor
import torch.backends.cudnn as cudnn
import numpy as np

from models.experimental import attempt_load
from detection.utils.datasets import LoadStreams, LoadImages
from detection.utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from detection.utils.plots import plot_one_box
from detection.utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel
import shutil

openedDrawersList = []
for i in range(13):
    try: 
        if i == 0:
            shutil.rmtree("runs/detect/exp")
        else:
            shutil.rmtree("runs/detect/exp" + str(i))
    except:
        pass
    
###################################### DRAWER THREADS FLAGS START ######################################
exitFlag = False

drawer_1_flag = False
drawer_2_flag = False
drawer_3_flag = False
drawer_4_flag = False
drawer_5_flag = False
drawer_6_flag = False

drawer_1_executed_first_one = False
drawer_2_executed_first_one = False
drawer_3_executed_first_one = False
drawer_4_executed_first_one = False
drawer_5_executed_first_one = False
drawer_6_executed_first_one = False
###################################### DRAWER THREADS FLAGS END ######################################

###################################### DRAWER-1 RETURN VARIABLES START ######################################
drawer_1_cam_1_dataset    = None
drawer_1_cam_1_device     = None
drawer_1_cam_1_half       = None
drawer_1_cam_1_model      = None
drawer_1_cam_1_classify   = None
drawer_1_cam_1_webcam     = None
drawer_1_cam_1_save_dir   = None
drawer_1_cam_1_names      = None
drawer_1_cam_1_save_txt   = None
drawer_1_cam_1_save_img   = None
drawer_1_cam_1_view_img   = None
drawer_1_cam_1_colors     = None
drawer_1_cam_1_imgsz      = None
drawer_1_cam_1_modelc     = None

drawer_1_cam_2_dataset    = None
drawer_1_cam_2_device     = None
drawer_1_cam_2_half       = None
drawer_1_cam_2_model      = None
drawer_1_cam_2_classify   = None
drawer_1_cam_2_webcam     = None
drawer_1_cam_2_save_dir   = None
drawer_1_cam_2_names      = None
drawer_1_cam_2_save_txt   = None
drawer_1_cam_2_save_img   = None
drawer_1_cam_2_view_img   = None
drawer_1_cam_2_colors     = None
drawer_1_cam_2_imgsz      = None
drawer_1_cam_2_modelc     = None
###################################### DRAWER-1 RETURN VARIABLES END ######################################

###################################### DRAWER-2 RETURN VARIABLES START ######################################
drawer_2_cam_1_dataset    = None
drawer_2_cam_1_device     = None
drawer_2_cam_1_half       = None
drawer_2_cam_1_model      = None
drawer_2_cam_1_classify   = None
drawer_2_cam_1_webcam     = None
drawer_2_cam_1_save_dir   = None
drawer_2_cam_1_names      = None
drawer_2_cam_1_save_txt   = None
drawer_2_cam_1_save_img   = None
drawer_2_cam_1_view_img   = None
drawer_2_cam_1_colors     = None
drawer_2_cam_1_imgsz      = None
drawer_2_cam_1_modelc     = None

drawer_2_cam_2_dataset    = None
drawer_2_cam_2_device     = None
drawer_2_cam_2_half       = None
drawer_2_cam_2_model      = None
drawer_2_cam_2_classify   = None
drawer_2_cam_2_webcam     = None
drawer_2_cam_2_save_dir   = None
drawer_2_cam_2_names      = None
drawer_2_cam_2_save_txt   = None
drawer_2_cam_2_save_img   = None
drawer_2_cam_2_view_img   = None
drawer_2_cam_2_colors     = None
drawer_2_cam_2_imgsz      = None
drawer_2_cam_2_modelc     = None
###################################### DRAWER-2 RETURN VARIABLES END ######################################

###################################### DRAWER-3 RETURN VARIABLES START ######################################
drawer_3_cam_1_dataset    = None
drawer_3_cam_1_device     = None
drawer_3_cam_1_half       = None
drawer_3_cam_1_model      = None
drawer_3_cam_1_classify   = None
drawer_3_cam_1_webcam     = None
drawer_3_cam_1_save_dir   = None
drawer_3_cam_1_names      = None
drawer_3_cam_1_save_txt   = None
drawer_3_cam_1_save_img   = None
drawer_3_cam_1_view_img   = None
drawer_3_cam_1_colors     = None
drawer_3_cam_1_imgsz      = None
drawer_3_cam_1_modelc     = None

drawer_3_cam_2_dataset    = None
drawer_3_cam_2_device     = None
drawer_3_cam_2_half       = None
drawer_3_cam_2_model      = None
drawer_3_cam_2_classify   = None
drawer_3_cam_2_webcam     = None
drawer_3_cam_2_save_dir   = None
drawer_3_cam_2_names      = None
drawer_3_cam_2_save_txt   = None
drawer_3_cam_2_save_img   = None
drawer_3_cam_2_view_img   = None
drawer_3_cam_2_colors     = None
drawer_3_cam_2_imgsz      = None
drawer_3_cam_2_modelc     = None
###################################### DRAWER-3 RETURN VARIABLES END ######################################

###################################### DRAWER-4 RETURN VARIABLES START ######################################
drawer_4_cam_1_dataset    = None
drawer_4_cam_1_device     = None
drawer_4_cam_1_half       = None
drawer_4_cam_1_model      = None
drawer_4_cam_1_classify   = None
drawer_4_cam_1_webcam     = None
drawer_4_cam_1_save_dir   = None
drawer_4_cam_1_names      = None
drawer_4_cam_1_save_txt   = None
drawer_4_cam_1_save_img   = None
drawer_4_cam_1_view_img   = None
drawer_4_cam_1_colors     = None
drawer_4_cam_1_imgsz      = None
drawer_4_cam_1_modelc     = None

drawer_4_cam_2_dataset    = None
drawer_4_cam_2_device     = None
drawer_4_cam_2_half       = None
drawer_4_cam_2_model      = None
drawer_4_cam_2_classify   = None
drawer_4_cam_2_webcam     = None
drawer_4_cam_2_save_dir   = None
drawer_4_cam_2_names      = None
drawer_4_cam_2_save_txt   = None
drawer_4_cam_2_save_img   = None
drawer_4_cam_2_view_img   = None
drawer_4_cam_2_colors     = None
drawer_4_cam_2_imgsz      = None
drawer_4_cam_2_modelc     = None
###################################### DRAWER-4 RETURN VARIABLES END ######################################

###################################### DRAWER-5 RETURN VARIABLES START ######################################
drawer_5_cam_1_dataset    = None
drawer_5_cam_1_device     = None
drawer_5_cam_1_half       = None
drawer_5_cam_1_model      = None
drawer_5_cam_1_classify   = None
drawer_5_cam_1_webcam     = None
drawer_5_cam_1_save_dir   = None
drawer_5_cam_1_names      = None
drawer_5_cam_1_save_txt   = None
drawer_5_cam_1_save_img   = None
drawer_5_cam_1_view_img   = None
drawer_5_cam_1_colors     = None
drawer_5_cam_1_imgsz      = None
drawer_5_cam_1_modelc     = None

drawer_5_cam_2_dataset    = None
drawer_5_cam_2_device     = None
drawer_5_cam_2_half       = None
drawer_5_cam_2_model      = None
drawer_5_cam_2_classify   = None
drawer_5_cam_2_webcam     = None
drawer_5_cam_2_save_dir   = None
drawer_5_cam_2_names      = None
drawer_5_cam_2_save_txt   = None
drawer_5_cam_2_save_img   = None
drawer_5_cam_2_view_img   = None
drawer_5_cam_2_colors     = None
drawer_5_cam_2_imgsz      = None
drawer_5_cam_2_modelc     = None
###################################### DRAWER-5 RETURN VARIABLES END ######################################

###################################### DRAWER-6 RETURN VARIABLES START ######################################
drawer_6_cam_1_dataset    = None
drawer_6_cam_1_device     = None
drawer_6_cam_1_half       = None
drawer_6_cam_1_model      = None
drawer_6_cam_1_classify   = None
drawer_6_cam_1_webcam     = None
drawer_6_cam_1_save_dir   = None
drawer_6_cam_1_names      = None
drawer_6_cam_1_save_txt   = None
drawer_6_cam_1_save_img   = None
drawer_6_cam_1_view_img   = None
drawer_6_cam_1_colors     = None
drawer_6_cam_1_imgsz      = None
drawer_6_cam_1_modelc     = None

drawer_6_cam_2_dataset    = None
drawer_6_cam_2_device     = None
drawer_6_cam_2_half       = None
drawer_6_cam_2_model      = None
drawer_6_cam_2_classify   = None
drawer_6_cam_2_webcam     = None
drawer_6_cam_2_save_dir   = None
drawer_6_cam_2_names      = None
drawer_6_cam_2_save_txt   = None
drawer_6_cam_2_save_img   = None
drawer_6_cam_2_view_img   = None
drawer_6_cam_2_colors     = None
drawer_6_cam_2_imgsz      = None
drawer_6_cam_2_modelc     = None
###################################### DRAWER-6 RETURN VARIABLES END ######################################

threadLock = threading.Lock()

threadList = ["Drawer-1", "Drawer-2", "Drawer-3", "Drawer-4", "Drawer-5", "Drawer-6"]
threads = []
threadID = 1



def drawer_flag_opener(opened_drawer_list):
    global drawer_1_flag
    global drawer_2_flag
    global drawer_3_flag
    global drawer_4_flag
    global drawer_5_flag
    global drawer_6_flag

    for opened_drawer in opened_drawer_list:
        if opened_drawer == 1:
            threadLock.acquire()
            drawer_1_flag = True
            threadLock.release()
        elif opened_drawer == 2:
            threadLock.acquire()
            drawer_2_flag = True
            threadLock.release()
        elif opened_drawer == 3:
            threadLock.acquire()
            drawer_3_flag = True
            threadLock.release()
        elif opened_drawer == 4:
            threadLock.acquire()
            drawer_4_flag = True
            threadLock.release()
        elif opened_drawer == 5:
            threadLock.acquire()
            drawer_5_flag = True
            threadLock.release()
        elif opened_drawer == 6:
            threadLock.acquire()
            drawer_6_flag = True
            threadLock.release()
        else:
            print("!!!Cekmece listesinde hatalı bir veri tespit edildi!!!")


def detect_pre(source, weights, save_img=False):
    view_img, save_txt, imgsz, trace = opt.view_img, opt.save_txt, opt.img_size, not opt.no_trace
    save_img = not opt.nosave and not source.endswith('.txt')  # save inference images
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))

    # Directories
    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    set_logging()
    device = select_device(opt.device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size

    if trace:
        model = TracedModel(model, device, opt.img_size)

    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]

    if classify:
        return dataset, device, half, model, classify, webcam, save_dir, names, save_txt, save_img, view_img, colors, imgsz, modelc
    return dataset, device, half, model, classify, webcam, save_dir, names, save_txt, save_img, view_img, colors, imgsz, None


def detect_post(dataset, device, half, model, classify, webcam,
                save_dir, names, save_txt, save_img, view_img, colors, imgsz, modelc=None, conf_thres=0.70):
    # Run inference
    if device.type != 'cpu':
        model(zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img = from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Warmup
        if device.type != 'cpu' and (
                old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]
            for i in range(3):
                model(img, augment=opt.augment)[0]

        # Inference
        t1 = time_synchronized()
        with no_grad():  # Calculating gradients would cause a GPU memory leak
            pred = model(img, augment=opt.augment)[0]
        t2 = time_synchronized()

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
        t3 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # img.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
            gn = tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if opt.save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or view_img:  # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)

            # Print time (inference + NMS)
            print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')

            # Stream results
            if view_img:
                imshow(str(p), im0)
                waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    imwrite(save_path, im0)
                    print(f" The image with the result is saved in: {save_path}")
                else:  # 'video' or 'stream'
                    if vid_path != save_path:  # new video
                        vid_path = save_path
                        if isinstance(vid_writer, VideoWriter):
                            vid_writer.release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(CAP_PROP_FPS)
                            w = int(vid_cap.get(CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                            save_path += '.mp4'
                        vid_writer = VideoWriter(save_path, VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer.write(im0)

    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        # print(f"Results saved to {save_dir}{s}")

    print(f'Done. ({time.time() - t0:.3f}s)')


def detect_drawer_1():
    global drawer_1_flag
    global drawer_1_executed_first_one

    global drawer_1_cam_1_dataset
    global drawer_1_cam_1_device
    global drawer_1_cam_1_half
    global drawer_1_cam_1_model
    global drawer_1_cam_1_classify
    global drawer_1_cam_1_webcam
    global drawer_1_cam_1_save_dir
    global drawer_1_cam_1_names
    global drawer_1_cam_1_save_txt
    global drawer_1_cam_1_save_img
    global drawer_1_cam_1_view_img
    global drawer_1_cam_1_colors
    global drawer_1_cam_1_imgsz
    global drawer_1_cam_1_modelc

    global drawer_1_cam_2_dataset
    global drawer_1_cam_2_device
    global drawer_1_cam_2_half
    global drawer_1_cam_2_model
    global drawer_1_cam_2_classify
    global drawer_1_cam_2_webcam
    global drawer_1_cam_2_save_dir
    global drawer_1_cam_2_names
    global drawer_1_cam_2_save_txt
    global drawer_1_cam_2_save_img
    global drawer_1_cam_2_view_img
    global drawer_1_cam_2_colors
    global drawer_1_cam_2_imgsz
    global drawer_1_cam_2_modelc

    if drawer_1_executed_first_one == False:

        (
            drawer_1_cam_1_dataset,
            drawer_1_cam_1_device,
            drawer_1_cam_1_half,
            drawer_1_cam_1_model,
            drawer_1_cam_1_classify,
            drawer_1_cam_1_webcam,
            drawer_1_cam_1_save_dir,
            drawer_1_cam_1_names,
            drawer_1_cam_1_save_txt,
            drawer_1_cam_1_save_img,
            drawer_1_cam_1_view_img,
            drawer_1_cam_1_colors,
            drawer_1_cam_1_imgsz,
            drawer_1_cam_1_modelc,
            ) = detect_pre(source='photos/cekmece1/camera1/1', weights="pt_files/best-cekmece1-camera1.pt")

        (
            drawer_1_cam_2_dataset,
            drawer_1_cam_2_device,
            drawer_1_cam_2_half,
            drawer_1_cam_2_model,
            drawer_1_cam_2_classify,
            drawer_1_cam_2_webcam,
            drawer_1_cam_2_save_dir,
            drawer_1_cam_2_names,
            drawer_1_cam_2_save_txt,
            drawer_1_cam_2_save_img,
            drawer_1_cam_2_view_img,
            drawer_1_cam_2_colors,
            drawer_1_cam_2_imgsz,
            drawer_1_cam_2_modelc,
            ) = detect_pre(source='photos/cekmece1/camera2/1', weights="pt_files/best-cekmece1-camera2.pt")
        threadLock.acquire()
        drawer_1_executed_first_one = True
        threadLock.release()
    else:
        while True:
            time.sleep(0.001)
            
            if drawer_1_flag:
                t_strt = time.time()
                detect_post(
                    drawer_1_cam_1_dataset,
                    drawer_1_cam_1_device,
                    drawer_1_cam_1_half,
                    drawer_1_cam_1_model,
                    drawer_1_cam_1_classify,
                    drawer_1_cam_1_webcam,
                    drawer_1_cam_1_save_dir,
                    drawer_1_cam_1_names,
                    drawer_1_cam_1_save_txt,
                    drawer_1_cam_1_save_img,
                    drawer_1_cam_1_view_img,
                    drawer_1_cam_1_colors,
                    drawer_1_cam_1_imgsz,
                    drawer_1_cam_1_modelc,
                    )
                detect_post(
                    drawer_1_cam_2_dataset,
                    drawer_1_cam_2_device,
                    drawer_1_cam_2_half,
                    drawer_1_cam_2_model,
                    drawer_1_cam_2_classify,
                    drawer_1_cam_2_webcam,
                    drawer_1_cam_2_save_dir,
                    drawer_1_cam_2_names,
                    drawer_1_cam_2_save_txt,
                    drawer_1_cam_2_save_img,
                    drawer_1_cam_2_view_img,
                    drawer_1_cam_2_colors,
                    drawer_1_cam_2_imgsz,
                    drawer_1_cam_1_modelc,
                    )
                path = 'cekmece1'
                print ('Cekmece 1 executed with: ' + path)
                threadLock.acquire()
                drawer_1_flag = False
                with open("detectionFinishCheck.txt", "r") as dosya:
                    newFile = dosya.readlines()
                    newFile[0] = "1\n"
                with open("detectionFinishCheck.txt", "w") as dosya:
                    dosya.writelines(newFile)
                threadLock.release()
                print ('thread finish in: ' + str(time.time() - t_strt))
            if exitFlag == True:
                break


def detect_drawer_2():
    global drawer_2_flag
    global drawer_2_executed_first_one

    global drawer_2_cam_1_dataset
    global drawer_2_cam_1_device
    global drawer_2_cam_1_half
    global drawer_2_cam_1_model
    global drawer_2_cam_1_classify
    global drawer_2_cam_1_webcam
    global drawer_2_cam_1_save_dir
    global drawer_2_cam_1_names
    global drawer_2_cam_1_save_txt
    global drawer_2_cam_1_save_img
    global drawer_2_cam_1_view_img
    global drawer_2_cam_1_colors
    global drawer_2_cam_1_imgsz
    global drawer_2_cam_1_modelc

    global drawer_2_cam_2_dataset
    global drawer_2_cam_2_device
    global drawer_2_cam_2_half
    global drawer_2_cam_2_model
    global drawer_2_cam_2_classify
    global drawer_2_cam_2_webcam
    global drawer_2_cam_2_save_dir
    global drawer_2_cam_2_names
    global drawer_2_cam_2_save_txt
    global drawer_2_cam_2_save_img
    global drawer_2_cam_2_view_img
    global drawer_2_cam_2_colors
    global drawer_2_cam_2_imgsz
    global drawer_2_cam_2_modelc

    if drawer_2_executed_first_one == False:

        (
            drawer_2_cam_1_dataset,
            drawer_2_cam_1_device,
            drawer_2_cam_1_half,
            drawer_2_cam_1_model,
            drawer_2_cam_1_classify,
            drawer_2_cam_1_webcam,
            drawer_2_cam_1_save_dir,
            drawer_2_cam_1_names,
            drawer_2_cam_1_save_txt,
            drawer_2_cam_1_save_img,
            drawer_2_cam_1_view_img,
            drawer_2_cam_1_colors,
            drawer_2_cam_1_imgsz,
            drawer_2_cam_1_modelc,
            ) = detect_pre(source='photos/cekmece2/camera1/1', weights="pt_files/best-cekmece2-camera1-3.pt")

        (
            drawer_2_cam_2_dataset,
            drawer_2_cam_2_device,
            drawer_2_cam_2_half,
            drawer_2_cam_2_model,
            drawer_2_cam_2_classify,
            drawer_2_cam_2_webcam,
            drawer_2_cam_2_save_dir,
            drawer_2_cam_2_names,
            drawer_2_cam_2_save_txt,
            drawer_2_cam_2_save_img,
            drawer_2_cam_2_view_img,
            drawer_2_cam_2_colors,
            drawer_2_cam_2_imgsz,
            drawer_2_cam_2_modelc,
            ) = detect_pre(source='photos/cekmece2/camera2/1', weights="pt_files/best-cekmece2-camera2-3.pt")
        threadLock.acquire()
        drawer_2_executed_first_one = True
        threadLock.release()
    else:
        while True:
            time.sleep(0.001)
            
            if drawer_2_flag:
                t_strt = time.time()
                detect_post(
                    drawer_2_cam_1_dataset,
                    drawer_2_cam_1_device,
                    drawer_2_cam_1_half,
                    drawer_2_cam_1_model,
                    drawer_2_cam_1_classify,
                    drawer_2_cam_1_webcam,
                    drawer_2_cam_1_save_dir,
                    drawer_2_cam_1_names,
                    drawer_2_cam_1_save_txt,
                    drawer_2_cam_1_save_img,
                    drawer_2_cam_1_view_img,
                    drawer_2_cam_1_colors,
                    drawer_2_cam_1_imgsz,
                    drawer_2_cam_1_modelc,
                    )
                detect_post(
                    drawer_2_cam_2_dataset,
                    drawer_2_cam_2_device,
                    drawer_2_cam_2_half,
                    drawer_2_cam_2_model,
                    drawer_2_cam_2_classify,
                    drawer_2_cam_2_webcam,
                    drawer_2_cam_2_save_dir,
                    drawer_2_cam_2_names,
                    drawer_2_cam_2_save_txt,
                    drawer_2_cam_2_save_img,
                    drawer_2_cam_2_view_img,
                    drawer_2_cam_2_colors,
                    drawer_2_cam_2_imgsz,
                    drawer_2_cam_1_modelc,
                    )
                path = 'cekmece2'
                print ('Cekmece 2 executed with: ' + path)
                threadLock.acquire()
                drawer_2_flag = False
                with open("detectionFinishCheck.txt", "r") as dosya:
                    newFile = dosya.readlines()
                    newFile[1] = "1\n"
                with open("detectionFinishCheck.txt", "w") as dosya:
                    dosya.writelines(newFile)
                threadLock.release()
                print ('thread finish in: ' + str(time.time() - t_strt))
            if exitFlag == True:
                break


def detect_drawer_3():    
    global drawer_3_flag
    global drawer_3_executed_first_one

    global drawer_3_cam_1_dataset
    global drawer_3_cam_1_device
    global drawer_3_cam_1_half
    global drawer_3_cam_1_model
    global drawer_3_cam_1_classify
    global drawer_3_cam_1_webcam
    global drawer_3_cam_1_save_dir
    global drawer_3_cam_1_names
    global drawer_3_cam_1_save_txt
    global drawer_3_cam_1_save_img
    global drawer_3_cam_1_view_img
    global drawer_3_cam_1_colors
    global drawer_3_cam_1_imgsz
    global drawer_3_cam_1_modelc

    global drawer_3_cam_2_dataset
    global drawer_3_cam_2_device
    global drawer_3_cam_2_half
    global drawer_3_cam_2_model
    global drawer_3_cam_2_classify
    global drawer_3_cam_2_webcam
    global drawer_3_cam_2_save_dir
    global drawer_3_cam_2_names
    global drawer_3_cam_2_save_txt
    global drawer_3_cam_2_save_img
    global drawer_3_cam_2_view_img
    global drawer_3_cam_2_colors
    global drawer_3_cam_2_imgsz
    global drawer_3_cam_2_modelc

    if drawer_3_executed_first_one == False:

        (
            drawer_3_cam_1_dataset,
            drawer_3_cam_1_device,
            drawer_3_cam_1_half,
            drawer_3_cam_1_model,
            drawer_3_cam_1_classify,
            drawer_3_cam_1_webcam,
            drawer_3_cam_1_save_dir,
            drawer_3_cam_1_names,
            drawer_3_cam_1_save_txt,
            drawer_3_cam_1_save_img,
            drawer_3_cam_1_view_img,
            drawer_3_cam_1_colors,
            drawer_3_cam_1_imgsz,
            drawer_3_cam_1_modelc,
            ) = detect_pre(source='photos/cekmece3/camera1/1', weights="pt_files/best-cekmece3-camera1.pt")

        (
            drawer_3_cam_2_dataset,
            drawer_3_cam_2_device,
            drawer_3_cam_2_half,
            drawer_3_cam_2_model,
            drawer_3_cam_2_classify,
            drawer_3_cam_2_webcam,
            drawer_3_cam_2_save_dir,
            drawer_3_cam_2_names,
            drawer_3_cam_2_save_txt,
            drawer_3_cam_2_save_img,
            drawer_3_cam_2_view_img,
            drawer_3_cam_2_colors,
            drawer_3_cam_2_imgsz,
            drawer_3_cam_2_modelc,
            ) = detect_pre(source='photos/cekmece3/camera2/1', weights="pt_files/best-cekmece3-camera2-2.pt")
        threadLock.acquire()
        drawer_3_executed_first_one = True
        threadLock.release()
    else:
        while True:
            
            time.sleep(0.001)
            if drawer_3_flag:
                t_strt = time.time()
                detect_post(
                    drawer_3_cam_1_dataset,
                    drawer_3_cam_1_device,
                    drawer_3_cam_1_half,
                    drawer_3_cam_1_model,
                    drawer_3_cam_1_classify,
                    drawer_3_cam_1_webcam,
                    drawer_3_cam_1_save_dir,
                    drawer_3_cam_1_names,
                    drawer_3_cam_1_save_txt,
                    drawer_3_cam_1_save_img,
                    drawer_3_cam_1_view_img,
                    drawer_3_cam_1_colors,
                    drawer_3_cam_1_imgsz,
                    drawer_3_cam_1_modelc,
                    )
                detect_post(
                    drawer_3_cam_2_dataset,
                    drawer_3_cam_2_device,
                    drawer_3_cam_2_half,
                    drawer_3_cam_2_model,
                    drawer_3_cam_2_classify,
                    drawer_3_cam_2_webcam,
                    drawer_3_cam_2_save_dir,
                    drawer_3_cam_2_names,
                    drawer_3_cam_2_save_txt,
                    drawer_3_cam_2_save_img,
                    drawer_3_cam_2_view_img,
                    drawer_3_cam_2_colors,
                    drawer_3_cam_2_imgsz,
                    drawer_3_cam_1_modelc,
                    )
                path = 'cekmece3'
                print ('Cekmece 3 executed with: ' + path)
                threadLock.acquire()
                drawer_3_flag = False
                with open("detectionFinishCheck.txt", "r") as dosya:
                    newFile = dosya.readlines()
                    newFile[2] = "1\n"
                with open("detectionFinishCheck.txt", "w") as dosya:
                    dosya.writelines(newFile)
                threadLock.release()
                print ('thread finish in: ' + str(time.time() - t_strt))
            if exitFlag == True:
                break


def detect_drawer_4():
    global drawer_4_flag
    global drawer_4_executed_first_one

    global drawer_4_cam_1_dataset
    global drawer_4_cam_1_device
    global drawer_4_cam_1_half
    global drawer_4_cam_1_model
    global drawer_4_cam_1_classify
    global drawer_4_cam_1_webcam
    global drawer_4_cam_1_save_dir
    global drawer_4_cam_1_names
    global drawer_4_cam_1_save_txt
    global drawer_4_cam_1_save_img
    global drawer_4_cam_1_view_img
    global drawer_4_cam_1_colors
    global drawer_4_cam_1_imgsz
    global drawer_4_cam_1_modelc

    global drawer_4_cam_2_dataset
    global drawer_4_cam_2_device
    global drawer_4_cam_2_half
    global drawer_4_cam_2_model
    global drawer_4_cam_2_classify
    global drawer_4_cam_2_webcam
    global drawer_4_cam_2_save_dir
    global drawer_4_cam_2_names
    global drawer_4_cam_2_save_txt
    global drawer_4_cam_2_save_img
    global drawer_4_cam_2_view_img
    global drawer_4_cam_2_colors
    global drawer_4_cam_2_imgsz
    global drawer_4_cam_2_modelc

    if drawer_4_executed_first_one == False:

        # (
        #     drawer_4_cam_1_dataset,
        #     drawer_4_cam_1_device,
        #     drawer_4_cam_1_half,
        #     drawer_4_cam_1_model,
        #     drawer_4_cam_1_classify,
        #     drawer_4_cam_1_webcam,
        #     drawer_4_cam_1_save_dir,
        #     drawer_4_cam_1_names,
        #     drawer_4_cam_1_save_txt,
        #     drawer_4_cam_1_save_img,
        #     drawer_4_cam_1_view_img,
        #     drawer_4_cam_1_colors,
        #     drawer_4_cam_1_imgsz,
        #     drawer_4_cam_1_modelc,
        #     ) = detect_pre(source='photos/cekmece2/camera1/1', weights="pt_files/best-cekmece2-camera1.pt")

        (
            drawer_4_cam_2_dataset,
            drawer_4_cam_2_device,
            drawer_4_cam_2_half,
            drawer_4_cam_2_model,
            drawer_4_cam_2_classify,
            drawer_4_cam_2_webcam,
            drawer_4_cam_2_save_dir,
            drawer_4_cam_2_names,
            drawer_4_cam_2_save_txt,
            drawer_4_cam_2_save_img,
            drawer_4_cam_2_view_img,
            drawer_4_cam_2_colors,
            drawer_4_cam_2_imgsz,
            drawer_4_cam_2_modelc,
            ) = detect_pre(source='photos/cekmece4/camera2/1', weights="pt_files/best-cekmece4-camera2.pt")
        threadLock.acquire()
        drawer_4_executed_first_one = True
        threadLock.release()
    else:
        while True:
            
            time.sleep(0.001)
            if drawer_4_flag:
                t_strt = time.time()
                # detect_post(
                #     drawer_4_cam_1_dataset,
                #     drawer_4_cam_1_device,
                #     drawer_4_cam_1_half,
                #     drawer_4_cam_1_model,
                #     drawer_4_cam_1_classify,
                #     drawer_4_cam_1_webcam,
                #     drawer_4_cam_1_save_dir,
                #     drawer_4_cam_1_names,
                #     drawer_4_cam_1_save_txt,
                #     drawer_4_cam_1_save_img,
                #     drawer_4_cam_1_view_img,
                #     drawer_4_cam_1_colors,
                #     drawer_4_cam_1_imgsz,
                #     drawer_4_cam_1_modelc,
                #     )
                detect_post(
                    drawer_4_cam_2_dataset,
                    drawer_4_cam_2_device,
                    drawer_4_cam_2_half,
                    drawer_4_cam_2_model,
                    drawer_4_cam_2_classify,
                    drawer_4_cam_2_webcam,
                    drawer_4_cam_2_save_dir,
                    drawer_4_cam_2_names,
                    drawer_4_cam_2_save_txt,
                    drawer_4_cam_2_save_img,
                    drawer_4_cam_2_view_img,
                    drawer_4_cam_2_colors,
                    drawer_4_cam_2_imgsz,
                    drawer_4_cam_1_modelc,
                    )
                path = 'cekmece4'
                print ('Cekmece 4 executed with: ' + path)
                threadLock.acquire()
                drawer_4_flag = False
                with open("detectionFinishCheck.txt", "r") as dosya:
                    newFile = dosya.readlines()
                    newFile[3] = "1\n"
                with open("detectionFinishCheck.txt", "w") as dosya:
                    dosya.writelines(newFile)
                threadLock.release()
                print ('thread finish in: ' + str(time.time() - t_strt))
            if exitFlag == True:
                break


def detect_drawer_5():    
    global drawer_5_flag
    global drawer_5_executed_first_one

    global drawer_5_cam_1_dataset
    global drawer_5_cam_1_device
    global drawer_5_cam_1_half
    global drawer_5_cam_1_model
    global drawer_5_cam_1_classify
    global drawer_5_cam_1_webcam
    global drawer_5_cam_1_save_dir
    global drawer_5_cam_1_names
    global drawer_5_cam_1_save_txt
    global drawer_5_cam_1_save_img
    global drawer_5_cam_1_view_img
    global drawer_5_cam_1_colors
    global drawer_5_cam_1_imgsz
    global drawer_5_cam_1_modelc

    global drawer_5_cam_2_dataset
    global drawer_5_cam_2_device
    global drawer_5_cam_2_half
    global drawer_5_cam_2_model
    global drawer_5_cam_2_classify
    global drawer_5_cam_2_webcam
    global drawer_5_cam_2_save_dir
    global drawer_5_cam_2_names
    global drawer_5_cam_2_save_txt
    global drawer_5_cam_2_save_img
    global drawer_5_cam_2_view_img
    global drawer_5_cam_2_colors
    global drawer_5_cam_2_imgsz
    global drawer_5_cam_2_modelc

    if drawer_5_executed_first_one == False:

        #(
            # drawer_5_cam_1_dataset,
            # drawer_5_cam_1_device,
            # drawer_5_cam_1_half,
            # drawer_5_cam_1_model,
            # drawer_5_cam_1_classify,
            # drawer_5_cam_1_webcam,
            # drawer_5_cam_1_save_dir,
            # drawer_5_cam_1_names,
            # drawer_5_cam_1_save_txt,
            # drawer_5_cam_1_save_img,
            # drawer_5_cam_1_view_img,
            # drawer_5_cam_1_colors,
            # drawer_5_cam_1_imgsz,
            # drawer_5_cam_1_modelc,
            # ) = detect_pre(source='photos/cekmece5/camera1/1', weights="pt_files/best-cekmece5-camera1.pt")

        (
            drawer_5_cam_2_dataset,
            drawer_5_cam_2_device,
            drawer_5_cam_2_half,
            drawer_5_cam_2_model,
            drawer_5_cam_2_classify,
            drawer_5_cam_2_webcam,
            drawer_5_cam_2_save_dir,
            drawer_5_cam_2_names,
            drawer_5_cam_2_save_txt,
            drawer_5_cam_2_save_img,
            drawer_5_cam_2_view_img,
            drawer_5_cam_2_colors,
            drawer_5_cam_2_imgsz,
            drawer_5_cam_2_modelc,
            ) = detect_pre(source='photos/cekmece5/camera2/1', weights="pt_files/best-cekmece5-camera2.pt")
        threadLock.acquire()
        drawer_5_executed_first_one = True
        threadLock.release()
    else:
        while True:
            
            time.sleep(0.001)
            if drawer_5_flag:
                t_strt = time.time()
                # detect_post(
                #     drawer_5_cam_1_dataset,
                #     drawer_5_cam_1_device,
                #     drawer_5_cam_1_half,
                #     drawer_5_cam_1_model,
                #     drawer_5_cam_1_classify,
                #     drawer_5_cam_1_webcam,
                #     drawer_5_cam_1_save_dir,
                #     drawer_5_cam_1_names,
                #     drawer_5_cam_1_save_txt,
                #     drawer_5_cam_1_save_img,
                #     drawer_5_cam_1_view_img,
                #     drawer_5_cam_1_colors,
                #     drawer_5_cam_1_imgsz,
                #     drawer_5_cam_1_modelc,
                #     )
                detect_post(
                    drawer_5_cam_2_dataset,
                    drawer_5_cam_2_device,
                    drawer_5_cam_2_half,
                    drawer_5_cam_2_model,
                    drawer_5_cam_2_classify,
                    drawer_5_cam_2_webcam,
                    drawer_5_cam_2_save_dir,
                    drawer_5_cam_2_names,
                    drawer_5_cam_2_save_txt,
                    drawer_5_cam_2_save_img,
                    drawer_5_cam_2_view_img,
                    drawer_5_cam_2_colors,
                    drawer_5_cam_2_imgsz,
                    drawer_5_cam_1_modelc,
                    conf_thres=0.80
                    )
                path = 'cekmece5'
                print ('Cekmece 5 executed with: ' + path)
                threadLock.acquire()
                drawer_5_flag = False
                with open("detectionFinishCheck.txt", "r") as dosya:
                    newFile = dosya.readlines()
                    newFile[4] = "1\n"
                with open("detectionFinishCheck.txt", "w") as dosya:
                    dosya.writelines(newFile)
                threadLock.release()
                print ('thread finish in: ' + str(time.time() - t_strt))
            if exitFlag == True:
                break


def detect_drawer_6():    
    global drawer_6_flag
    global drawer_6_executed_first_one

    global drawer_6_cam_1_dataset
    global drawer_6_cam_1_device
    global drawer_6_cam_1_half
    global drawer_6_cam_1_model
    global drawer_6_cam_1_classify
    global drawer_6_cam_1_webcam
    global drawer_6_cam_1_save_dir
    global drawer_6_cam_1_names
    global drawer_6_cam_1_save_txt
    global drawer_6_cam_1_save_img
    global drawer_6_cam_1_view_img
    global drawer_6_cam_1_colors
    global drawer_6_cam_1_imgsz
    global drawer_6_cam_1_modelc

    global drawer_6_cam_2_dataset
    global drawer_6_cam_2_device
    global drawer_6_cam_2_half
    global drawer_6_cam_2_model
    global drawer_6_cam_2_classify
    global drawer_6_cam_2_webcam
    global drawer_6_cam_2_save_dir
    global drawer_6_cam_2_names
    global drawer_6_cam_2_save_txt
    global drawer_6_cam_2_save_img
    global drawer_6_cam_2_view_img
    global drawer_6_cam_2_colors
    global drawer_6_cam_2_imgsz
    global drawer_6_cam_2_modelc

    if drawer_6_executed_first_one == False:

        # (
        #     drawer_6_cam_1_dataset,
        #     drawer_6_cam_1_device,
        #     drawer_6_cam_1_half,
        #     drawer_6_cam_1_model,
        #     drawer_6_cam_1_classify,
        #     drawer_6_cam_1_webcam,
        #     drawer_6_cam_1_save_dir,
        #     drawer_6_cam_1_names,
        #     drawer_6_cam_1_save_txt,
        #     drawer_6_cam_1_save_img,
        #     drawer_6_cam_1_view_img,
        #     drawer_6_cam_1_colors,
        #     drawer_6_cam_1_imgsz,
        #     drawer_6_cam_1_modelc,
        #     ) = detect_pre(source='photos/cekmece2/camera1/1', weights="pt_files/best-cekmece2-camera1.pt")

        (
            drawer_6_cam_2_dataset,
            drawer_6_cam_2_device,
            drawer_6_cam_2_half,
            drawer_6_cam_2_model,
            drawer_6_cam_2_classify,
            drawer_6_cam_2_webcam,
            drawer_6_cam_2_save_dir,
            drawer_6_cam_2_names,
            drawer_6_cam_2_save_txt,
            drawer_6_cam_2_save_img,
            drawer_6_cam_2_view_img,
            drawer_6_cam_2_colors,
            drawer_6_cam_2_imgsz,
            drawer_6_cam_2_modelc,
            ) = detect_pre(source='photos/cekmece6/camera2/1', weights="pt_files/best-cekmece6-camera2-2.pt")
        threadLock.acquire()
        drawer_6_executed_first_one = True
        threadLock.release()
    else:
        while True:
            
            time.sleep(0.001)
            if drawer_6_flag:
                t_strt = time.time()
                # detect_post(
                #     drawer_6_cam_1_dataset,
                #     drawer_6_cam_1_device,
                #     drawer_6_cam_1_half,
                #     drawer_6_cam_1_model,
                #     drawer_6_cam_1_classify,
                #     drawer_6_cam_1_webcam,
                #     drawer_6_cam_1_save_dir,
                #     drawer_6_cam_1_names,
                #     drawer_6_cam_1_save_txt,
                #     drawer_6_cam_1_save_img,
                #     drawer_6_cam_1_view_img,
                #     drawer_6_cam_1_colors,
                #     drawer_6_cam_1_imgsz,
                #     drawer_6_cam_1_modelc,
                #     )
                detect_post(
                    drawer_6_cam_2_dataset,
                    drawer_6_cam_2_device,
                    drawer_6_cam_2_half,
                    drawer_6_cam_2_model,
                    drawer_6_cam_2_classify,
                    drawer_6_cam_2_webcam,
                    drawer_6_cam_2_save_dir,
                    drawer_6_cam_2_names,
                    drawer_6_cam_2_save_txt,
                    drawer_6_cam_2_save_img,
                    drawer_6_cam_2_view_img,
                    drawer_6_cam_2_colors,
                    drawer_6_cam_2_imgsz,
                    drawer_6_cam_1_modelc,
                    )
                path = 'cekmece6'
                print ('Cekmece 6 executed with: ' + path)
                threadLock.acquire()
                drawer_6_flag = False
                with open("detectionFinishCheck.txt", "r") as dosya:
                    newFile = dosya.readlines()
                    newFile[5] = "1\n"
                with open("detectionFinishCheck.txt", "w") as dosya:
                    dosya.writelines(newFile)
                threadLock.release()
                print ('thread finish in: ' + str(time.time() - t_strt))
            if exitFlag == True:
                break
            

class ThreadBuilder(threading.Thread):
    def __init__(self, thread_id: int, name: str, drawer_count: int):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.drawer_count = drawer_count

    def run(self) -> None:
        print("Starting " + self.name)
        run_process(self)
        print("Exiting " + self.name)


def run_process(self: ThreadBuilder):
    if self.drawer_count == 1:
        detect_drawer_1()
    elif self.drawer_count == 2:
        detect_drawer_2()
    elif self.drawer_count == 3:
        detect_drawer_3()
    elif self.drawer_count == 4:
        detect_drawer_4()
    elif self.drawer_count == 5:
        detect_drawer_5()
    elif self.drawer_count == 6:
        detect_drawer_6()
    else:
        print("Hata!!!")


def changeDrawerList(list):
    global openedDrawersList
    openedDrawersList = list
    drawer_flag_opener(openedDrawersList)
    print(openedDrawersList)
    print("CHANGE DRAWER LIST")


def runMain():
    global opt
    parser = argparse.ArgumentParser()
    #parser.add_argument('--weights', nargs='+', type=str, default='yolov7.pt', help='model.pt path(s)')
    #parser.add_argument('--source', type=str, default='inference/images', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.70, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--no-trace', action='store_true', help='don`t trace model')
    opt = parser.parse_args()
    opt.source = "photos/cekmece2/camera1/1"
    opt.weights = "pt_files/best-cekmece2-camera1-v2.pt"
    opt.save_txt = True
    # opt.img_size = 640
    # opt.conf_thres = 0.25
    # opt.iou_thres = 0.45
    # opt.device = ''
    # opt.view_img = False
    # opt.save_txt = False
    # opt.save_conf = False
    # opt.nosave = False
    # opt.classes:int = None
    # opt.agnostic_nms = False
    # opt.augment = False
    # opt.update = False
    # opt.project = 'runs/detect'
    # opt.name = 'exp'
    # opt.exist_ok = False
    # opt.no_trace = False

    global threadID
    global threads
    global threadList
    global exitFlag
    global openedDrawersList

    for tName in threadList:
        thread = ThreadBuilder(threadID, tName, threadID)
        thread.start()
        threadID += 1
        thread.join()
        
    threadID = 1

    for tName in threadList:
        thread = ThreadBuilder(threadID, tName, threadID)
        thread.start()
        threads.append(thread)
        threadID += 1

    """
    exitFlag = True     

    for t in threads:
        t.join()
    print("Exiting Main Thread")
    """

