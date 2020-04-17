import cv2
import os
import numpy as np
import argparse
import re
import sys
import time
from corner import search_exact_corner
from pathlib import Path

def shape_section(img, rect_shape):
    return img[rect_shape[0][1]:rect_shape[1][1], rect_shape[0][0]:rect_shape[1][0]] 

def get_rect_shape(rect, channel=3):
    return rect[1][1] - rect[0][1], rect[1][0] - rect[0][0], channel

def project_into_img(point, shape, pad=0):
    return (
        np.clip(point[0] - pad, 0, shape[1]),
        np.clip(point[1] - pad, 0, shape[0])
        )

def clear_shell():
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

def get_manual_rect(img=None, pad=30, **options):
    coordinates = None
    while True:
        value = input('Enter the coordinates exactly like that "(x1, y1), (x2, y2)" (type "cancel" to exit):\n')
        if value.lower() == 'cancel':
            break
        values = re.findall(r'(\d+)', value)
        if len(values) != 4:
            print('You have to insert exactly 4 coordinates')
            continue
        coordinates = ((int(values[0]), int(values[1])), (int(values[2]), int(values[3])))
        if not img is None:
            rect_img = img.copy()
            cv2.rectangle(rect_img, coordinates[0], coordinates[1], (0, 255, 0), 2)
            rect_img = cv2.copyMakeBorder(rect_img,pad,pad,pad,pad,cv2.BORDER_CONSTANT,value=(0,0,0))
            print('You can check the selection in the open window')
            imshow(rect_img, 'Coordinates')
        
        finish = input('Found this coordinates {} do you want to continue [y/n]?'.format(coordinates))
        if finish.lower().startswith('y'):
            if not img is None:
                cv2.destroyAllWindows()
            break
        else:
            continue
    return coordinates

mouse_coordinates = None
def store_coordinates(event, x, y, flags, param):
    global mouse_coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_coordinates = (x, y)
        cv2.destroyAllWindows()

def imshow(img, name='', sizeW=1280, sizeH=720, wait=0, mouseCallback=None, windowFlag=cv2.WINDOW_NORMAL):
    cv2.namedWindow(name, windowFlag)
    cv2.resizeWindow(name, sizeW, sizeH)
    if not mouseCallback is None:
        cv2.setMouseCallback(name, mouseCallback)
    cv2.imshow(name, img)
    cv2.waitKey(wait)

def get_visual_rect(img=None, pad=30, search=True, searchRadius=5, **options):
    if img is None:
        print('There is an error during the visualzation of the image, please use the -m option in order to insert the coordinates manually')
        return None

    global mouse_coordinates
    pad_img = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(0,0,0))

    while True:
        print('In the image please select with the mouse the top-left corner of the rectangle')

        mouse_coordinates = None
        imshow(pad_img, 'Coordinates', mouseCallback=store_coordinates)

        raw_point1 = mouse_coordinates
        if search:
            raw_point1 = search_exact_corner(pad_img, raw_point1, searchRadius)
            raw_point1 = (raw_point1[0] - 1, raw_point1[1] - 1)

        point1 = project_into_img(raw_point1, img.shape, pad)
        
        print('Found point {}'.format(point1))
        print('Now please select the bottom-right corner of the rectangle')

        mouse_coordinates = None
        imshow(pad_img, 'Coordinates', mouseCallback=store_coordinates)
        
        raw_point2 = mouse_coordinates
        if search:
            raw_point2 = search_exact_corner(pad_img, raw_point2, searchRadius)
            raw_point2 = (raw_point2[0] + 1, raw_point2[1] + 1)

        point2 = project_into_img(raw_point2, img.shape, pad)
        
        print('Found point {}'.format(point2))
        if point2[0] < point1[0] or point2[1] < point1[1]:
            print('You have to select first the top-left corner and than the bottom-right')
            continue
        coordinates = (point1, point2)
        rect_img = img.copy()
        cv2.rectangle(rect_img, coordinates[0], coordinates[1], (255, 0, 0), 2)
        rect_img = cv2.copyMakeBorder(rect_img,pad,pad,pad,pad,cv2.BORDER_CONSTANT,value=(0,0,0))
        imshow(rect_img, 'Coordinates', wait=1)
        finish = input('Found this coordinates {} do you want to continue [y/n/cancel]?'.format(coordinates))
        cv2.destroyAllWindows()
        if finish.lower().startswith('y'):
            break
        elif finish.lower().startswith('c'):
            return None
    return coordinates


def get_frame_at(cap, seconds):
    cap.set(cv2.CAP_PROP_POS_MSEC , seconds * 1000)
    return cap.read()

def yes_no_input(question):
    answer = input(question)
    return answer.lower().startswith('y')

