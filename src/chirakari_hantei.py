import pyrealsense2 as rs
import numpy as np
import tkinter as tk
import cv2
import os
import capture_depth_image
import save_frame_sec
import detect_counter
import utils
import main

def chirakari_hantei():
  output_name = utils.get_unused_out_dir_num()
  os.makedirs(f'../data/out/{output_name}', exist_ok=True)

  output_video_file_name = f'../data/out/{output_name}/{output_name}.mp4'

  # ビデオを撮影し、保存する
  capture_depth_image.capture_depth_image(output_video_file_name, 4)

  sec_array = [1, 2, 3]
  detect_count_array = []
  src_array = []

  for sec in sec_array:
    output_image_file_name = f'../data/out/{output_name}/{output_name}_{sec}sec.jpg'

    # 指定された秒数の画像を保存
    save_frame_sec.save_frame_sec(output_video_file_name, sec, output_image_file_name)

    # 画像から物体を検出し、物体の数と物体を矩形で囲んだ画像を取得
    detect_count, src = detect_counter.detect_counter(output_image_file_name)
    detect_count_array.append(detect_count)
    src_array.append(src)

  # 3回分のdetect_countのうち2番目の大きさのものをdetect_countとsrcに代入
  sorted_detect_count_array = sorted(detect_count_array)
  medium_count = sorted_detect_count_array[1]
  detect_count_index = detect_count_array.index(medium_count)
  detect_count = detect_count_array[detect_count_index]
  src = src_array[detect_count_index]

  # 外接矩形された画像を表示
  cv2.imshow('output', src)
  cv2.waitKey(3000)

  # 終了処理
  cv2.destroyAllWindows()

  root = tk.Tk()
  root.title(u"散らかり判定")
  root.geometry("600x400")

  if detect_count > 10:
    label = tk.Label(text=u'部屋が汚れています！大至急片付けましょう！\n')
    label.pack()
  elif detect_count > 0:
    label = tk.Label(text=u'部屋が少し汚いので片付けてください！\n')
    label.pack()
  else:
    label = tk.Label(text=u'部屋が汚れています！大至急片付けましょう！\n')
    label.pack()

  def ok_button_click():
    root.destroy()

  okButton = tk.Button(root, text='OK', command=ok_button_click)
  okButton.pack()

  root.mainloop()

  os.remove(output_video_file_name)
  main.main_func()

if __name__ == '__main__':
  chirakari_hantei()