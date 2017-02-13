def operation(text,ID):
    from gensim.models.doc2vec import TaggedDocument

    from nltk import word_tokenize
    from nltk.stem import WordNetLemmatizer,porter
    from nltk.corpus import stopwords

    from autocorrect import spell
    import string
    import re

    def noPunct(txt):
        punct_list = string.punctuation + '’' + '”' + '“'
        for punct in punct_list:
            txt = txt.replace(punct,'')
        return txt

    def noNumber(txt):
        return re.sub(r'[$\s]*\d+\.?\d*','',txt)

    extra_stopwords = stopwords.words('english') + ['nt','wo','wa','tg','va','ca','mo','le','ha','sm','itt','k']

    def LemmaTokenizer(doc):
        wnl = WordNetLemmatizer()
        lemmas = [wnl.lemmatize(t) for t in word_tokenize(str.lower(doc))]
        lemmas = [noPunct(l) for l in lemmas]
        lemmas = [noNumber(l) for l in lemmas]
        lemmas = [x for x in lemmas if x not in extra_stopwords]
        lemmas = list(filter(lambda x: len(x) > 0,lemmas))
        return lemmas
    
    return TaggedDocument(LemmaTokenizer(text),['d'+str(ID)])