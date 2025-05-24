import torch
import torchvision.transforms as transforms
from PIL import Image
from config import Common

def predict_image(image_path, model_path='./model/weather-2025-05-14-15-05-07.pth'):
    # 1. 读取图片
    image = Image.open(image_path)
    # 2. 进行缩放
    image = image.resize(Common.imageSize)
    # 3. 加载模型
    model = torch.load(model_path, weights_only=False,map_location="cpu")
    model = model.to(Common.device)
    model.eval()
    # 4. 转为tensor张量
    transform = transforms.ToTensor()
    x = transform(image)
    x = torch.unsqueeze(x, 0)  # 升维
    x = x.to(Common.device)
    # 5. 传入模型
    with torch.no_grad():
        output = model(x)
    # 6. 使用argmax选出最有可能的结果
    output = torch.argmax(output)
    return Common.labels[output.item()]