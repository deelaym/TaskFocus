from django import template
import markdown
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import datetime

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    text = markdown.markdown(text, safe_mode='escape')
    return mark_safe(text[3:-4]) # Markdown добавляет тег <p></p>



def validate_video(text):
    validator = URLValidator()
    text = text.split()
    for word in text:
        try:
            validator(word)
            if 'youtube' in word or 'vimeo' in word:
                text.remove(word)
                return True, ' '.join(text), word
        except ValidationError:
            pass
    return False, ' '.join(text)

@register.filter(name='is_video')
def is_video(text):
    flag, *_ = validate_video(text)
    return flag


@register.filter(name='task_text')
def task_text(text):
    _, text, *_ = validate_video(text)
    return text


@register.filter(name='task_video')
def task_video(text):
    *_, video = validate_video(text)
    return video


@register.simple_tag
def today():
    return datetime.date.today()