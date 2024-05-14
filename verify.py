import cv2
import os

# Function to parse YOLO format label files
def parse_label_file(label_file):
    boxes = []
    with open(label_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            if len(parts) < 3:
                continue
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            boxes.append((class_id, x_center, y_center, width, height))
    return boxes

# Function to create directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to save cropped images of a specific class
def save_cropped_images_of_class(image_dir, label_dir, class_id):
    class_dir = f'class_{class_id}'
    create_directory(class_dir)
    for filename in os.listdir(label_dir):
        if filename.endswith('.txt'):
            label_file = os.path.join(label_dir, filename)
            image_file = os.path.join(image_dir, os.path.splitext(filename)[0] + '.' + image_format)
            if os.path.exists(image_file):
                image = cv2.imread(image_file)
                boxes = parse_label_file(label_file)
                for idx, box in enumerate(boxes):
                    if box[0] == class_id:
                        image_height, image_width, _ = image.shape
                        x_center = int(box[1] * image_width)
                        y_center = int(box[2] * image_height)
                        box_width = int(box[3] * image_width)
                        box_height = int(box[4] * image_height)
                        x_min = max(int(x_center - box_width / 2), 0)
                        y_min = max(int(y_center - box_height / 2), 0)
                        x_max = min(int(x_center + box_width / 2), image_width)
                        y_max = min(int(y_center + box_height / 2), image_height)
                        cropped_image = image[y_min:y_max, x_min:x_max]
                        cropped_filename = f'{filename.split(".")[0]}_{idx}.{image_format}'
                        cv2.imwrite(os.path.join(class_dir, cropped_filename), cropped_image)

# Example usage
image_dir = 'images'
label_dir = 'labels'
image_format = 'png'
classes = 13  # Change this to the desired class ID
for cls in range(classes):
    save_cropped_images_of_class(image_dir, label_dir, cls)