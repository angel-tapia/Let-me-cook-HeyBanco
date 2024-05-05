import os
import json
import googleapiclient.discovery

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from youtube_transcript_api import YouTubeTranscriptApi


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyA-Ob-GrL8WpOKJOvKnKNwvvnfyJ3R8gDE"
youtube = googleapiclient.discovery.build(
  api_service_name, api_version, developerKey=DEVELOPER_KEY)

videos = ['1UB3ItLqDis', 'j0uh_yqhPe4', 'XTfJTbIjxbs', 'G46hKv1xPAo', 'ab8GxZJoadU', 'pa1KVQk7Jxk']

answer = ""

for video in videos:
  print(video)
  transcript = YouTubeTranscriptApi.get_transcript(video, languages=['es'])
  if(transcript != None):
     print("aqui")

  processedTranscript = ""

  for entry in transcript:
      processedTranscript += entry['text'] + " "

  answer += processedTranscript + '\n\n\n\n'

with open('testingotro.txt', 'w', encoding='utf-8') as f:
  f.write(answer)

print(answer)