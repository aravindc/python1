from imageai.Detection import ObjectDetection
import os

execution_path = os.path.dirname(__file__).replace('\\', '/')+'/'

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(
     os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
     # os.path.join(execution_path, "resnet_model_ex-020_acc-0.651714.h5"))
detector.loadModel()
custom_objects = detector.CustomObjects(person=True, car=False)
detections = detector.detectCustomObjectsFromImage(
      input_image=os.path.join(execution_path, "test3.jpg"),
      output_image_path=os.path.join(execution_path, "image_new.png"),
      custom_objects=custom_objects, minimum_percentage_probability=60)


for eachObject in detections:
    print(eachObject["name"] + " : " + eachObject["percentage_probability"])
    print("--------------------------------")
