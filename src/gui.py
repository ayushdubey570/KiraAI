# src/gui.py
import sys
import os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QMovie, QPainter, QColor

class KiraGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        # --- WINDOW FLAGS ---
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool 
        )
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(1400, 100, 350, 500)

        # --- LAYOUT ---
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # --- LABEL ---
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("background-color: transparent;")
        self.layout.addWidget(self.label)

        # --- DRAG VARIABLES ---
        self.old_pos = None

        # --- LOAD ASSETS ---
        self.movies = {}
        self.current_state = "idle"
        
        self.load_gif("idle", "idle.gif")
        self.load_gif("speaking", "talking.gif")
        self.load_gif("thinking", "thinking.gif")

        self.set_state("idle")

    def load_gif(self, name, filename):
        path = os.path.join("assets", filename)
        if os.path.exists(path):
            movie = QMovie(path)
            movie.setBackgroundColor(QColor(0, 0, 0, 0)) 
            movie.setScaledSize(QSize(350, 500))
            self.movies[name] = movie
        else:
            print(f"[GUI Warning] Missing asset: {path}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))

    # --- SIMPLIFIED DRAG LOGIC (The Delta Method) ---
    def mousePressEvent(self, event):
        """Record the mouse position when you click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        """Move the window by the difference (delta) of mouse movement."""
        if event.buttons() == Qt.MouseButton.LeftButton and self.old_pos:
            # Calculate how far the mouse moved
            delta = event.globalPosition().toPoint() - self.old_pos
            
            # Move the window by that amount
            self.move(self.x() + delta.x(), self.y() + delta.y())
            
            # Reset old_pos for the next tiny movement
            self.old_pos = event.globalPosition().toPoint()
            event.accept()

    def set_state(self, state_name):
        state_name = state_name.lower()
        if state_name == self.current_state:
            return

        self.current_state = state_name
        if self.label.movie():
            self.label.movie().stop()

        movie = self.movies.get(state_name, self.movies.get("idle"))
        if movie:
            self.label.setMovie(movie)
            movie.start()