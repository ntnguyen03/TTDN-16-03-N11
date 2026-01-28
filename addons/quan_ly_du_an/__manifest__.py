{
    'name': 'Quản Lý Dự Án',
    'version': '1.0',
    'summary': 'Module quản lý dự án cho công ty',
    'depends': ['base', 'mail', 'nhan_su'],
    'data':[
        'security/ir.model.access.csv',
        'views/du_an.xml',
        'views/loai_du_an.xml',
        'views/cong_viec.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}