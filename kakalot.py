import os
import time
import math
import requests
from bs4 import BeautifulSoup

headers = {'User-gent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def request(link):
    r = requests.get(link, headers=headers)

    res = r.text
    soup = BeautifulSoup(res, "html.parser")
    return soup

def progress(i, num_of_chapters, chap_begin_time):
    #assigning | for
    comp = "|"
    rem = "_"

    prog_percent = (i / num_of_chapters) * 100
    prog_percent_bar = math.ceil(prog_percent)

    chap_end_time = time.time()
    
    one_chap_time = chap_end_time - chap_begin_time
    
    est_time = float((num_of_chapters - i) * one_chap_time)
    mins, secs = divmod(est_time, 60)
    hrs, mins = divmod(mins, 60)

    hrs, mins, secs = str(math.floor(hrs)).zfill(2), str(math.floor(mins)).zfill(2), str(math.floor(secs)).zfill(2)

    est_time = (f"{hrs}:{mins}:{secs}")

    prog_bar = f"[{comp*prog_percent_bar}{rem * (100 - prog_percent_bar)}]{round(prog_percent, 2)}"

    return est_time, prog_bar


def kakalot(name):
    chap_begin_time = time.time()
    res_manga_names = []
    res_manga_links = []
    i = 0

    manga_name_url = name.replace(" ", "%20") 
    search_url = f"https://ww3.mangakakalot.tv/search/{manga_name_url}"

    search_res = request(search_url)

    res_manga = search_res.find_all(class_="story_name")

    print(f"\n\nResults for {name}\n")
    for result in res_manga:
        result_name = result.text.lower().replace("\n", "")
        if name.lower() not in result_name:
            res_manga.remove(result)

        elif result_name.startswith(name) or f" {name}" in result_name:
                res_manga_links.append(result.a["href"])
                res_manga_names.append(result_name.title())
                i += 1 
                print(f"\t{i}. {result_name.title()}")

    user_select = int(input("\nEnter the manga you want to download: "))

    res_manga_name, res_manga_link = res_manga_names[user_select-1], res_manga_links[user_select-1]

    try:
        os.mkdir(res_manga_name.replace(":", "-"))
        os.chdir(res_manga_name.replace(":", "-"))

    except FileExistsError:
        os.chdir(res_manga_name.replace(":", "-"))


    chosen_manga = request(f"https://ww3.mangakakalot.tv{res_manga_link}")

    chapters = chosen_manga.find(class_="chapter-list").find_all("a")[::-1]

    # print(chapters)

    num_of_chapters = len(chapters)
    # print(num_of_chapters)

    for i in range(num_of_chapters):
        chapter_name = chapters[i].text.removeprefix("\n")
        chapter_link = chapters[i]["href"]

        try:
            os.mkdir(chapter_name.replace(":", "-"))
            os.chdir(chapter_name.replace(":", "-"))

        except FileExistsError:
            os.chdir(chapter_name.replace(":", "-"))

        chapter = request(f"https://ww3.mangakakalot.tv{chapter_link}")

        chapter_pages = chapter.find(id="vungdoc").find_all("img")


        for page in chapter_pages:
            est_time, prog_bar = progress(i, num_of_chapters, chap_begin_time)

            print(prog_bar, f"Est. Time: {est_time}", end="\r")

            page_img_src = page["data-src"]
            page_file_name = page["alt"]

            page_img = requests.get(page_img_src)

            with open(f"{page_file_name}.jpg", "wb") as img:
                img.write(page_img.content)


        os.chdir("..")

    print("Download Completed!")
    print(F"saved to {os.getcwd()}")
    
if __name__ == "__main__":
    name = input("Enter name of the manga: \n>>")
    kakalot(name)



