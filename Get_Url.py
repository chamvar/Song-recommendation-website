import requests
import re

def get_link(x):
    url = f"https://www.youtube.com/results?q={x}"
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count += 1
        if i == "WEB_PAGE_TYPE_WATCH":
            break
    if lst[count - 5] == "/results":
        raise Exception("No Video Found for this Topic!")
    return f"https://www.youtube.com{lst[count - 5]}"

def extract_video_id(youtube_url):
    pattern = r"(?<=v=)[a-zA-Z0-9_-]+"
    
    match = re.search(pattern, youtube_url)
    
    if match:
        video_id = match.group(0)
        return video_id
    else:
        return None