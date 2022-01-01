import argparse
import os
import json
# import preprocessing.util as util
import re

def process_BT(in_filepath, out_filepath = "/Users/hexinlu/Desktop/GQP/end2end_neural_el-master/data/new_datasets/BT-data.txt"):
    # entityNameIdMap = util.EntityNameIdMap()
    # entityNameIdMap.init_compatible_ent_id()
    # gold paths: all the path t
    gold_paths = []
    # queue = [in_filepath]
    queue = ["/Users/hexinlu/Desktop/GQP/end2end_neural_el-master/data/basic_data/basis-data"]
    files = []
    while queue:
        path = queue.pop(0)
        li = os.listdir(path)
        for item in li:
            if item == "gold":
                gold_paths.append(os.path.join(path,item))
            elif os.path.isdir(os.path.join(path,item)):
                queue.append(os.path.join(path,item))
            else: continue
    for path in gold_paths:
        for file in os.listdir(path):
            files.append(os.path.join(path,file))
    pair_num = 0
    BTDB_num = 0
    unknown_id = 0
    file_num = 0
    # 原来的包括staroff不包括endoff
    # 文本格式：\n\n换行，并且在一些地方有/，
    #          3。标点符号处理：单独作为一行，但是换的时候需要看看是否是全部都有
    # 需要输出的内容：还有一些数量的需要
    with open(out_filepath,"w") as fout:
        print(fout)
        for file in files:
            file_num+= 1
            with open(file) as fin:
                data = json.load(fin)
                fout.write("DOCSTART_"+data['documentMetadata']['title'][0].replace(' ','_')+"\n")
                text = data['data'][:-1] #这里先去掉一个
                cur = 0
                for item in data["attributes"]["entities"]["items"]:
                    pair_num+=1
                    if item["entityId"][0] =="E":
                        BTDB_num+=1
                        continue
                    start = item["mentions"][0]["startOffset"]
                    end = item["mentions"][0]["endOffset"]
                    # fout.write(word +'\n' for word in text[cur:start].split())
                    # 保留分割符号进行分割
                    # 要解决的问题，分隔（空格，标点符号，\n\n单独分开不变号）
                    textPart = text[cur:start]
                    paraText = textPart.replace("\n\n"," *NL*")
                    wordList = re.split(r'([\s,.:!\'?<>;"(){}-])',paraText)
                    for word in wordList:
                        if word and word.isspace()==False:
                            fout.write(word + '\n')
                    # spaceFreelist = textPart.replace("\n\n"," *NL*")
                    # spaceFreelist.split()
                    # wordList = []
                    # for words in spaceFreelist:
                    #     wordList += re.split(r'([,.:!\'?<>;"(){}-])',words)
                    # # fout.write(word + '\n' for word in wordList if word)
                    # for word in wordList:
                    #     if word:
                    #         fout.write(word + '\n')

                    wiki_title = text[start:end].replace(" ","_")
                    wiki_id = item["entityId"][1:]
                    # new_ent_id = entityNameIdMap.compatible_ent_id(wiki_title,wiki_id)
                    new_ent_id = wiki_id
                    if new_ent_id is not None:
                        fout.write("MMSTART_"+ new_ent_id+"\n")
                        # fout.write(word+"\n" for word in text[start:end].split())
                        textPart = text[start:end]
                        paraText = textPart.replace("\n\n", " *NL*")
                        wordList = re.split(r'([\s,.:!\'?<>;"(){}-])', paraText)
                        for word in wordList:
                            if word and word.isspace() == False:
                                fout.write(word + '\n')
                        # spaceFreelist = textPart.replace("\n\n", " *NL*")
                        # spaceFreelist.split()
                        # wordList = []
                        # for words in spaceFreelist:
                        #     wordList += re.split(r'([,.:!\'?<>;"(){}-])', words)
                        # # fout.write(word + '\n' for word in wordList)
                        # for word in wordList:
                        #     if word:
                        #         fout.write(word + '\n')
                        fout.write("MMEND\n")
                    else:
                        unknown_id+=1
                        # fout.write(word + "\n" for word in text[start:end].split())
                        textPart = text[start:end]
                        paraText = textPart.replace("\n\n", " *NL*")
                        wordList = re.split(r'([\s,.:!\'?<>;"(){}-])', paraText)
                        for word in wordList:
                            if word and word.isspace() == False:
                                fout.write(word + '\n')
                    cur = end
                # fout.write(word+"\n" for word in text[end:].split())
                textPart = text[end:]
                paraText = textPart.replace("\n\n", " *NL*")
                wordList = re.split(r'([\s,.:!\'?<>;"(){}-])', paraText)
                for word in wordList:
                    if word and word.isspace() == False:
                        fout.write(word + '\n')
                fout.write("DOCEND\n")

    print("processBT   pair_num:", pair_num)
    print("processBT   BTDB_num", BTDB_num)
    print("processBT   unknown_id", unknown_id)
    print("processBT   file_num", file_num)





def creat_necessary_folders():
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--BT_folder", default="../data/basic_data/")
    parser.add_argument("--output_folder", default= "../data/new_datasets/")
    return parser.parse_args()

if __name__ == "_main_":
    args = _parse_args()
    creat_necessary_folders()
    print(args.BT_folder+"basis-data")
    process_BT(args.BT_folder+"basis-data", args.output_folder+"BT_train.txt")

# print(process_BT("/Users/hexinlu/Desktop/GQP/wpi-gqp-2020-master/basis-data","out_filepath1"))
args = _parse_args()
creat_necessary_folders()
print(args.BT_folder+"basis-data")
process_BT(args.BT_folder+"basis-data",)