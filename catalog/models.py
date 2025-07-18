from django.db import models

# Create your models here.

from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import date

from .constants import (
    FieldConstants,
    HelpTexts,
    LoanStatus,
)

class Genre(models.Model):
    
    name = models.CharField(
        max_length=FieldConstants.MAX_LENGTH_NAME,
        unique=True,
        help_text= HelpTexts.GENRE_NAME
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message=_("enre already exists (case insensitive match)")
            )
        ]

class Language(models.Model):
    
    name = models.CharField(max_length=FieldConstants.MAX_LENGTH_NAME,
                            unique=True,
                            help_text=HelpTexts.LANGUAGE_NAME)

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = _("Language already exists (case insensitive match)")
            ),
        ]

class Author(models.Model):
    
    first_name = models.CharField(max_length=FieldConstants.MAX_LENGTH_AUTHOR_NAME)
    last_name = models.CharField(max_length=FieldConstants.MAX_LENGTH_AUTHOR_NAME)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    

class Book(models.Model):

    title = models.CharField(max_length=FieldConstants.MAX_LENGTH_NAME)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    summary = models.TextField(
        max_length=FieldConstants.MAX_LENGTH_SUMMARY, help_text=HelpTexts.SUMMARY)
    isbn = models.CharField(_('ISBN'), max_length=FieldConstants.MAX_LENGTH_ISBN,
                            unique=True,
                            help_text=HelpTexts.ISBN)
    genre = models.ManyToManyField(
        Genre, help_text=HelpTexts.GENRE_FIELD)
    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = _('Genre')
    
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    

class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text=HelpTexts.BOOK_ID)
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=FieldConstants.MAX_LENGTH_IMPRINT)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
        )

    status = models.CharField(
        max_length=FieldConstants.BOOK_INSTANCE_STATUS_MAX_LENGTH,
        choices=LoanStatus.choices,
        blank=True,
        default=LoanStatus.MAINTENANCE,
        help_text=HelpTexts.BOOK_AVAILABILITY,
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)
