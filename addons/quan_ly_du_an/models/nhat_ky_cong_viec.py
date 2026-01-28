from odoo import models, fields, api
from odoo.exceptions import ValidationError # Nhớ import cái này
from datetime import date

class NhatKyCongViec(models.Model):
    _name = "nhat_ky_cong_viec"
    _description = "Nhật ký công việc chi tiết"
    _order = "ngay_lam_viec desc"

    cong_viec_id = fields.Many2one('quan_ly_cong_viec', string="Đầu việc", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)

    ngay_lam_viec = fields.Date(string="Ngày", default=fields.Date.today)
    thoi_gian_lam = fields.Float(string="Số giờ làm")
    so_luong_hoan_thanh = fields.Float(string="Sản lượng làm được") # Nhớ thêm trường này nếu thiếu
    ket_qua = fields.Text(string="Kết quả/Ghi chú")

    @api.constrains('nhan_vien_id', 'cong_viec_id')
    def _check_nguoi_lam(self):
        for rec in self:
            # Lấy thông tin từ công việc cha
            nguoi_phu_trach = rec.cong_viec_id.nguoi_thuc_hien_id
            nhom_thuc_hien = rec.cong_viec_id.nhan_vien_ids

            if rec.nhan_vien_id != nguoi_phu_trach and rec.nhan_vien_id not in nhom_thuc_hien:
                raise ValidationError(
                    f"Nhân viên {rec.nhan_vien_id.ten_nhan_vien} không được giao nhiệm vụ này nên không thể báo cáo!"
                )