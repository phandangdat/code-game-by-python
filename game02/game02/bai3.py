a = []
#hảm nhập dữ liêu
def nhap():
    n = int(input("nhập vào số lượng phần tử cần tính tổng: "))
    for i in range(0,n):
        a.append(int(input("nhập vào phần tử thứ " + str(i+1) + ": ")))
        #a[i] = int(input("nhập vào phần tử thứ " + str(i+1) + ": "))
#hàm tính tổng
def tinhtong():
    nhap()
    sum = 0
    for i in a:
        sum = sum + i
    return sum
#hàm xuất tổng
def xuat():
    print(tinhtong())
xuat()