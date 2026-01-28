from odoo import models, fields, api
from odoo.exceptions import UserError
import google.generativeai as genai
import json
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# --- MODEL 1: LƯU LỊCH SỬ CHAT (Database thật) ---
class AiBotHistory(models.Model):
    _name = 'ai.bot.history'
    _description = 'Lịch sử Chat AI'
    _rec_name = 'question'      
    _order = 'create_date desc' 

    question = fields.Text(string="Câu hỏi", readonly=True)
    answer = fields.Html(string="Trả lời", readonly=True, sanitize=False)
    create_date = fields.Datetime(string="Thời gian hỏi", readonly=True)


# --- MODEL 2: CỬA SỔ CHAT (Popup tạm thời) ---
class AiBotWizard(models.TransientModel):
    _name = 'ai.bot.wizard'
    _description = 'Cửa sổ Chat AI'

    question = fields.Text(string="Câu hỏi", required=True)
    answer = fields.Html(string="Trả lời", readonly=True, sanitize=False)
    
    # Hàm hỗ trợ xử lý ngày tháng khi dump JSON
    def _json_serial(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return str(obj)

    # Hàm lấy nhãn hiển thị (Label)
    def _get_selection_label(self, model_name, field_name, value):
        if not value: return "Chưa xác định"
        try:
            selection = self.env[model_name]._fields[field_name].selection
            return dict(selection).get(value, value)
        except:
            return value

    def action_ask_ai(self):
        MY_API_KEY = os.environ.get('GOOGLE_API_KEY')
        
        # Code fallback cho môi trường test (nếu file .env lỗi)
        if not MY_API_KEY:
             MY_API_KEY = "AIzaSy..." # Điền key dự phòng của bạn vào đây nếu cần

        if not MY_API_KEY or "AIzaSy" not in MY_API_KEY:
             raise UserError("Lỗi: Không tìm thấy API Key hợp lệ!")

        try:
            genai.configure(api_key=MY_API_KEY)
            
            # Dùng model Lite cho nhanh và ổn định
            model = genai.GenerativeModel('gemini-2.5-flash', generation_config={'temperature': 0.0})

   
            # A. NHÂN VIÊN
            employees = self.env['nhan_vien'].search([])
            emp_data = []
            for e in employees:
                emp_data.append({
                    "ho_ten": e.ten_nhan_vien,
                    "chuc_vu": e.chuc_vu_id.ten_chuc_vu or "Chưa có",
                    "phong_ban": e.phong_ban_id.ten_phong_ban or "Chưa có",
                    "trang_thai": self._get_selection_label('nhan_vien', 'trang_thai', e.trang_thai),
                })

            # B. DỰ ÁN (CẬP NHẬT PHẦN TÀI CHÍNH MỚI)
            projects = self.env['quan_ly_du_an'].search([])
            proj_data = []
            for p in projects:
                # Format tiền tệ cho đẹp (Ví dụ: 1,000,000 VNĐ)
                ngan_sach = "{:,.0f} VNĐ".format(p.tong_ngan_sach or 0)
                thuc_te = "{:,.0f} VNĐ".format(p.tong_thuc_te or 0)
                chenh_lech = "{:,.0f} VNĐ".format(p.tong_chenh_lech or 0)
                
                # Logic đánh giá sơ bộ để gợi ý cho AI
                tinh_hinh_tai_chinh = "An toàn (Dư)" if p.tong_chenh_lech >= 0 else "BÁO ĐỘNG (Tiêu lố)"

                proj_data.append({
                    "ten_du_an": p.ten_du_an,
                    "quan_ly": p.quan_ly_id.ten_nhan_vien if p.quan_ly_id else "Chưa có",
                    "trang_thai": self._get_selection_label('quan_ly_du_an', 'trang_thai', p.trang_thai),
                    "ngay_ket_thuc": p.ngay_ket_thuc,
                    
                    "tong_ngan_sach_du_kien": ngan_sach,
                    "tong_chi_tieu_thuc_te": thuc_te,
                    "so_tien_du_thieu": chenh_lech,
                    "danh_gia_tai_chinh": tinh_hinh_tai_chinh
                })

            # C. CÔNG VIỆC
            tasks = self.env['quan_ly_cong_viec'].search([]) 
            task_data = []
            for t in tasks:
                task_data.append({
                    "ten_cong_viec": t.ten_cong_viec,
                    "thuoc_du_an": t.du_an_id.ten_du_an if t.du_an_id else "Không xác định",
                    "nguoi_thuc_hien": t.nguoi_thuc_hien_id.ten_nhan_vien if t.nguoi_thuc_hien_id else "Chưa giao",
                    "trang_thai": self._get_selection_label('quan_ly_cong_viec', 'trang_thai', t.trang_thai),
                    "do_uu_tien": self._get_selection_label('quan_ly_cong_viec', 'do_uu_tien', t.do_uu_tien),
                    "tien_do": f"{t.tien_do}%",
                    "gio_da_lam": t.gio_thuc_te
                })

            # Đóng gói JSON
            full_database = {
                "nhan_vien": emp_data, 
                "du_an": proj_data,
                "cong_viec": task_data
            }
            # Chuyển đổi sang chuỗi JSON để gửi cho AI
            database_json = json.dumps(full_database, default=self._json_serial, ensure_ascii=False)

            full_prompt = f"""
            Bạn là Trợ lý ảo quản lý dự án (Project Manager Assistant). 
            Hãy trả lời câu hỏi dựa trên dữ liệu JSON dưới đây.
            
            YÊU CẦU TRẢ LỜI:
            1. Định dạng HTML: Dùng thẻ <b>in đậm</b> cho các con số tài chính và tên người. Dùng <ul><li> cho danh sách.
            2. Về Tài chính: Nếu hỏi về tài chính/chi phí, hãy so sánh giữa "Dự kiến" và "Thực tế". Nếu "BÁO ĐỘNG" (bị âm), hãy cảnh báo người dùng.
            3. Ngôn ngữ: Tiếng Việt chuyên nghiệp, ngắn gọn.

            DỮ LIỆU HỆ THỐNG:
            ```json
            {database_json}
            ```
            
            CÂU HỎI CỦA NGƯỜI DÙNG: {self.question}
            """

            response = model.generate_content(full_prompt)
            clean_answer = response.text.replace('```html', '').replace('```', '')

            self.answer = clean_answer
            
            # 2. Lưu vào bảng Lịch sử (ai.bot.history)
            self.env['ai.bot.history'].create({
                'question': self.question,
                'answer': clean_answer
            })

        except Exception as e:
            raise UserError(f"Lỗi kết nối AI: {str(e)}")
            
        # Giữ nguyên cửa sổ Popup để xem kết quả
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ai.bot.wizard', # Trỏ về chính nó
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new', # Mở dạng Popup
        }