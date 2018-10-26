from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Chapter, Item, SubItem
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Prefetch
from django.db import models

# Create your views here.
@login_required
def chapter_list(request):
    chapters_list = Chapter.objects.order_by('id')
    items = Item.objects.filter(chapter__in=chapters_list)
    subitems = SubItem.objects.filter(item__in=items)
    items = Item.objects.filter(chapter__in=chapters_list).prefetch_related(Prefetch('subitems', queryset=subitems))
    chapters_list = Chapter.objects.order_by('id').prefetch_related(Prefetch('items', queryset=items))

    template = loader.get_template('jobs/chapter.html')

    context = {
        'chapters_list': chapters_list,
    }
    return HttpResponse(template.render(context, request))

@login_required
def chapter_detail(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    items = Item.objects.filter(chapter=chapter)
    subitems = SubItem.objects.filter(item__in=items).annotate(total=Sum(F('subjobs__price')*F('subjobs__multiplier'),output_field=models.FloatField()))
    items_subitems = Item.objects.filter(
                                        chapter=chapter
                    ).annotate(total=Sum(F('jobs__price')*F('jobs__multiplier'),
                               output_field=models.FloatField())
                    ).prefetch_related(Prefetch('subitems', queryset=subitems))

    template = loader.get_template('jobs/chapter_detail.html')
    context = {
        'chapter': chapter,
        'items': items,
        'items_subitems': items_subitems,
    }
    return HttpResponse(template.render(context, request))

@login_required
def item_detail(request, chapter_id, item_number):
    item = get_object_or_404(Item.objects.filter(chapter=chapter_id, number=item_number))
    subitems = SubItem.objects.filter(item=item).annotate(total=Sum(F('subjobs__price')*F('subjobs__multiplier'),output_field=models.FloatField()))
    item_subitems = Item.objects.filter(
                                        chapter=chapter_id, number=item_number
                    ).annotate(total=Sum(F('jobs__price')*F('jobs__multiplier'),
                               output_field=models.FloatField())
                    ).prefetch_related(Prefetch('subitem', queryset=subitems))

    template = loader.get_template('jobs/item_detail.html')
    context = {
        'item': item,
        'item_subitems': item_subitems,
    }
    return HttpResponse(template.render(context, request))

@login_required
def subitem_detail(request, chapter_id, item_number, subitem_number):
    item = get_object_or_404(Item.objects.filter(chapter=chapter_id, number=item_number))
    subitems = SubItem.objects.filter(item=item, number=subitem_number).annotate(total=Sum(F('subjobs__price')*F('subjobs__multiplier'),output_field=models.FloatField()))

    template = loader.get_template('jobs/subitem_detail.html')
    context = {
        'subitems': subitems,
    }
    return HttpResponse(template.render(context, request))

@login_required
def chapter_all(request):
    chapters_list = Chapter.objects.order_by('id')
    items = Item.objects.filter(chapter__in=chapters_list)
    subitems = SubItem.objects.filter(item__in=items)
    items = Item.objects.filter(chapter__in=chapters_list).prefetch_related(Prefetch('subitems', queryset=subitems))
    chapters_list = Chapter.objects.order_by('id').prefetch_related(Prefetch('items', queryset=items))

    template = loader.get_template('jobs/chapter_all.html')

    context = {
        'chapters_list': chapters_list,
    }
    return HttpResponse(template.render(context, request))
