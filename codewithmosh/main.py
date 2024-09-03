# 导入所需的库
import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips
from faker import Faker
import os



def read_file(url_file_path):
    with open (url_file_path, "r") as f:
        urls = f.read().splitlines()
        return urls


def download(url, index):
    # if index > 150:
    #     fake = Faker()
    #     headers = {
    #         'User-Agent': fake.user_agent()
    #     }
    #     response = requests.get(url, headers = headers) #使用fake生成假的请求头
    #     with open (f"{index}.mp4", "wb") as f:
    #         f.write(response.content)
    #
    # else:
    file_name = f"{index}.mp4"
    # 判断文件名是否已存在
    if os.path.exists(file_name):
        # 返回文件名和大小
        return file_name, os.path.getsize(file_name)

    else:
        with open (file_name, "wb") as f:
            fake = Faker()
            headers = {
                'User-Agent': fake.user_agent()
            }
            response = requests.get(url, headers = headers)
            f.write(response.content)

            return file_name, os.path.getsize(file_name)


def concatenate_videos(video_files):
    clips = [VideoFileClip(video) for video in video_files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("final.mp4")




def main():
    url_file_path = r"D:\coding\代码\codewithmosh\urls.txt"
    urls = read_file(url_file_path)
    video_files = []
    for index, url in enumerate(urls):
        video_file = download(url, index)
        video_files.append(video_file)
        print("url为{}的第{}个文件处理成功".format(url, index))

    concatenate_videos(video_files)




if __name__ == "__main__":

    main()