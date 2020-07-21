import xlwt


class Store:
    def __init__(self):
        self.count = 0
        self.Excel_book = xlwt.Workbook(encoding='utf8')
        self.sheet = self.Excel_book.add_sheet("地球科学学院")
        self.sheet.write(0, 0, '序号')
        self.sheet.write(0, 1, '姓名')
        self.sheet.write(0, 2, '入职时间')
        self.sheet.write(0, 3, '职称')
        self.sheet.write(0, 4, '毕业学校')
        self.sheet.write(0, 5, '性别')
        self.sheet.write(0, 6, '学科')
        self.sheet.write(0, 7, '项目信息')
        self.sheet.write(0, 8, '论文信息')
        self.sheet.write(0, 9, '个人主页链接')

    def save(self):
        self.Excel_book.save('中国地质大学.xls')
