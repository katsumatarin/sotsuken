import os
import cv2
import datetime
import capture_depth_image
import save_frame_sec
import detect_counter

def daily_check():
  today = datetime.date.today()
  yesterday = today - datetime.timedelta(days=1)
  today_str = today.strftime('%Y%m%d')
  yesterday_str = yesterday.strftime('%Y%m%d')

  today_dir = f'./data/daily/{today_str}'

  os.makedirs(today_dir, exist_ok=True)
  today_video_file_name = os.path.join(today_dir, f'{today_str}.mp4')

  capture_depth_image.capture_depth_image(today_video_file_name)

  print('何秒目を今日の部屋の画像に設定しますか？')
  sec = int(input())

  today_image_file_name = os.path.join(today_dir, f'{today_str}.jpg')
  yesterday_image_file_name = f'./data/daily/{yesterday_str}/{yesterday_str}.jpg'

  save_frame_sec.save_frame_sec(today_video_file_name, sec,   today_image_file_name)

  os.remove(today_video_file_name)

  yesterday_count, _ = detect_counter.detect_counter(yesterday_image_file_name)
  today_count, _ = detect_counter.detect_counter(today_image_file_name)

  if yesterday_count < today_count:
    print('昨日よりモノが増えているようです。片付けましょう')
  elif yesterday_count > today_count:
    print('昨日よりモノの数が減りました！このまま綺麗な部屋を維持しましょう。')
  else:
    print('昨日とモノの数は変わっていません。')

  # 外接矩形された画像を表示
  yesterday_image = cv2.imread(yesterday_image_file_name)
  cv2.imshow('yesterday', yesterday_image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  today_image = cv2.imread(today_image_file_name)
  cv2.imshow('today', today_image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


if __name__ == '__main__':
  daily_check()