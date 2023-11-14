import spacy

nlp = spacy.load("fr_core_news_sm")


def show_ents(doc): 
    if doc.ents: 
        for ent in doc.ents:
            print(ent.text +' - '+ ent.label_ + ' - '+str(spacy.explain(ent.label_)))
    else:
        print("Aucune entité trouvée")

doc = nlp(u"I will eat next month in L.A for only 4$")
show_ents(doc);