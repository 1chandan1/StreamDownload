from time import time
import m3u8
import requests
from threading import Thread

check = []
a = 0
stop = False
Vname = input("Video name :")
url = input("Enter the m3u8 link of the resolution that you want:")
while True:
    try:
        r = requests.get(url)
        m3u8_master = m3u8.loads(r.text)
        m3u8_master.data['playlists'][-1]['uri']
        url = input(
            "It may be the master m3u8 link. Enter link of indivisual resolution which you want :\n"
        )
        continue
    except:
        pass
    try:
        r = requests.get(url)
        Playlist = m3u8.loads(r.text)
        tsfile = Playlist.data['segments']
        if tsfile == []:
            url = input("Enter correct Link :")
            continue
        break
    except:
        url = input("Enter correct Link :")
print("Press Enter to STOP")


def downLink():
    global a, run
    start = time()
    while True:
        global stop
        if stop:
            print("STOP")
            break
        r = requests.get(url)
        Playlist = m3u8.loads(r.text)
        tsfile = Playlist.data['segments']
        for link in tsfile:
            if link["uri"] not in check:
                check.append(link["uri"])
                a += 1
                print(time() - start, end="\r")
        if time() - start > 3000:
            run = False
            break


def download():
    global a, stop
    b = 0
    run = True
    with open(Vname + ".ts", "wb") as f:
        while run:
            if a > b:
                p = requests.get(check[b])
                f.write(p.content)
                b += 1
            if stop:
                f.close()
                break


def STOP():
    global stop
    input()
    stop = True


s1 = Thread(target=downLink)
s2 = Thread(target=download)
s3 = Thread(target=STOP)
s1.start()
s2.start()
s3.start()
