class sinhvien:
    name = []
    age = []
    def __init__(self,name,age):
        self.name.append(name)
        self.age.append(age)
    def nhap(self):
        n = int(input("nhập vào số lượng sinh viên: "))
        for i in range(0,n):
            self.name.append(input("nhập vào tên sinh viên " + str(i+1) + ": "))
            self.age.append(input("nhập vào tuổi sinh viên: " + str(i+1) + ":"))
    def xuat(self):
        print("danh sách sinh viên là")
        for i in range(1,len(self.name)):
            print("tên:",self.name[i],"tuổi:",self.age[i])

sv1 = sinhvien("nguyễn văn a",14)
sv1.nhap()
sv1.xuat()