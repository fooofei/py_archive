#coding=utf-8


'''
    
    使用 Python 解压 zip 7z  gzip 等类型文件
    
    使用 :
    1. pip install libarchive-c

    2. windows 从 https://github.com/nexB/scancode-toolkit/tree/develop/src/extractcode/bin/win-32/bin 下载 bin 为了使用 libarchive.dll
    3 . 配置环境变量:
        1. 在 System Variables ( 注意不是 User Variables/Path ) 中配置, 给寻找 dll 路径使用，
            配置示例 LIBARCHIVE=C:\Python27\Lib\site-packages\libarchive\windows_bin\libarchive.dll
            
        2. User Variables/Path 中加上 C:\Python27\Lib\site-packages\libarchive\windows_bin 是为了 1 中的 LoadLibrary(libarchive.dll) 成功
        没有 2 的话，libarchive.dll 依赖的其他 dll 会找不到， LoadLibrary 失败(通过 C++ LoadLibrary 才提示出这个错误 Python 不提示)
    
    libarchive ref https://github.com/Changaco/python-libarchive-c
    
'''

import os
import libarchive

curpath = os.path.dirname(os.path.realpath(__file__))


def io_hash_stream(stream, hash_algorithm=u'md5',block_size=2 ** 20):
    import hashlib
    hash_ins = {u'md5':hashlib.md5(),
                u'sha1':hashlib.sha1()}.get(hash_algorithm,None)
    if not hash_ins:
        raise ValueError(u'not get proper hash algorithm')
    while 1:
        data = stream.read(block_size)
        if not data:
            break
        hash_ins.update(data)
    return hash_ins.hexdigest()

def io_hash_fullpath(fullpath,hash_algorithm=u'md5'):
    with open(fullpath,'rb') as f:
        return io_hash_stream(stream=f,hash_algorithm=hash_algorithm)



def _archive_framework(fullpath_archive,fname_in_archive_to_extract, dir_to_save, pre_hash):

    import shutil

    with libarchive.file_reader(fullpath_archive) as x:
        for ev in x:
            sub_path = ev.pathname
            if sub_path.endswith(fname_in_archive_to_extract):
                p_w = os.path.join(dir_to_save, sub_path)
                p_w_d = os.path.dirname(p_w)
                if os.path.exists(p_w):
                    os.remove(p_w)
                if not os.path.exists(p_w_d):
                    os.makedirs(p_w_d)
                print (u' --> extract {}'.format(sub_path))
                with open(p_w, 'wb') as fw:
                    for block in ev.get_blocks():
                        fw.write(block)
                # check the file we extract is has the same hash with the file we prepare
                assert (io_hash_fullpath(p_w) == pre_hash)
                shutil.rmtree(dir_to_save)
                break


def entry():

    _archive_framework(os.path.join(curpath, u'7z')
                       ,u'flashmediaelement.swf'
                       ,os.path.join(curpath,u'7z_e')
                       ,io_hash_fullpath(os.path.join(curpath,u'7z_flashmediaelement.swf')))
    print (u'pass test archvie 7z\n\n')

    _archive_framework(os.path.join(curpath,u'gzip')
                       ,u'player-block.swf'
                       ,os.path.join(curpath,u'gzip_e')
                       ,io_hash_fullpath(os.path.join(curpath,u'gzip_player-block.swf')))
    print (u'pass test archvie gzip\n\n')

    _archive_framework(os.path.join(curpath, u'zip')
                       , u'SqlMonitor.swf'
                       , os.path.join(curpath, u'zip_e')
                       , io_hash_fullpath(os.path.join(curpath, u'zip_SqlMonitor.swf')))
    print (u'pass test archvie zip\n\n')




if __name__ == '__main__':
    entry()