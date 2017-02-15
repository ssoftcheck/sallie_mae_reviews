def operation(text,ID):
    from gensim.models.doc2vec import TaggedDocument
    exec(open('processing_functions.py',encoding='utf-8').read())
    
    return TaggedDocument(LemmaTokenizer(str.lower(text)),['d'+str(ID)])