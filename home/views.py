from django.shortcuts import render
# from .functions import squared

# Create your views here.

def home_view(request):
    context = {
        ###################
        # TO BE COMPLETED #
        ###################
    }
    # import pudb; pu.db()
    return render(request,'home/home.html', context=context)

def about_us_view(request):
    return render(request,'home/about_us.html')