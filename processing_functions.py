from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer,porter
from nltk.corpus import stopwords, wordnet

extra_stopwords = stopwords.words('english') + ['x','company','would','get','school','student','sally','salliemae','im','sallie','mae','loan','nt','wo','wa','tg','va','ca','mo','le','ha','sm','itt','k','smae']
extra_stopwords = extra_stopwords + ['not_' + x for x in extra_stopwords]

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(",".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

def top_words(model,feature_names,n_top_words):
    topics = []
    terms = []
    for topic_idx, topic in enumerate(model.components_):
        topics.append(topic_idx)
        terms.append(','.join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    return pandas.DataFrame({'topic':topics,'terms':terms},columns=['topic','terms'])    

def noPunct(txt):
    punct_list = string.punctuation + '’' + '”' + '“'
    for punct in punct_list:
        txt = txt.replace(punct,'')
    return txt

def noNumber(txt):
    return re.sub(r'[$\s]*\d+\.?\d*','',txt)

def addNegation(x):
    pattern = r'not (.+)[' + string.punctuation + r']'
    q = re.search(pattern,x,flags=re.IGNORECASE)
    if q is None:
        return x
    replacement = ['not_' + i for i in q.group(1).split(' ')]
    replacement = ' '.join(replacement)
    return x.replace(q.group(),replacement)

def pos_key(s):
    if s[0] == 'V':
        return wordnet.VERB
    elif s[0] == 'R':
        return wordnet.ADV
    elif s[0] == 'J':
        return wordnet.ADJ
    #Noun or other
    else:
        return wordnet.NOUN

def LemmaTokenizer(doc):
    wnl = WordNetLemmatizer()
    tokens = word_tokenize(doc)
    tokens = [noPunct(l) for l in tokens]
    tokens = [noNumber(l) for l in tokens]
    tokens = [t for t in tokens if len(t) > 0]
    tokens = [t for t in tokens if str.lower(t) not in extra_stopwords]
    tokens = [wnl.lemmatize(t[0],pos_key(t[1])) for t in pos_tag(tokens)]
    return tokens

def StemmerTokenizer(doc):
    port = porter.PorterStemmer()
    tokens = word_tokenize(doc)
    tokens = [noPunct(t) for t in tokens]
    tokens = [noNumber(l) for l in tokens]
    tokens = [t for t in tokens if len(t) > 0]
    tokens = [t for t in tokens if str.lower(t) not in extra_stopwords]
    tokens = [port.stem(t) for t in tokens]
    return tokens

