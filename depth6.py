#動画から秒数を指定して画像を切り取る

import cv2
import os

def save_frame_sec(video_path, sec, result_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(os.path.dirname(result_path), exist_ok=True)

    fps = cap.get(cv2.CAP_PROP_FPS)

    cap.set(cv2.CAP_PROP_POS_FRAMES, round(fps * sec))

    ret, frame = cap.read()

    if ret:
        cv2.imwrite(result_path, frame)

save_frame_sec('data/temp/sample_depth.mp4', 0, 'data/temp/result_0sec.jpg')
save_frame_sec('data/temp/sample_depth.mp4', 10, 'data/temp/result_10sec.jpg')
save_frame_sec('data/temp/sample_depth.mp4', 20, 'data/temp/result_20sec.jpg')
save_frame_sec('data/temp/sample_depth.mp4', 30, 'data/temp/result_30sec.jpg')
save_frame_sec('data/temp/sample_depth.mp4', 40, 'data/temp/result_40sec.jpg')
save_frame_sec('data/temp/sample_depth.mp4', 50, 'data/temp/result_50sec.jpg')
save_frame_sec('data/temp/sample_depth.mp4', 60, 'data/temp/result_60sec.jpg')