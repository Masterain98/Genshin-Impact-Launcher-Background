import httpx
import os

RESOLUTION_SET = [[1440, 3120], [1, 1], [1152, 2048]]
RETRY_TIMES = 3


def url_process(url: str) -> tuple:
    url = url.split("/")
    return url[-1], url[-2], url[-3], url[-4]


def get_cn_background():
    error_message = ""
    url = ("https://sdk-static.mihoyo.com/hk4e_cn/mdk/launcher/api/content?filter_adv=true&key=eYd89JmJ&language=zh-cn"
           "&launcher_id=18")
    for _ in range(RETRY_TIMES):
        try:
            response = httpx.get(url, timeout=15).json()
            break
        except (httpx.ReadTimeout, httpx.RemoteProtocolError, httpx.ConnectTimeout) as e:
            error_message += f"```{str(e)}```\n"
            continue
    else:
        print(f"::error title=Failed to cache CN background::{error_message}")
        return None
    background_url = response["data"]["adv"]["background"]
    file_name, day, month, year = url_process(background_url)
    os.makedirs(f"./output/cn/{year}/{month}/{day}/", exist_ok=True)
    with open(f"./output/cn/{year}/{month}/{day}/{file_name}", "wb") as f:
        f.write(httpx.get(background_url).content)


def get_bilibili_background():
    error_message = ""
    url = ("https://sdk-static.mihoyo.com/hk4e_cn/mdk/launcher/api/content?filter_adv=true&key=KAtdSsoQ&language=zh-cn"
           "&launcher_id=17")
    for _ in range(RETRY_TIMES):
        try:
            response = httpx.get(url)
            break
        except (httpx.ReadTimeout, httpx.RemoteProtocolError, httpx.ConnectTimeout) as e:
            error_message += f"```{str(e)}```\n"
            continue
    else:
        print(f"::error title=Failed to cache MYS wallpaper::{error_message}")
        return None
    response = response.json()
    background_url = response["data"]["adv"]["background"]
    file_name, day, month, year = url_process(background_url)
    os.makedirs(f"./output/bilibili/{year}/{month}/{day}/", exist_ok=True)
    with open(f"./output/bilibili/{year}/{month}/{day}/{file_name}", "wb") as f:
        f.write(httpx.get(background_url).content)


def get_os_background():
    language_set = ["zh-cn", "zh-tw", "en-us", "ja-jp", "ko-kr", "fr-fr", "de-de", "es-es", "pt-pt", "ru-ru",
                    "id-id", "vi-vn", "th-th"]
    for language in language_set:
        os.makedirs(f"./output/os/{language}/", exist_ok=True)
        url = ("https://sdk-os-static.mihoyo.com/hk4e_global/mdk/launcher/api/content?filter_adv=true&key=gcStgarh"
               f"&language={language}&launcher_id=10")
        response = httpx.get(url).json()
        try:
            background_url = response["data"]["adv"]["background"]
            file_name, day, month, year = url_process(background_url)
            os.makedirs(f"./output/os/{language}/{year}/{month}/{day}/", exist_ok=True)
            with open(f"./output/os/{language}/{year}/{month}/{day}/{file_name}", "wb") as f:
                f.write(httpx.get(background_url).content)
        except TypeError:
            print(f"Background for {language} is not available.")


def get_cn_cloud():
    for r in RESOLUTION_SET:
        url = "https://api-cloudgame.mihoyo.com/hk4e_cg_cn/gamer/api/getUIConfig?height=%s&width=%s" % (r[0], r[1])
        response = httpx.get(url).json()
        background_url = response["data"]["bg_image"]["url"]
        file_name, day, month, year = url_process(background_url)
        os.makedirs(f"./output/cloud_cn/{year}/{month}/{day}/", exist_ok=True)
        with open(f"./output/cloud_cn/{year}/{month}/{day}/{file_name}", "wb") as f:
            f.write(httpx.get(background_url).content)


