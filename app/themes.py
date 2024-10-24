
themes = {
    "Grey, White, Black": {
        "background-color": "#2E2E2E",
        "text-color": "#D3D3D3",
        "button-background": "#4D4D4D",
        "button-hover": "#666666",
        "progress-bar": "#4CAF50",
        "toolbar-background": "#1E1E1E",
        "toolbar-button-background": "#3C3C3C",
        "toolbar-button-hover": "#555555",
        "toolbar-button-text-color": "#FFFFFF",
        "window-border": "#000000",
        "input-background": "#3E3E3E",
        "input-border": "#666666",
        "input-text-color": "#FFFFFF",
        "label-font-size": "14px",
        "label-font-weight": "bold",
        "label-text-color": "#D3D3D3",
        "button-pressed": "#5E5E5E",
        "window-border-radius": "5px"
    },
    "Black and Yellow": {
        "background-color": "#1B1B1B",
        "text-color": "black",
        "button-background": "#F2A900",
        "button-hover": "#D89E00",
        "button-pressed": "#C78C00",
        "progress-bar": "#F2A900",
        "toolbar-background": "#222222",
        "toolbar-button-background": "#F2A900",
        "toolbar-button-hover": "#D89E00",
        "toolbar-button-text-color": "black",
        "window-border": "#444444",
        "input-background": "#2C2C2C",
        "input-border": "#444444",
        "input-text-color": "black",
        "label-font-size": "14px",
        "label-font-weight": "bold",
        "label-text-color": "black",
        "error_logs_text-color": "white",
        "window-border-radius": "5px"
    },
    "Red and Black": {
        "background-color": "#1A1A1A",
        "text-color": "#FF4136",
        "button-background": "#FF4136",
        "button-hover": "#FF6347",
        "button-pressed": "#FF2B2B",
        "progress-bar": "#FF4136",
        "toolbar-background": "#111111",
        "toolbar-button-background": "#FF4136",
        "toolbar-button-hover": "#FF6347",
        "toolbar-button-text-color": "#FFFFFF",
        "window-border": "#FF4136",
        "input-background": "#333333",
        "input-border": "#FF4136",
        "input-text-color": "#FF4136",
        "label-font-size": "14px",
        "label-font-weight": "bold",
        "label-text-color": "#FF4136",
        "window-border-radius": "5px"
    },
    "Blue and Silver": {
        "background-color": "#1E1E2E",
        "text-color": "#C0C0C0",
        "button-background": "#5F9EA0",
        "button-hover": "#4682B4",
        "button-pressed": "#1E90FF",
        "progress-bar": "#5F9EA0",
        "toolbar-background": "#2C2C3C",
        "toolbar-button-background": "#4682B4",
        "toolbar-button-hover": "#1E90FF",
        "toolbar-button-text-color": "#E0E0E0",
        "window-border": "#5F9EA0",
        "input-background": "#3A3A4A",
        "input-border": "#4682B4",
        "input-text-color": "#C0C0C0",
        "label-font-size": "14px",
        "label-font-weight": "bold",
        "label-text-color": "#C0C0C0",
        "window-border-radius": "5px"
    },
    "Dark Green and Grey": {
        "background-color": "#0F1E1E",
        "text-color": "#98FB98",
        "button-background": "#2E8B57",
        "button-hover": "#3CB371",
        "button-pressed": "#006400",
        "progress-bar": "#2E8B57",
        "toolbar-background": "#0C1515",
        "toolbar-button-background": "#3CB371",
        "toolbar-button-hover": "#006400",
        "toolbar-button-text-color": "#E0E0E0",
        "window-border": "#2E8B57",
        "window-border-color" : "black",
        "input-background": "#1C2B2B",
        "input-border": "#2E8B57",
        "input-text-color": "#98FB98",
        "label-font-size": "14px",
        "label-font-weight": "bold",
        "label-text-color": "#98FB98",
        "window-border-radius": "5px"
    }
}


def apply_theme(app, theme_name):
    """Apply the selected theme to the app."""
    theme = themes.get(theme_name, themes["Grey, White, Black"])  # Default to "Grey, White, Black" if not found
    app.setStyleSheet(f"""
        QWidget {{
            background-color: {theme['background-color']};
            color: {theme['text-color']};
        }}
        QMainWindow {{
            background-color: {theme['background-color']};
            color: {theme['text-color']};
            min-width: 950px;
            min-height: 500px;
            border: 1px solid {theme['window-border']};
            border-radius: {theme['window-border-radius']};
        }}
        QLabel {{
            color: {theme['label-text-color']};
            font-size: {theme['label-font-size']};
            font-weight: {theme['label-font-weight']};
        }}
        QPushButton {{
            background-color: {theme['button-background']};
            color: {theme['text-color']};
            border-radius: {theme['window-border-radius']};
        }}
        QPushButton:hover {{
            background-color: {theme['button-hover']};
        }}
        QPushButton:pressed {{
            background-color: {theme['button-pressed']};
        }}
        QProgressBar::chunk {{
            background-color: {theme['progress-bar']};
        }}
        QLineEdit, QComboBox {{
            background-color: {theme['input-background']};
            color: {theme['input-text-color']};
            border: 2px solid {theme['input-border']};
            border-radius: 5px;
        }}
        QToolBar {{
            background-color: {theme['toolbar-background']};
        }}
        QToolButton {{
            background-color: {theme['toolbar-button-background']};
            color: {theme['toolbar-button-text-color']};
        }}
        QToolButton:hover {{
            background-color: {theme['toolbar-button-hover']};
        }}
         /* Top Menu Bar Styling */
        QMenuBar {{
            background-color: {theme['toolbar-background']};
            color: {theme['toolbar-button-text-color']};
            border-bottom: 1px solid {theme['window-border']};
        }}
        QMenuBar::item {{
            background-color: {theme['toolbar-button-background']};
            color: {theme['toolbar-button-text-color']};
            padding: 5px 15px;
            border-radius: 5px;
        }}
        QMenuBar::item:selected {{
            background-color: {theme['toolbar-button-hover']};
            color: {theme['text-color']};
        }}
        QMenuBar::item:pressed {{
            background-color: {theme['button-pressed']};
        }}

        /* Menu Items Styling */
        QMenu {{
            background-color: {theme['toolbar-background']};
            color: {theme['text-color']};
            border: 1px solid {theme['toolbar-button-background']};
        }}
        QMenu::item {{
            background-color: {theme['toolbar-button-background']}; /* Change the background of menu items */
            color: {theme['text-color']};
            padding: 5px 20px;
            border-radius: 4px;
        }}
        QMenu::item:selected {{
            background-color: {theme['button-hover']}; /* Change background when hovered */
            color: {theme['text-color']};
        }}
        QMenu::item:pressed {{
            background-color: {theme['button-pressed']}; /* Change background when pressed */
            color: {theme['text-color']};
        }}

        /* Tool Buttons Styling */
        QToolButton {{
            background-color: {theme['toolbar-button-background']};
            color: {theme['toolbar-button-text-color']};
            border-radius: 5px;
            padding: 5px;
        }}
        QToolButton:hover {{
            background-color: {theme['toolbar-button-hover']};
        }}
        QToolButton:pressed {{
            background-color: {theme['button-pressed']};
        }}

        /* Styling Other Components */
        QPushButton {{
            background-color: {theme['button-background']};
            color: {theme['text-color']};
            border-radius: {theme['window-border-radius']};
            padding: 8px 15px;
        }}
        QPushButton:hover {{
            background-color: {theme['button-hover']};
        }}
        QPushButton:pressed {{
            background-color: {theme['button-pressed']};
        }}
    """)

