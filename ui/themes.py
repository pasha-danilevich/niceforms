"""Управление темами и стилями.""" 
 
class ThemeManager: 
    """Менеджер тем для формы.""" 
 
    def __init__(self): 
        self.styles = { 
            "form_width": "max-w-2xl", 
            "primary_gradient": "bg-gradient-to-r from-blue-500 to-purple-600", 
            "error_bg": "bg-red-50", 
            "success_bg": "bg-green-50", 
            "padding": "p-6" 
        } 