def get_os_sg_cloud():
    for r in RESOLUTION_SET:
        url = "https://sg-cg-api.hoyoverse.com/hk4e_global/cg/gamer/api/getUIConfig?height=%s&width=%s" % (r[0], r[1])
        headers = {
            "x-rpc-cg_game_biz": "hk4e_global",
        }
        response = httpx.get(url, headers=headers).json()
        background_url = response["data"]["bg_image"]["url"]
        file_name, day, month, year = url_process(background_url)
        os.makedirs(f"./output/cloud_sg/{year}/{month}/{day}/", exist_ok=True)
        with open(f"./output/cloud_sg/{year}/{month}/{day}/{file_name}", "wb") as f:
            f.write(httpx.get(background_url).content)


def try_all_resolution():
    import multiprocessing
    import threading
    import json

    client = httpx.Client(headers={"x-rpc-cg_game_biz": "hk4e_global"})
    background_url_list = []
    log = open("log.txt", "w")

    def process_resolution(x, y):
        url = "https://sg-cg-api.hoyoverse.com/hk4e_global/cg/gamer/api/getUIConfig?height=%s&width=%s" % (x, y)
        response = client.get(url).json()
        background_url = response["data"]["bg_image"]["url"]
        print(f"Resolution: {x}x{y}, URL: {background_url}")
        log.write(f"Resolution: {x}x{y}, URL: {background_url}\n")
        background_url_list.append(background_url)

    num_cores = multiprocessing.cpu_count()
    threads = []
    for i in range(1, 3840, 10):
        for j in range(1, 2160, 10):
            if len(threads) >= num_cores:
                for thread in threads:
                    thread.join()
                del threads[:]
            thread = threading.Thread(target=process_resolution, args=(i, j))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    client.close()
    log.close()
    background_url_list = list(set(background_url_list))
    with open("background_url_list.json", "w") as f:
        json.dump(background_url_list, f)


def mys_wallpaper():
    print("::group::Checking MYS wallpaper")
    error_message = ""
    api_url = ("https://hk4e-api.mihoyo.com/event/contenthub/v1/wall_papers?page={page_number}&size=100&type={type}&ba"
               "dge_uid=100000000&badge_region=cn_qd01&game_biz=hk4e_cn&lang=zh-cn")
    wallpaper_type_list = [
        {"type": "0", "name": "Patch Wallpapers"},
        {"type": "1", "name": "Event Wallpapers"},
        {"type": "2", "name": "Character Wallpapers"},
    ]
    for w in wallpaper_type_list:
        page_number = 1
        while True:
            print(f"Downloading {w['name']} at page {page_number}...")
            this_url = api_url.format(page_number=page_number, type=w["type"])
            print(f"URL: {this_url}")
            try:
                response = httpx.get(this_url).json()
            except UnicodeDecodeError:
                break
            for wallpaper in response["data"]["wallpapers"]:
                wallpaper_title = wallpaper["title"]
                wallpaper_url_list = list([pic["url"] for pic in wallpaper["pic_list"]])
                for url in wallpaper_url_list:
                    file_name, day, month, year = url_process(url)
                    os.makedirs(f"./output/mys/{w['name']}/{wallpaper_title}/{year}/{month}/{day}/", exist_ok=True)
                    # check if file exists
                    if os.path.exists(f"./output/mys/{w['name']}/{wallpaper_title}/{year}/{month}/{day}/{file_name}"):
                        continue
                    with open(f"./output/mys/{w['name']}/{wallpaper_title}/{year}/{month}/{day}/{file_name}",
                              "wb") as f:
                        print(f"Downloading {w['name']}/{wallpaper_title}/{year}/{month}/{day}/{file_name}...")
                        for _ in range(RETRY_TIMES):
                            try:
                                conn = httpx.get(url)
                                break
                            except (httpx.ReadTimeout, httpx.RemoteProtocolError, httpx.ConnectTimeout) as e:
                                error_message += f"```{str(e)}```\n"
                                continue
                        else:
                            print(f"::error title=Failed to cache MYS wallpaper::{error_message}")
                            return None
                        f.write(conn.content)
            if not response["data"]["has_more"]:
                break
            else:
                page_number += 1
    print("::endgroup::")


def main():
    get_cn_background()
    get_bilibili_background()
    get_os_background()
    get_cn_cloud()
    get_os_sg_cloud()
    # try_all_resolution()
    mys_wallpaper()


if __name__ == "__main__":
    main()
