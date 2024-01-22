class PubmedArticle:
    def __init__(self, data):
        self.medlineCitation = data.find("MedlineCitation")
        self.id = self.medlineCitation.find("PMID").text
        self.title = self.medlineCitation.find("Article/ArticleTitle").text
        self.abstract = ''
        self.words = []
        self.weight = 0
        self.meshHeadings = []

        self.fetchArticleText()
        self.fetchMeshHeadings()
        self.chAbstract = self.abstract

    def fetchArticleText(self):
        abstracts = self.medlineCitation.findall("Article/Abstract/AbstractText")
        for abstract in abstracts:
            self.abstract += ' ' + abstract.text
    
    def fetchMeshHeadings(self):
        headings = self.medlineCitation.findall("MeshHeadingList/MeshHeading/DescriptorName")
        for heading in headings:
            self.meshHeadings.append(heading.text)
