import os
import time
import requests
from bs4 import BeautifulSoup

headers = {'User-gent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def request(link):
    r = requests.get(link, headers=headers)
    res = r.text
    soup = BeautifulSoup(res, "html.parser")
    return soup


#function to search manga
def search_manga(name):
    res_manga_names = []
    res_manga_links = []
    
    manga_name_url = name.replace(" ", "%20") 
    search_url = f"https://ww3.mangakakalot.tv/search/{manga_name_url}"

    search_res = request(search_url)

    res_manga = search_res.find_all(class_="story_name")

    for result in res_manga:
        result_name = result.text.lower().replace("\n", "")
        if name.lower() not in result_name:
            res_manga.remove(result)

        elif result_name.startswith(name) or f" {name}" in result_name:
                res_manga_links.append(result.a["href"])
                res_manga_names.append(result_name.title())

    return res_manga_names, res_manga_links


def manga_download(res_manga_name, res_manga_link):

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
        chapter_link = chapters[i]["href"]

        try:
            os.mkdir(f"Chapter {i}")
            os.chdir(f"Chapter {i}")

        except FileExistsError:
            os.chdir(f"Chapter {i}")

        chapter = request(f"https://ww3.mangakakalot.tv{chapter_link}")

        chapter_pages = chapter.find(id="vungdoc").find_all("img")


        for j, page in enumerate(chapter_pages):

            page_img_src = page["data-src"]

            page_img = requests.get(page_img_src)

            with open(f"{j}.jpg", "wb") as img:
                img.write(page_img.content)

        os.chdir("..")

    os.chdir("..")

if __name__ == "__main__":
    search_manga()
    manga_download()



