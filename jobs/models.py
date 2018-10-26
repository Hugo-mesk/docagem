from django.db import models
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from djangocms_text_ckeditor.fields import HTMLField


# Create your models here.
class Attached_File(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    document = models.FileField()
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.document.name

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

class Pictures(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment = models.ImageField(verbose_name=_('Description'))
    user = models.ForeignKey(User, verbose_name=_('User'))
    creation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment.name

    class Meta:
        verbose_name = _("Picture")
        verbose_name_plural = _("Pictures")

class Drawings(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment = models.ImageField(verbose_name=_('Description'))
    user = models.ForeignKey(User, verbose_name=_('User'))
    creation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment.name

    class Meta:
        verbose_name = _("Drawing")
        verbose_name_plural = _("Drawings")


class Chapter(models.Model):
    title = models.CharField(verbose_name=_('Title'),
                              max_length=60)
    files = GenericRelation(Attached_File, verbose_name=_("Files"),
                            null=True,
                            blank=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.title)

    class Meta:
        verbose_name = _("Chapter")
        verbose_name_plural = _("Chapters")


class Concept(models.Model):
    number = models.PositiveIntegerField()
    title = models.CharField(verbose_name=_('Title'),
                              max_length=60)
    equipment = models.CharField(verbose_name=_('Equipment'),
                              max_length=60,
                              null=True,
                              blank=True)
    maker =  models.CharField(verbose_name=_('Maker'),
                              max_length=60,
                              null=True,
                              blank=True)
    serial_number = models.CharField(verbose_name=_('Serial Number'),
                                     max_length=60,
                                     null=True,
                                     blank=True)
    equipment_model =  models.CharField(verbose_name=_('Equipment Model'),
                              max_length=60,
                              null=True,
                              blank=True)
    description = models.TextField(verbose_name=_('Description'))
    html_description = HTMLField(configuration='CKEDITOR_SETTINGS',
                                null=True,
                                blank=True)
    files = GenericRelation(Attached_File, verbose_name=_("Files"),
                            null=True,
                            blank=True)
    picture = GenericRelation(Pictures, verbose_name=_("Pictures"),
                              null=True,
                              blank=True)
    drawings = GenericRelation(Drawings, verbose_name=_("Drawings"),
                              null=True,
                              blank=True)


    class Meta:
        abstract = True


class Item(Concept):
    chapter = models.ForeignKey(Chapter,
                                on_delete=models.PROTECT,
                                null=False,
                                related_name="items")

    def __str__(self):
        return'{}.{} - {}'.format(self.chapter.id, self.number, self.title)


    class Meta:
        unique_together = ("chapter", "number")

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class SubItem(Concept):
    item = models.ForeignKey(Item,
                             on_delete=models.PROTECT,
                             null=False,
                             related_name="subitems")

    def __str__(self):
        return'{}.{}.{} - {}'.format(self.item.chapter.id, self.item.number, self.number, self.title)

    class Meta:
        unique_together = ("item", "number")

    class Meta:
        verbose_name = _("Sub Item")
        verbose_name_plural = _("Sub Itens")


class Jobs(models.Model):
    item = models.ForeignKey(Item,
                             on_delete=models.PROTECT,
                             null=False,
                             related_name="jobs")
    number = models.PositiveIntegerField()
    description = models.TextField(verbose_name=_('Description'))
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       default_currency='USD',
                       default=0.0,
                       null=True,
                       blank=True)
    multiplier = models.DecimalField(verbose_name=_('Multiplier'),
                                     max_digits=5,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)
    remarks = models.TextField(verbose_name=_('Remarks'),
                               null=True,
                               blank=True)

    @property
    def sub_total(self):
        if self.price :
            if self.multiplier:
                return self.price * self.multiplier
            else:
                return 0.0
        else:
            return 0.0

    class Meta:
        permissions = (("can_view_job_prices", "The ability to see prices"),)
        unique_together = ("item", "number")


    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")


class SubJobs(models.Model):
    subitem = models.ForeignKey(SubItem,
                             on_delete=models.PROTECT,
                             null=False)
    number = models.PositiveIntegerField()
    description = models.TextField(verbose_name=_('Description'))
    price = MoneyField(max_digits=10,
                       decimal_places=2,
                       default_currency='USD',
                       default=0.0,
                       null=True,
                       blank=True)
    multiplier = models.DecimalField(verbose_name=_('Multiplier'),
                                     max_digits=5,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)
    remarks = models.TextField(verbose_name=_('Remarks'),
                               null=True,
                               blank=True)

    @property
    def sub_total(self):
        if self.price :
            if self.multiplier:
                return self.price * self.multiplier
            else:
                return 0.0
        else:
            return 0.0

    class Meta:
        permissions = (("can_view_subjob_prices", "The ability to see prices"),)
        unique_together = ("subitem", "number")


    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Sub Job")
        verbose_name_plural = _("Sub Jobs")
