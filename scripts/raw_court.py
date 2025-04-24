import cv2
import numpy as np
class Court:
    def __init__(self,video_path):
        self.points=[]
        self.video_path=video_path
        self.frame=[]
        self.perspective_matrix=[]


    def click_event(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))
            print(f"点击坐标: ({x}, {y})")
            # 在点击位置画一个小圆圈作为标记
            cv2.circle(self.frame, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Select Court Boundary", self.frame)


    def test(self):
        cap = cv2.VideoCapture(self.video_path)
        success, self.frame = cap.read()
        if success:
            # 创建一个窗口并绑定鼠标点击事件
            cv2.namedWindow("Select Court Boundary", cv2.WINDOW_NORMAL)
            cv2.setMouseCallback("Select Court Boundary", self.click_event)
        print("请点击球场边界的点位，按 'q' 键结束选择并保存坐标。")
        while True:
            cv2.imshow("Select Court Boundary", self.frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        cv2.destroyAllWindows()
        print("已保存的点坐标:", self.points)

    def draw_court(self):
        # 定义图的尺寸
        width = 600
        height = 900
        padding = 150  # 四周的边距
        # 标准网球场尺寸（双打）
        court_length = 23.77
        court_width = 10.97
        singles_court_width = 8.23
        # 网的位置（中线）
        net_position = court_length / 2  # 11.885米

        dst_points = np.float32([[padding, padding], [width - padding, padding], [width - padding, height - padding],
                                 [padding, height - padding]])
        src_points = np.float32(self.points)

        # 计算透视变换矩阵
        self.perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

        # 计算鸟瞰图中网球场的尺寸
        available_width = width - 2 * padding
        available_height = height - 2 * padding
        scale = min(available_width / court_width, available_height / court_length)
        court_width_pixels = int(court_width * scale)
        court_length_pixels = int(court_length * scale)
        singles_court_width_pixels = int(singles_court_width * scale)

        # 创建一个空白图像用于绘制网球场
        court_image = np.zeros((height, width, 3), dtype=np.uint8)
        court_image[:] = (0, 128, 0)  # 绿色背景

        # 计算网球场在图像中的起始位置
        start_x = padding + (available_width - court_width_pixels) // 2
        start_y = padding + (available_height - court_length_pixels) // 2

        # 绘制外边框（双打边线）
        cv2.rectangle(court_image, (start_x, start_y),
                      (start_x + court_width_pixels, start_y + court_length_pixels),
                      (255, 255, 255), 2)

        # 绘制中线
        midline_y = start_y + court_length_pixels // 2
        midline_x=start_x+court_width_pixels//2

        # cv2.line(court_image, (start_x + court_width_pixels // 2, start_y),
        #          (start_x + court_width_pixels // 2, start_y + court_length_pixels),
        #          (255, 255, 255), 2)
        #
        cv2.line(court_image,(start_x,midline_y),(start_x+court_width_pixels,midline_y),(0,0,0),2)
        # 计算发球线位置（距离中线6.4米）
        service_line_offset = int(6.4 * scale)  # 转换为像素
        # 上侧发球线（靠近顶边）
        service_line_top = midline_y - service_line_offset
        # 下侧发球线（靠近底边）
        service_line_bottom = midline_y + service_line_offset
        # 绘制单打边线
        single_side_offset = (court_width_pixels - singles_court_width_pixels) // 2
        cv2.line(court_image, (start_x + single_side_offset, start_y),
                 (start_x + single_side_offset, start_y + court_length_pixels),
                 (255, 255, 255), 2)
        cv2.line(court_image, (start_x + court_width_pixels - single_side_offset, start_y),
                 (start_x + court_width_pixels - single_side_offset, start_y + court_length_pixels),
                 (255, 255, 255), 2)

        # 绘制两条发球线
        cv2.line(court_image, (start_x+single_side_offset, service_line_top),
                 (start_x + court_width_pixels-single_side_offset, service_line_top),
                 (255, 255, 255), 2)
        cv2.line(court_image, (start_x+single_side_offset, service_line_bottom),
                 (start_x + court_width_pixels-single_side_offset, service_line_bottom),
                 (255, 255, 255), 2)

        cv2.line(court_image,(midline_x,service_line_top),(midline_x,service_line_bottom),(255,255,255),2)



        return court_image
    # def draw_court(self):
    #     # 定义图的尺寸
    #     width = 600
    #     height = 900
    #     padding = 150  # 四周的边距
    #     # 标准网球场尺寸（双打）
    #     court_length = 23.77
    #     court_width = 10.97
    #     singles_court_width = 8.23
    #     # 网的位置
    #     net_position = court_length / 2
    #
    #     dst_points = np.float32([[padding, padding], [width - padding, padding], [width - padding, height - padding],
    #                              [padding, height - padding]])
    #     src_points = np.float32(self.points)
    #
    #     # 计算透视变换矩阵
    #     self.perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    #
    #
    #     # 计算鸟瞰图中网球场的尺寸
    #     available_width = width - 2 * padding
    #     available_height = height - 2 * padding
    #     scale = min(available_width / court_width, available_height / court_length)
    #     court_width_pixels = int(court_width * scale)
    #     court_length_pixels = int(court_length * scale)
    #     singles_court_width_pixels = int(singles_court_width * scale)
    #     # 创建一个空白图像用于绘制网球场
    #     court_image = np.zeros((height, width, 3), dtype=np.uint8)
    #     # 设置背景颜色，这里以绿色为例
    #     court_image[:] = (0, 128, 0)
    #
    #     # 计算网球场在鸟瞰图中的位置
    #     start_x = padding + (available_width - court_width_pixels) // 2
    #     start_y = padding + (available_height - court_length_pixels) // 2
    #
    #     # 绘制网球场的基本线条
    #     # 外边框（双打边线）
    #     cv2.rectangle(court_image, (start_x, start_y), (start_x + court_width_pixels, start_y + court_length_pixels),
    #                   (255, 255, 255), 2)
    #     # 中线
    #     cv2.line(court_image, (start_x + court_width_pixels // 2, start_y),
    #              (start_x + court_width_pixels // 2, start_y + court_length_pixels), (255, 255, 255), 2)
    #     # 发球线
    #     service_line_y = start_y + int(net_position * scale)
    #     cv2.line(court_image, (start_x, service_line_y), (start_x + court_width_pixels, service_line_y), (255, 255, 255), 2)
    #     # 单打边线
    #     single_side_offset = (court_width_pixels - singles_court_width_pixels) // 2
    #     cv2.line(court_image, (start_x + single_side_offset, start_y),
    #              (start_x + single_side_offset, start_y + court_length_pixels), (255, 255, 255), 2)
    #     cv2.line(court_image, (start_x + court_width_pixels - single_side_offset, start_y),
    #              (start_x + court_width_pixels - single_side_offset, start_y + court_length_pixels), (255, 255, 255), 2)
    #
    #     # cv2.imshow("image",court_image)
    #     # cv2.waitKey(0)
    #     return court_image

    def draw_player(self,boxes):
        imgwithplayer=self.draw_court()
        width = 600
        height = 900
        padding = 150  # 四周的边距
        dst_points = np.float32([[padding, padding], [width - padding, padding], [width - padding, height - padding],
                                 [padding, height - padding]])
        src_points = np.float32(self.points)

        # 计算透视变换矩阵
        self.perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

        for i, box in enumerate(boxes):
            # 计算边界框的中心点
            x1, y1, x2, y2 = box
            center_x = int((x1 + x2) / 2)
            center_y = int(y2)

            # 将中心点坐标进行透视变换
            point = np.array([[center_x, center_y]], dtype=np.float32)
            point = np.array([point])
            mapped_point = cv2.perspectiveTransform(point, self.perspective_matrix)[0][0]

            # 在球场图像上绘制球员位置
            cv2.circle(imgwithplayer, (int(mapped_point[0]), int(mapped_point[1])), 5, (0, 0, 255), -1)
        return imgwithplayer

    def draw_ball(self,boxes,image):
        imgwithball=image
        width = 600
        height = 900
        padding = 150  # 四周的边距
        dst_points = np.float32([[padding, padding], [width - padding, padding], [width - padding, height - padding],
                                 [padding, height - padding]])
        src_points = np.float32(self.points)

        # 计算透视变换矩阵
        perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

        for i, box in enumerate(boxes):
            # 计算边界框的中心点
            x1, y1, x2, y2 = box
            center_x = int((x1 + x2) / 2)
            center_y = int(y2)

            # 将中心点坐标进行透视变换
            point = np.array([[center_x, center_y]], dtype=np.float32)
            point = np.array([point])
            mapped_point = cv2.perspectiveTransform(point, perspective_matrix)[0][0]

            # 在球场图像上绘制球员位置
            cv2.circle(imgwithball, (int(mapped_point[0]), int(mapped_point[1])), 5, (255, 0, 0), -1)
        return imgwithball
