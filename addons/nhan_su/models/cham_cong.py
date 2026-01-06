from odoo import models, fields, api

class ChamCong(models.Model):
    _name = 'cham_cong'
    _description = 'Bảng chấm công'
    _rec_name = 'nhan_vien_id'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ngay = fields.Date("Ngày", default=fields.Date.today, required=True)
    gio_vao = fields.Float("Giờ vào") # Dùng Float (ví dụ 8.5 là 8h30)
    gio_ra = fields.Float("Giờ ra")
    
    so_gio_lam = fields.Float("Tổng giờ làm", compute='_tinh_gio_lam', store=True)

    @api.depends('gio_vao', 'gio_ra')
    def _tinh_gio_lam(self):
        for rec in self:
            if rec.gio_ra > rec.gio_vao:
                rec.so_gio_lam = rec.gio_ra - rec.gio_vao
            else:
                rec.so_gio_lam = 0.0