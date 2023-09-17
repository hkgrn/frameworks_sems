import os
import requests
import threading
import multiprocessing
import asyncio
import time
import argparse


def download_image(url):
    start_time = time.time()  # Засекаем время начала загрузки
    response = requests.get(url)
    if response.status_code == 200:
        # Извлекаем имя файла из URL
        filename = os.path.basename(url)
        with open(filename, "wb") as file:
            file.write(response.content)
            end_time = time.time()  # Засекаем время завершения загрузки
            print(f"Скачано: {filename} (Время: {end_time - start_time:.2f} сек)")


parser = argparse.ArgumentParser(description="Скачивание изображений с заданных URL-адресов.")
parser.add_argument("urls", nargs="+", help="Список URL-адресов изображений")
args = parser.parse_args()

image_urls = args.urls

threads = []
for url in image_urls:
    thread = threading.Thread(target=download_image, args=(url,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

processes = []
for url in image_urls:
    process = multiprocessing.Process(target=download_image, args=(url,))
    processes.append(process)
    process.start()

for process in processes:
    process.join()


async def async_download_image(url):
    start_time = time.time()
    response = await loop.run_in_executor(None, lambda: requests.get(url))
    if response.status_code == 200:
        filename = os.path.basename(url)
        with open(filename, "wb") as file:
            file.write(response.content)
            end_time = time.time()
            print(f"Скачано (асинхронно): {filename} (Время: {end_time - start_time:.2f} сек)")

loop = asyncio.get_event_loop()
tasks = [async_download_image(url) for url in image_urls]

start_time_total = time.time()  # Засекаем время начала выполнения программы

loop.run_until_complete(asyncio.gather(*tasks))

end_time_total = time.time()
print(f"Программа завершена. Общее время: {end_time_total - start_time_total:.2f} сек")