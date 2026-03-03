import subprocess
import sys
import webbrowser
import time

def main():
    print("=" * 60)
    print("🚀 ЗАПУСК АНАЛИЗАТОРА КОЛЛОКАЦИЙ")
    print("=" * 60)
    
    # Проверяем установку зависимостей
    try:
        import flask
        print("✅ Flask установлен")
    except ImportError:
        print("📦 Устанавливаем зависимости...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Запускаем сервер
    print("🌐 Запуск веб-сервера...")
    server_process = subprocess.Popen([sys.executable, "app.py"])
    
    # Ждем запуск сервера
    time.sleep(2)
    
    # Открываем браузер
    webbrowser.open("http://localhost:5000")
    print("✅ Приложение запущено! Открываю браузер...")
    print("   Нажмите Ctrl+C для остановки")
    
    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("\n👋 Останавливаю сервер...")
        server_process.terminate()

if __name__ == "__main__":
    main()