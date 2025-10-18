# Suhail

A friendly and simple software to help you make M3U playlists for your Sony Walkman/other MP3 players, probably

## Description
 
Making playlists for Sony Walkman MP3 players in [current year] is troublesome. Sony is incapable of developing a functional, bloat-free application and Windows Media Player is Windows Media Player, so I usually have to resort to copying file paths into a M3U file by hand. Nobody has time for that.

Thankfully, Suhail is now here! Suhail is a friendly software application designed to speed up making playlists for MP3 players with correct absolute pathing and encoding types. With Suhail, you can simply plug your Walkman into your computer, choose your music folder and start adding songs to a playlist using simple and clear buttons. Suhail will handle everything else for you and give you a finished M3U file! No more crying over complicated workarounds! 

I've tried to make Suhail **as user-friendly as possible** so that even people who *don't* live glued to their computers would be able to work these MP3 players a bit easier without tearing their hair out in frustration. If you can do basic file management and put MP3 files into the music folder on your Walkman, you can definitely work with Suhail!

### Features
* Easy playlist creation
* Import playlists and edit them with ease
* Encoding for dummies
* An inoffensive little guy for emotional support
* Literally nothing else

![A screenshot of the UI placed here to showcase how simple it is.](https://files.catbox.moe/i22jn5.png)
![Ditto, but this time with files displayed.](https://files.catbox.moe/77z3t7.png)


*P.S. This is my first Python project and I made it during a stressful all-nighter. I come from the land of JavaScript. Please have mercy*

## Getting Started

Download the latest release of Suhail and run the executable. Simple as that!
It might also help if you plug your MP3 player into your computer before you start making playlists for it.

## Help

#### *"My playlist is showing up on my device, but I can't see any of the songs when I go play it!"*

This is most likely an encoding issue. The device recognizes the file but cannot read the text properly. If your device is, for example, in Japanese, choose the correct encoding option for it. They've been haphazardly labeled for your convenience. You can also go change the encoding of a M3U file by opening it in Notepad.

#### *"The encoding is correct, but the files Suhail is generating don't work on my device!"*

Very much possible!

Suhail has been tested exclusively on a Sony Walkman NW-S13. This means I've tested the Shift_JIS encoding exclusively and the resulting M3U files have only been tested on my device. I'd guess that a program as simple as this one should generate valid playlists for a multitude of devices, but older tech is a complete fucking tossup and I cannot guarantee anything


## FAQ

#### *"Why is the program an anime boy?"*

We need more whimsy and joy in our lives.

#### *"Does this run on Linux/MacOS?"*

Not sure! Haven't tested! Not a priority, really. I could work this out on Ubuntu at some point, but MacOS users are on their own.


## Authors
Ellen alias Catskulls 
[catskulls.place](https://catskulls.place/)



#### Acknowledgments
Shout out to Kent Ito and his 1 minute 18 second cover of Magic Number I had on loop for 10 hours straight making this. Also Lisdexamfetamine
