import textacy
from textacy.extract import triples
import spacy
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


class GutenPro:

    def __init__(self,book):
        """
        Constructor for the GutenPro class
        Args:
            book: A http link to a guntenberg resource (i.e https://www.gutenberg.org/files/46/46-h/46-h.htm)
        """
        r = requests.get(book)
        self.soup=BeautifulSoup(r.content,features="lxml")


    """""""""""""""""""""""""""
    #
    #     PRIVATE METHODS
    #
    """""""""""""""""""""""""""

    def _find_chapters(self):
        self.chapters =[]
        if self.soup.findAll('h2'):
            self.chapters.extend(self.soup.findAll('h2'))
        elif self.soup.findAll('div',{"class": "chapter"}):
            self.chapters.extend(self.soup.findAll('div',{"class": "chapter"}))
        elif self.soup.findAll('p',{"class": "ph1"}):
            self.chapters.extend(self.soup.findAll('p',{"class": "ph1"}))
        elif self.soup.findAll('h3'):
            if self.soup.findAll('h2'):
                self.chapters.extend(self.soup.findAll('h2'))
            else:
                self.chapters.extend(self.soup.findAll('h3'))
        elif self.soup.findAll('h4'):
            if self.soup.findAll('h2'):
                self.chapters.extend(self.soup.findAll('h2'))
            else:
                self.chapters.extend(self.soup.findAll('h4'))
        else:
            self.chapters.extend(self.soup.findAll('h3'))

    def _process_chapters(self):
        self.chapter_map = {}
        iter_chapters=tqdm(self.chapters,colour='green')
        for chapter in iter_chapters:
            title = chapter.text.strip()
            iter_chapters.set_description(f'Processing chapter: {title}')
            paras = []

            nextNode = chapter
            got_a_p=False
            while True:
                try:
                    nextNode = nextNode.next_sibling
                except AttributeError:
                    print("This time the heuristic did not work")
                    break
                if nextNode == "\n":
                    nextNode = nextNode.next_sibling
                try:
                    tag_name = nextNode.name
                except AttributeError:
                    tag_name = ""
                if tag_name == "p":
                    got_a_p=True
                    paras.append(nextNode.getText())
                else:
                    if got_a_p:
                        break
            self.chapter_map[title] = paras

    """""""""""""""""""""""""""
    #
    #     PUBLIC METHODS
    #
    """""""""""""""""""""""""""


    def chapterize(self):
        """
        This function tries to identify chapters.
        The algorithm is based on some heuristics that do not work all times. Sorry!

        Returns:
            DataFrame: A dataframe where rows are paragraphs and columns are the chapters. Columns' names are the chapter title

        """
        self.chapters = self._find_chapters()
        self.chapter_map = self._process_chapters()
        self.df_chapter_map=pd.DataFrame.from_dict(self.chapter_map,orient='index').fillna(value='NA').transpose()
        return self.df_chapter_map

    def get_spacy_doc(self):
        self.spacy_model_name = 'en_core_web_sm'
        if not spacy.util.is_package(self.spacy_model_name):
            spacy.cli.download(self.spacy_model_name)

        for column in self.df_chapter_map:
            docs=[]
            for eachvalue in self.df_chapter_map[column].values:
                docs.append(textacy.make_spacy_doc(eachvalue,self.spacy_model_name))
            newcolumn=column+' spacy_docs'
            self.df_chapter_map[newcolumn]=docs
        return self.df_chapter_map

    def get_quoted_speech(self):
        my_df=self.get_spacy_doc()
        for column in my_df[[col for col in my_df if col.endswith('spacy_docs')]]:
            quotes=[]
            for spacy_doc in my_df[column].values:
               quotes.append(triples.direct_quotations(spacy_doc))
            newcolumn=column+'_quotes'
            my_df[newcolumn]=quotes
        return my_df
