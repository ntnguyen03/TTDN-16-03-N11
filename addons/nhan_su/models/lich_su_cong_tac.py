from odoo import models, fields

class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Lịch sử công tác'
    _rec_name = 'nhan_vien_id'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    
    # Liên kết để biết lúc đó làm ở đâu, chức vụ gì
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban")
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ")
    
    ghi_chu = fields.Text("Ghi chú")