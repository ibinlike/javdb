import os
import glob
from os import path

def clean_files():
    dirname = os.getcwd()
    print(dirname)
    filename = [f for f in glob.glob(dirname + '/**/*.*', recursive=True)]
    valid_video_files =['.mp4', '.avi', '.mkv','.wmv']
    valid_img_files =['.jpg','png']

    valid_files = valid_video_files + valid_img_files
    valid_files.append('.py')

    def del_small_size_files(f):
        src = path.realpath(f)
        size = os.path.getsize(src)
        if size <500000000:
            print(f)
            user_input = input('file is too small, delete or keep? input enter ')
            if user_input == '':
                os.remove(src)
            else:
                pass

    for f in filename:
        if os.path.isfile(f):
            _, file_extension = os.path.splitext(f)
            if file_extension not in valid_files:

                print("\n")
                print('the file name is: {}'.format(f))
                print("\n")
                test = input('file is not valid, confirm to delete, input enter!')
                if test == '':
                    os.remove(path.realpath(f))
                else:
                    pass
            elif file_extension in valid_video_files:
                del_small_size_files(f)
            elif file_extension in valid_img_files:
                if 'poster' not in f:
                    print("\n")
                    print('the file name is :{}'.format(f))
                    print("\n")
                    test = input('image is not valid, confirm to delete, input enter!')
                    if test == '':
                        os.remove(path.realpath(f))
                    else:
                        pass
                else:
                    pass
            else:
                pass

def clean_dir():    
    stuff = os.getcwd()
    stuff = os.path.abspath(os.path.expanduser(os.path.expandvars(stuff)))
    print(stuff)
    for root,_,files in os.walk(stuff):
        if root[len(stuff):].count(os.sep) > 3:
            for f in files:
                _, file_extension = os.path.splitext(f)
                dir = os.path.join(root,f)
                if 'old' in dir:
                    pass
                elif file_extension in dir:
                    pre = '/'.join(dir.split('/')[:5]) + '/'
                    print('path:{}'.format(pre))
                    print('filename:{}'.format(f))
                    new_path = os.path.join(pre, f)
                    print('new_path:{}'.format(new_path))
                    test = input('confirm?')
                    if test == '':
                        os.rename(dir, new_path)
                        if os.path.isfile(new_path):
                            print('move success')
                            print(root)
                            test2 = input('remove root')
                            if test2 == '':
                                os.rmdir(root)
                        else:
                            print('someting wrong')
                    else:
                        pass
                else:
                    pass

if __name__ == "__main__":
    os.chdir('/mnt/share')
    clean_files()
    clean_dir()
