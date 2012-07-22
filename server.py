#!/usr/bin/python
import web
import gv
import ast

urls = ('/', 'index')

search = web.form.Form(
    web.form.Textbox('question'),
    web.form.Button('search'),
)


class index:
    
    def matchTuple(self, relation, subj, tuples, words):
        for a,b,c in tuples:
            if (b == relation and c == subj):
                for word in words:
                    if word[0] == a:
                        return word
        return None
    
    def extractAnswer(self, parsed):
        response = "<html>"
        response+=str(parsed)
        response+="<hr>"
        QuestionWord = None
        print parsed['sentences'][0]
        for a in parsed['sentences'][0]['words']:
            if (a[1]['PartOfSpeech']=='WRB'):
                QuestionWord = a
        
        if (QuestionWord == None):
            response+="Please have at least one question word, e.g., What, When, Where, Which, Who, and How."
            return response
        
        response+="<b>QuestionWord:</b> "+str(QuestionWord[0])+"<br>"
        
        MainVerb = index.matchTuple(self,'advmod', QuestionWord, parsed['sentences'][0]['tuples'], parsed['sentences'][0]['words'])
        
        if (MainVerb == None):
            response+="Please have at least one main verb, e.g., is, am, are, does, do, have, has, and etc."
            return response;
        
        response+="<b>MainVerb:</b> "+str(MainVerb[0])+"<br>"
    
        return response
    
    def GET(self):
        response = "<html><form name=\"input\" action=\".\" method=\"post\">";
        response += search().render()
        response += "</form></html>"
        return response
    
    def POST(self):
        data = web.input()
        parsed = ast.literal_eval(gv.corenlp.parse(data["question"]))
        return index.extractAnswer(self, parsed)
    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    