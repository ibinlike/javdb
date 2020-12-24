import os
import json
import jsonlines

#This file provide a mapping between the star and its code in javdb
star_code_mapping_data_path = './data/star_code_mapping.json'
star_init_url_list_path = './data/star_init_url.json'

url_pre = 'https://javdb6.com/actors/'
tag_pre = '?t=s,d'

def build_mapping(star_code_mapping_data_path):
  if os.path.isdir('./data'):

    print('Data dir existing...')
    print('\n')
    pass
  else:
    print('Data dir does not exist, create data dir...')
    print('\n')
    os.mkdir('data')
  done = False
  if os.path.isfile(star_code_mapping_data_path):
    print('star code file exist...loading...')
    print('\n')
    with jsonlines.open(star_code_mapping_data_path) as reader:
      star_code_list = [c for c in reader]
      print(star_code_list)
      print("\n")
      print("There are {} star codes existing...".format(len(star_code_list)))
  else:
      print('Create empty list...')
      print('\n')
      star_code_list =[]
  while done == False:
      star_code = input('please input the star_code: if no more star name, input N:')
      if star_code in star_code_list:
        print('Star already in the list')
        print('\n')
        continue
      elif star_code != 'N':
        star_code_list.append(star_code)
      else:
        done = True
  print("Input complete, start to dump...")
  print('\n')
  with jsonlines.open(star_code_mapping_data_path, mode = 'w') as writer:
      for c in star_code_list:
        writer.write(c)
      print('Dump completed...')
      print('\n')


#generate the star init pages

def build_url(star_code_mapping_data_path, url_pre, tag_pre, star_init_url_list_path):
  try:
    print('Loading data...')
    print('\n')
    with jsonlines.open(star_code_mapping_data_path) as reader:
        star_init_url_list = []
        for s in reader:
          star_init_url = url_pre+s+tag_pre
          star_init_url_list.append(star_init_url)
    print('Loading completed...')
    print('\n')
    print('Start to dump...')
    print('\n')  
    with jsonlines.open(star_init_url_list_path, mode = 'w') as writer:
      for url in star_init_url_list:
        writer.write(url)
    print('Dump completed')
  except:
    print('Something wrong...')
      
if __name__ == "__main__":
   build_mapping(star_code_mapping_data_path)
   build_url(star_code_mapping_data_path, url_pre, tag_pre, star_init_url_list_path) 
