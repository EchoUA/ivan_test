import string

from django.shortcuts import render
from django.shortcuts import HttpResponse

from text_analyzer.forms import WordForm


class Word():
    """
    For process the input and display output data.
    """

    def __init__(self, text):
        self.text = text


    def text_split(self):
        output_words = {}
        text_words =  [x.replace(',', "") for x in self.text.lower().split()]
        mapping = [(':', ''), ('!', ''), ('?', ''), (';', ''), ("'", ''), ('"', ''), ('(', ''),
                   (')', ''), ('[', ''), (']', ''), ('#', '')]
        for word in text_words:
            for k, v in mapping:
                word = word.replace(k, v)
        for i in range(len(text_words)):
            if text_words[i].count('.') > 1:
                text_words[i] = text_words[i].replace('.', ',')
        text_with_dots = " ".join(text_words).strip()
        splited_text = text_with_dots.split('.')
        splited_text = [x.replace(',', '.')for x in splited_text]
        all_words = ' '.join(splited_text).split()
        unic_words = set(all_words)
        for word in unic_words:
            word_counter = all_words.count(word)
            output_words[word] = [word_counter, ]
        for i, sentense in enumerate(splited_text):
            if not sentense:
                continue
            for key in output_words.keys():
                c_i = sentense.split().count(key)
                if c_i:
                    for j in range(c_i):
                        output_words[key] += str(i+1)
        return output_words


    def list_make(self, words_dict):
        words_list =[]
        for k, v in words_dict.items():
            str_to_append = str(k)+'\t'+'{'+str(v[0])+':'+','.join(v[1:])+'}'
            words_list.append(str_to_append)
        return sorted(words_list)


    def for_print(self, words_list):
        if len(words_list) > 25:
            k = len(words_list) // 25
            for_index = 0
            for j in range(k+1):
                for i, alpha in enumerate(string.ascii_lowercase):
                    if i+for_index >= len(words_list):
                        break
                    words_list[i+for_index] = [alpha*(j+1) + '.'] + [words_list[i+for_index]]
                for_index = for_index +  i + 1
        else:
            for i, alpha in enumerate(string.ascii_lowercase):
                if i >= len(words_list):
                    break
                words_list[i] = [alpha +'.'] +  [words_list[i]]

        return words_list



def main_view(request):
    form = WordForm()
    return render(request, 'text_analyzer/base.html', {'form':form})


def start_process(request):
    form = WordForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['sentense']
        w = Word(text)
        output_words = w.text_split()
        words_list = w.list_make(output_words)
        output = w.for_print(words_list)
        return render(request, 'text_analyzer/base.html', {'form':WordForm(), 'output':output})
    else:
        return HttpResponse("Yours form not valdi!!!")
