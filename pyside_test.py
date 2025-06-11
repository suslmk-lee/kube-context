import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel

# 1. QApplication 인스턴스 생성
app = QApplication(sys.argv)

# 2. 메인 윈도우 생성
window = QWidget()
window.setWindowTitle('PySide6 Test')
window.setGeometry(100, 100, 280, 80)

# 3. 라벨 위젯 생성
hello_msg = QLabel('<h1>Hello, PySide6!</h1>', parent=window)
hello_msg.move(60, 15)

# 4. 윈도우 표시
window.show()

# 5. 이벤트 루프 시작
sys.exit(app.exec())
