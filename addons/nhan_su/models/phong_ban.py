from odoo import models, fields, api

class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'

    _rec_name = 'ten_phong_ban'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân Viên")