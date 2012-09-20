#coding=gbk
'''
Created on 2012-5-26

@author: guoxc
'''
import os

def visit_dir(path, upper):
    """ -_-|| """
    lis = os.listdir(path)
    for item in lis:
        pathname = os.path.join(path, item)
        path_list = upper + [str(item),]
        if not os.path.isfile(pathname):
            visit_dir(pathname, path_list)
        else:
            rename_str = "_".join(path_list)
            print rename_str
            rename_str = os.path.join(path, rename_str)
            os.rename(pathname, rename_str)
if __name__ == "__main__":
    PATH = "./data"
    visit_dir(PATH, [])
