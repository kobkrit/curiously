#!/usr/bin/python
import web
import gv
import ast
import re
import urllib2

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
    
    
    def matchPOS(self, pos, parseTree, mode="Normal"):
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
            if (mode == "NP"):
                print item
                if (item.find("VP")>-1):
                    continue
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
            
            NP = index.matchPOS(self, "NP", parseTree, "NP")
            N = index.extractWord(self,NP)
            
            VBN = index.matchPOS(self, "V.*", parseTree)
            V = index.extractWord(self,VBN)
        return Q,N,V
    
    
    def GET(self):
        return render.index()
    
    def POST(self):
        data = web.input()
        question = data["question"]
        parsed = ast.literal_eval(gv.corenlp.parse(question))
        Q,N,V = index.extractAnswer(self, parsed)
        
        url="http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=place&QueryString="+N.replace(" ","%20")
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        fetch = response.read()
        print fetch
        answerText = "<ul>"
        answers = re.findall("<Description>(.+)</Description>",fetch)
        for answer in answers:
            answerText+="<li>"+answer+"</li>"
        answerText += "</ul>"
        
        #=======================================================================
        # url="https://d5gate.ag5.mpi-sb.mpg.de/webyagospotlx/Browser?entity="+N.replace(" ","_")
        # print url
        # req = urllib2.Request(url)
        # response = urllib2.urlopen(req)
        # fetch = response.read()
        # print fetch
        # answers = re.findall("(&nbsp;&nbsp;(.+)&nbsp;&nbsp;|/webyagospotlx/Browser\?entity=([^>]+)\>)",fetch)
        # for (a,b,c) in answers:
        #    if c =='':
        #        answerText+="<br><b>"+b+"</b>: "
        #    else:
        #        answerText+=c+","
        # answerText+="<br>"
        #=======================================================================
        
        return "<html>"+question+"<br>"+str((Q,N,V))+"<br>"+str(answerText)+"</html>"
    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    