from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.conf import settings
import random
from datetime import datetime
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
        name = request.POST.get("name")

        
        try:
            grade = int(carat_weight) * 2  
            price_range = f"{grade * 50000}đ - {grade * 70000}đ"
            result = {"grade": grade, "price_range": price_range}
        except (ValueError, TypeError):
            result = {"grade": "Invalid", "price_range": "Invalid"}


        request.session['valuation_data'] = {
            'name': name,
            'origin': origin,
            'shape': shape,
            'measurements': measurements,
            'carat_weight': carat_weight,
            'color': color,
            'clarity': clarity,
            'cut': cut,
            'proportions': proportions,
            'polish': polish,
            'symmetry': symmetry,
            'fluorescence': fluorescence,
            'grade': result['grade'],
            'price_range': result['price_range']
        }
    return render(request, "valuation.html", {"result": result})

def print_valuation_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="valuation_certificate.pdf"'

    font_path = os.path.join(settings.BASE_DIR, "system/static/system/font/Arial.ttf")
    pdfmetrics.registerFont(TTFont("Arial", font_path))

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Arial", 12)



    #lay ngay gio
    today =  datetime.now()
    formatted = today.strftime("%d/%m/%Y")


    #lay ma dinh gia

    random_number = random.randint(10000,99999)
    random_date = str(random_number)


    # Lấy dữ liệu từ session
    valuation_data = request.session.get('valuation_data', {})

    # Vẽ logo
    logo_path = os.path.join(settings.BASE_DIR, "system/static/system/img/logo.png")
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 50, 700, width=100, height=100)

    # Tiêu đề
    p.setFont("Arial", 16)
    p.drawString(200, 750, "Giấy Định Giá Kim Cương")

    # Thông tin khách hàng
    p.setFont("Arial", 12)
    p.drawString(50, 650, f"Tên khách hàng: {valuation_data.get('name', '')}")
    p.drawString(50, 630, f"Mã định giá: {random_date}")
    p.drawString(50, 610, f"Ngày định giá: {formatted}")

    # Thông tin kim cương
    p.drawString(50, 580, "Thông tin kim cương:")
    p.drawString(70, 560, f"Nguồn gốc: {valuation_data.get('origin', '')}")
    p.drawString(70, 540, f"Hình dáng: {valuation_data.get('shape', '')}")
    p.drawString(70, 520, f"Số đo: {valuation_data.get('measurements', '')}")
    p.drawString(70, 500, f"Trọng lượng: {valuation_data.get('carat_weight', '')} Carat")
    p.drawString(70, 480, f"Màu sắc: {valuation_data.get('color', '')}")
    p.drawString(70, 460, f"Độ trong: {valuation_data.get('clarity', '')}")
    p.drawString(70, 440, f"Độ cắt: {valuation_data.get('cut', '')}")
    p.drawString(70, 420, f"Tỉ lệ: {valuation_data.get('proportions', '')}")
    p.drawString(70, 400, f"Đánh bóng: {valuation_data.get('polish', '')}")
    p.drawString(70, 380, f"Đối xứng: {valuation_data.get('symmetry', '')}")
    p.drawString(70, 360, f"Huỳnh quang: {valuation_data.get('fluorescence', '')}")
    p.drawString(70, 340, f"Giá trị ước tính: {valuation_data.get('price_range', '')}")

    # Người định giá
    p.drawString(50, 300, "Người định giá: Trần Văn B")

    p.showPage()
    p.save()

    return response
