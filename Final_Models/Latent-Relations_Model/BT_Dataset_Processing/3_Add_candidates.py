import json

with open("./freq.json","r") as f:
    json.dump(mentions,f)

with open('./test3_output.json', 'r') as f:
    dataset = json.load(f)

def prior_probability(mentions,mention,entity):
    freq = mentions[mention]['entities'][entity]
    total_freq = mentions[mention]['total_freq']
    prior_pro = '%.3f'%(freq/total_freq)
    return prior_pro
if __name__ == '__main__':
    total = 0
    num_30 = 0
    num_5 = 0
    error = 0
    newdataset = {}
    for i in range(1, len(dataset) + 1):
        newdataset[str(i) + '.json'] = []
        for each in dataset[str(i) + '.json']:
            new_each = {}
            # each mention
            mention = each['mention']
            # mention = processwords(mention)[0]
            context = []
            leftctx = each['leftctx']
            context.append(leftctx)
            rightctx = each['rightctx']
            context.append(rightctx)
            context = tuple(context)

            total += 1
            new_candidates = []
            entities = []
            if mention in mentions:
                for entity in list(mentions[mention]['entities'].keys()):
                    new_candidate = []
                    prior = prior_probability(mentions, mention, entity)
                    new_candidate.append(entity)
                    new_candidate.append(prior)
                    new_candidate = tuple(new_candidate)
                    new_candidates.append(new_candidate)
                    entities.append(entity)
            if len(new_candidates) >= 5:
                num_5 += 1
                new_candidates = sorted(new_candidates, key=lambda tup: tup[1], reverse=True)

                gold = []
                entity = each['gold']['entityname']
                gold.append(entity)
                gold.append(1e-5)
                gold.append(-1)
                gold = tuple(gold)
                # store
                new_each['mention'] = mention
                new_each['context'] = context
                new_each['candidates'] = new_candidates
                new_each['gold'] = gold

                newdataset[str(i) + '.json'].append(new_each)
                if len(new_candidates) >= 30:
                    num_30 += 1

            else:
                error += 1

    # print(num_5)
    # print(num_30)
    with open('./test3_finaltestoldwiki2.json', 'w') as f:
        json.dump(newdataset, f)