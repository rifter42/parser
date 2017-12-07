from params import *
import re

str1 = "Сегодня 12:30"
str2 = str1[:-6]
str1 = re.sub("Сегодня", dates_list[str2], str1)
print(str1)
