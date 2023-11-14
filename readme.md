# YouTube Transcriber
This application is a YouTube Transcriber built with Python, Streamlit, AssemblyAI, and other libraries. It allows users to input a YouTube link and get the transcription of the audio in the video. The transcription is done using AssemblyAI's API.
<!-- ![YouTube Transcriber Site](./ytt/ytt.png "caption") -->
| ![YouTube Transcriber Site](https://i.ibb.co/WDDGmK2/ytt.png) |
|:--:|
| *YouTube Transcriber Homepage* |

## Features
- Transcribe YouTube videos
- Check the status of the transcription
- Download the transcription as subtitles in .srt format
- Convert the subtitles to lyrics and download them as a .txt file
- Toggle the display of the transcript

## How it Works
The application uses the `yt_dlp` library to download the audio from the YouTube video. The audio is then uploaded to - AssemblyAI's API for transcription. The status of the transcription can be checked and once it's completed, the transcript can be downloaded as subtitles in .srt format or as lyrics in a .txt file.

## Libraries Used
- `streamlit`: For creating the web application
- `assemblyai`: For transcribing the audio
- `yt_dlp`: For downloading the audio from YouTube videos
- `requests`: For making `HTTP` requests
- `re`: For regular expressions
- `pysrt`: For handling `.srt` files
- `threading`: For multithreading

## How to Run
1. Clone the repository
2. Install the required libraries from the `requirements.txt` file
3. Run the ytt.py file

## Note
This application requires an API key from AssemblyAI for the transcription. You can acquire one [here](https://www.assemblyai.com/app).

## Limitations
The formatting of the transcripts and overall speed still need some work.
