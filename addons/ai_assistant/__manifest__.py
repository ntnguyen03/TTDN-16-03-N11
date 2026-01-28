{
    'name': 'Trợ lý ảo AI (Gemini)',
    'version': '1.0',
    'summary': 'Chatbot ERP sử dụng Google Gemini - Strict Mode',
    'author': 'Nam Nguyen',
    'depends': ['base', 'quan_ly_du_an', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_bot_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}