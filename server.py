#!/usr/bin/python
import web
import gv
import ast
import re

urls = ('/', 'index')
render = web.template.render('templates/')

class index:
    def matchTupleAC(self, A, C, tuples, words):
        toReturn = []
        for a,b,c in tuples:
            if (re.match(A,a) and re.match(C,c)):
                for word in words:
                    if word[0] == b:
                        toReturn.append(word)
        return toReturn
    
    def matchTupleAB(self, A, B, tuples, words):
        toReturn = []
        for a,b,c in tuples:
            if (re.match(A,a) and re.match(B,b)):
                for word in words:
                    if word[0] == c:
                        toReturn.append(word)
        return toReturn
    
    
    def matchPOS(self, pos, parseTree):
        all = []
        lenMax = 0
        textMax = ""
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
            all.append(keep)
            
        for item in all:
            if lenMax<len(item):
                lenMax = len(item)
                textMax = item
        return textMax
    
    def extractWord(self, item):
        return " ".join(re.findall("\([A-Z]{2,3} ([^\(\)]+)\)",item))
    
    def extractAnswer(self, parsed):
        for sentence in parsed['sentences']:            
            parseTree = sentence['parsetree']
            
            QW = index.matchPOS(self, "W.*", parseTree)
            Q = index.extractWord(self,QW)
            
            
            NP = index.matchPOS(self, "NP", parseTree)
            N = index.extractWord(self,NP)
            
            VBN = index.matchPOS(self, "VBN", parseTree)
            V = index.extractWord(self,VBN)
        return Q,N,V
    
    
    def GET(self):
        return render.index()
    
    def POST(self):
        data = web.input()
        question = data["question"]
        parsed = ast.literal_eval(gv.corenlp.parse(question))
        Q,N,V = index.extractAnswer(self, parsed)
        return "<html>"+question+"<br>"+str((Q,N,V))+"</html>"
    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    