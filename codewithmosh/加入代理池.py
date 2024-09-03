import aiohttp
import asyncio
import aiofiles
from faker import Faker
from moviepy.editor import concatenate_videoclips, VideoFileClip
from tqdm.asyncio import tqdm
import os
from PROXYPOOL import proxy_pool
import random


class pool:

    def __init__(self):
        self.headers = {
            "User-Agent": Faker().user_agent()
        }
        self.url = "https://sky.moluo.ltd/api/v1/client/subscribe?token=4cb0b8d617014f9807398f61e6cc70ca"
        self.proxies = {}


    def proxy(self):
        pp = proxy_pool()
        self.proxies = pp.get_pool(self.url)
        return self.proxies

    def choose_proxy(self):
        chosen = random.choice(list(self.proxies.items()))
        return chosen


TARGET_DIR = r'E:\代码\codewithmosh\downloaded_file'
# Function to download a single video
async def download_video(session, url, filename):
    async with asyncio.Semaphore(10):
        file_path = os.path.join(TARGET_DIR, filename)
        headers = {
            "User-Agent": Faker().user_agent()
        }

        downloaded = 0

        if os.path.exists(file_path):
            downloaded = os.path.getsize(file_path)

        headers['Range'] = f'bytes={downloaded}-'
        async with session.get(url, headers=headers) as response:
            if response.status in [200, 206]:
                content_range = response.headers.get('Content-Range')
                if content_range:
                    total_size = int(content_range.split('/')[1])
                else:
                    total_size = response.headers.get('Content-Length', 0) + downloaded

                async with aiofiles.open(file_path, mode='ab') as file:
                    with tqdm(total=total_size, initial=downloaded, unit='B', unit_scale=True, desc=filename, unit_divisor = 1024) as pbar:
                        async for chunk in response.content.iter_chunked(1024):
                            await file.write(chunk)
                            pbar.update(len(chunk))








async def get_content_length(session, url):
    headers = {
        "User-Agent": Faker().user_agent()
    }
    async with session.head(url, headers=headers) as response:
        content_length = response.headers.get('Content-Length')
        if content_length:
            return int(content_length)
        return None


def read_urls(file_path):
    # 使用with语句打开文件并读取所有行到一个列表中
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    # 返回读取到的URL列表
    return urls


def concatenate_videos(video_files):
    # 使用列表推导式创建VideoFileClip对象列表
    clips = [VideoFileClip(video) for video in video_files]
    # 拼接视频片段
    final_clip = concatenate_videoclips(clips)
    # 输出最终的视频文件
    final_clip.write_videofile("final_video.mp4")


# Main function to handle multiple downloads
async def main():
    pool.proxy()
    urls = read_urls(r'E:\代码\codewithmosh\urls.txt')
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i, url in enumerate(urls):
            filename = f'video_{i}.mp4'

            # 检查文件是否存在
            if os.path.exists(filename):
                # 获取本地文件大小
                local_size = os.path.getsize(filename)
                # 获取服务器文件大小
                server_size = await get_content_length(session, url)

                if server_size is None:
                    print(f"Could not get file size from server for {url}")
                    tasks.append(download_video(session, url, filename))
                elif local_size < server_size:
                    print(f"Local file is smaller than server file for {url}. Downloading again.")
                    tasks.append(download_video(session, url, filename))
                else:
                    print(f"File {filename} already downloaded and is complete.")
            else:
                tasks.append(download_video(session, url, filename))

        await asyncio.gather(*tasks)


    video_file.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    concatenate_videos(video_file)




video_file = []
# Run the main function
if __name__ == '__main__':
    try:
        asyncio.run(main())

    except Exception as e:
        try:
            asyncio.run(main())

        except Exception as e:
            try:
                asyncio.run(main())

            except Exception as e:
                asyncio.run(main())


