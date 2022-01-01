import json
from os import listdir
import os
import re
import re, string
from wrapper import wbgetentities
from wrapper import wbsearchentities
from nltk.tokenize import sent_tokenize

def filelist(path):
    filelist = listdir(path)
    fileIndex = []
    for i in range(0, len(filelist)):
        index = filelist[i].split(".")[0]
        fileIndex.append(int(index))
# new_filelist =[]
    for j in range(1, len(fileIndex)):
        for k in range(0, len(fileIndex) - 1):
            if fileIndex[k] > fileIndex[k + 1]:
                preIndex = fileIndex[k]
                preFile = filelist[k]
                fileIndex[k] = fileIndex[k + 1]
                filelist[k] = filelist[k + 1]
                fileIndex[k + 1] = preIndex
                filelist[k + 1] = preFile
    return filelist

def process_words(words):
    punc = '\n,.:#!\'?<>;"(){}-'
    # leftctx
    words = re.sub(r"[%s]+" % punc, "", words)
    words_list = words.split(' ')
    return words, words_list

def processwords(mention):
  import re
  punc = '\n,.:#!\'?<>;"{}-'
    # leftctx
  clean_mention = re.sub(r"[%s]+" % punc, "", mention).lower()
  words_list = clean_mention.split(' ')
  return clean_mention, words_list

def sentence_token_nltk(str):
    sent_tokenize_list = sent_tokenize(str)
    return sent_tokenize_list

if __name__ == '__main__':
    error = []
    dataset = {}
    error_mention =[]
#mention #left context #right context #gold - entityid entityname
    path = '/Users/maggiemin/Documents/gqp_bt/wpi-gqp-2020-master/basis-data/5f3d2f439b9af441309c99cb/adm/gold'
    labelpath = '/Users/maggiemin/Documents/gqp_bt/wpi-gqp-2020-master/basis-data/5f3d2f439b9af441309c99cb/adm/gold/'
    filelist = filelist(path)
    for file in filelist:
        print(file)
    #print(file)
        dataset[file] = []
        with open(labelpath+file, 'r', encoding='utf8')as f:
            data = json.load(f)
        #print(data)
            article = data['data']
            sentences = sentence_token_nltk(article)
            doc = {}
            doc['conll_doc'] = {}
            doc['conll_doc']['sentences'] = []
            doc['conll_doc']['mentions'] = []
            doc['conll_m'] = {}
            for s in sentences:
                _, sentence = process_words(s)
                doc['conll_doc']['sentences'].append(sentence)
            items = data['attributes']['entities']['items']
            for item in items:
                mention_pos = item['mentions'][0]
                end_pos = mention_pos['endOffset']
                print(end_pos)
                mention = article[mention_pos['startOffset']:mention_pos['endOffset']]
                mention,mentionlist = process_words(mention)
                #mention = mention.lower()
                print(mentionlist)
                m = {}

                sentid = 0
                sen_pos = 0
                status = 'f'
                for s in sentences:
                    sen_pos += len(s)+4
                    print(sen_pos)
                    _,sentence = process_words(s)
                    print(sentence)
                    if end_pos <= sen_pos:
                        if mentionlist[0] in sentence and mentionlist[-1] in sentence:
                            start = sentence.index(mentionlist[0])
                            end = sentence.index(mentionlist[-1])
                            lastsentid = sentid
                            m["sent_id"] = sentid
                            m["start"] = start
                            m["end"] = end
                            doc['conll_doc']['mentions'].append(m)
                            doc['conll_m'][mention] = m
                            status = 't'
                            break

                    sentid +=1
                # if status == 'f':
                #     m["sent_id"] = lastsentid
                #     m["start"] = 0
                #     m["end"] = 0
                #     doc['conll_doc']['mentions'].append(m)
                #     doc['conll_m'][mention] = m
                #     error.append(mention)

            dataset[file].append(doc)
    print(len(error))
    with open('/Users/maggiemin/Documents/gqp_bt/bt/train_sentence_relationwithoutlower.json', 'w') as f:
        json.dump(dataset, f)

    # with open('/Users/maggiemin/Documents/gqp_bt/bt/train_sentence_relation_error.txt', 'w') as f:
    #     f.write(str(error))