import os
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Проектна структура:
# project_root/
# ├─ pizzaapp/
# │  └─ utils.py (цей файл)
# ├─ fonts/
# │  └─ dejavu-fonts-ttf-2.37/
# │     └─ ttf/
# │        └─ DejaVuSans.ttf

# Збірка шляху до TTF-файла
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # → project_root
FONT_PATH = os.path.join(
    BASE_DIR,
    'fonts',
    'dejavu-fonts-ttf-2.37',
    'ttf',
    'DejaVuSans.ttf'
)

# Реєстрація шрифту для кирилиці
FONT_NAME = 'DejaVuSans'
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


def generate_pdf_receipt(order):
    """Генерує PDF-квитанцію для замовлення."""
    # Налаштування відповіді HTTP
    response = HttpResponse(content_type='application/pdf')
    filename = f"receipt_{order.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Створення canvas
    c = canvas.Canvas(response)
    c.setFont(FONT_NAME, 14)
    c.drawString(50, 800, f"Квитанція до замовлення №{order.id}")
    c.setFont(FONT_NAME, 12)
    c.drawString(50, 780, f"Дата: {order.created_at.strftime('%Y-%m-%d %H:%M')}")

    # Позиціювання рядків
    y = 750
    total = 0
    for item in order.items.all():
        line = f"{item.product.name} x{item.quantity} — {item.product.price * item.quantity} ₴"
        c.drawString(50, y, line)
        y -= 20
        total += item.product.price * item.quantity

    # Підсумок
    c.drawString(50, y - 10, f"Всього: {total} ₴")
    c.showPage()
    c.save()
    return response
