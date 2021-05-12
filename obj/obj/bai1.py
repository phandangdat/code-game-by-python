#khai báo lớp
class nguoi:
    #khai báo thuộc tinh
    #ten = "nguyễn văn a"
    def __init__(self,name):
        self.ten = name
    def xuat(self):
        print("xin chào:",self.ten)

#khởi tạo đối tượng thuộc lớp người
nguoi1 = nguoi("nguyễn văn b")
nguoi1.xuat()
