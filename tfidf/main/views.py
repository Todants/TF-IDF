from collections import defaultdict

from django.shortcuts import render
from .models import MyFiles
import re
import string


def index(request):
    if request.POST:
        files_name = []
        for f in request.FILES.getlist('file'):
            files_name.append(f.name)
            MyFiles.objects.create(
                file=f
            )

        main_file = files_name[0]
        with open(f"media/upldfile/{main_file}", 'r', encoding="utf-8") as temp_file:
            read_data = temp_file.read()
        res = re.sub('[' + string.punctuation + ']', '', read_data).split()
        lengh_res = len(res)
        tf_dct = {}
        for el in res:
            tf_dct[el] = round(res.count(el) / lengh_res, 5)
        print(files_name)
        idf_dct = defaultdict(int)
        for f in files_name:
            with open(f"media/upldfile/{f}", 'r', encoding="utf-8") as temp_file:
                read_data = temp_file.read()
            res = set(re.sub('[' + string.punctuation + ']', '', read_data).split())

            for i in tf_dct:
                if i in res:
                    idf_dct[i] += 1
        lengh_files_name = len(files_name)
        for i in idf_dct:
            idf_dct[i] = round(lengh_files_name / idf_dct[i], 5)

        word_data = [{'word': i, 'tf': tf_dct[i], 'idf': idf_dct[i]} for i in idf_dct]
        word_data = sorted(word_data, key=lambda x: x['idf'], reverse=True)
        return render(request, 'main/index.html', {'word_data': word_data})

    return render(request, 'main/index.html')
