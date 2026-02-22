from django.shortcuts import render

def home(request):
    context = {
        'title': 'Головна: Наші заклади у Луцьку',
        'content': 'Вітаємо! Оберіть заклад, щоб побачити опис для соцмереж.',
        'page_type': 'home'
    }
    return render(request, 'main_app/index.html', context)

def somerset(request):
    context = {
        'title': 'Somerset Hotel',
        'content': 'Затишний, озеленений готель для сімейного відпочинку. Ідеальне місце для спокою в центрі міста.',
        'page_type': 'detail'
    }
    return render(request, 'main_app/index.html', context)

def dcip(request):
    context = {
        'title': 'DCIP (Don’t Call It Pizza)',
        'content': 'Елегантна та вишукана піцерія. Це не просто піца, це гастрономічний досвід.',
        'page_type': 'detail'
    }
    return render(request, 'main_app/index.html', context)

def bean_water(request):
    context = {
        'title': 'Bean and Water',
        'content': 'Кав’ярня з дуже затишною та м’якою атмосферою. Найкраща кава для твого ранку.',
        'page_type': 'detail'
    }
    return render(request, 'main_app/index.html', context)