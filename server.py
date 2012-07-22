#!/usr/bin/python
import web
import gv
import ast
import re

urls = ('/', 'index')
render = web.template.render('templates/')

class index:
    def matchTupleAC(self, A, C, tuples, words):
        print A, C
        for a,b,c in tuples:
            if (re.match(A,a) and re.match(C,c)):
                for word in words:
                    if word[0] == b:
                        return word
        return None
    
    def matchTupleAB(self, A, B, tuples, words):
        print A, B
        for a,b,c in tuples:
            if (re.match(A,a) and re.match(B,b)):
                for word in words:
                    if word[0] == c:
                        return word
        return None
    
    
    def matchPOS(self, pos, parseTree):
        toReturn = []
        list = [m.start() for m in re.finditer('(?=\('+pos+')', parseTree)]
        print list
        for start in list:
            level = 0
            keep = ""
            for ch in parseTree[start:]:
                if (ch == "("):
                    level+=1
                elif (ch == ")"):
                    level-=1
                keep+=ch
                if (level == 0):
                    break;
            toReturn.append(keep)
        return toReturn
    
    
    def extractAnswer(self, parsed):
        response = "<html>"
        for sentence in parsed['sentences']:
            #Log
            response+=str(sentence['text'])
            response+="<hr>"
            response+=str(parsed)
            response+="<hr>"
            
            parseTree = sentence['parsetree']
            
            
            QWs = index.matchPOS(self, "W.*", parseTree)
            response+="<b>All QWs:</b> "+str(QWs)+"<br>"
            QW = filter(lambda x: re.match("\([^\(\)]+\)",x), QWs)
            response+="<b>Good QW:</b> "+str(QW)+"<br>"
            
            #NounPhrase Extraction
            NPs = index.matchPOS(self, "N.*", parseTree)
            response+="<b>All NPs:</b> "+str(NPs)+"<br>"
            NP = filter(lambda x: re.match("\([^\(\)]+\)",x), NPs)
            response+="<b>Good NP:</b> "+str(NP)+"<br>"
    
            #Verb Extraction
            VBs = index.matchPOS(self, "V.*", parseTree)
            response+="<b>All VBs:</b> "+str(VBs)+"<br>"
            VB = filter(lambda x: re.match("\([^\(\)]+\)",x), VBs)
            response+="<b>Good VB:</b> "+str(VB)+"<br>"
            
            response+="<hr><hr>"

#===============================================================================
#        #Question Word Extraction
#        QuestionWord = None
#        print parsed['sentences'][0]
#        for a in parsed['sentences'][0]['words']:
#            if (re.match('W.*', a[1]['PartOfSpeech'])):
#                QuestionWord = a
#        if (QuestionWord == None):
#            response+="Please have at least one question word, e.g., What, When, Where, Which, Who, and How."
#            return response
#        
# 
#        MainVerb = index.matchTupleAC(self,'advmod', QuestionWord[0], parsed['sentences'][0]['tuples'], parsed['sentences'][0]['words'])
#        if (MainVerb == None):
#            response+="Please have at least one main verb, e.g., is, am, are, does, do, have, has, and etc."
#            return response;
#        response+="<b>MainVerb:</b> "+str(MainVerb[0])+"<br>"
#     
#        #MainTarget Extraction
#        MainTarget = index.matchTupleAB(self,'nsubj.*', str(MainVerb[0]), parsed['sentences'][0]['tuples'], parsed['sentences'][0]['words'])
#        if (MainTarget == None):
#           response+="Please have at least one noun, e.g., thing, Paris, human, ballon."
#           return response;
#        response+="<b>MainTarget:</b> "+str(MainTarget[0])+"<br>"
#        
#        #AuxVerb Extraction
#        AuxVerb = index.matchTupleAB(self,'.*mod', str(MainTarget[0]), parsed['sentences'][0]['tuples'], parsed['sentences'][0]['words'])
#        if (AuxVerb!=None):
#           response+="<b>AuxVerb:</b> "+str(AuxVerb[0])+"<br>"
#        
#    
#===============================================================================
        return response
    
    def GET(self):
        return render.index()
    
    def POST(self):
        data = web.input()
        parsed = ast.literal_eval(gv.corenlp.parse(data["question"]))
        return index.extractAnswer(self, parsed)
    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    