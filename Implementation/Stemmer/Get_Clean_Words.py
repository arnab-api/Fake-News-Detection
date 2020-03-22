import os
import json
import glob




def Discard_Punctuations(s):
    
    ret=""
    
    puncts = ["।", ",", "?", "!", "-", "_", "(", ")", "{", "}", "[", "]", "'", "ঃ", ";", "|", "\\", "\"", "/"]
    
    for i in range(0, len(s)):
        if(s[i] in puncts):
            continue
        if(s[i]=='\n' or s[i]=='\t'):
            ret+= " "
        else:
            ret+=s[i]
    
    return ret


def Discard_Stopwords(s):
    
    f = open("Bangla_Stopwords.txt", "r")
    stops = f.read()
    stops = stops.split('\n')
    
    words = s.split()
    
    ret = ""
    
    for i in range(0, len(words)):
        if(words[i] in stops):
            continue
        ret+=words[i]+" "
    
    return ret


def Process(str):
    
    ret = Discard_Punctuations(str)
    ret = Discard_Stopwords(ret)
    
    
    inFile = open("Inputs/in1.txt", "w")
    inFile.write(ret)
    inFile.close()
    
    os.system('javac Parser/Stemmer.java')
    os.system('java Parser/Stemmer')
    
    outFile = open("Outputs/in1.txt", "r")
    ret = outFile.read()
    
    return ret


out_data = []

for cat in glob.glob('category/*'):
    file_list = glob.glob(cat+"/*")
    for f in file_list:
        fl = open(f, "r")
        s = fl.read()
        # uni = str(s,'utf-8')
        # print(s)

        s = Process(s).strip()
        print(s)
        # print(cat.split('/')[-1], f.split('/')[-1])

        out_data.append({
                'category' : cat.split('/')[-1],
                'file_name' : f.split('/')[-1],
                'body' : s
                })
        break
    break
       

# with open('2_OUTs/Corpus.json', 'w') as outfile:
#         json.dump(out_data, outfile)
