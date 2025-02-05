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
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .models import ValuationRequest
from django.contrib import messages



def is_staff(user):
    return user.is_staff  


@login_required
@user_passes_test(is_staff)
def valuation_request_list(request):
    requests = ValuationRequest.objects.all()
    return render(request, 'Request_table.html', {'requests': requests})


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Request_table')  
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    
    return render(request, 'home.html')


def send_request(request, request_id):
    # Lấy yêu cầu từ database
    request_to_send = get_object_or_404(ValuationRequest, id=request_id)
    
    # Cập nhật trạng thái của yêu cầu
    request_to_send.status = 'Đã hoàn thành'
    request_to_send.save()

    # Tạo file PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="valuation_certificate_{request_to_send.id}.pdf"'

    font_path = os.path.join(settings.BASE_DIR, "system/static/system/font/Arial.ttf")
    pdfmetrics.registerFont(TTFont("Arial", font_path))

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Arial", 12)

    today = datetime.now()
    formatted = today.strftime("%d/%m/%Y")

    random_number = random.randint(10000, 99999)
    random_date = str(random_number)

    # Vẽ thông tin vào PDF
    logo_path = os.path.join(settings.BASE_DIR, "system/static/system/img/logo.png")
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 50, 700, width=100, height=100)

    p.setFont("Arial", 16)
    p.drawString(200, 750, "Giấy Định Giá Kim Cương")

    p.setFont("Arial", 12)
    p.drawString(50, 650, f"Tên khách hàng: {request_to_send.name}")
    p.drawString(50, 630, f"Mã định giá: {random_date}")
    p.drawString(50, 610, f"Ngày định giá: {formatted}")

    p.drawString(50, 580, "Thông tin kim cương:")
    p.drawString(70, 560, f"Nguồn gốc: {request_to_send.origin}")
    p.drawString(70, 540, f"Hình dáng: {request_to_send.shape}")
    p.drawString(70, 520, f"Số đo: {request_to_send.measurements}")
    p.drawString(70, 500, f"Trọng lượng: {request_to_send.carat_weight} Carat")
    p.drawString(70, 480, f"Màu sắc: {request_to_send.color}")
    p.drawString(70, 460, f"Độ trong: {request_to_send.clarity}")
    p.drawString(70, 440, f"Độ cắt: {request_to_send.cut}")
    p.drawString(70, 420, f"Tỉ lệ: {request_to_send.proportions}")
    p.drawString(70, 400, f"Đánh bóng: {request_to_send.polish}")
    p.drawString(70, 380, f"Đối xứng: {request_to_send.symmetry}")
    p.drawString(70, 360, f"Huỳnh quang: {request_to_send.fluorescence}")
    p.drawString(70, 340, f"Giá trị ước tính: {request_to_send.price_range}")

    p.drawString(50, 300, "Người định giá: Trần Văn B")

    p.showPage()
    p.save()

    # Trả về file PDF
    return response 

def delete_request(request, request_id):
    
    request_to_delete = get_object_or_404(ValuationRequest, id=request_id)     
    request_to_delete.delete() 
    return redirect('Request_table')


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
        phone = request.POST.get("phone")
        
        try:
            grade = int(carat_weight) * 2  
            price_range = f"{grade * 50000}đ - {grade * 70000}đ"
            result = {"grade": grade, "price_range": price_range}
        except (ValueError, TypeError):
            result = {"grade": "Invalid", "price_range": "Invalid"}


        

        request.session['valuation_data'] = {
            'phone': phone,
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

        
        
        ValuationRequest.objects.create(
            name=name,
            date = datetime.now().date(),
            phone=phone,
            origin=origin,
            shape=shape,
            measurements=measurements,
            carat_weight=carat_weight,
            color=color,
            clarity=clarity,
            cut=cut,
            proportions=proportions,
            polish=polish,
            symmetry=symmetry,
            fluorescence=fluorescence,
            grade=result['grade'],
            price_range=result['price_range']
        )
        
    return render(request, "valuation.html", {"result": result})


