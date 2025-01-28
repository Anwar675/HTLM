from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.conf import settings
import os


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
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="valuation_certificate.pdf"'

    font_path = os.path.join(settings.BASE_DIR, "system/static/system/font/Arial.ttf")
    pdfmetrics.registerFont(TTFont("Arial", font_path))

    
    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Arial", 12)

   
    logo_path = os.path.join(settings.BASE_DIR, "system/static/system/img/logo.png")

   
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 50, 700, width=100, height=100)

    
    p.setFont("Arial", 16)
    p.drawString(200, 750, "Giấy Định Giá Kim Cương")

    p.setFont("Arial", 12)
    p.drawString(50, 650, "Tên khách hàng: Nguyễn Văn A")
    p.drawString(50, 630, "Mã định giá: 12345678")
    p.drawString(50, 610, "Ngày định giá: 28/01/2025")

    
    p.drawString(50, 580, "Thông tin kim cương:")
    p.drawString(70, 560, "Nguồn gốc: Natural")
    p.drawString(70, 540, "Hình dáng: Round")
    p.drawString(70, 520, "Số đo: 5,2 x 5,2 x 3,1 mm")
    p.drawString(70, 500, "Trọng lượng: 1.2 Carat")
    p.drawString(70, 480, "Màu sắc: D")
    p.drawString(70, 460, "Độ trong: VS1")
    p.drawString(70, 440, "Độ cắt: tuyệt vời")
    p.drawString(70, 420, "Tỉ lệ: tốt")
    p.drawString(70, 400, "Đánh bóng: tốt")
    p.drawString(70, 380, "Đối xứng: tốt")
    p.drawString(70, 360, "Huỳnh quang: tốt")
    p.drawString(70, 340, "Giá trị ước tính: 50,000,000 VND")

    
    p.drawString(50, 300, "Người định giá: Trần Văn B")

    
    p.showPage()
    p.save()

    return response
