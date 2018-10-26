from django.contrib import admin
from .models import (Chapter, Item, SubItem, Jobs, Attached_File,
                     Pictures, SubJobs, Drawings)
from django.contrib.contenttypes.admin import GenericTabularInline #, GenericStackedInline
from django.contrib.auth import get_user_model


class AttachedFileInline(GenericTabularInline):
    model = Attached_File
    extra = 0


class PictureAdmin(admin.ModelAdmin):
    model = Pictures
    exclude = ( 'user', 'id')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(PictureAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
        return super(PictureAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ('user',)
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['user'] = request.user
        request.GET = data
        return super(PictureAdmin, self).add_view(request, form_url="", extra_context=extra_context)


class PicturesInline(GenericTabularInline):
    model = Pictures
    extra = 0


class DrawingsAdmin(admin.ModelAdmin):
    model = Drawings
    exclude = ( 'user','id' )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(DrawingsAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
        return super(DrawingsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ('user',)
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['user'] = request.user
        request.GET = data
        return super(DrawingsAdmin, self).add_view(request, form_url="", extra_context=extra_context)


class DrawingsInline(GenericTabularInline):
    model = Drawings
    extra = 0


class ChapterAdmin(admin.ModelAdmin):
    inlines = [
               AttachedFileInline,
              ]
    list_display = ('id', 'title')
    ordering = ('id', 'title')

class ItemAdmin(admin.ModelAdmin):
    inlines = [
               AttachedFileInline,
               PicturesInline,
               DrawingsInline,
              ]
    list_display = ('chapter','number', 'title')
    ordering = ('chapter_id','number', 'title')

    def chapter_id(self, obj):
        return obj.chapter.id

    chapter_id.admin_order_field = 'chapter__id'
    chapter_id.short_description = 'Chapter'


class SubItemAdmin(admin.ModelAdmin):
    inlines = [
               AttachedFileInline,
               PicturesInline,
               DrawingsInline,
              ]
    list_display = ('item','number', 'title')
    ordering = ('item__chapter_id','item__number','number', 'title')

class JobsAdmin(admin.ModelAdmin):
    list_display = ('item', 'number', 'description', 'sub_total')
    ordering = ('item','number')


class SubJobsAdmin(admin.ModelAdmin):
    list_display = ('subitem', 'number', 'description', 'sub_total')
    ordering = ('subitem','number')


# Register your models here.
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SubItem, SubItemAdmin)
admin.site.register(Jobs, JobsAdmin)
admin.site.register(SubJobs, SubJobsAdmin)
admin.site.register(Attached_File)
admin.site.register(Pictures, PictureAdmin)
admin.site.register(Drawings, DrawingsAdmin)