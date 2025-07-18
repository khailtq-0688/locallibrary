from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices

class FieldConstants:
    MAX_LENGTH_NAME = 200
    MAX_LENGTH_ISBN = 13
    MAX_LENGTH_SUMMARY = 1000
    MAX_LENGTH_IMPRINT = 200
    MAX_LENGTH_AUTHOR_NAME = 100
    BOOK_INSTANCE_STATUS_MAX_LENGTH = 1
    PAGINATION_PER_PAGE = 10

class HelpTexts:
    GENRE_NAME = _("Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    LANGUAGE_NAME = _("Enter the book's natural language (e.g. English, French, Japanese etc.)")
    SUMMARY = _("Enter a brief description of the book")
    ISBN = _('13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    GENRE_FIELD = _("Select a genre for this book")
    BOOK_ID = _("Unique ID for this particular book across whole library")
    BOOK_AVAILABILITY = _("Book availability")

class LoanStatus(TextChoices):
    MAINTENANCE = 'm', _('Maintenance')
    ON_LOAN = 'o', _('On loan')
    AVAILABLE = 'a', _('Available')
    RESERVED = 'r', _('Reserved')
