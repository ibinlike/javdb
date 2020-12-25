import json
import os
from qbittorrent import Client
import requests
from datetime import datetime
import time
import jsonlines

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}


download_urls_file_path = './data/result.json'
downloaded_id_path = './data/downloaded.json'
qb = Client('http://192.168.2.171:8080/')

qb.login('admin', 'like1978')

share_dir = '/mnt/share/'

default_save_path = qb.get_default_save_path()


def load_download_information(file_path,downloaded_path):
    if os.path.isfile(downloaded_id_path):
        with jsonlines.open(downloaded_id_path) as reader:
            downloaded_id = [id for id in reader]
            print(downloaded_id)
        
    else:
         downloaded_id =[]
    with jsonlines.open(file_path) as reader:
        #print('There are total {} download links...'.format(len(reader)))
        print('load success...')
        new_added = 0
        for item in reader:
            print(item)
            dt = datetime.strptime(item['movie_meta'], '%m/%d/%Y')
            if dt.year > 2016:
                star_save_path = share_dir + str(item['movie_star'])
                print('start_save_path:', star_save_path)
                if os.path.isdir(star_save_path):
                    print('dir is existing...')
                    pass
                else:
                    print('dir is not there...')
                    print('create dir...')
                    os.mkdir(star_save_path)
                if (item['movie_id'] not in downloaded_id) and ('VR' or 'vr' not in item['movie_title']):
                   # print(item['movie_img_src'])
                    print('movie is valid, process downloading...')
                    incompleted = True
                    while incompleted:
                        try:
                            img_r = requests.get(item['movie_img_src'], headers = headers)
                            movie_save_path = star_save_path + '/' + str(item['movie_id'])
                            print('movie_save_path:', movie_save_path)
                            if os.path.isdir(movie_save_path):
                                pass
                            else:
                                os.mkdir(movie_save_path)
                            with open(movie_save_path+'/'+'poster.jpg', 'wb') as f:
                                  f.write(img_r.content)
                            incompleted = False
                            savepath = 'E:\\'+'Download'+'\\'+ str(item['movie_star']) + '\\'+str(item['movie_id'])
                            print(savepath)
                            qb.download_from_link(item['mega_link'], savepath=savepath, category = item['movie_star'])
                            downloaded_id.append(item['movie_id'])
                            new_added += 1
                            time.sleep(10)
                        except:
                            print('Connection issue..')
                            time.sleep(60)
                else:
                    print("{} has already been downloaded before, skip!".format(item['movie_id']))
                    pass
            else:
                pass
    with jsonlines.open(downloaded_id_path, mode = 'w') as writer:
        for item in downloaded_id:
            writer.write(item)
    print('Totally {} new  download added'.format(new_added))

if __name__ == "__main__":
    load_download_information(download_urls_file_path, downloaded_id_path)
    
