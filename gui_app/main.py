from tkinter import *
from win10toast import ToastNotifier
from pygame import RESIZABLE
from kakalot_gui import search_manga, manga_download
import os

root = Tk()
root.title("Kaklot Scraper")
root.iconbitmap("kakalot_favicon.ico")
root.configure(bg="#262626")
root.rowconfigure(13, minsize=40)
root.resizable(False, False)

toast = ToastNotifier()


def search_res(name):
    #getting manga names and links list from kakalot_gui
    manga_names_list, manga_links_list = search_manga(name)

    #initializing lists to store popped names and links for later
    prev_manga_names = []
    prev_manga_links = []

    #function to display results
    def display_results(manga_names, manga_links):
        for i, manga_name in enumerate(manga_names):
            #if the name is longer than 30 characters, clips the character above 30
            if len(manga_name) > 30:
                manga_name  = f"{manga_name[:-(len(manga_name)-30)]}..."

            #if character is less than 30 pads them to cover up the previous results
            else:
                manga_name = manga_name.ljust(50, " ")#padding 50 cause spaces take less width than other characters

            #caps the displayed results at 10
            if i < 10:
                root.grid_rowconfigure(i+2, minsize=40)
                #doewnload command
                def manga_down(manga_name = manga_names[i], manga_link = manga_links[i]):
                    manga_download(manga_name, manga_link)
                    #notifies when download is complete
                    toast.show_toast(
                        f"{manga_name} download Complete",
                        f"Saved to {os.getcwd()}\\{manga_name}",
                        icon_path= "kakalot_favicon.ico",
                        duration = 5,
                        threaded = True,)

                #name label
                Label(root, text=f"{i+1}. {manga_name.upper()}", font=("Poppins", 10), bg="#262626", fg="#54cae5").grid(row=i+2, column=0, pady=2, padx=10, sticky="w")

                #download button
                Button(root,text="DOWNLOAD", bg="#262626", fg="#54cae5", font=("Montserrat", 8), command=manga_down).grid(row=i+2, column=1, padx=4, pady=2)

    #next command
    def next():
        #if more than 10 items in list, loops through 10 times else loops through the amount of items there are
        if len(manga_names_list) >= 10:
            for i in range(10):
                prev_manga_names.append(manga_names_list.pop(0)) #removes the 1st item from the list and adds it to prev list
                prev_manga_links.append(manga_links_list.pop(0))

            display_results(manga_names_list, manga_links_list)
        
        else:
            for i in range(len(manga_names_list)):
                prev_manga_names.append(manga_names_list.pop(0))
                prev_manga_links.append(manga_links_list.pop(0))

            display_results(manga_names_list, manga_links_list)


    def prev():
        if len(prev_manga_names) >= 10:
            #if more than 10 items in list, loops through 10 times else loops through the amount of items there are
            for i in range(10):
                manga_names_list.insert(0, prev_manga_names.pop(0))#removes 1st item from the prev list and inserts it to the beginning of original list
                manga_links_list.insert(0, prev_manga_links.pop(0))

            display_results(manga_names_list, manga_links_list)

        else:
            for i in range(len(prev_manga_names)):
                manga_names_list.insert(0, prev_manga_names.pop(0))
                manga_links_list.insert(0, prev_manga_links.pop(0))

            display_results(manga_names_list, manga_links_list)


    display_results(manga_names_list, manga_links_list)
            

    next_btn = Button(root, text="Next",command=next, font=("Montserrat", 12), bg="#262626", fg="#54cae5", width=5)

    next_btn.grid(row=13, column=0, sticky="w", padx=5)



    prev_btn = Button(root, text="Prev",command=prev, font=("Montserrat", 12), bg="#262626", fg="#54cae5", width=5)

    prev_btn.grid(row=13, column=1)
    

    Label(root, text="Note:\nThe app will become unresponsive after the downlaod has started.\nYou will be notified after the download is finished.\nIf your focus assist is on, you'll not get alerted.\nYou can download another manga only after the current one is completed.",font=("Montserrat", 12), bg="#262626", fg="#d12323").grid(row=15, columnspan=4)






def search():
    #title label
    Label(root, text="KAKALOT SCRAPER", font=("Shamar", 36), fg="#54cae5", bg="#262626").grid(row=0, column=0, columnspan=5, padx=10)
    #input field
    manga_search = Entry(root, width=75)
    manga_search.grid(row=1, column=0, pady=20, columnspan=3, padx=10)

    def button_search(): #gets the keyword user typed in and passes it to search_res function
        user_search = manga_search.get()
        search_res(user_search)

    def quit():
        root.destroy()

    #search and quit buttons
    Button(root, text="Search",font=("Montserrat", 12), command=button_search, bg="#262626", fg="#54cae5").grid(row=1, column=3, padx=5)
    Button(root, text="Quit", font=("Montserrat", 12), command=quit,bg="#262626", fg="#54cae5", width=5).grid(row=13, column=3, pady=5)
search()

root.mainloop()