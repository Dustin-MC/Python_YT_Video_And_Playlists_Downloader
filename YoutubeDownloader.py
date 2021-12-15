#Youtube downloade (by kixne - DustinMC)
#Version: 21.12.14

import platform
from os import system
from os import path
from os import mkdir
from io import open

import pickle
from typing import Counter

from pytube import Playlist
from pytube import YouTube
from pytube.cli import on_progress

import ffmpeg
from os import remove


#__Functions
def ClearConsole():
 if user_os== "Linux" or user_os=="Darwin": system("clear")
 elif user_os== "Windows": system("cls")

def GetMenuOption():
 global user_option
 while True:
  ClearConsole()
  try:
   return int(input("""Youtube Video Downloader
  (by Kixne - DustinMC)
  
  Menu:
   1. Start download
   2. Downloader settings
   3. Exit
   Option: """))
  except: pass

def GeneralCheking():
 #Cheking for temps directory
 if path.exists("./.ytd_temps") and path.isdir("./.ytd_temps"): pass
 else: mkdir("./.ytd_temps")

 #Cheking for downloads directory
 if path.exists("./ytd_downloads") and path.isdir("./ytd_downloads"): pass
 else: mkdir("./ytd_downloads")

 GetDownloaderSettings()

def GetDownloaderSettings():
 global ytd_settings

 try:
  settings_file= open("./.ytd_temps/ytd_settings.bin", "rb")
  ytd_settings= pickle.load(settings_file)
  settings_file.close()
  del(settings_file)
 
 except:
  ModifySettings(ytd_settings)

def ModifySettings(ytd_settings):
 #Video download quality
 while True:
  ClearConsole()
  try:
   ytd_settings["video_quality"]=int(input("""Quality to video downloads:
   1. 144p
   2. 240p
   3. 360p
   4. 480p
   5. 720p
   Option: """))
   if ytd_settings["video_quality"]>0 and ytd_settings["video_quality"]<=5:
    break
  except: pass
 if ytd_settings["video_quality"]==1:
  ytd_settings["video_quality"]="144p"
 elif ytd_settings["video_quality"]==2:
  ytd_settings["video_quality"]="240p"
 elif ytd_settings["video_quality"]==3:
  ytd_settings["video_quality"]="360p"
 elif ytd_settings["video_quality"]==4:
  ytd_settings["video_quality"]="480p"
 elif ytd_settings["video_quality"]==5:
  ytd_settings["video_quality"]="720p"

 #Audio download quality
 while True:
  ClearConsole()
  try:
   ytd_settings["audio_quality"]=int(input("""Quality to audio downloads:
   1. 048kbps
   2. 128kbps
   3. 160kbps
  Option: """))
   if ytd_settings["audio_quality"]>0 and ytd_settings["audio_quality"]<=3:
    break
  except: pass
 if ytd_settings["audio_quality"]==1:
  ytd_settings["audio_quality"]= "48kbps"
 elif ytd_settings["audio_quality"]==2:
  ytd_settings["audio_quality"]="128kbps"
 elif ytd_settings["audio_quality"]==3:
  ytd_settings["audio_quality"]="160kbps"

 #Enumerate playlist items?
 while True:
  ClearConsole()
  try:
   ytd_settings["enumerate_playlist_downloads"]=int(input("""Enumerate downloaded items of playlists:
   1. Yes
   2. No
  Option: """))
   if ytd_settings["enumerate_playlist_downloads"]==1 or ytd_settings["enumerate_playlist_downloads"]==2:
    break
  except: pass
 if ytd_settings["enumerate_playlist_downloads"]==1:
  ytd_settings["enumerate_playlist_downloads"]= True
 if ytd_settings["enumerate_playlist_downloads"]==2:
  ytd_settings["enumerate_playlist_downloads"]= False

 #Saving downloader settings
 ClearConsole()
 settings_file= open("./.ytd_temps/ytd_settings.bin", "wb")
 pickle.dump(ytd_settings, settings_file)
 settings_file.close()
 del(settings_file)
 print("Downloader settings updated!")
 input("\nPress 'Enter' to continue")

def SetPlaylistDirectoryName():
 # Playlist directory name (automatic or manual)
 while True:
  try:
   directory_name= int(input("""
   Directory name to save the playlist items
    1. Create it Automatically
    2. Create it Manually
    Option: """))
   if directory_name==1 or directory_name==2: break
  except: pass

 #Defining the directory name automatically
 if directory_name==1:
  directory_name= "Playlist"
  counter= 0
  while True:
   counter+=1
   if CheckDirectoryName(f"{directory_name}_{counter}"):
    directory_name= f"{directory_name}_{counter}"
    return directory_name
 #Defining the directory name manually
 else:
  while True:
   directory_name= input("Directory name: ")
   if CheckDirectoryName(directory_name):
    return directory_name

