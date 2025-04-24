from ultralytics import YOLO
from scripts.raw_court import Court
import cv2

class Detection:
    def __init__(self,model_ball_path,model_player_path,video_path):
        self.model_ball_path=model_ball_path
        self.model_player_path=model_player_path
        self.video_path=video_path
        self.ballpos=[]
        self.playerpos=[]



    def detect(self):
        mycourt=Court(self.video_path)
        model_ball = YOLO(self.model_ball_path)
        model_player = YOLO(self.model_player_path)
        cap = cv2.VideoCapture(self.video_path)
        if cap:
            print("视频文件存在")
        else:
            print("无法打开")

        mycourt.test()
        while cap.isOpened():
            # 读取视频帧
            success, frame = cap.read()

            if success:
                # 对当前帧进行推理
                results_ball = model_ball(frame,conf=0.5)
                results_player=model_player.track(frame)
                # 获取球员坐标
                # boxes_player = results_player[0].boxes.xyxy
                # img=mycourt.draw_player(boxes_player)
                boxes_player = []
                try:
                    boxes_player = results_player[0].boxes
                    xyxy_player = boxes_player.xyxy.cpu().numpy()
                    cls_player = boxes_player.cls.cpu().numpy()
                    names = model_player.names

                    for i in range(len(xyxy_player)):
                        x1, y1, x2, y2 = xyxy_player[i].astype(int)
                        class_index = int(cls_player[i])
                        class_name = names[class_index]
                        if class_name == 'person':
                            self.playerpos.append((x1, y1, x2, y2))  # 将球员坐标添加到列表
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                            print(f"检测到类别: {class_name}, 坐标: ({x1}, {y1}, {x2}, {y2})")
                    img=mycourt.draw_player(self.playerpos)
                    self.playerpos.clear()
                except IndexError:
                    print("未检测到球员")



                print(boxes_player)
                # # 获取小球的坐标
                boxes_ball = results_ball[0].boxes.xyxy
                print("ball:",boxes_ball)
                # # 把小球绘制到图上
                test_img=mycourt.draw_ball(boxes_ball,img)

                # 获取带有检测结果的帧
                annotated_frame = results_ball[0].plot(img=frame)
                # annotated_frame = results_player[0].plot(img=annotated_frame)
                cv2.imshow("YOLO Inference", annotated_frame)
                cv2.imshow("test",test_img)
                # 按 'q' 键退出循环
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # 视频结束，退出循环
                break

        # 释放资源
        cap.release()
        cv2.destroyAllWindows()

