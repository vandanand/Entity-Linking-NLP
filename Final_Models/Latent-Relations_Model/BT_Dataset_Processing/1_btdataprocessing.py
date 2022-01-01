import json
from os import listdir
import os
import re
import re, string
from wrapper import wbgetentities
from wrapper import wbsearchentities

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

if __name__ == '__main__':
    error = []
    mention_num = 0
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
            mentions = data['attributes']
        #print(mentions)
            items = mentions['entities']['items']
        #print(items)
            for item in items:
                print(item['entityId'])
                mention_num +=1
                if not item['entityId'].startswith('Q'):
                    continue

                each = {}
                entity ={}
                mention_pos = item['mentions'][0]
                mention = article[mention_pos['startOffset']:mention_pos['endOffset']]
                leftctx = article[:mention_pos['startOffset']]
                rightctx = article[mention_pos['endOffset']:]

            #process left and right context
                leftctx, leftlist = process_words(leftctx)
                if len(leftlist) > 100:
                    leftctx = ' '.join(leftlist[-100:])
                rightctx, rightlist = process_words(rightctx)
                if len(rightlist)>100:
                    rightctx = ' '.join(rightlist[0:100])

                #get gold name
                entityid = item['entityId']
                entities = wbgetentities(entityid)
                if not 'entities' in entities:
                    error.append(entityid)
                    continue
                if 'labels' in entities['entities'][entityid]:
                    entityname = entities['entities'][entityid]['labels']['en']['value']
                else:
                    error.append(entityid)
                    continue
                #mention_num += 1
            # #get candidates
            #     candidates =[]
            #     entity = candidates_selection(mention, entity)
            #     print(len(entity))
            #     print(len(candidates))
            #
            # #get 10 candidates
            #     if len(entity)<10:
            #         _, mention_list = process_words(mention)
            #         if len(mention_list)>1:
            #             for i in range(1, len(mention_list)):
            #                 new_mention = ' '.join(mention_list[:-i])
            #                 print(new_mention)
            #                 entity = candidates_selection(new_mention, entity)
            #                 print(len(entity))
            #                 if len(entity)<10:
            #                     new_mention = ' '.join(mention_list[i:])
            #                     entity = candidates_selection(new_mention, entity)
            #                     print(len(entity))
            #                 if len(entity) == 10:
            #                     break
            #         else:
            #             mention_list = list(mention)
            #             for i in range(1,len(mention_list)):
            #                 new_mention = ''.join(mention_list[:-i])
            #                 print(new_mention)
            #                 entity = candidates_selection(new_mention, entity)
            #                 if len(entity)==10:
            #                     break
            #     if len(entity) < 10:
            #         error_mention.append(mention)
            #         error_mention.append(len(entity))
            #         error_mention.append(entityname)
            #         break

            # store values
                each["mention"] = mention
                each["leftctx"] = leftctx
                each["rightctx"] = rightctx
                #each["candidates"] = candidates
                each["gold"] = {}
                each["gold"]["entityid"] = entityid
                each["gold"]["entityname"] = entityname

                dataset[file].append(each)


#write
    # with open('/Users/maggiemin/Documents/gqp_bt/bt/test3_error2.txt', 'w') as f:
    #     f.write(str(error))
    with open('/Users/maggiemin/Documents/gqp_bt/bt/test3_output.json',"w") as file2:
        json.dump(dataset, file2)
    # print(mention_num)
    # print(len(error))
    #print(error)

