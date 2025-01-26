from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'home.html')


def diamond_valuation_view(request):
    result = {"grade": "-", "price_range": "(0đ - 0đ)"}

    if request.method == "POST":
        origin = request.POST.get("origin")
        shape = request.POST.get("shape")
        measurements = request.POST.get("measurements")
        carat_weight = request.POST.get("carat_weight")
        color = request.POST.get("color")
        clarity = request.POST.get("clarity")
        cut = request.POST.get("cut")
        proportions = request.POST.get("proportions")
        polish = request.POST.get("polish")
        symmetry = request.POST.get("symmetry")
        fluorescence = request.POST.get("fluorescence")

        
        try:
            grade = int(carat_weight) * 2  
            price_range = f"{grade * 50000}đ - {grade * 70000}đ"
            result = {"grade": grade, "price_range": price_range}
        except (ValueError, TypeError):
            result = {"grade": "Invalid", "price_range": "Invalid"}

    return render(request, "valuation.html", {"result": result})

def print_valuation_view(request):
    context = {
        "origin": request.POST.get("origin", ""),
        "shape": request.POST.get("shape", ""),
        "measurements": request.POST.get("measurements", ""),
        "carat_weight": request.POST.get("carat_weight", ""),
        "color": request.POST.get("color", ""),
        "clarity": request.POST.get("clarity", ""),
        "cut": request.POST.get("cut", ""),
        "proportions": request.POST.get("proportions", ""),
        "polish": request.POST.get("polish", ""),
        "symmetry": request.POST.get("symmetry", ""),
        "fluorescence": request.POST.get("fluorescence", ""),
        "result": {"grade": "-", "price_range": "(0đ - 0đ)"}
    }
    return render(request, 'print.html', context)
