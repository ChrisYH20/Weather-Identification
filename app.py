from flask import Flask, render_template, request, redirect, url_for
import os

from werkzeug.utils import secure_filename

from predict_wed import predict_image
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # 保存上传的文件
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # filename = f"{timestamp}_{file.filename}"
            # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # file.save(filepath)
            # 修改app.py中的这部分代码
            filename = f"{timestamp}_{secure_filename(file.filename)}"  # 使用secure_filename处理文件名
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')  # 确保使用正斜杠
            file.save(filepath)

            # 进行预测
            result = predict_image(filepath)

            return render_template('index.html',
                                   image_path=filepath,
                                   prediction=result)

    return render_template('index.html')


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', debug=True)