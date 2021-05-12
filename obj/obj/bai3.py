class nguoi:
    def __init__(self,name):
        self.name = name
    def xuat(self):
        print(self.name)

class sinhvien(nguoi):
    def __init__(self,sname,sclass):
        nguoi.__init__(self,sname)
        self.sclass = sclass

sv1 = sinhvien("nguyễn văn a","CNTT")
print(sv1.name,sv1.sclass)