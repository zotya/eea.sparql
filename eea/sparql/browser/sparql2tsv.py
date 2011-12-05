from Products.Five import BrowserView

class SPARQL2TSV(BrowserView):
    def json(self):
        import pdb; pdb.set_trace();
        f = open('/home/zotya/Desktop/json1.txt', 'r')
        data = f.read()
        return data
