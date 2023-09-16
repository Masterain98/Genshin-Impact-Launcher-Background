import httpx
import os

resolution_set = [[1440, 3120], [1, 1], [1152, 2048]]


def url_process(url: str) -> tuple:
    url = url.split("/")
    return url[-1], url[-2], url[-3], url[-4]


def get_cn_background():
    url = ("https://sdk-static.mihoyo.com/hk4e_cn/mdk/launcher/api/content?filter_adv=true&key=eYd89JmJ&language=zh-cn"
           "&launcher_id=18")
    response = httpx.get(url).json()
    background_url = response["data"]["adv"]["background"]
    file_name, day, month, year = url_process(background_url)
    os.makedirs(f"./output/cn/{year}/{month}/{day}/", exist_ok=True)
    with open(f"./output/cn/{year}/{month}/{day}/{file_name}", "wb") as f:
        f.write(httpx.get(background_url).content)


def get_bilibili_background():
    url = ("https://sdk-static.mihoyo.com/hk4e_cn/mdk/launcher/api/content?filter_adv=true&key=KAtdSsoQ&language=zh-cn"
           "&launcher_id=17")
    response = httpx.get(url).json()
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
    for r in resolution_set:
        url = "https://api-cloudgame.mihoyo.com/hk4e_cg_cn/gamer/api/getUIConfig?height=%s&width=%s" % (r[0], r[1])
        response = httpx.get(url).json()
        background_url = response["data"]["bg_image"]["url"]
        file_name, day, month, year = url_process(background_url)
        os.makedirs(f"./output/cloud_cn/{year}/{month}/{day}/", exist_ok=True)
        with open(f"./output/cloud_cn/{year}/{month}/{day}/{file_name}", "wb") as f:
            f.write(httpx.get(background_url).content)


def get_os_sg_cloud():
    for r in resolution_set:
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


def main():
    get_cn_background()
    get_bilibili_background()
    get_os_background()
    get_cn_cloud()
    get_os_sg_cloud()


if __name__ == "__main__":
    main()
