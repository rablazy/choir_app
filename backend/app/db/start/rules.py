from app.db.start.constants import (
    CHAPTER_VERSES_COUNT_EN,
    CHAPTER_VERSES_COUNT_FR,
    CHAPTER_VERSES_COUNT_MG,
)
from app.db.start.import_version import RulesEnum
from app.models.bible import BookTypeEnum

STANDARD_RULES = [
    (RulesEnum.BOOK_COUNT, [66]),
    (RulesEnum.BOOK_COUNT_BY_CATEG, [BookTypeEnum.OLD, 39]),
    (RulesEnum.BOOK_COUNT_BY_CATEG, [BookTypeEnum.NEW, 27]),
    (RulesEnum.BOOK_CATEGORY, [16, BookTypeEnum.OLD]),
    (RulesEnum.BOOK_CATEGORY, [60, BookTypeEnum.NEW]),
    (RulesEnum.BOOK_CHAPTER_COUNT, [1, 50]),
    (RulesEnum.BOOK_CHAPTER_COUNT, [27, 12]),  # DAN 12 chapters
    (RulesEnum.VERSE_COUNT, [28, 4, 19]),  # HOS 4 - 19 verses
    (RulesEnum.VERSE_COUNT, [49, 6, 24]),  # EFE  6 - 24 verses
    (RulesEnum.ALL_VERSE_PRESENT, []),
    # check subtitle for mg1886
]

MG_RULES = [
    (RulesEnum.COUNT_ALL_VERSE, [31099]),
    (RulesEnum.COUNT_ALL_VERSE, [23141, BookTypeEnum.OLD]),
    (RulesEnum.COUNT_ALL_VERSE, [7958, BookTypeEnum.NEW]),
    (RulesEnum.COUNT_VERSE_PER_BOOK, [CHAPTER_VERSES_COUNT_MG]),
] + STANDARD_RULES

EN_RULES = [
    (RulesEnum.COUNT_VERSE_PER_BOOK, [CHAPTER_VERSES_COUNT_EN]),
]

FR_RULES = [
    (RulesEnum.COUNT_VERSE_PER_BOOK, [CHAPTER_VERSES_COUNT_FR]),
]

KJV_RULES = (
    [
        (
            RulesEnum.VERSE_TEXT,
            [
                66,
                20,
                11,
                "And I saw a great white throne, and him that sat on it, from whose face the earth and the heaven fled away; and there was found no place for them.",
            ],
        )
    ]
    + STANDARD_RULES
    + EN_RULES
)

DIEM_RULES = [
    (RulesEnum.BOOK_COUNT, [73]),
    (RulesEnum.BOOK_COUNT_BY_CATEG, [BookTypeEnum.OLD, 39]),
    (RulesEnum.BOOK_COUNT_BY_CATEG, [BookTypeEnum.NEW, 27]),
    (RulesEnum.BOOK_COUNT_BY_CATEG, [BookTypeEnum.APOCRYPHAL, 7]),
    (RulesEnum.BOOK_CATEGORY, [38, BookTypeEnum.OLD]),  # zakaria
    (RulesEnum.BOOK_CATEGORY, [41, BookTypeEnum.NEW]),  # marka
    (RulesEnum.BOOK_CATEGORY, [73, BookTypeEnum.APOCRYPHAL]),  # baroka
    (RulesEnum.BOOK_CHAPTER_COUNT, [14, 36]),  # 2 Tantara
    (RulesEnum.BOOK_CHAPTER_COUNT, [66, 22]),  # Apokalypsy
    (RulesEnum.BOOK_CHAPTER_COUNT, [72, 19]),  # Baroka
    (RulesEnum.VERSE_COUNT, [42, 8, 56]),  # Lioka 8.
    (RulesEnum.ALL_VERSE_PRESENT, []),
]
