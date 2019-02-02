# 4chan Thread Image Downloader (4chanthread-imgdl)
Python3 script to download all full resolution images, webms in a 4chan thread. This includes images tagged as spoilers.
The main purpose of this program is **data archival**.

## How it works
The only required argument for the script is --url="4chan/4channel.org http/https URL here"
By default, the program will scan for all images(excluding thumbnails) on the thread, create a folder in the same directory the script is in, and place all downloaded images and webms there.

## Wget
This script can be used in conjunction with wget. To do this, first use --output"urls.txt" to output a text file of all images scanned in the thread. Next, prevent the program from downloading by adding --no-dl. This will cause the program to just scan the urls of the images and dump them all to a file. Use "wget -i url.txt" to download all the pictures.

## Warning
Do not be stupid. Do not use this to overload 4chan servers or cause excessive amounts of bandwidth to be used. I will not be responsible for how you use the software.

## Other arguments
1. "--timeout=x" -> Accepts an integer. Wait time (in seconds) between each picture download
2. "--http" -> Do not use https (HTTPS is used by default)
