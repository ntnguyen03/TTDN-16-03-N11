from odoo import models, fields, api

class ChiPhiDuAn(models.Model):
    _name = 'chi_phi_du_an'
    _description = 'Chi tiết các khoản chi'
    _rec_name = 'cong_viec_id'

    du_an_id = fields.Many2one('quan_ly_du_an', string='Thuộc dự án/kế hoạch', required=True, ondelete='cascade')

    cong_viec_id = fields.Many2one(
        'quan_ly_cong_viec', 
        string="Đầu việc chi tiêu", 
        required=True,
        domain="[('du_an_id', '=', du_an_id)]"
    )

    so_tien_du_kien = fields.Float(string="Dự kiến chi")
    so_tien_thuc_te = fields.Float(string="Thực tế chi")

    chenh_lech = fields.Float(string="Chênh lệch", compute='_tinh_chenh_lech', store=True)
    ghi_chu = fields.Text(string="Ghi chú")

    @api.depends('so_tien_du_kien', 'so_tien_thuc_te')
    def _tinh_chenh_lech(self):
        for r in self:
            r.chenh_lech = r.so_tien_du_kien - r.so_tien_thuc_te