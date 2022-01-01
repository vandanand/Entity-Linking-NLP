import json
with open('/Users/maggiemin/Downloads/train3_finaltestoldwiki2.json', 'r') as f:
    dataset = json.load(f)

with open('/Users/maggiemin/Documents/gqp_bt/bt/train_sentence_relationwithoutlower.json', 'r') as f:
    dataset2 = json.load(f)

newdataset = {}
num=0
for i in range(1, len(dataset) + 1):


    newdataset[str(i) + '.json'] = []
    for each in dataset[str(i) + '.json']:
        eachnew = {}
        data = dataset2[str(i) + '.json']
        mention = each['mention']

        if mention in data[0]['conll_m']:
            num+=1
            eachnew['mention'] = each['mention']
            eachnew['context'] = each['context']
            eachnew['gold'] = each['gold']
            eachnew['candidates'] = each['candidates']
            eachnew['conll_doc'] = data[0]['conll_doc']
            eachnew['conll_m'] = data[0]['conll_m'][mention]
            newdataset[str(i) + '.json'].append(eachnew)
    if newdataset[str(i) + '.json'] == []:
        newdataset.pop(str(i) + '.json')
print(num)
print(len(newdataset))
with open('/Users/maggiemin/Documents/gqp_bt/train4_finalinputtestoldwiki2.json', 'w') as f:
    json.dump(newdataset, f)
