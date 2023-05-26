from ultralytics import YOLO


class PlantsAI:
    def __init__(self, weights_path, image_size=224):
        self.model = YOLO(weights_path, task='classify')
        self.image_size = image_size

    def __call__(self, image):
        results = self.model(source=image, imgsz=[self.image_size, self.image_size])
        class_names = []
        for result in results:
            index = result.probs.argmax()
            class_name = result.names[int(index)]
            class_names.append(class_name)
        return class_names
    
    def __del__(self):
        del self.model
