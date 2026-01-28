from odoo import models, fields, api

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ten_nhan_vien'

    # --- 1. THÔNG TIN CƠ BẢN ---
    # Mã định danh: Tự động tính, lưu trữ, và bắt buộc
    ma_dinh_danh = fields.Char(
        string="Mã định danh", 
        required=True, 
        store=True, 
        compute='_compute_ma_dinh_danh'
    )
    
    ten_nhan_vien = fields.Char("Họ và tên", required=True)
    anh_dai_dien = fields.Binary("Ảnh đại diện", attachment=True) # Mới thêm
    
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác')
    ], string="Giới tính", default='nam') # Mới thêm
    
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    
    # --- 2. THÔNG TIN LIÊN HỆ ---
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    dia_chi = fields.Text("Địa chỉ thường trú")
    
    # --- 3. CÔNG VIỆC HIỆN TẠI (Quan trọng) ---
    # Thêm 2 trường này để biết ngay nhân viên đang ở đâu, làm gì
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban hiện tại")
    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ hiện tại")
    
    trang_thai = fields.Selection([
        ('thu_viec', 'Thử việc'),
        ('chinh_thuc', 'Chính thức'),
        ('da_nghi', 'Đã nghỉ việc')
    ], string="Trạng thái", default='thu_viec') # Mới thêm

    # --- 4. CHẾ ĐỘ & LƯƠNG ---
    # (Có thể tách ra module Hợp đồng sau này, tạm thời giữ lại để nhập liệu đơn giản)
    luong = fields.Float("Mức lương cơ bản") 
    bao_hiem_xa_hoi = fields.Char("Số sổ BHXH")

    # --- 5. DANH SÁCH LIÊN KẾT (One2many) ---
    lich_su_ids = fields.One2many('lich_su_cong_tac', 'nhan_vien_id', string="Lịch sử công tác")
    chung_chi_ids = fields.One2many('chung_chi', 'nhan_vien_id', string="Văn bằng & Chứng chỉ")
    cham_cong_ids = fields.One2many('cham_cong', 'nhan_vien_id', string="Bảng chấm công")

    # --- LOGIC TÍNH TOÁN ---
    @api.depends('ten_nhan_vien', 'ngay_sinh')
    def _compute_ma_dinh_danh(self):
        for rec in self:
            if rec.ten_nhan_vien and rec.ngay_sinh:
                # 1. Lấy chữ cái đầu (VD: Lò Đức Mạnh -> LĐM)
                cac_tu = rec.ten_nhan_vien.strip().split()
                if cac_tu:
                    chu_cai_dau = "".join([w[0].upper() for w in cac_tu])
                else:
                    chu_cai_dau = "NV" # Fallback nếu tên rỗng
                
                # 2. Lấy ngày sinh (YYYYMMDD)
                ngay_sinh_str = rec.ngay_sinh.strftime("%Y%m%d")
                
                # 3. Ghép lại
                rec.ma_dinh_danh = f'{chu_cai_dau}{ngay_sinh_str}'
            else:
                # Nếu chưa nhập đủ thì để False (hoặc chuỗi tạm) để không bị lỗi required
                rec.ma_dinh_danh = False