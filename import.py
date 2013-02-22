import codecs
import nltk
import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words("german"))
stop_words.add('[ugs.]')

file_to_import='/home/venkatesh/Documents/DeutschKurz/dict.cc/DE-EN-38130.txt'
anki_import_file='/home/venkatesh/Documents/DeutschKurz/dict.cc/DE-EN-38130.anki_cards'
anki_import_cloze_file='/home/venkatesh/Documents/DeutschKurz/dict.cc/DE-EN-38130.anki_cloze'


vocab_list = codecs.open(file_to_import,encoding='utf-8',mode='r')
anki_import = codecs.open(anki_import_file,encoding='utf-8',mode='w')
vocab_stem_list=[]
sentence_list=[]

germanStemmer=nltk.stem.SnowballStemmer("german")

vocabMap = {}

for line in vocab_list:
    line = line.rstrip('\r\n')
    de_part,en_part=line.split('\t')
    vocabMap.setdefault(de_part,[])
    vocabMap[de_part].append(en_part)
    

for de_part,en_part in vocabMap.items():
    gender_info=re.search(r'{([^}]+)}',de_part)
    sentence_check=re.search(r'([\?!]|\.$)',de_part)
    if (gender_info != None):
        gender = gender_info.group(1)
        word = re.sub(r'{([^}]+)}','',de_part)
        word = re.sub(r'^(die|der|das)\s','',word)
        for part in re.split('\s',de_part):
            vocab_stem_list.append(germanStemmer.stem(part)) 
        if ( gender == 'm'):
            word = 'der '+word
            tag='mannlich'
        elif (gender in ['f','pl']):
            word = 'die '+word
            if (gender=='f'):
                tag='weiblich'
            else:
                tag='plural'
        elif (gender == 'n'):
            word = 'das '+word
            tag='neutral'
        anki_import.write(word+'\t'+', '.join(en_part)+'\t'+tag+'\n')
    elif (sentence_check != None):
        sentence_list.append(de_part)
    else:
        parts = re.split('\s',de_part)
        if len(parts) > 2:
                sentence_list.append(de_part)
        else:
            for part in parts:
                vocab_stem_list.append(germanStemmer.stem(part))
            anki_import.write(de_part+'\t'+', '.join(en_part)+'\t'+''+'\n')

anki_cloze_import = codecs.open(anki_import_cloze_file,encoding='utf-8',mode='w')
vocab_stem_set=set(vocab_stem_list)

for sword in stop_words:
    if sword in vocab_stem_set:
        vocab_stem_set.remove(sword)
start_sent = '<div><span style=" font-style: normal; font-weight: normal;">'
end_sent = '</span></div>'

for de_part in sentence_list:
    en_part=vocabMap[de_part]
    tokens = re.split('\s',de_part)
    for i,token in enumerate(tokens):
        stem = germanStemmer.stem(re.sub(r'[\.,\?,!\'"]','',token))
        if (stem in vocab_stem_set):
            tokens[i]='{{c1::'+token+'}}'
    de_sent = ' '.join(tokens)
    anki_cloze_import.write(', '.join(en_part)+' : '+de_sent+'\tsent\n')

anki_import.flush()
anki_import.close()

anki_cloze_import.flush()
anki_cloze_import.close()
            
        
            
    
