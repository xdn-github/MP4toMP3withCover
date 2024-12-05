cover_sec = input("请输入封面图提取时间/Input the time of cover picture(s):")

import os
import subprocess

raw_video_list = os.listdir('./')
for raw_video_name in raw_video_list:
    origin_video_type = raw_video_name.split('.')[-1]
    if origin_video_type == 'mp4':
        convert_video_name = raw_video_name.strip("." + origin_video_type)
        convert_video_name = convert_video_name + '.mp3'
        # 转换MP4toMP3
        mp3_type_cmd = 'ffmpeg -i "{}" temp_"{}"'.format(raw_video_name, convert_video_name)
        p = subprocess.Popen(mp3_type_cmd, shell=True)
        p.wait()
        # 提取视频封面图, 手动调整提取封面的时间(s)
        cover_cmd = 'ffmpeg -i "{0}" -y -f image2 -ss {1} -t 0.001 "{2}".jpg'.format(raw_video_name, cover_sec, convert_video_name)
        p = subprocess.Popen(cover_cmd, shell=True)
        p.wait()
        # 给MP3添加封面
        mp3_cover_cmd = 'ffmpeg -i temp_"{0}" -i "{0}".jpg -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" "{0}"'.format(convert_video_name)
        p = subprocess.Popen(mp3_cover_cmd, shell=True)
        p.wait()
        # 删除不要的文件
        os.remove(convert_video_name + ".jpg")
        os.remove("temp_" + convert_video_name)
