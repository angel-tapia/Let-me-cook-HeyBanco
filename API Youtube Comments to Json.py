import os
import json
import googleapiclient.discovery

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyA-Ob-GrL8WpOKJOvKnKNwvvnfyJ3R8gDE"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    # Videos to be analyzed
    videos = ['1UB3ItLqDis', 'j0uh_yqhPe4', 'XTfJTbIjxbs', 'G46hKv1xPAo', 'ab8GxZJoadU', 'pa1KVQk7Jxk']
            # , 'TQvS7zW9wwo',
            # 'xrkqZpnEDWQ', 'v_0trHKMqXg', 'fxt32Cp3Vhc', 'Udh6HMCFhwY', 'WEAPmWsz7yw', 'haJSw_hopSw', '6NhSf9gT5hc',
            # 'd8ATQAQ8ieo', '-XOfPkgkqxU', 'ALIaTVQ0S8I', 'm279rGnkDAM', 'jEvPFHuv-Vo', '9QB3kiE6j_A', 'CbLoUYT37tc',
            # 'IGeMyLKsBHo', 'DagO_N1CJZA'
            # ]
    
    # Dictionary mapping video IDs to their corresponding banks
    video_banks = {
        '1UB3ItLqDis': 'heybanco',
        'j0uh_yqhPe4': 'heybanco',
        'XTfJTbIjxbs': 'heybanco',
        'G46hKv1xPAo': 'heybanco',
        'ab8GxZJoadU': 'heybanco',
        'pa1KVQk7Jxk': 'heybanco',
    }
    
    ignore = {
        'TQvS7zW9wwo': 'bbva',
        'xrkqZpnEDWQ': 'bbva',
        'v_0trHKMqXg': 'bbva',
        'fxt32Cp3Vhc': 'bbva',
        'Udh6HMCFhwY': 'bbva',
        'WEAPmWsz7yw': 'bbva',
        'haJSw_hopSw': 'NuBank',
        '6NhSf9gT5hc': 'NuBank',
        'd8ATQAQ8ieo': 'NuBank',
        '-XOfPkgkqxU': 'NuBank',
        'ALIaTVQ0S8I': 'NuBank',
        'm279rGnkDAM': 'NuBank',
        'jEvPFHuv-Vo': 'Santander',
        '9QB3kiE6j_A': 'Santander',
        'CbLoUYT37tc': 'Santander',
        'IGeMyLKsBHo': 'Santander',
        'DagO_N1CJZA': 'Santander'
    }

    
    comments_json = []  # create an empty list for JSON objects
    number = 0  # Number represents the current video we are analyzing

    for video in videos:
        if video_banks[video] != 'heybanco':
            continue
        number += 1
        request = youtube.commentThreads().list(
            part='snippet,replies',
            maxResults=100,
            videoId=video,
            order='time',
            textFormat='plainText',
        )

        while True:
            response = request.execute()
            for comment in response['items']:
                text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                replies = []

                if comment['snippet']['totalReplyCount'] > 0:
                    for reply in comment['replies']['comments']:
                        replies.append(reply)

                comment_json = {
                    "date": comment['snippet']['topLevelComment']['snippet']['publishedAt'],
                    "contenido": text,
                    "source": 'Youtube',
                    "bank": video_banks[video],
                }
                comments_json.append(comment_json)

                for reply in replies:
                    reply_json = {
                        "date": reply['snippet']['publishedAt'],
                        "contenido": reply['snippet']['textDisplay'],
                        "source": 'Youtube',
                        "bank": video_banks[video],
                    }
                    comments_json.append(reply_json)

            if 'nextPageToken' not in response:
                break
            else:
                request = youtube.commentThreads().list(
                    part='snippet,replies',
                    maxResults=100,
                    videoId=video,
                    order='time',
                    textFormat='plainText',
                    pageToken=response['nextPageToken']
                )

    comments_json_str = json.dumps(comments_json, indent=4)
    with open('Youtube.json', 'w', encoding='utf-8') as f:
        f.write(comments_json_str)

    with open('textMessagesYoutube.txt', 'w', encoding='utf-8') as f:
        for comment in comments_json:
            f.write(comment['contenido'] + '\n')

if __name__ == "__main__":
    main()