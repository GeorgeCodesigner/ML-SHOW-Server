from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
import json
import numpy.matlib
import numpy as np
# 线性回归算法/单变量线性回归算法
def lr_oneVar(request):
    data = {}
    try:
        area=[]
        price=[]
        region = request.GET['region']
        # 根据region读取相应的文件
        arr = region.split(',')
        with open('sl/static/resources/oneVarData/sz_'+arr[len(arr)-1]+'.txt', 'r') as f:
            # 将每一行相应的值分别存在area和price数组中
            for line in f.readlines():
                lineArr = line.strip().split(',')
                area.append(float(lineArr[0]))
                price.append(float(lineArr[1]))
        # 退出with open,自动关闭文件
        m=len(price)
        # 选择假设函数模型为单变量线性回归:h(x) = theta_0 + theta_1 * x
        X=np.hstack((np.matlib.ones((m, 1)), np.asmatrix(area).reshape((m,1)))) # 增加x_0项，对area数组转换成的矩阵,然后重组成m*1的矩阵
        theta=normalEqn(X,price)
        if isinstance(theta, bool)==True:
            data['success'] = False
            data['message'] = '请求成功但计算过程出错'
        else:
            print('正规方程算法求出的theta:', theta.getA1().tolist())
            J = computeCost(X, price, theta)
            print('正规方程算法求出的代价函数最小值J_min:', J)
            if J != False:
                thetaList = theta.getA1().tolist()
                thetaArr=[]
                for i in range(0, len(thetaList)):
                    thetaArr.append(round(thetaList[i], 2)) # 保留两位小数
                data['success'] = True
                data['message'] = '请求成功'
                data['theta'] = thetaArr
                data['J'] = round(J,2)
                data['x']=area
                data['y']=price
            else:
                data['success'] = False
                data['message'] = '请求成功但计算过程出错'
    except:
        data['success'] = False
        data['message'] = '请求失败，请稍后再试'
    finally:
        return HttpResponse(json.dumps(data), content_type="application/json")

# 正规方程算法的实现方法
def normalEqn(X, y):
    try:
        XT=np.transpose(X) #对X转置
        theta=np.dot(np.dot(np.linalg.pinv(np.dot(XT,X)),XT),y)
        theta=np.transpose(theta) #对theta转置
        return theta
    except:
        # 如果有错误就返回False
        return False
# 计算代价函数的方法
def computeCost(X, y, theta):
    try:
        m=len(y)
        Y=np.asmatrix(y).reshape((m,1)) #对y数组转换成的矩阵,然后重组成m*1的矩阵
        J=0
        h=np.dot(X,theta)
        z=h-Y
        zArr=np.transpose(z).getA1().tolist() #对z转置，然后转换成ndarray，再转换成数组
        for i in range(0,len(zArr)):
            J = J + np.square(zArr[i])
        J = J/(2*m)
        return J
    except:
        return False