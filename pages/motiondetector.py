import streamlit as st
import cv2

st.title("Motion Detector")
start = st.button("Start camera")
stop = st.button("Stop camera")

first_frame = None
status_list = []

if start:
    streamlit_image = st.image([])
    video = cv2.VideoCapture(0)

    while True:

        status = 0  # status 0 means there is no movement (no rectangle)
        # read the current frame from the camera
        check, frame = video.read()

        # to reduce the processing power, we can convert the frame to grayscale (black and white)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Another transformation to apply to make calculations more efficient is gaussian blur method (reduces noise)
        # 3 arguments: the image to apply, the amount of blurness, standard deviation
        gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if first_frame is None:
            first_frame = gray_frame_gau

        delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

        thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

        # To remove noise, we can dilate the image (makes the white area more white)
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

        # find contours (the white areas) in the dilated image
        contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue

            # draw a rectangle around the contour (the moving object)
            x, y, w, h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if rectangle.any():
                status = 1  # status 1 means there is movement (rectangle)

        cv2.putText(frame, "Spot The Bae", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (20, 100, 255), 1, cv2.LINE_AA)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        streamlit_image.image(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

