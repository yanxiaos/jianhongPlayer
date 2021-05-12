import os
from RequestServer import getMusic


# 下载音乐
def downMusic(file_dir, name, music, file_type):
    with open(file_dir + "/" + name + file_type, "wb") as file:
        for m in music.iter_content():
            file.write(m)


# 获取音乐文件路径
def getMusicPath(types, name):
    """types: play,download"""
    music_path = None
    # 初始化下载目录
    cache_dir = os.path.join(os.curdir, 'cache')
    download_dir = os.path.join(os.curdir, "download")
    # 如果目录不存在则创建目录
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)

    if types == "play":
        # 判断文件是否已下载
        if os.path.exists(download_dir + "/" + name + ".mp3"):
            print("download existence")
            music_path = download_dir + "/" + name + ".mp3"
        # 判断文件是否已缓存
        elif os.path.exists(cache_dir + "/" + name + ".jh"):
            print("cache existence")
            music_path = cache_dir + "/" + name + ".jh"
        else:
            music = getMusic(types, name)
            if music.status_code == 200:
                downMusic(cache_dir, name, music, ".jh")
                music_path = cache_dir + "/" + name + ".jh"
            elif music.status_code == 403:
                return None
            else:
                return None
    elif types == "download":
        music = getMusic(types, name)
        if music.status_code == 200:
            downMusic(download_dir, name, music, ".mp3")
            music_path = download_dir + "/" + name + ".mp3"
        else:
            return None
    return music_path


if __name__ == "__main__":
    print(getMusicPath("play", "阿涵 - 备爱"))
