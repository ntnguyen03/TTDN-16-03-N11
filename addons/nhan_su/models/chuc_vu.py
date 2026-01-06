from odoo import models, fields

class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Chức vụ công việc'
    _rec_name = 'ten_chuc_vu'  # Quan trọng để hiển thị tên khi chọn

    ma_chuc_vu = fields.Char("Mã chức vụ", required=True)
    ten_chuc_vu = fields.Char("Tên chức vụ", required=True)
    mo_ta = fields.Text("Mô tả công việc")
    
    # Quan hệ ngược: Xem chức vụ này đang có những nhân viên nào
    nhan_vien_ids = fields.One2many('nhan_vien', 'chuc_vu_id', string="Danh sách nhân viên")