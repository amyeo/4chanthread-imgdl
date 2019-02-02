import sys
import getopt
import requests
from bs4 import BeautifulSoup
import urllib.request
import time
import os

def write_to_file(urls, filename):
    f = open(filename, "w+")
    for line in urls:
        f.write(line + '\n')
    f.close()
    pass

def main(cargs):
    #Set default variables. Required variables are blank
    URL = ''
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
    USE_HTTPS = True
    TIMEOUT = 0
    DUMP_URLS_TO_FILE = False
    URL_OUTPUT_FILE_NAME = "urls.txt"
    DOWNLOAD_IMGS = True

    #get command line arguments and plug in here
    try:
        cmd_options = ["help", "output=", "url=", "http", "user-agent=", "no-dl", "timeout="]
        options, args = getopt.getopt(cargs, [], cmd_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    for currArg, currVal in options:
        if currArg == "--help":
            print("4chanthread-imgdl Help: ")
            print("--output=\"output .txt file for URLs. For use with wget -i\"")
            print("--url=\"4chan or 4channel http or https URL goes here\" [REQUIRED]")
            print("--http Use HTTP instead of HTTPS")
            print("--user-agent=\"user agent string\" Specify your own user agent string")
            print("--no-dl Parse the thread, but do not download anything. For use with --output=")
            print("--timeout=\"int\" Specifies the time to wait (in seconds) between each image download")
            sys.exit(0)
        elif currArg == "--output":
            URL_OUTPUT_FILE_NAME = currVal
            DUMP_URLS_TO_FILE = True
        elif currArg == "--url":
            URL = currVal
        elif currArg == "--http":
            USE_HTTPS = False
        elif currArg == "--user-agent":
            USER_AGENT = currVal
        elif currArg == "--no-dl":
            DOWNLOAD_IMGS = False
        elif currArg == "--timeout":
            TIMEOUT = currVal

    #check validity of variables here (in particulat if url is blank)
    if URL == '':
        print("URL Must be present at least.")
        sys.exit(1)
    
    r = requests.get(URL, headers={'user-agent': USER_AGENT}) #request the page
    soup = BeautifulSoup(r.text, 'html.parser') #extract HTML text and put to parser
    possible_imgs = soup.find_all(target="_blank") #get all links to possible imgs
    filtered_imgs_url = []
    prefix='https:'
    if not USE_HTTPS:
        prefix='http:'
        print("Warning: HTTPS disabled.")
    for x in possible_imgs:
        if 'class' in x.attrs:
            if "fileThumb" in x.attrs['class']: #do not download thumbnails
                pass
        elif 'i.4cdn.org' in x['href']:
            filtered_imgs_url.append(prefix+x.get('href'))

    #dump urls to file option
    if DUMP_URLS_TO_FILE:
        write_to_file(filtered_imgs_url,URL_OUTPUT_FILE_NAME)

    #quit here of download disabled.
    if DOWNLOAD_IMGS:
        #create folder here first
        #for foldername, get numerical code + thread name
        #split url with delimiter "/" and get the last 2 indexes
        URL_split = URL.split('/')
        thread_id = URL_split[len(URL_split)-1]
        thread_title = URL_split[len(URL_split)-2]
        folder_name = thread_id + '-' + thread_title
        #make folder
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        print("[Download ", len(filtered_imgs_url), " Images.]")
        cnt = 1
        for url in filtered_imgs_url:
            fname = url.split('/')[-1] #get filename
            print("DL: ", fname, ", ", cnt, "/",len(filtered_imgs_url))
            save_path = folder_name + '/' + fname
            if not os.path.exists(save_path): #do not save images already there
                try:
                    urllib.request.urlretrieve(url, save_path)
                except:
                    if os.path.exists(save_path): #do not keep broken files
                        os.remove(save_path)
                    print("File failed to download.")
                else:
                    print("OK")
            else:
                print("File skipped(already exists).")
            cnt = cnt + 1
            if TIMEOUT > 0:
                time.sleep(TIMEOUT)

if __name__ == '__main__':
    main(sys.argv[1:])

