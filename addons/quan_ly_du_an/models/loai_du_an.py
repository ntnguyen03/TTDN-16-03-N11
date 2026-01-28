from odoo import models, fields, api

class LoaiDuAn(models.Model):
    _name = 'loai_du_an'
    _description = 'Phân loại dự án/ kế hoạch'
    _rec_name = 'ten_loai'

    ten_loai = fields.Char(string='Tên loại dự án', required=True)
    mo_ta = fields.Text(string='Mô tả thêm')