import os
import json




def Discard_Punctuations(s):
    
    ret=""
    
    puncts = ["।", ",", "?", "!", "-", "_", "(", ")", "{", "}", "[", "]", "'", "ঃ", ";", "|", "\\", "\"", "/", "⟨", "⟩", ",",  "،", "、", "‒",  "–",  "—",  "―", "‹", "›",  "«", "»", "‘", "’",  "“", "”",  "'", "'",  "′",  "″",  "‴"]
    
    for i in range(0, len(s)):
        if(s[i] in puncts):
            continue
        if(s[i]=='\n' or s[i]=='\t'):
            ret+= " "
        else:
            ret+=s[i]
    
    return ret


def Discard_Stopwords(s):
    
    f = open("Bangla_Stopwords.txt", "r" , encoding = 'utf-8')
    stops = f.read()
    stops = stops.split('\n')
    
    words = s.split()
    
    ret = ""
    
    for i in range(0, len(words)):
        if(words[i] in stops):
            continue
        ret+=words[i]+" "
    
    for sw in stops:
        ret = ret.replace(sw+' ', ' ')

    return ret


def Process(str):
    
    ret = Discard_Punctuations(str)
    ret = Discard_Stopwords(ret)
    
    print(ret , type(ret))
	
    inFile = open("Inputs/in1.txt", "w")
    inFile.write(ret)
    inFile.close()
    
    os.system('javac Parser/Stemmer.java')
    os.system('java Parser/Stemmer')
    
    outFile = open("Outputs/in1.txt", "r")
    ret = outFile.read()
    
    return ret


path = 'C:/Users/User/Desktop/Thesis_Windows/Bangla Newspapers/'
with open(path + "kaler_kantho_cleaned_5.json", "r" , encoding='utf8') as read_file:
    
    data = json.load(read_file)
    
    size = len(data)
    
    print("Data Loaded !!")
    
    out_data = []  
    
    cnt=0
    
    for i in range(0, 5):
        head = Process(data[i]['headline']).strip()
        body = Process(data[i]['body']).strip()
        
        if(cnt%100==0):
            print(cnt, " of ", size)
        
        cnt+=1
        
        out_data.append({
                'headline' : head,
                'body' : body
                })
    
    with open('OUTPUT/kaler_kantha_out_4.json', 'w') as outfile:
        json.dump(out_data, outfile)


