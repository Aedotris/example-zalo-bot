## Giới thiệu

Đây là một ứng dụng Python sử dụng thư viện `zlapi` để tương tác với API Zalo. Ứng dụng này bao gồm một lớp `Client` kế thừa từ `ZaloAPI` với khả năng xử lý các tin nhắn, lấy thông tin người dùng, và gửi tin nhắn phản hồi.

## Yêu cầu

- Python 3.9 hoặc mới hơn
- Thư viện `zlapi`

## Cài đặt

Trước tiên, bạn cần cài đặt thư viện `zlapi`. Bạn có thể cài đặt nó bằng pip:

```bash
pip install zlapi
```

## Cấu hình

Để sử dụng ứng dụng, bạn cần cung cấp các thông tin sau:

- `imei`: IMEI của thiết bị bạn sử dụng.
- `session_cookies`: Cookies phiên làm việc của bạn từ Zalo.

Chỉnh sửa các thông tin này trong mã nguồn trước khi chạy ứng dụng:

```python
imei = "YOUR_IMEI"
session_cookies = {
    # Thêm cookies của bạn ở đây
}
client = Client('api_key', 'secret_key', imei=imei, session_cookies=session_cookies)
```

