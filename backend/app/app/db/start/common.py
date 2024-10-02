import enum
import logging
import os
import pydantic_core
from pydash import omit

from app import crud
from app.models.bible import Bible, Book, BookTypeEnum, Chapter, Verse, Language
from app.db.session import SessionLocal
from app.schemas.bible import BibleItem

import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RulesEnum(enum.Enum):
    """Validation methods

    Args:
        enum (str): method name to call in validator
    """
    BOOK_COUNT = "book_count"
    BOOK_COUNT_BY_CATEG = "boot_count_by_category"
    BOOK_CATEGORY = "book_category"
    BOOK_CHAPTER_COUNT = "book_chapter_count"
    VERSE_COUNT = "count_verse"
    VERSE_TEXT = "verse_text"


class BibleValidator:
    
    def __init__(self, bible_id: int, rules: dict = {}) -> None:
        if bible_id <= 0:
            raise ValueError("Set a valid value to bible_id")
        self.db = SessionLocal()
        self.bible_id = bible_id
        self.rules = rules        
        self.version_filter = [Book.bible_id == self.bible_id]    
        
    def run(self):
        if self.rules:
            for rule, params in self.rules.items():                                          
                getattr(self, RulesEnum(rule).value)(*params)
        
    
    def book_count(self, expected):
        assert(self._q_book().count() == expected)  
        
    def boot_count_by_category(self, category, expected):        
        assert(self._q_book().filter(Book.category == category).count() == expected)
        
    def book_category(self, rank, expected):
        """assert books placed in right category     

        Args:
            rank (int): book rank
            expected (BookTypeEnum): expected category
        """
        assert(self._q_book().filter(Book.rank==rank).first().category == expected)
        
    def book_chapter_count(self, book_rank, expected_chapter_count):              
        assert(self._q_chapter().filter(Book.rank == book_rank).count() == expected_chapter_count)
        
    def count_verse(self, book_rank, chapter_rank, expected):        
        assert(self._q_verse().filter(
            Book.rank == book_rank, Chapter.rank==chapter_rank).count() == expected)
        
    def verse_text(self, book_rank, chapter_rank, verse_rank, expected):        
        v = self._q_verse().filter(
                Book.rank == book_rank, 
                Chapter.rank == chapter_rank,
                Verse.rank == verse_rank
            ).first()         
        assert(v is not None and v.content == expected)
        
    def _q_book(self):        
        return self.db.query(Book).filter(*self.version_filter)
    
    def _q_chapter(self):        
        return self.db.query(Chapter).join(Chapter.book).filter(*self.version_filter)
    
    def _q_verse(self):        
        return self.db.query(Verse).join(Chapter).join(Chapter.book).filter(*self.version_filter)
                    

class BibleImporter:

    def __init__(self,
                 lang: str,
                 version: str,   
                 encoding: str =  "UTF-8",                              
                 validation_rules: dict = {}
        ):
        self.db = SessionLocal()
        self.lang = lang
        self.language = None
        self._init_language()

        self.version = version
        self.bible_id = None
        self.validation_rules = validation_rules
        
        self.file_path = None
        self.file_type = None
        self.file_encoding = encoding               


    def import_version(self, bible_item: BibleItem):
        existing_version = self._get_existing_version()                
        if existing_version:
            # update to manage later            
            self.bible_id = existing_version.id
        else:        
            bible = Bible(**(omit(bible_item.__dict__, "books", "lang")))
            bible.lang_id = self.language.id
            crud.bible.create(self.db, bible)
            
            self.bible_id = bible.id # save newly created bible id, used later on
            logger.info("Bible %s inserted, id: %s", self.version, self.bible_id)
            
            books = bible_item.books
            for b in books:                
                book = Book(**(omit(b.__dict__, "chapters", "chapter_count")))
                book.category = BookTypeEnum(b.category)
                book.bible_id = bible.id
                crud.book.create(self.db, book)

                if b.chapters:
                    logger.info("%s Inserting book %s with %s chapters ...", 
                                self.version, book, len(b.chapters))
                    for chap in b.chapters:
                        chapter = Chapter(**(omit(chap.__dict__, "book_rank", "verses")))  # "book_id",
                        chapter.book_id = book.id
                        crud.chapter.create(self.db, chapter)

                        if chap.verses:
                            for v in chap.verses:
                                verse = Verse(**(omit(v.__dict__, "chapter_rank", "book_rank")))
                                verse.chapter_id = chapter.id
                                chapter.verses.append(verse)

            self.db.commit()
            logger.info("%s book inserted.", len(books))
            
        return self.bible_id

    def run_import(self):         
        self.import_data()         
        self.validate_data()     
        
    def import_data(self):                
        raise NotImplementedError
    
    def validate_data(self):
        """Checking bible content
        You can override this method if you want
        """
        logger.info("Checking bible %s data right now ...", self.version)
        BibleValidator(self.bible_id, self.validation_rules).run()                  
        logger.info("Checking done !") 
    
    def default_file_path(self):
        """Default file path to look for file to import           

        Returns:
            str: full path
        """
        return os.path.join(ROOT, 'data', 'bible', self.lang, f"{self.version}.{self.file_type}")  
        
    def _init_language(self):
        """Checks if lang to be used exists in db

        Raises:
            ValueError: if lang not found
        """
        self.language = crud.language.get_by_code(self.db, self.lang)
        if not self.language : 
            raise ValueError(f"Source language {self.lang} not found in db") 
            
    def _get_existing_version(self):       
        """Check if same version already exists in db

        Returns:
            int: count
        """
        return crud.bible.query_by_version(self.db, self.version).first()        
       
                

class JsonBible(BibleImporter):
    
    def __init__(self, *args, **kwargs):
        super(JsonBible, self).__init__(*args, **kwargs)
        self.file_type = 'json'        
    
    def import_data(self):
        """
        Import generic bible with <BibleItem> json format in input
        """        
        file_path = self.file_path or self.default_file_path()   
        with open(file_path, 'r+', encoding=self.file_encoding) as f:            
            datas = f.read()  
            bible_item = BibleItem.model_validate(pydantic_core.from_json(datas))  
            super().import_version(bible_item)                                       
                              
                