import sys,math
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QFileDialog, QGridLayout, QWidget

class CalInfoEntropyDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("计算对比中英文本的信息熵")
        self.setGeometry(100, 100, 400, 200)
        layout = QGridLayout()
        


        # QTextEdit demo
        # self.text_output = QTextEdit(self)
        # self.text_output.setReadOnly(True)  
        # layout.addWidget(self.text_output)

        # Button demo
        # self.att_button = QPushButton("B", self)
        # self.att_button.clicked.connect(self.hell)
        # self.att_button.setEnabled(True)
        # layout.addWidget(self.att_button)

        self.label_cn = QLabel(f"中文结果：")
        self.label_cn.setFixedHeight(30)
        layout.addWidget(self.label_cn,1,2)  
        

        self.label_en = QLabel(f"英文结果：")
        self.label_en.setFixedHeight(30)
        layout.addWidget(self.label_en,1,4)   
        
        self.line_edit_cn = QLineEdit()
        self.line_edit_cn.setReadOnly(True) 
        layout.addWidget(self.line_edit_cn,2,2)   

        self.line_edit_en = QLineEdit()
        self.line_edit_en.setReadOnly(True) 
        layout.addWidget(self.line_edit_en,2,4) 

        self.load_button_cn = QPushButton("添加中文文本",self)
        self.load_button_cn.clicked.connect(lambda:self.load_file_path("cn"))
        layout.addWidget(self.load_button_cn,3,2)

        self.load_button_en = QPushButton("添加英文文本",self)
        self.load_button_en.clicked.connect(lambda:self.load_file_path("en"))
        layout.addWidget(self.load_button_en,3,4)

        self.load_button_en = QPushButton("计算信息熵",self)
        self.load_button_en.clicked.connect(lambda:self.cal_ent())
        layout.addWidget(self.load_button_en,4,3)

        self.setLayout(layout)

        self.cn_load_file_path = ""
        self.en_load_file_path = ""

    def load_file_path(self,para):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt);;All Files (*)")
        if para=="en":
            self.en_load_file_path = file_path
            self.line_edit_en.setText(file_path)
        elif para=="cn":
            self.cn_load_file_path = file_path
            self.line_edit_cn.setText(file_path)

    def cal_ent(self):
        self.line_edit_en.clear()
        self.line_edit_en.clear()

        res_en = calEntropyBin(getEnTextAsFreqDict(self.en_load_file_path))
        res_cn = calEntropyBin(getCnTextAsFreqDict(self.cn_load_file_path))
        ent_en = f"{res_en:.6f}"  
        ent_cn = f"{res_cn:.6f}" 
        try:
            self.line_edit_en.setText(ent_en)
            self.line_edit_cn.setText(ent_cn)
        except EntValueError as e:
            self.line_edit_en.setText(ent_en)
            self.line_edit_cn.setText(ent_cn)


class EntValueError(Exception):
    def __init__(self, message="数值错"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"EntValueError: {self.message}"


def calSelfInfoBin(prob):
    """
    计算自信息
    返回一个自信息,单位按bit计
    """
    # 截断逻辑
    if prob is None or prob <= 0 or prob > 1:
        raise EntValueError(f"{prob}频率非法")

    return -math.log(prob, 2)


def calEntropyBin(freq: dict):
    """
    计算信息熵
    传入如下格式的字典 {"ch":frequency(double)}
    返回一个信息熵,单位按bit计
    """

    # 截断逻辑
    if freq is None or freq == {} or isinstance(freq, dict) == False:
        raise EntValueError("无效输入")
    else:
        one = 1
        for k, v in freq.items():
            one = one - v
        if one > 0.0001:
            raise EntValueError("频率归一化异常")

    # 计算熵
    ent = 0
    for k, v in freq.items():
        ent = ent + v * calSelfInfoBin(v)
    return ent


def getEnTextAsFreqDict(addr: str) -> dict:
    """
    统计一段任意长的英文文本的字母频率
    传入文本所在的地址
    返回一个如下格式的字典 {"ch":frequency(double)}
    """
    symbol = "abcdefghijklmnopqrstuvwxyz "
    dicf = {}
    count = 0  # 有效字符总数

    try:
        with open(addr, "r", encoding="utf-8") as file:
            textr = file.read().lower()
    except FileNotFoundError as e:
        raise EntValueError("文件不存在")

    # 截断逻辑
    if textr is None or textr == "":
        raise EntValueError("无效输入")

    # 统计有效字符数(含文本清洗逻辑,非“ ”与字母的其他字符不会被计入)
    for ch in textr:
        if ch in symbol and dicf.get(ch) is not None:
            dicf[ch] = dicf[ch] + 1
            count = count + 1
        elif ch in symbol and dicf.get(ch) is None:
            dicf[ch] = 1
            count = count + 1

    # 统计有效字符数频率
    for k, v in dicf.items():
        dicf[k] = dicf[k] / count

    return dicf


def getCnTextAsFreqDict(addr: str) -> dict:
    """
    统计一段任意长的中文文本的汉字频率
    传入文本所在的地址
    返回一个如下格式的字典 {"ch":frequency(double)}
    """
    dicf = {}
    count = 0  # 有效字符总数

    try:
        with open(addr, "r", encoding="utf-8") as file:
            textr = file.read()

    except FileNotFoundError as e:
        raise EntValueError("文件不存在")

    # 截断逻辑
    if (textr is None) or textr == "":
        raise EntValueError("无效输入")

    # 统计有效字符数(含文本清洗逻辑)
    # \u4e00-\u9fa5是常用汉字的unicode码
    for ch in textr:
        if ("\u4e00" <= ch <= "\u9fa5") and dicf.get(ch) is not None:
            dicf[ch] = dicf[ch] + 1
            count = count + 1
        elif ("\u4e00" <= ch <= "\u9fa5") and dicf.get(ch) is None:
            dicf[ch] = 1
            count = count + 1

    # 统计有效字符数频率
    for k, v in dicf.items():
        dicf[k] = dicf[k] / count

    return dicf
        

def _main():
    app = QApplication(sys.argv)
    window = CalInfoEntropyDemo()
    window.show()
    sys.exit(app.exec_())