def create_slide_mask(video_heigth, video_width, sample_heigth, sample_width, exclude_rects):
    mask = np.ones((video_heigth, video_width), dtype=np.uint8)
    for rect in exclude_rects:
        cv2.rectangle(mask, rect[0], rect[1], 0, thickness=-1)
    mask = shape_section(mask, slide_rect) 
    mask = cv2.resize(mask, dsize=(sample_width, sample_heigth), interpolation=cv2.INTER_CUBIC)
    return mask

def slide_to_sample(slide, sample_heigth, sample_width):
    sample = cv2.cvtColor(slide, cv2.COLOR_RGB2GRAY)
    sample = cv2.resize(sample, dsize=(sample_width, sample_heigth), interpolation=cv2.INTER_CUBIC)
    sample = cv2.blur(sample, (5,5))
    return sample

def calculate_diff(curr_sample, prev_sample, mask):
    result = np.zeros_like(mask, dtype=np.int32)
    result = curr_sample * mask.astype(np.int32)
    result -= prev_sample
    result = np.power(result, 2)
    return result.sum()

def get_time_string(time):
    hours, time = divmod(time, 3600)
    minutes, seconds = divmod(time, 60)
    return '{:d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Path of the video", action="store", dest="filename", type=str)
    ap.add_argument("-o", "--output", help="Folder where the slides will be saved", action="store", dest="dst_folder", default=None, type=str)
    ap.add_argument("--start_at", default=0, help="Skip the first N seconds of video", action="store", dest="start_at", type=int)
    ap.add_argument("-s", "--step", default=2, help="Read a frame every N seconds", action="store", dest="sec_step", type=int)
    ap.add_argument("--sample_heigth", default=100, help="Heigth of the samples that will be compared, the default is 100 in order to reduce the calculus", action="store", dest="sample_heigth", type=int)
    ap.add_argument("-m", "--manual", help="If you want to define the slide coordinates manually", action="store_true", dest="manual")
    
    args = vars(ap.parse_args())
    filename = Path(args['filename'])
    video_name = filename.stem
    if args['dst_folder'] is None:
        dst_folder = Path(os.path.join(filename.parent, video_name + '_slides'))
        dst_folder.mkdir(parents=True, exist_ok=True)
    else:
        dst_folder = Path(args['dst_folder']).mkdir(parents=True, exist_ok=True)
    start_at = args['start_at']
    sec_step = args['sec_step']
    sample_heigth = args['sample_heigth']

    cap = cv2.VideoCapture(str(filename))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_heigth = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    sample_width = int(sample_heigth * video_width / video_heigth)

    clear_shell()
    print('Found this video-info:')
    print('\t-Frames per second (fps):\t{:.2f}'.format(fps))
    print('\t-Total number of frames:\t{}'.format(frame_count))
    print('\t-Video duration: {}'.format(get_time_string(duration)))
    print('\t-Video width:\t{}'.format(video_width))
    print('\t-Video heigth:\t{}'.format(video_heigth))
    print()

    get_rect = get_visual_rect
    if args['manual']:
        get_rect = get_manual_rect

    success, image = get_frame_at(cap, duration/2)
    slide_rect = get_rect(image, pad=100)
    if slide_rect is None:
        sys.exit(0)

    exclude_rects = []
    while yes_no_input('\nDo you want to add some excluding area [y/n]?'):
        exclude_rect = get_rect(image, pad=100, search=False)
        if exclude_rect is None:
            break
        exclude_rects.append(exclude_rect)
    print()

    mask = create_slide_mask(video_heigth, video_width, sample_heigth, sample_width, exclude_rects)

    time = start_at
    success, image = get_frame_at(cap, time)

    previous_sample = np.zeros_like(mask)
    counter = 0

    print('Start reading the video')
    while time <= duration and success:
        slide = shape_section(image, slide_rect)
        sample = slide_to_sample(slide, sample_heigth, sample_width)
        diff_val = calculate_diff(sample, previous_sample, mask)/(sample_heigth * sample_width)
        if diff_val > 1:
            cv2.imwrite(os.path.join(dst_folder, '{}_slide_{:04d}.png'.format(video_name, counter)), slide)
            counter += 1
            previous_sample = sample * mask
            imshow(slide, 'Slide saved', wait=10)
        print('{}\tvideo_time={}\tperc={:.02f}%\tDiff_val={:08.02f}\t{}'.format(
            'SAVED' if diff_val > 1 else '     ',
            get_time_string(time),
            time/(duration - start_at)*100,
            diff_val,
            '{}_slide_{:04d}.png'.format(video_name, counter) if diff_val > 1 else '',
        ))
        time += sec_step
        success, image = get_frame_at(cap, time)