import os
from collections import defaultdict

import nltk
import pymorphy2
from django.shortcuts import render
from nltk.tokenize import RegexpTokenizer

from .models import MyFiles

nltk.download('punkt')
nltk.download('wordnet')


def index(request):
    tokenizer = RegexpTokenizer(r'\w+')
    morph = pymorphy2.MorphAnalyzer()
    uploaded_files = request.session.get('uploaded_files', [])

    if request.POST:
        files = request.FILES.getlist('file')
        if files:
            for f in uploaded_files[0]:
                os.remove(f'media/{f}')
            uploaded_files[0] = []
            uploaded_files[1] = []
            for f in files:
                newfile = MyFiles.objects.create(
                    file=f
                )
                uploaded_files[0].append(newfile.file.name)
                uploaded_files[1].append(f.name)
            uploaded_files[2] = uploaded_files[0][0]
            request.session['uploaded_files'] = uploaded_files

        button_text = request.POST.get('button_name', None)
        if button_text:
            uploaded_files[2] = uploaded_files[0][uploaded_files[1].index(button_text)]
            request.session['uploaded_files'] = uploaded_files

        toggle = request.POST.get('toggle', None)
        if toggle:
            uploaded_files[3] = not(uploaded_files[3])
            request.session['uploaded_files'] = uploaded_files

    if uploaded_files[2] == '':
        request.session['uploaded_files'] = [[], [], '', False]
        return render(request, 'main/index.html')

    files_name = uploaded_files[0]
    user_files_name = uploaded_files[1]
    toggle_state = uploaded_files[3]

    main_file = uploaded_files[2]
    buttons_data = [{'label': i, 'color': '#0000CD' if user_files_name.index(i) == files_name.index(main_file) else '#00BFFF'} for i in user_files_name]
    with open(f"media/{main_file}", 'r', encoding="utf-8") as temp_file:
        read_data = temp_file.read()

    res = tokenizer.tokenize(read_data)
    for i in range(len(res)):
        res[i] = res[i].lower()

    if toggle_state:
        for i in range(len(res)):
            res[i] = morph.parse(res[i])[0].normal_form

    lengh_res = len(res)
    tf_dct = {}
    for el in res:
        tf_dct[el] = round(res.count(el) / lengh_res, 5)

    idf_dct = defaultdict(int)
    for f in files_name:
        with open(f"media/{f}", 'r', encoding="utf-8") as temp_file:
            read_data = temp_file.read()

        res = list(set(tokenizer.tokenize(read_data)))
        for i in range(len(res)):
            res[i] = res[i].lower()

        if toggle_state:
            for i in range(len(res)):
                res[i] = morph.parse(res[i])[0].normal_form

        for i in tf_dct:
            if i in res:
                idf_dct[i] += 1
    lengh_files_name = len(files_name)
    for i in idf_dct:
        idf_dct[i] = round(lengh_files_name / idf_dct[i], 5)

    word_data = [{'word': i, 'tf': tf_dct[i], 'idf': idf_dct[i]} for i in idf_dct]
    word_data = sorted(word_data, key=lambda x: x['idf'], reverse=True)

    per_page = 50
    page_number = request.GET.get('page')
    page_number = int(page_number) if page_number else 1

    start_index = (page_number - 1) * per_page
    end_index = start_index + per_page

    current_page_data = word_data[start_index:end_index]
    has_previous_page = page_number > 1
    has_next_page = end_index < len(word_data)

    return render(request, 'main/index.html', {
        'word_data': current_page_data,
        'buttons': buttons_data,
        'has_previous_page': has_previous_page,
        'has_next_page': has_next_page,
        'previous_page_number': page_number - 1 if has_previous_page else None,
        'next_page_number': page_number + 1 if has_next_page else None,
        'toggle_state': 'ON' if toggle_state else 'OFF',
    })
