from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
from datetime import datetime
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} - {format % args}")
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.send_home_page()
        elif path == '/about':
            self.send_about_page()
        elif path == '/services':
            self.send_services_page()
        elif path == '/contact':
            self.send_contact_page()
        elif path == '/form':
            self.send_form_page()
        elif path == '/success':
            self.send_success_page()
        else:
            self.send_404_page()
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/submit':
            self.handle_form_submission()
        else:
            self.send_404_page()
    
    def load_html_template(self, title, content):
        """Загружает базовый шаблон и вставляет контент"""
        with open('templates/base.html', 'r', encoding='utf-8') as f:
            template = f.read()
        
        return template.replace('{{title}}', title).replace('{{content}}', content)
    
    def send_html_response(self, title, content, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = self.load_html_template(title, content)
        self.wfile.write(html.encode('utf-8'))
    
    def send_home_page(self):
        with open('templates/home.html', 'r', encoding='utf-8') as f:
            content = f.read()
        self.send_html_response("Главная страница", content)
    
    def send_about_page(self):
        with open('templates/about.html', 'r', encoding='utf-8') as f:
            content = f.read()
        self.send_html_response("О нас", content)
    
    def send_services_page(self):
        with open('templates/services.html', 'r', encoding='utf-8') as f:
            content = f.read()
        self.send_html_response("Услуги", content)
    
    def send_contact_page(self):
        with open('templates/contact.html', 'r', encoding='utf-8') as f:
            content = f.read()
        self.send_html_response("Контакты", content)
    
    def send_form_page(self):
        with open('templates/form.html', 'r', encoding='utf-8') as f:
            content = f.read()
        self.send_html_response("Обратная связь", content)
    
    def send_success_page(self):
        with open('templates/success.html', 'r', encoding='utf-8') as f:
            content = f.read()
        self.send_html_response("Сообщение отправлено", content)
    
    def send_404_page(self):
        with open('templates/404.html', 'r', encoding='utf-8') as f:
            content = f.read()
        self.send_html_response("Страница не найдена", content, 404)
    
    def handle_form_submission(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            
            if content_length == 0:
                self.send_error(400, "Пустой запрос")
                return
            
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            form_data = parse_qs(post_data)
            
            name = form_data.get('name', [''])[0].strip()
            email = form_data.get('email', [''])[0].strip()
            subject = form_data.get('subject', [''])[0].strip()
            message = form_data.get('message', [''])[0].strip()
            
            errors = []
            if not name:
                errors.append("Имя обязательно для заполнения")
            if not email:
                errors.append("Email обязателен для заполнения")
            elif '@' not in email:
                errors.append("Некорректный email адрес")
            if not message:
                errors.append("Сообщение обязательно для заполнения")
            
            if errors:
                error_content = f"""
                <h1>Ошибка при отправке формы</h1>
                <div class="error">
                    <h3>Исправьте следующие ошибки:</h3>
                    <ul>
                """
                for error in errors:
                    error_content += f"<li>{error}</li>"
                
                error_content += """
                    </ul>
                </div>
                <p><a href="/form">Вернуться к форме</a></p>
                """
                self.send_html_response("Ошибка отправки", error_content, 400)
                return
            
            print(f"Получена форма: Имя={name}, Email={email}, Тема={subject}")
            print(f"Сообщение: {message[:100]}...")
            
            self.send_response(302)
            self.send_header('Location', '/success')
            self.end_headers()
            
        except Exception as e:
            print(f"Ошибка при обработке формы: {e}")
            self.send_error(500, f"Внутренняя ошибка сервера: {str(e)}")

def run_server(port=8000):
    # Создаем папку templates если её нет
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("Создана папка templates. Добавьте HTML файлы перед запуском сервера.")
        return
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    print(f"Сервер запущен на http://localhost:{port}")
    print("Доступные страницы:")
    print("   /         - Главная страница")
    print("   /about    - О нас")
    print("   /services - Услуги")
    print("   /contact  - Контакты")
    print("   /form     - Форма обратной связи")
    print("\nДля остановки сервера нажмите Ctrl+C")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")

if __name__ == '__main__':
    run_server()
