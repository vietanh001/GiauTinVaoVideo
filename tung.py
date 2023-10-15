import cv2
import numpy as np

def dct_coefficients(frame):
    return cv2.dct(np.float32(frame)/255.0)

def idct_coefficients(frame):
    return cv2.idct(frame) * 255.0

def lsb_embed(data, frame):
    index = 0
    for x in range(frame.shape[0]):
        for y in range(frame.shape[1]):
            if index < len(data):
                frame[x][y] = (frame[x][y] & ~1) | (data[index] & 1)
                index += 1
            else:
                break
    return frame

def extract_lsb(frame, size):
    extracted_data = bytearray()
    index = 0
    for x in range(frame.shape[0]):
        for y in range(frame.shape[1]):
            if index < size:
                extracted_data.append(frame[x][y] & 1)
                index += 1
            else:
                break
    return extracted_data

def scene_change_detection(video_path, threshold):
    cap = cv2.VideoCapture(video_path)
    _, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_dct = dct_coefficients(prev_gray)

    scene_changes = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dct = dct_coefficients(gray)

        diff = np.abs(prev_dct - dct)
        if np.mean(diff) > threshold:
            scene_changes.append(cap.get(cv2.CAP_PROP_POS_FRAMES))

        prev_dct = dct

    cap.release()
    return scene_changes

def embed_data_in_video(video_path, output_path, data, threshold):
    scene_changes = scene_change_detection(video_path, threshold)

    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    frame_number = 0
    data_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_number in scene_changes and data_index < len(data):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            dct = dct_coefficients(gray)
            modified_dct = lsb_embed(data[data_index], dct)
            modified_gray = idct_coefficients(modified_dct)
            frame = cv2.cvtColor(np.uint8(modified_gray), cv2.COLOR_GRAY2BGR)
            data_index += 1

        out.write(frame)
        frame_number += 1

    cap.release()
    out.release()

def main():
    video_path = 'video.mp4' # Đường dẫn tới video đầu vào
    output_path = 'output_video.mp4' # Đường dẫn tới video đầu ra sau khi giấu tin
    data = bytearray(b'secret_message') # Dữ liệu cần giấu
    threshold = 0.5 # Ngưỡng chuyển cảnh

    # Nhúng dữ liệu vào video
    embed_data_in_video(video_path, output_path, data, threshold)

    # Giả sử chúng ta muốn trích xuất dữ liệu đã giấu trong video
    scene_changes = scene_change_detection(output_path, threshold)
    cap = cv2.VideoCapture(output_path)
    extracted_data = bytearray()

    for scene_change in scene_changes:
        cap.set(cv2.CAP_PROP_POS_FRAMES, scene_change)
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            dct = dct_coefficients(gray)
            extracted_data.extend(extract_lsb(dct, 8))  # Giả định mỗi khung chứa 8 bit dữ liệu

    # Chuyển dữ liệu trích xuất thành chuỗi
    extracted_data = bytes(extracted_data)
    extracted_message = extracted_data.decode('utf-8')
    print(f"Extracted message: {extracted_message}")

if __name__ == '__main__':
    main()