def CheckDirectoryName(directory_name):
 pass
 while True:
  if path.exists(f"./ytd_downloads/{directory_name}") and path.isdir(f"./ytd_downloads/{directory_name}"):
   return False
  else:
   mkdir(f"./ytd_downloads/{directory_name}")
   return True

def DownloadSource(video, video_index, source_len, directory_name):
 ClearConsole()
 print(f"""Video: {video_index}/{source_len}
 Title: {video.title}
 Time: {ParseSecondsToTime(video.length)}
 Author: {video.author}
 Date: {video.publish_date}""")

 #Creating final file path and name
 video_title= (video.title).replace("/",":")
 if directory_name!= None:
  if ytd_settings["enumerate_playlist_downloads"]==True:
   ceros= len(str(source_len))-len(str(video_index))
   if ceros>0:
    file_path= f"./ytd_downloads/{directory_name}/{'0'*ceros}{video_index}. {(video_title)}.mp4"
   else:
    file_path= f"./ytd_downloads/{directory_name}/{video_index}. {(video_title)}.mp4"
  else:
   file_path= f"./ytd_downloads/{directory_name}/{(video_title)}.mp4"
 else:
  file_path= f"./ytd_downloads/{(video_title)}.mp4"

 #Downloading video track (temp)
 video_chanel= video.streams.filter(adaptive=True, resolution=ytd_settings["video_quality"]).first()
 print(f"""
 Downloading video_channel...
 Size: {round((video_chanel.filesize)/1024**2, 2)}MiB or {video_chanel.filesize}bytes""")
 video_chanel.download(output_path="./.ytd_temps", filename="video_channel.mp4")

 #Downloading audio track (temp)
 audio_chanel= video.streams.filter(type="audio", abr=ytd_settings["audio_quality"]).first()
 print(f"""\n\n Downloading audio_channel...
 Size: {round((audio_chanel.filesize)/1024**2, 2)}MiB or {audio_chanel.filesize}bytes""")
 audio_chanel.download(output_path="./.ytd_temps", filename="audio_channel.mp3")
 
 #Merging audio and video tracks (Saving final file)
 MergeChannels(file_path)

 #Removing temporal audio and video channels
 remove("./.ytd_temps/video_channel.mp4")
 remove("./.ytd_temps/audio_channel.mp3")

def MergeChannels(final_path):
 # Adds the video and audio as an input for ffmpeg
 video = ffmpeg.input("./.ytd_temps/video_channel.mp4")
 audio = ffmpeg.input("./.ytd_temps/audio_channel.mp3")

 # Runs the FFMPEG module to join the audio and video
 ffmpeg.output(video, audio, final_path, acodec='copy', vcodec='copy').run()



def ParseSecondsToTime(sec):
 h, min= 0,0
 if sec>3600:
  h= sec//3600
  sec-= h*3600
 if sec>60:
  min= sec//60
  sec-= min*60
 return f"{h}:{min}:{sec}"

#Variables
user_option= None
user_os= platform.system()
ytd_settings= {}


GeneralCheking()

#Main Loop
while True:
 user_option= GetMenuOption()
 
 #Start download
 if user_option==1:
  ClearConsole()
  download_type= None
  directory_name= ""

  #Getting download type (playlist or single video)
  while True:
   try:
    download_type= int(input("""
    Download type:
     1. Playlist
     2. Single video
    Option: """))
    if download_type==1:
     directory_name= SetPlaylistDirectoryName()
     break
    elif download_type==2:
     break
   except: pass

  #Creating video or playlist object
  while True:
   ClearConsole()
   try:
    url= input("Youtube link: ")
    if download_type==1:
     source= Playlist(url)
     len(source)
     break
    else:
     video= YouTube(url, on_progress_callback=on_progress)
     break
   except: pass

  #Downloading source
  ClearConsole()
  if download_type==1:
   video_index= 0
   source_len= len(source)
   for video_url in source.video_urls:
    video= YouTube(video_url, on_progress_callback=on_progress)
    video_index+= 1
    DownloadSource(video, video_index,source_len, directory_name)
   ClearConsole()
   input("""Download finalized.
   
   Thanks by using Kixne Software.
    Press 'Enter' to continue """)
  else:
   DownloadSource(video, 1, 1, None)
   ClearConsole()
   input("""Download finalized.
   
   Thanks by using Kixne Software.
    Press 'Enter' to continue """)

 #Modifying downloader settings
 elif user_option==2:
  ClearConsole()
  print("Current downloader settings:")
  for x in ytd_settings.keys():
   print(f" {x}: {ytd_settings[x]}")
  while True:
   try:
    x= int(input("""\nChange settings?
    1. Yes
    2. No
    Option: """))
    if x==1:
     ModifySettings(ytd_settings)
     break
    elif x==2: break
   except: pass

 #Exit program
 elif user_option==3:
  ClearConsole()
  print("""
  Thaks by Using Kixne software.
  
  Remember:
   You can support us visiting:
   https://kixne.github.io/web
  
  Program finalized.
  """)
  quit()