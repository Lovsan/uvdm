
themes = {
    "Grey, White, Black": {
        "background-color": "#2E2E2E",
        "text-color": "red",
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
    }
}

def apply_theme(app, theme):
    """Apply the given theme to the app."""
    app.setStyleSheet(f"""
        QMainWindow {{
            background-color: {theme.get('background-color', '#FFFFFF')};
        }}
        QPushButton {{
            background-color: {theme.get('button-background', '#CCCCCC')};
            color: {theme.get('text-color', '#000000')};
        }}
        QPushButton:hover {{
            background-color: {theme.get('button-hover', '#AAAAAA')};
        }}
        QProgressBar::chunk {{
            background-color: {theme.get('progress-bar', '#4CAF50')};
        }}
        QToolBar {{
            background-color: {theme.get('toolbar-background', '#333333')};
        }}
    """)
