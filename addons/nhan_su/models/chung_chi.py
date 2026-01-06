from odoo import models, fields

class ChungChi(models.Model):
    _name = 'chung_chi'
    _description = 'Chứng chỉ nhân viên'
    _rec_name = 'ten_chung_chi'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ten_chung_chi = fields.Char("Tên chứng chỉ", required=True)
    noi_cap = fields.Char("Nơi cấp")
    ngay_cap = fields.Date("Ngày cấp")
    ngay_het_han = fields.Date("Ngày hết hạn")
    file_dinh_kem = fields.Binary("File Scan")  # Để upload ảnh chứng chỉ