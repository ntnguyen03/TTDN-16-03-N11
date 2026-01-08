from odoo import models, fields, api

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ten_nhan_vien'

    # SỬA LỖI 1: Tên hàm compute phải khớp với tên hàm bên dưới
    ma_dinh_danh = fields.Char(
        "Mã định danh", 
        required=True, 
        store=True, 
        compute='_compute_ma_dinh_danh' # Tên hàm cần khớp
    )
    
    ten_nhan_vien = fields.Char("Tên nhân viên", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    dia_chi = fields.Text("Địa chỉ")
    luong = fields.Float("Lương")
    bao_hiem_xa_hoi = fields.Char("Bảo hiểm xã hội")
    
    # CẢNH BÁO: Đảm bảo bạn đã có model 'chuc_vu' trong hệ thống
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ hiện tại")

    # CẢNH BÁO: Đảm bảo các model này đã tồn tại
    lich_su_ids = fields.One2many('lich_su_cong_tac', 'nhan_vien_id', string="Lịch sử công tác")
    chung_chi_ids = fields.One2many('chung_chi', 'nhan_vien_id', string="Danh sách chứng chỉ")
    cham_cong_ids = fields.One2many('cham_cong', 'nhan_vien_id', string="Bảng chấm công")

    # SỬA LỖI 1: Dùng api.depends thay vì onchange cho field compute
    @api.depends('ten_nhan_vien', 'ngay_sinh')
    def _compute_ma_dinh_danh(self):
        for rec in self:
            if rec.ten_nhan_vien and rec.ngay_sinh:
                cac_tu = rec.ten_nhan_vien.strip().split()
                # Thêm kiểm tra để tránh lỗi nếu tên nhập toàn dấu cách
                if cac_tu:
                    chu_cai_dau = "".join([w[0].upper() for w in cac_tu])
                    ngay_sinh_str = rec.ngay_sinh.strftime("%Y%m%d")
                    rec.ma_dinh_danh = f'{chu_cai_dau}{ngay_sinh_str}'
                else:
                    rec.ma_dinh_danh = False
            else:
                rec.ma_dinh_danh = False

    # van_ban_den_ids = fields.One2many(
    #     'van_ban_den',
    #     'nhan_vien_xu_ly_id',
    #     string="Văn bản phụ trách"
    # )

    # van_ban_den_count = fields.Integer(
    #     compute="_compute_vb_count"
    # )
    
    # def _compute_vb_count(self):
    #     for rec in self:
    #         # Code này đúng, nhưng có thể viết ngắn gọn hơn:
    #         # rec.van_ban_den_count = len(rec.van_ban_den_ids)
    #         rec.van_ban_den_count = self.env['van_ban_den'].search_count([
    #             ("nhan_vien_xu_ly_id", "=", rec.id)
    #         ])

    # def action_open_van_ban_den(self):
    #     self.ensure_one()
    #     return {
    #         "type": "ir.actions.act_window",
    #         "name": "Văn bản đến",
    #         "res_model": "van_ban_den",
    #         "view_mode": "tree,form",
    #         "domain": [("nhan_vien_xu_ly_id", "=", self.id)],
    #         "context": {'default_nhan_vien_xu_ly_id': self.id} # Thêm dòng này để khi tạo mới sẽ tự điền tên nhân viên
    #     }