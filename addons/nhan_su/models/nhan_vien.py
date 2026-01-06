from odoo import models, fields, api


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'

    _rec_name = 'ten_nhan_vien'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ten_nhan_vien = fields.Char("Tên nhân viên", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    dia_chi = fields.Text("Địa chỉ")
    luong = fields.Float("Lương")
    bao_hiem_xa_hoi = fields.Char("Bảo hiểm xã hội")
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ hiện tại")

    lich_su_ids = fields.One2many('lich_su_cong_tac', 'nhan_vien_id', string="Lịch sử công tác")
    chung_chi_ids = fields.One2many('chung_chi', 'nhan_vien_id', string="Danh sách chứng chỉ")
    cham_cong_ids = fields.One2many('cham_cong', 'nhan_vien_id', string="Bảng chấm công")