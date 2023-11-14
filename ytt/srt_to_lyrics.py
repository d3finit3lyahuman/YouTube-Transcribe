import re

def srt_to_lyrics(srt_file_path, txt_file_path):
    with open(srt_file_path, 'r') as srt_file:
        srt_contents = srt_file.read()

    # Remove timestamps and numbering
    lyrics = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', '', srt_contents)

    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(lyrics)


if __name__ == '__main__':
    srt_to_lyrics('mpQUDxoQUyU.srt', 'lyrics.txt')
