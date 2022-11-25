from django.shortcuts import render

# Create your views here.

def country_details_view(request):
    context = {
        ###################
        # TO BE COMPLETED #
        ###################
    }
    # import pudb; pu.db()
    return render(request,'country_details/country_details.html', context=context)