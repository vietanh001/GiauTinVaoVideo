import cv2
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

class Tach:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.check_open()
        self.video_to_frames()

    def check_open(self):
        # Kiểm tra xem video đã được mở chưa
        if not self.cap.isOpened():
            print("Không thể mở video")
            exit()

        # Tạo thư mục frames nếu chưa tồn tại
        self.output_folder = "frames_tach"
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def video_to_frames(self):
        frame_idx = 0
        while True:
            # Đọc frame từ video
            ret, frame = self.cap.read()
            if not ret:
                break
            # Ghi frame thành file ảnh
            frame_filename = os.path.join(self.output_folder, f"frame_{frame_idx}.png")  # Lưu file ảnh vào thư mục frames
            print(f"frame_{frame_idx}.png")
            cv2.imwrite(frame_filename, frame)

            # Tăng số thứ tự frame
            frame_idx += 1

        # Giải phóng tài nguyên
        self.cap.release()
        cv2.destroyAllWindows()
        print("Đã tách video thành frames")

if __name__ == "__main__":
    t = Tach("E:\Môn học\Giấu tin\Code\Phát hiện chuyển cảnh\/video.mp4")
    print(t.check_open())
    print(t.video_to_frames())