import os

class NotFoundError(Exception):
  pass

def get_unused_out_dir_num():
  dir_list = os.listdir(path='./data/out')
  for i in range(1000):
    search_dir_name = '%03d' % i
    if search_dir_name not in dir_list:
      return search_dir_name
  raise NotFoundError('Error')