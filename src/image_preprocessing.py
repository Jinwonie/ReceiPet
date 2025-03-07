import cv2
import numpy as np
import streamlit as st
from base64 import b64encode

def receipt_preprocessing(image):
    try:
        # 입력 이미지를 numpy.ndarray로 읽기
        file_bytes = np.frombuffer(image.read(), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        height, width = img.shape[:2]

        # 전처리: Grayscale
        target_width = 1024
        aspect_ratio = height / width
        new_size = (target_width, int(target_width * aspect_ratio))
        resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_CUBIC)

        gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

        blur_img = cv2.GaussianBlur(gray_img, ksize=(5, 5), sigmaX=0, sigmaY=0)

        binary_img = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 11)

        

        # numpy.ndarray 이미지를 Base64로 변환
        _, buffer = cv2.imencode('.png', binary_img)

        base64_image = b64encode(buffer).decode('utf-8')
    
        return base64_image
    except Exception as e:
        st.write("이미지를 처리하는 것에 실패했습니다. 다시 시도해주세요.")
