from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from utils.rabbit_worker import send_to_queue

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    # Значения по умолчанию, чтобы не ломать шаблон при GET
    name = phone = date = ''

    if request.method == 'POST':
        # 1) Извлекаем и приводим к строкам
        name  = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        date  = request.form.get('date', '').strip()
        to_connect  = request.form.get('to_connect', '').strip()

        payload = {'name': name, 'phone': phone, 'date': date, 'to_connect': to_connect}
        send_to_queue('booking_queue', payload)

        return redirect(url_for('index'))

    # При GET или если есть ошибки — рендерим форму снова
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)