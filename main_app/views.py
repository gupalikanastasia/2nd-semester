from django.shortcuts import render

def home(request):
    context = {
        'title': 'Головна: Sleepy Pandy',
        'content': 'Вітаємо! Оберіть категорію, щоб зробити замовлення',
        'page_type': 'home'
    }
    return render(request, 'main_app/index.html', context)

def coffee(request):
    context = {
        'title': 'Кава',
        'content': 'Смачна, запашна кава яка підійме ваш настрі в найпохмуріший ранок.',
        'page_type': 'detail'
    }
    return render(request, 'main_app/index.html', context)

def cakes(request):
    context = {
        'title': 'Авторська випічка',
        'content': 'Елегантна та вишукана випічка, що зачарує вас своїм смаком',
        'page_type': 'detail'
    }
    return render(request, 'main_app/index.html', context)

def desserts(request):
    context = {
        'title': 'Десерти',
        'content': 'Солодкі та цікаві десерти яких ви ще точно не куштували',
        'page_type': 'detail'
    }
    return render(request, 'main_app/index.html', context)