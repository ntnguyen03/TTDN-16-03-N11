from odoo import models, fields, api
from odoo.exceptions import ValidationError

class QuanLyCongViec(models.Model):
    _name = 'quan_ly_cong_viec'
    _description = 'Quản lý công việc'
    _rec_name = 'ten_cong_viec'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ten_cong_viec = fields.Char(string='Tên công việc', required=True)
    
    nguoi_thuc_hien_id = fields.Many2one(
        'nhan_vien', 
        string='Người phụ trách', 
        tracking=True,
        domain="[('id', 'in', du_an_thanh_vien_ids)]"
    )

    nhan_vien_ids = fields.Many2many(
        'nhan_vien',
        string='Nhóm thực hiện',
        domain="[('id', 'in', du_an_thanh_vien_ids)]"
    )

    du_an_thanh_vien_ids = fields.Many2many(
        related='du_an_id.thanh_vien_ids',
        readonly=True,
    )
    
    nhat_ky_ids = fields.One2many('nhat_ky_cong_viec', 'cong_viec_id', string='Nhật ký làm việc')
    
    du_an_id = fields.Many2one('quan_ly_du_an', string='Thuộc Dự án', required=True, ondelete='cascade')

    do_uu_tien = fields.Selection([
        ('binh_thuong', 'Bình thường'),
        ('gap', 'Gấp/Quan trọng'),
        ('hoa_toc', 'Hỏa tốc')
    ], string='Độ ưu tiên', default='binh_thuong', tracking=True)

    trang_thai = fields.Selection([
        ('chua_lam', 'Chưa làm'),
        ('dang_lam', 'Đang làm'),
        ('xong', 'Đã xong')
    ], string='Trạng thái', default='chua_lam', tracking=True)

    tien_do = fields.Integer(string='Tiến độ (%)', compute='_tinh_tien_do', store=True)
    
    gio_du_kien = fields.Float(string='Giờ dự kiến')
    gio_thuc_te = fields.Float(string='Tổng giờ đã làm', compute='_tinh_gio_thuc', store=True)
    
    mo_ta = fields.Text(string='Hướng dẫn chi tiết')

    don_vi_tinh = fields.Char(string='Đơn vị tính', default='Cái/Lần', help="Ví dụ: Trang, Dòng, Banner...")
    
    so_luong_can_lam = fields.Float(string='Số lượng chỉ tiêu', default=1.0, required=True)
    
    so_luong_da_lam = fields.Float(string='Số lượng đã hoàn thành', compute='_tinh_so_luong_thuc', store=True)

    @api.depends('so_luong_da_lam', 'so_luong_can_lam', 'nhat_ky_ids.so_luong_hoan_thanh')
    def _tinh_tien_do(self):
        for r in self:
            if r.so_luong_can_lam > 0:
                pt = (r.so_luong_da_lam / r.so_luong_can_lam) * 100
                r.tien_do = int(pt)
            else:
                r.tien_do = 0

    @api.depends('nhat_ky_ids.so_luong_hoan_thanh')
    def _tinh_so_luong_thuc(self):
        for r in self:
            r.so_luong_da_lam = sum(r.nhat_ky_ids.mapped('so_luong_hoan_thanh'))

    @api.depends('nhat_ky_ids.thoi_gian_lam')
    def _tinh_gio_thuc(self):
        for r in self:
            r.gio_thuc_te = sum(r.nhat_ky_ids.mapped('thoi_gian_lam'))


class QuanLyDuAnMoRong(models.Model):
    _inherit = 'quan_ly_du_an'
    cong_viec_ids = fields.One2many('quan_ly_cong_viec', 'du_an_id', string='Danh sách công việc')