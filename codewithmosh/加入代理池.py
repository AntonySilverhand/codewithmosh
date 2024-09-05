import aiohttp
import asyncio
import aiofiles
from faker import Faker
from moviepy.editor import concatenate_videoclips, VideoFileClip
from tqdm.asyncio import tqdm
import os
from PROXYPOOL import proxy_pool
import random



def choose_proxy(pool):

    proxy, value = random.choice(list(pool.items()))
    return proxy, value

def renew_proxy(purl):

    pp = proxy_pool()
    pp.get_pool(url=purl)
    pool = pp.proxies
    return pool

TARGET_DIR = r'E:\代码\codewithmosh\downloaded_file'
# Function to download a single video
async def download_video(session, url, filename, pool):
    async with asyncio.Semaphore(10):
        file_path = os.path.join(TARGET_DIR, filename)
        downloaded = 0

        if os.path.exists(file_path):
            downloaded = os.path.getsize(file_path)


        headers = {
            "User-Agent": Faker().user_agent()
        }

        headers['Range'] = f'bytes={downloaded}-'
        proxy, value = choose_proxy(pool=pool)
        proxies = f"https://{proxy}"

        try:
            async with session.get(url, headers=headers, proxy = proxies) as response:
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

        except Exception as e:
            print(f"Error downloading {url}: {e}")
            value -= 1
            if value <= 5:
                renew_proxy(purl)
            await asyncio.sleep(random.uniform(1, 5))
            await download_video(session, url, filename, pool)





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

    tasks = []
    pool = renew_proxy(purl)
    print(pool)
    urls = read_urls(r'E:\代码\codewithmosh\urls.txt')

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
                    tasks.append(download_video(session, url, filename, pool))
                elif local_size < server_size:
                    print(f"Local file is smaller than server file for {url}. Downloading again.")
                    tasks.append(download_video(session, url, filename, pool))
                else:
                    print(f"File {filename} already downloaded and is complete.")
            else:
                tasks.append(download_video(session, url, filename, pool))

        await asyncio.gather(*tasks)


    video_file.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    concatenate_videos(video_file)






# Run the main function
if __name__ == '__main__':
    purl = "https://sky.moluo.ltd/api/v1/client/subscribe?token=4cb0b8d617014f9807398f61e6cc70ca"
    video_file = []
    while True:
        asyncio.run(main())



