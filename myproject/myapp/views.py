import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
import os

@csrf_protect
def autocompletar_view(request):
    return render(request, 'autocompletar.html')

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def _search_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_all_words(self, node, prefix, words):
        if node.is_end_of_word:
            words.append(prefix)
        
        for char, next_node in node.children.items():
            self._collect_all_words(next_node, prefix + char, words)

    def autocomplete(self, prefix):
        node = self._search_node(prefix)
        if not node:
            return []  
        words = []
        self._collect_all_words(node, prefix, words)
        return words


def LCS(T1, T2):
    n = len(T1)
    m = len(T2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    longitud_maxima = 0
    inicio = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if T1[i - 1] == T2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > longitud_maxima:
                    longitud_maxima = dp[i][j]
                    inicio = i - longitud_maxima

    return T1[inicio:inicio + longitud_maxima], inicio

def Manacher(request):
    context = {
        'message': '...',
        'highlighted_text': None,
    }
    if request.method == 'POST':
        uploaded_file = request.FILES.get('filemana')
        if uploaded_file:
            file_content = uploaded_file.read().decode('utf-8')  
            T = str(file_content)
            palindromo, start_index = manacher(T)
            context['message'] = palindromo
            
            # Highlight the palindrome in the text
            end_index = start_index + len(palindromo) - 1
            context['highlighted_text'] = highlight_pattern(T, [start_index], [end_index])

    return render(request, 'manacher.html', context)

def lcs(request):
    context = {
        'message': '...',
        'highlighted_text1': None,
        'highlighted_text2': None,
    }

    if request.method == 'POST':
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        if file1 and file2:
            textoUno = file1.read().decode('utf-8')
            textoDos = file2.read().decode('utf-8')
            lcs_result, start_idx1 = LCS(textoUno, textoDos)
            start_idx2 = textoDos.index(lcs_result)
            highlighted_text1 = highlight_pattern(textoUno, [start_idx1], [start_idx1 + len(lcs_result) - 1])
            highlighted_text2 = highlight_pattern(textoDos, [start_idx2], [start_idx2 + len(lcs_result) - 1])
            
            context['message'] = lcs_result
            context['highlighted_text1'] = highlighted_text1
            context['highlighted_text2'] = highlighted_text2

    return render(request, 'lcs.html', context)


def manacher(d):
    n = len(d)
    if n == 0:
        return "", -1
    
    m = "@#"
    for x in d:
        m += x + "#"
    m += "$"

    y = [0] * len(m)
    mdp = 0
    enp = 0
    longitud_maxima = 0
    inicio = 0

    for i in range(1, len(m) - 1):
        espejo = 2 * mdp - i

        if i < enp:
            y[i] = min(enp - i, y[espejo])

        while m[i + y[i] + 1] == m[i - y[i] - 1]:
            y[i] += 1

        if i + y[i] > enp:
            mdp = i
            enp = i + y[i]

        if y[i] > longitud_maxima:
            longitud_maxima = y[i]
            inicio = (i - longitud_maxima) // 2

    return d[inicio:inicio + longitud_maxima], inicio

@csrf_protect
def autocompletar_view(request):
    if request.method == 'POST':
        if 'fileauto' in request.FILES:
            uploaded_file = request.FILES['fileauto']
            file_content = uploaded_file.read().decode('utf-8')
            words = cortarPalabras(file_content)
            request.session['words'] = words
            
            return render(request, 'autocompletar.html')
        
        elif 'userWord' in request.POST:
            user_input = request.POST.get('userWord', '')
            words = request.session.get('words', [])
            
            trie = Trie()
            for word in words:
                trie.insert(word)
            
            suggestions = trie.autocomplete(user_input)
            return JsonResponse({'suggestions': suggestions})
    
    return render(request, 'autocompletar.html')


def home(request):
    context = {
        'message': 'Evidencia 1 Algoritmos Avanzados!',
        'T': '',
        'P': '',
        'highlighted_text': None,
        'current_match': 0,
        'total_matches': 0,
    }

    if request.method == 'POST':
        uploaded_file = request.FILES.get('text_file')
        user_P = request.POST.get('user_P', '')
        current_match = int(request.POST.get('current_match', 0))
        T = request.POST.get('T', '')

        if uploaded_file:
            T = uploaded_file.read().decode('utf-8')

        if T and user_P:
            inicios, fines = KMP_Matcher(T, user_P)
            total_matches = len(inicios)

            if total_matches > 0:
                current_match = current_match % total_matches
                highlighted_text = highlight_pattern(T, [inicios[current_match]], [fines[current_match]])
            else:
                highlighted_text = T
                current_match = 0

            context.update({
                'T': T,
                'P': user_P,
                'highlighted_text': highlighted_text,
                'current_match': current_match,
                'total_matches': total_matches,
            })

    return render(request, 'home.html', context)


def KMP_Matcher(T, P):
    n = len(T)
    m = len(P)
    pi = computePrefixFunction(P)
    q = 0
    inicioPatron = []
    finPatron = []
    for i in range(n):
        while q > 0 and P[q] != T[i]:
            q = pi[q - 1]
        if P[q] == T[i]:
            q = q + 1
        if q == m:
            finPatron.append(i)
            inicioPatron.append(i - m + 1)
            q = pi[q - 1]
    return inicioPatron, finPatron

def computePrefixFunction(P):
    m = len(P)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and P[k] != P[q]:
            k = pi[k - 1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k
    return pi

def highlight_pattern(text, start_positions, end_positions):
    highlighted = ""
    last_index = 0
    for start, end in zip(start_positions, end_positions):   
        highlighted += text[last_index:start]       
        highlighted += f'<span class="highlight">{text[start:end+1]}</span>'
        last_index = end + 1

   
    highlighted += text[last_index:]
    
    return highlighted

    
def cortarPalabras(texto):
    palabras=[]
    palabra=" "
    for i in range(len(texto)):
        if texto[i] != " ":
            palabra+= texto[i]
        elif texto[i] == " ":
            palabras.append(palabra)
            palabra=""
    return palabras
