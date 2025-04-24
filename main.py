from utils import read_video, save_video
from ultralytics import YOLO
from trackers import BallTracker
from scripts.raw_court import Court
from show.heatmap import Map
import cv2
import numpy as np
# 初始化球体追踪器
model_ball="E:/MyTennis/Tennis_System/train/yolo_tennis.pt"
model_player="E:/MyTennis/Tennis_System/train/yolo11n.pt"
input_video_path = "D:/qq/video_input2.mp4"


# 加载模型
tracker = BallTracker(model_path=model_ball)
model=YOLO(model_player)
# 读取视频所有帧
video_frames = read_video(input_video_path)
bird_outputframes=[]
pos_player=[]
# 第一阶段：检测所有帧的球位置
ball_detections = []
for frame in video_frames:
    ball_dict = tracker.detect_frame(frame)
    ball_detections.append(ball_dict)

# 第二阶段：统一插值处理
interpolated_detections = tracker.interpolate_ball_positions(ball_detections)
# 第三阶段：绘制边界框
output_frames = tracker.draw_bboxes(video_frames, interpolated_detections)

# 绘制球场鸟瞰图
court=Court(input_video_path)
court.test()
court_image=court.draw_court()
court_copy=court_image.copy()
# output_frames = tracker.draw_bboxes(video_frames, ball_detections)


# 显示原始视频追踪结果
for i,frame in enumerate(output_frames):
    results=model(frame)
    # 对每一帧进行球检测
    # court_image = np.zeros_like(court_image)
    court_image = court.draw_court()
    coordinates = interpolated_detections[i][1]
    x1, y1, x2, y2 = coordinates
    center_x = int((x1 + x2) / 2)
    center_y = int(y2)
    # 将中心点坐标进行透视变换
    point = np.array([[center_x, center_y]], dtype=np.float32)
    point = np.array([point])
    mapped_point = cv2.perspectiveTransform(point, court.perspective_matrix)[0][0]
    cv2.circle(court_image, (int(mapped_point[0]), int(mapped_point[1])), 5, (0, 0, 255), -1)
    cv2.putText(court_image, 'Tennis ball', (int(mapped_point[0]) + 10, int(mapped_point[1])),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    # cv2.imshow("Ball Detection", court_image)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    try:
        boxes_player = results[0].boxes
        xyxy_player = boxes_player.xyxy.cpu().numpy()
        cls_player = boxes_player.cls.cpu().numpy()
        names = model.names

        for i in range(len(xyxy_player)):
            x1, y1, x2, y2 = xyxy_player[i].astype(int)
            class_index = int(cls_player[i])
            class_name = names[class_index]
            if class_name == 'person'and x1>400 and x2<1500 :
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "player", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                center_x = int((x1 + x2) / 2)
                center_y = int(y2)
                point = np.array([[center_x, center_y]], dtype=np.float32)
                point = np.array([point])
                mapped_point = cv2.perspectiveTransform(point, court.perspective_matrix)[0][0]
                cv2.circle(court_image, (int(mapped_point[0]), int(mapped_point[1])), 5, (255, 0, 0), -1)
                if int(mapped_point[1])<450:
                    cv2.putText(court_image, 'player A', (int(mapped_point[0]) + 10, int(mapped_point[1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                else:
                    cv2.putText(court_image, 'player B', (int(mapped_point[0]) + 10, int(mapped_point[1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                pos_player.append((mapped_point[0],mapped_point[1]))
    except IndexError:
        print("未检测到球员")
    cv2.imshow("Ball Detection", court_image)
    cv2.imshow("Results Show", frame)
    bird_outputframes.append(court_image)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# 鸟瞰图结果
# for item in interpolated_detections:
#     coordinates = item[1]
#     x1, y1, x2, y2 = coordinates
#     center_x = int((x1 + x2) / 2)
#     center_y = int(y2)
#     # 将中心点坐标进行透视变换
#     point = np.array([[center_x, center_y]], dtype=np.float32)
#     point = np.array([point])
#     mapped_point = cv2.perspectiveTransform(point, court.perspective_matrix)[0][0]
#     cv2.circle(court_image, (int(mapped_point[0]), int(mapped_point[1])), 5, (0, 0, 255), -1)
#     cv2.imshow("Ball Detection", court_image)
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         break
# 绘制热力图
mymap=Map()
mymap.Heatmap(court_copy,pos_player)

save_video(output_frames, "output_videos/output.avi")
save_video(bird_outputframes,"output_videos/bird_out.avi")
cv2.destroyAllWindows()