import pyrealsense2 as rs
import numpy as np
import cv2
import os
import capture_depth_image
import save_frame_sec
import detect_counter

def chirakari_hantei():
  print("出力ファイル名を入力してください")
  output_name = input()
  os.makedirs(f'./data/out/{output_name}', exist_ok=True)

  output_video_file_name = f'./data/out/{output_name}/{output_name}.mp4'

  # ビデオを撮影し、保存する
  capture_depth_image.capture_depth_image(output_video_file_name)

  while(True):
    print(f"何秒目の部屋の散らかりをチェックしますか？終了する場合は-1を入力してください。")
    sec = int(input())

    if sec == -1:
      break

    output_image_file_name = f'./data/out/{output_name}/{output_name}_{sec}sec.jpg'

    # 指定された秒数の画像を保存
    save_frame_sec.save_frame_sec(output_video_file_name, sec, output_image_file_name)

    # 画像から物体を検出し、物体の数と物体を矩形で囲んだ画像を取得
    detect_count, src = detect_counter.detect_counter(output_image_file_name)

    if detect_count > 10:
      print('部屋が汚れています！大至急片付けましょう！')
    elif detect_count > 0:
      print('部屋が少し汚いので片付けてください！')
    else:
      print('とても綺麗です！このまま継続しましょう！')

    # 外接矩形された画像を表示
    cv2.imshow('output', src)
    cv2.waitKey(0)

    # 終了処理
    cv2.destroyAllWindows()


  os.remove(output_video_file_name)

if __name__ == '__main__':
  chirakari_hantei()