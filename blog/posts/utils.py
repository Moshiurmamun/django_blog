import datetime
import math
import re

from django.utils.html import strip_tags

def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall('\w+', word_string)
    count = len(matching_words)
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.00) #assuming 200 wpm reading
    return int(read_time_min)
