# -*- coding: utf-8 -*-
"""
Original file is located at
    https://colab.research.google.com/drive/1fA9ZtjKcLYkpvIoliwefSwQTm1SV7Cmo
"""

import zipfile

from google.colab import drive

drive.mount('/content/drive/')

!unzip '/content/drive/My Drive/Colab Notebooks/model/textWithAnchorsFromAllWikipedia2014Feb.txt.zip'

f = open('/content/textWithAnchorsFromAllWikipedia2014Feb.txt')
mentions ={}
num_line = 0
for line in open('/content/textWithAnchorsFromAllWikipedia2014Feb.txt'):
  sentence = f.readline()
  num_line+=1
  if num_line % 1000 ==0:
      print(num_line,' ',len(mentions),' ','doingwell')
  if sentence.find('<doc id="') == -1:
      while sentence.find('<a href="') != -1:
          pos = sentence.find('<a href="')
          ent_start = pos + 9
          sentence = sentence[ent_start:]
          ent_end = sentence.find('">')
          entity = sentence[:ent_end]
          sentence = sentence[ent_end + 2:]
          men_end = sentence.find('</a>')
          mention = sentence[:men_end]
            # print(mention,entity)

          if mention not in mentions:
              mentions[mention] = {}
              mentions[mention]['total_freq'] = 1
              mentions[mention]['entities'] = {}
          else:
              mentions[mention]['total_freq'] += 1
          if entity not in mentions[mention]['entities']:
              mentions[mention]['entities'][entity] = 1

          else:
              mentions[mention]['entities'][entity] += 1
                #print(mentions)
f.close()

with open("/content/freq.json","w") as f:
    json.dump(mentions,f)

