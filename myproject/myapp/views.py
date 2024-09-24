from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def home(request):
    context = {
        'message': 'Evidencia 1 Algoritmos Avanzados!',
        'T': None,
        'highlighted_text': None,
    }

    if request.method == 'POST':
        user_T = request.POST.get('user_T', '')
        user_P = request.POST.get('user_P', '')
        T = str(user_T)
        P = str(user_P)
        inicio, fin = KMP_Matcher(T, P)
        highlighted_text = highlight_pattern(T, inicio, fin)
        context['T'] = user_T
        context['highlighted_text'] = highlighted_text

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

    # Iterate through the found positions
    for start, end in zip(start_positions, end_positions):
        # Add text before the match
        highlighted += text[last_index:start]
        # Add the match with a highlight
        highlighted += f'<span class="highlight">{text[start:end+1]}</span>'
        # Update the last index
        last_index = end + 1

    # Add any remaining text after the last match
    highlighted += text[last_index:]
    
    return highlighted
