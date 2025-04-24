import cv2
import numpy as np

class Map:
    def __init__(self):
        pass

    def Heatmap(self,court_image,points):

        # 获取图像尺寸
        height, width = court_image.shape[:2]

        # 示例坐标点（替换为你的坐标数据）


        # 创建热力图层
        heatmap = np.zeros((height, width), dtype=np.float32)

        # 绘制每个坐标点的影响区域
        for x, y in points:
            if 0 <= x < width and 0 <= y < height:
                # 在热力图上绘制白色圆点，半径和强度可调
                # cv2.circle(heatmap, (int(x), int(y)), 30, 1, -1)
                temp_heatmap = np.zeros((height, width), dtype=np.float32)
                cv2.circle(temp_heatmap, (int(x), int(y)), 30, 1, -1)
                heatmap += temp_heatmap

        # 应用高斯模糊（调整核大小控制平滑度）
        heatmap = cv2.GaussianBlur(heatmap, (55, 55), 0)

        # 归一化并转换为8位
        heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # 应用颜色映射（JET颜色）
        heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # 混合原图与热力图（调整alpha控制透明度）
        alpha = 0.5
        combined = cv2.addWeighted(court_image, 1 - alpha, heatmap_color, alpha, 0)

        # 显示结果
        cv2.imshow('Court with Heatmap', combined)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 如需保存结果
        cv2.imwrite('output_videos/court_heatmap.png', combined)