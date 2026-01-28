from odoo import models, fields, api

class QuanLyDuAn(models.Model):
    _name = 'quan_ly_du_an'
    _description = 'Quản lý Dự án / Kế hoạch'
    _rec_name = 'ten_du_an'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ten_du_an = fields.Char(string='Tên Kế hoạch/Dự án', required=True, tracking=True)

    quan_ly_id = fields.Many2one('nhan_vien', string='Người phụ trách', required=True, tracking=True)
    thanh_vien_ids = fields.Many2many(
        'nhan_vien', 
        string='Thành viên dự án',
        help="Chỉ những người có tên ở đây mới được giao việc trong dự án này."
        
    )
    active = fields.Boolean(string='Đang hoạt đông', default=True)
    
    loai_du_an_id = fields.Many2one('loai_du_an', string='Phân loại')
    #cong_viec_ids = fields.One2many('quan_ly_cong_viec', 'du_an_id', string='Danh sách công việc')

    trang_thai = fields.Selection([
        ('tao_moi', 'Tạo mới'),
        ('dang_lam', 'Đang thực hiện'),
        ('tam_dung', 'Tạm dừng'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy bỏ')
    ], string='Trạng thái', default='tao_moi', tracking=True)

    ngay_bat_dau = fields.Date(string='Ngày bắt đầu')
    ngay_ket_thuc = fields.Date(string='Ngày kết thúc')
    
    
    chi_phi_van_hanh = fields.Float(string='Chi phí vận hành/Vật tư')
    tong_ngan_sach = fields.Float(string='Tổng Dự kiến', compute='_tinh_tong_chi_phi', store=True)
    tong_thuc_te = fields.Float(string='Tổng Thực tế', compute='_tinh_tong_chi_phi', store=True)
    tong_chenh_lech = fields.Float(string='Tổng Chênh lệch', compute='_tinh_tong_chi_phi', store=True)
    
    # Lien ket bang chi tiet chi tieu
    chi_phi_ids = fields.One2many('chi_phi_du_an', 'du_an_id', string='Bảng kê chi phí')

    @api.depends('chi_phi_ids.so_tien_du_kien', 'chi_phi_ids.so_tien_thuc_te', 'chi_phi_van_hanh')
    def _tinh_tong_chi_phi(self):
        for r in self:
            # 1. Tính tổng dự kiến (Các đầu việc + Vận hành cố định)
            sum_du_kien = sum(r.chi_phi_ids.mapped('so_tien_du_kien'))
            r.tong_ngan_sach = sum_du_kien + r.chi_phi_van_hanh

            # 2. Tính tổng thực tế (Các đầu việc thực chi + Vận hành đã chi)
            # (Giả sử chi phí vận hành là cố định phải chi, nên cộng cả vào thực tế)
            sum_thuc_te = sum(r.chi_phi_ids.mapped('so_tien_thuc_te'))
            r.tong_thuc_te = sum_thuc_te + r.chi_phi_van_hanh

            # 3. Tính chênh lệch tổng
            r.tong_chenh_lech = r.tong_ngan_sach - r.tong_thuc_te