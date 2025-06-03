import cv2
import os
from natsort import natsorted

def pngs_to_mp4(input_folder, output_file, fps=30):
    # 获取所有png图片路径，并排序
    images = [img for img in os.listdir(input_folder) if img.endswith(".jpg") or img.endswith(".png")]
    images = natsorted(images)
    print(f'{images =  }')
    if not images:
        print("No PNG images found in the folder.")
        return

    # 读取第一张图片确定尺寸
    first_img_path = os.path.join(input_folder, images[0])
    frame = cv2.imread(first_img_path)
    height, width, layers = frame.shape

    # 定义视频编码器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(input_folder, image)
        frame = cv2.imread(img_path)
        if frame is None:
            print(f"Warning: Unable to read {img_path}")
            continue
        video.write(frame)

    video.release()
    print(f"Video saved as {output_file}")

def merge_imgs_to_mp4(input_folder1, input_folder2, output_file, fps=30):
    """
    将input_folder1和input_folder2中的图片按文件名排序后，横向拼接（宽度方向），合成视频。
    Args:
        input_folder1 (str): 第一个图片文件夹路径
        input_folder2 (str): 第二个图片文件夹路径
        output_file (str): 输出视频文件路径
        fps (int): 视频帧率
    """
    # 获取两个文件夹下的图片名并排序
    images1 = [img for img in os.listdir(input_folder1) if img.endswith(".jpg") or img.endswith(".png")]
    images2 = [img for img in os.listdir(input_folder2) if img.endswith(".jpg") or img.endswith(".png")]
    images1 = natsorted(images1)
    images2 = natsorted(images2)
    print(f'{images1 = }')
    print(f'{images2 = }')

    # 取两者最短长度，避免越界
    min_len = min(len(images1), len(images2))
    if min_len == 0:
        print("No images found in one of the folders.")
        return

    # 读取第一对图片，确定尺寸
    img1 = cv2.imread(os.path.join(input_folder1, images1[0]))
    img2 = cv2.imread(os.path.join(input_folder2, images2[0]))
    if img1 is None or img2 is None:
        print("Error reading the first image from one of the folders.")
        return

    # 如果高度不一致，调整img2到img1的高度
    if img1.shape[0] != img2.shape[0]:
        img2 = cv2.resize(img2, (img2.shape[1], img1.shape[0]))
    # 如果宽度不一致，也可以选择resize，或直接拼接
    height = img1.shape[0]
    width = img1.shape[1] + img2.shape[1]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for i in range(min_len):
        frame1 = cv2.imread(os.path.join(input_folder1, images1[i]))
        frame2 = cv2.imread(os.path.join(input_folder2, images2[i]))
        if frame1 is None or frame2 is None:
            print(f"Warning: Unable to read {images1[i]} or {images2[i]}")
            continue
        # 调整高度一致
        if frame1.shape[0] != frame2.shape[0]:
            frame2 = cv2.resize(frame2, (frame2.shape[1], frame1.shape[0]))
        # 横向拼接
        merged = cv2.hconcat([frame1, frame2])
        video.write(merged)

    video.release()
    print(f"Merged video saved as {output_file}")


    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert PNG images to MP4 video.")
    parser.add_argument("--input_folder", type=str, help="Folder containing PNG images")
    parser.add_argument("--input_folder2", type=str, help="Second folder containing PNG images for merging")
    parser.add_argument("--output_file", type=str, help="Output MP4 video file")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second for the output video")
    parser.add_argument("--merge", action='store_true', help="Merge two folders of images into a single video")
    args = parser.parse_args()
    print(f'{args = }')
    input_folder = args.input_folder  # 修改为你的图片文件夹路径
    output_file = args.output_file
    if args.merge:
        # input_folder2 = input("Enter the second input folder for merging: ")
        merge_imgs_to_mp4(input_folder, args.input_folder2, output_file, fps=args.fps)
    else:
        pngs_to_mp4(input_folder, output_file, fps=args.fps)