import cv2
import numpy as np
import csv
from ultralytics import YOLO

points = []
court_line=[]
# 鼠标点击事件处理函数
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"点击坐标: ({x}, {y})")
        # 在点击位置画一个小圆圈作为标记
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Select Court Boundary", frame)
# 加载YOLOv8模型
model = YOLO('yolov8n.pt')

# 打开视频文件
video_path = r"D:\\qq\\video_input2.mp4"
cap = cv2.VideoCapture(video_path)
if cap:
    print("视频文件存在")
else:
    print("无法打开")

success, frame = cap.read()
if success:
    # 创建一个窗口并绑定鼠标点击事件
    cv2.namedWindow("Select Court Boundary",cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Select Court Boundary", click_event)

    print("请点击球场边界的点位，按 'q' 键结束选择并保存坐标。")
    # while True:
    #     cv2.imshow("Select Court Boundary", frame)
    #     key = cv2.waitKey(1) & 0xFF
    #     if key == ord('q'):
    #         break
    # cv2.destroyWindow("Select Court Boundary")
    # 定义鸟瞰图的目标尺寸
    width = 600
    height = 900

    padding = 150  # 四周的边距
    dst_points = np.float32([[padding, padding], [width - padding, padding], [width - padding, height - padding],
                             [padding, height - padding]])
    src_points = np.float32(points)

    # 定义目标点（鸟瞰图上的四个角点）
    # dst_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    # src_points = np.float32(points)

    # 计算透视变换矩阵
    perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # 标准网球场尺寸（双打）
    court_length = 23.77
    court_width = 10.97
    singles_court_width = 8.23
    # 网的位置
    net_position = court_length / 2

    # 计算鸟瞰图中网球场的尺寸
    available_width = width - 2 * padding
    available_height = height - 2 * padding
    scale = min(available_width / court_width, available_height / court_length)
    court_width_pixels = int(court_width * scale)
    court_length_pixels = int(court_length * scale)
    singles_court_width_pixels = int(singles_court_width * scale)
    # 创建一个空白图像用于绘制网球场
    court_image = np.zeros((height, width, 3), dtype=np.uint8)
    # 设置背景颜色，这里以绿色为例
    court_image[:] = (0, 128, 0)

    # 计算网球场在鸟瞰图中的位置
    start_x = padding + (available_width - court_width_pixels) // 2
    start_y = padding + (available_height - court_length_pixels) // 2

    # 绘制网球场的基本线条
    # 外边框（双打边线）
    cv2.rectangle(court_image, (start_x, start_y), (start_x + court_width_pixels, start_y + court_length_pixels),
                  (255, 255, 255), 2)
    # 中线
    cv2.line(court_image, (start_x + court_width_pixels // 2, start_y),
             (start_x + court_width_pixels // 2, start_y + court_length_pixels), (255, 255, 255), 2)
    # 发球线
    service_line_y = start_y + int(net_position * scale)
    cv2.line(court_image, (start_x, service_line_y), (start_x + court_width_pixels, service_line_y), (255, 255, 255), 2)
    # 单打边线
    single_side_offset = (court_width_pixels - singles_court_width_pixels) // 2
    cv2.line(court_image, (start_x + single_side_offset, start_y),
             (start_x + single_side_offset, start_y + court_length_pixels), (255, 255, 255), 2)
    cv2.line(court_image, (start_x + court_width_pixels - single_side_offset, start_y),
             (start_x + court_width_pixels - single_side_offset, start_y + court_length_pixels), (255, 255, 255), 2)
    cv2.line(court_image,(start_x+single_side_offset,start_y+200),(start_x+court_width_pixels-single_side_offset,start_y+200),(255,255,255),2)
    cv2.line(court_image, (start_x + single_side_offset, start_y+court_length_pixels - 200),
             (start_x + court_width_pixels - single_side_offset, start_y + court_length_pixels - 200), (255, 255 , 255), 2)

    # v2.imshow("Standard Tennis Court Bird's Eye View", court_image)
    # print(points)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_filename = 'bird_eye_view_video.avi'
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))
    test_out=cv2.VideoWriter("input_video.avi",fourcc,fps,(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # 在帧上运行YOLOv8追踪，持续追踪帧间的物体
            results = model.track(frame, persist=True)
            # 在帧上展示结果
            annotated_frame = results[0].plot()
            # 展示带注释的帧
            cv2.imshow("YOLOv8 Tracking", annotated_frame)
            # 复制一份球场图像用于绘制球员位置
            court_with_players = court_image.copy()

            # 获取检测到的球员的边界框
            boxes = results[0].boxes.xyxy.cpu().numpy()
            classes = results[0].boxes.cls.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.id is not None else []
            for i, box in enumerate(boxes):
                # 检查类别是否为 person（通常类别编号为 0）
                if classes[i] == 0:
                    # 计算边界框的中心点
                    x1, y1, x2, y2 = box
                    center_x = int((x1 + x2) / 2)
                    center_y = int(y2)

                    # 将中心点坐标进行透视变换
                    point = np.array([[center_x, center_y]], dtype=np.float32)
                    point = np.array([point])
                    mapped_point = cv2.perspectiveTransform(point, perspective_matrix)[0][0]
                    if ids[i]==3:
                        with open('player3.csv', 'a', newline='') as csvfile:
                            # 创建 CSV 写入器
                            writer = csv.writer(csvfile)
                            # 写入每一行坐标
                            writer.writerow(mapped_point)
                    # 在球场图像上绘制球员位置
                    cv2.circle(court_with_players, (int(mapped_point[0]), int(mapped_point[1])), 5, (0, 0, 255), -1)
            # 显示带有球员位置的球场图像
            cv2.imshow("Court with Players", court_with_players)
            out.write(court_with_players)
            test_out.write(annotated_frame)
            # 如果按下'q'则退出循环
            # bird_eye_view = cv2.warpPerspective(frame, perspective_matrix, (width, height))
            # cv2.imshow("Bird's Eye View", bird_eye_view)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # 如果视频结束则退出循环
            break

cap.release()
cv2.destroyAllWindows()

