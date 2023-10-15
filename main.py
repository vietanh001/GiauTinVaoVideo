import os
import shutil
from scapy.all import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication,  QLabel, QDesktopWidget, QLineEdit, QPushButton, QFileDialog, QTextEdit
import cv2
import numpy as np

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.setWindowTitle(
            "Giấu tin vào video bằng phương pháp phát hiện chuyển cảnh")
        self.resize(1200, 850)
        self.center()

        # Tạo nút để tải video từ máy tính
        self.video_button = QPushButton("Tải video", self)
        self.video_button.setFont(QtGui.QFont("Arial", 12))
        self.video_button.setGeometry(QtCore.QRect(100, 20, 100, 50))
        self.video_button.clicked.connect(self.load_video)
        self.video_button.setStyleSheet(
            "background-color: #33FFFF; border-radius: 20px; border: 1px solid black;")

        # Tạo label để hiển thị video
        self.video_label = QLabel(self)
        self.video_label.setGeometry(QtCore.QRect(20, 110, 780, 480))
        self.video_label.setStyleSheet("border: 1px solid black;")
        self.video_label.setScaledContents(True)

        # Tạo nút để tách video thành các frames
        self.video_to_frames_button = QPushButton("Tách Video -> Frames", self)
        self.video_to_frames_button.setFont(QtGui.QFont("Arial", 12))
        self.video_to_frames_button.setGeometry(QtCore.QRect(450, 20, 230, 50))
        self.video_to_frames_button.clicked.connect(self.video_to_frames)
        self.video_to_frames_button.setStyleSheet(
            "background-color: #33FFFF; border-radius: 20px; border: 1px solid black;")

        # Hiển thị tin trạng thái tách
        self.label_tach = QLabel(self)
        font.setPointSize(12)
        self.label_tach.setFont(font)
        self.label_tach.setGeometry(QtCore.QRect(460, 60, 350, 50))
        self.label_tach.setScaledContents(True)

        # Tạo nút hiển thị thứ các cảnh chuyển
        self.show_frames_change_button = QPushButton("Các cảnh chuyển", self)
        self.show_frames_change_button.setFont(QtGui.QFont("Arial", 12))
        self.show_frames_change_button.setGeometry(
            QtCore.QRect(900, 20, 200, 50))
        self.show_frames_change_button.clicked.connect(self.show_frames_change)
        self.show_frames_change_button.setStyleSheet(
            "background-color: #33FFFF; border-radius: 20px; border: 1px solid black;")

        # Hiển thị tin trạng thái tách
        self.label_change_frame = QLabel(self)
        font.setPointSize(12)
        self.label_change_frame.setFont(font)
        self.label_change_frame.setGeometry(QtCore.QRect(945, 60, 350, 50))
        self.label_change_frame.setScaledContents(True)

        # Tạo text hiển thị thứ tự các frames chuyển cảnh
        self.text_frames_change = QTextEdit(self)
        self.text_frames_change.setGeometry(830, 110, 350, 480)
        font.setPointSize(12)
        self.text_frames_change.setFont(font)
        self.text_frames_change.setStyleSheet("border: 1px solid black")
        self.text_frames_change.setReadOnly(True)
        self.text_frames_change.setPlainText(
            "Thứ tự các frames chuyển cảnh là: ")

        # Tạo nhãn chú thích
        self.label = QLabel(self)
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setText(
            "Nhập thứ tự các frames được cách nhau bằng dấu cách")
        self.label.setGeometry(QtCore.QRect(50, 680, 350, 50))
        # self.label.setStyleSheet("border: 1px solid red;")
        self.label.setScaledContents(True)

        # Thêm QLineEdit và QPushButton để nhập nội dung tin cần giấu
        self.text_sub_edit = QLineEdit(self)
        font.setPointSize(13)
        self.text_sub_edit.setFont(font)
        self.text_sub_edit.setStyleSheet(
            "border: 1px solid black; padding-left: 10px; border-radius: 20px")
        self.text_sub_edit.setPlaceholderText(
            "Nhập nội dung tin cần giấu vào video")
        self.text_sub_edit.move(20, 600)
        self.text_sub_edit.resize(400, 50)

        # Tạo mục để nhập những frames muốn giấu thông tin
        self.num_frames_edit = QLineEdit(self)
        font.setPointSize(13)
        self.num_frames_edit.setFont(font)
        self.num_frames_edit.setStyleSheet(
            "border: 1px solid black; padding-left: 10px; border-radius: 20px")
        self.num_frames_edit.setPlaceholderText(
            "Thứ tự các frames để giấu thông tin")
        self.num_frames_edit.move(20, 720)
        self.num_frames_edit.resize(400, 50)

        # Tạo mục thông báo quá trình giấu tin
        self.message_gt = QLineEdit(self)
        font.setPointSize(9)
        self.message_gt.setFont(font)
        # self.num_frames_edit.setStyleSheet("border: 1px solid black; padding-left: 10px; border-radius: 20px")
        self.message_gt.setPlaceholderText(
            "Thứ tự các frames để giấu thông tin")
        self.message_gt.move(40, 780)
        self.message_gt.resize(200, 50)

        # Tạo nút để giấu tin
        self.giau_tin = QPushButton("Giấu tin", self)
        self.giau_tin.setFont(QtGui.QFont("Arial", 12))
        self.giau_tin.setGeometry(QtCore.QRect(450, 650, 100, 50))
        self.giau_tin.clicked.connect(self.giau_tin_button)
        self.giau_tin.setStyleSheet(
            "background-color: #33FFFF; border-radius: 20px; border: 1px solid black;")

        # Tạo nút hiện thị tin đã giấu
        self.tach_tin = QPushButton("Tách tin", self)
        self.tach_tin.setFont(QtGui.QFont("Arial", 12))
        self.tach_tin.setGeometry(QtCore.QRect(880, 600, 230, 50))
        self.tach_tin.clicked.connect(self.tach_tin_button)
        self.tach_tin.setStyleSheet(
            "background-color: #33FFFF; border-radius: 20px; border: 1px solid black;")

        # Tạo nhãn chú thích
        self.label = QLabel(self)
        self.label.setText("Nội dung tin mật")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setGeometry(QtCore.QRect(920, 640, 350, 50))
        # self.label.setStyleSheet("border: 1px solid red;")
        self.label.setScaledContents(True)

        # Hiển thị tin đã được giấu
        self.tin_da_giau = QTextEdit(self)
        self.tin_da_giau.setGeometry(830, 680, 350, 150)
        font.setPointSize(13)
        self.tin_da_giau.setFont(font)
        self.tin_da_giau.setStyleSheet("border: 1px solid black")
        self.tin_da_giau.setReadOnly(True)

    # Tải video lên
    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn video", "", "Video Files (*.mp4 *.avi *.mkv)")
        if file_path:
            self.video_path = file_path
            self.play_video()

    # Hiển thị video lên màn hình
    def play_video(self):
        # Load video từ file
        cap = cv2.VideoCapture(self.video_path)

        # Kiểm tra xem video đã được mở chưa
        if not cap.isOpened():
            print("Không thể mở video")
            return

        # Lặp qua từng frame trong video và hiển thị trên màn hình
        while True:
            # Đọc frame từ video
            ret, frame = cap.read()
            if not ret:
                break

            # Hiển thị frame trên màn hình
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(
                frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(image)
            self.video_label.setPixmap(pixmap)

            # Chờ một khoảng thời gian rồi hiển thị frame tiếp theo
            QtWidgets.QApplication.processEvents()
            time.sleep(1 / 30)

        # Giải phóng tài nguyên
        cap.release()

    # Tách video thành các frames
    def video_to_frames(self):

        # Load video từ file
        if len(str(self.video_path)) == 0:
            self.label_tach.setText("Chưa chọn video để tải lên")
            return

        # Thay đổi đường dẫn đến video của bạn
        video_path = str(self.video_path)
        cap = cv2.VideoCapture(video_path)

        # Kiểm tra xem video đã được mở chưa
        if not cap.isOpened():
            self.label_tach.setText("Không thể mở video")
            exit()
        self.label_tach.setText("Đang diễn ra quá trình tách")
        # Tạo thư mục frames nếu chưa tồn tại
        output_folder = "frames_tach"
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Lặp qua từng frame trong video và lưu lại thành các file ảnh
        frame_idx = 0

        while True:
            # Đọc frame từ video
            ret, frame = cap.read()
            if not ret:
                break

            # Ghi frame thành file ảnh
            # Lưu file ảnh vào thư mục frames
            frame_filename = os.path.join(
                output_folder, f"frame_{frame_idx}.png")
            cv2.imwrite(frame_filename, frame)
            # self.label_tach.setText("Đang diễn ra quá trình tách")

            # Tăng số thứ tự frame
            frame_idx += 1

        # Giải phóng tài nguyên
        cap.release()
        cv2.destroyAllWindows()
        self.label_tach.setText("Quá trình tách thành công")

    # Hiện thị thức tự các frames chuyển cảnh
    def show_frames_change(self):
        output_folder_change = "frames_change"
        if os.path.exists(output_folder_change):
            shutil.rmtree(output_folder_change)

        kq = "Các frames chuyển cảnh ở các frame: "
        # Đường dẫn đến folder chứa các ảnh
        input_folder = "frames_tach"
        # Tạo thư mục frames_change nếu chưa tồn tại

        if not os.path.exists(output_folder_change):
            os.makedirs(output_folder_change)

        # Lấy danh sách các file trong folder
        image_files = os.listdir(input_folder)
        image_files.sort()
        # Lặp qua các file trong danh sách để đọc ảnh
        prev_dct = None  # Hệ số DCT của ảnh trước đó
        for idx, filename in enumerate(image_files):
            # Đọc ảnh từ file
            image_path = os.path.join(input_folder, filename)
            frame = cv2.imread(image_path)

            # Chuyển đổi ảnh sang grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Thực hiện biến đổi DCT
            dct = cv2.dct(np.float32(gray))
            # So sánh hệ số DCT của ảnh hiện tại với ảnh trước đó (nếu có)
            if prev_dct is not None:
                # Tính độ khác biệt giữa hệ số DCT của hai ảnh
                diff = cv2.absdiff(dct, prev_dct)

                # Xác định ngưỡng để phát hiện cảnh chuyển
                # Ngưỡng phát hiện cảnh chuyển (có thể điều chỉnh)
                threshold = 10000
                if np.sum(diff) > threshold:
                    # print(f"Cảnh chuyển xảy ra ở ảnh {idx}")
                    kq += str(idx) + ", "
                    change_frame_filename = os.path.join(
                        output_folder_change, f"frame_{idx}.png")
                    cv2.imwrite(change_frame_filename, frame)

            # Lưu hệ số DCT của ảnh hiện tại để làm ảnh trước đó cho lần lặp tiếp theo
            prev_dct = dct

        # Hủy các cửa sổ đang hiển thị (nếu có)
        cv2.destroyAllWindows()
        self.label_change_frame.setText("Thành công!")
        self.text_frames_change.setText(kq)

    def giau_tin_ham(img, message):
        height, width, channels = img.shape
        message_len = len(message)
        if message_len * 8 > height * width * channels:
            raise ValueError("Message is too large for image.")
        message += '\0' * (height * width * channels // 8 - message_len)
        binary_message = ''.join(format(ord(i), '08b') for i in message)
        binary_index = 0
        for row in range(height):
            for col in range(width):
                for channel in range(channels):
                    if binary_index >= len(binary_message):
                        return img
                    img[row][col][channel] = (
                        img[row][col][channel] & 254) + int(binary_message[binary_index])
                    binary_index += 1
        return img

    def extract_message(self, img):
        binary_message = ''
        height, width, channels = img.shape
        for row in range(height):
            for col in range(width):
                for channel in range(channels):
                    binary_message += str(img[row][col][channel] & 1)
        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i + 8]
            if byte == '00000000' or byte == '0010 0000':
                break
            message += chr(int(byte, 2))
        return message

    def giau_tin_button(self):
        print(str(self.text_sub_edit.text()) +
              " " + str(self.num_frames_edit.text()))
        s = self.num_frames_edit.text()
        list = (s.split(" "))
        n = len(list)
        messages = str(self.text_sub_edit.text()+"  ")
        lenth_packet = round(len(messages)/n)
        if (lenth_packet <= 0):
            lenth_packet = 1
            n = 1
        list_message = [messages[i:i+lenth_packet]
                        for i in range(0, len(messages), lenth_packet)]

        for i in range(0, n):
            s = f"frames_change/frame_{list[i]}.png"
            path_frame_change = s
            # path_frame_change = str("frames_change"+r'\\'+"frame_"+str(list[i])+".png")
            print(path_frame_change + "\n")
            img = cv2.imread(path_frame_change)
            if (i >= len(list_message)):
                list_message.append(' ')
            img_with_message = self.giau_tin_ham(img, list_message[i])
            cv2.imwrite(path_frame_change, img_with_message)

    def center(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
