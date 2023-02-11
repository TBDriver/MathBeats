import numpy as np 
import matplotlib.pyplot as plt 
from math import factorial
'''
计算多阶贝塞尔函数的各个点坐标
部分代码来源网络(写了好久好恶心)
'''
'''
def Calculator_bezier(control_point1x,control_point1y,control_point2x,control_point2y,Tick):
    def B_nx(n, i, x): # 索引求值
        if i > n:
            return 0
        elif i == 0:
            return (1-x)**n
        elif i == 1:
            return n*x*((1-x)**(n-1))
        return B_nx(n-1, i, x)*(1-x)+B_nx(n-1, i-1, x)*x

    def get_value(p, canshu):
        sumx = 0.
        sumy = 0.
        length = len(p)-1
        for i in range(0, len(p)):
            sumx += (B_nx(length, i, canshu) * p[i][0])
            sumy += (B_nx(length, i, canshu) * p[i][1])
        return sumx, sumy

    def get_newxy(p,x):
        xx = [0] * len(x)
        yy = [0] * len(x)
        for i in range(0, len(x)):
            print('x[i]=', x[i])
            a, b = get_value(p, x[i])
            xx[i] = a
            yy[i] = b
            print('xx[i]=', xx[i])
        return xx, yy

    p = array([       # 控制点,可以通过增加数量改变阶数
        [control_point1x, control_point1y],
        [control_point2x, control_point2y]
    ])

    x = linspace(0, 1, Tick)
    xx, yy = get_newxy(p, x)
    speed=[]
    temp = 0
    
    for i in x,xx:
        for j in range(len(i)):
            if temp == 0:
                speed.append(i[j])
            else:
                speed.append(speed[j]/i[j])
        temp += 1
    
    return speed #y # 返回值
Mask_Smooth = Calculator_bezier(0.42, 0, 0.58, 1, 60)
print(Mask_Smooth)

import numpy as np 
import matplotlib.pyplot as plt 
from math import factorial

def Calculator_bezier(control_point1x,control_point1y,control_point2x,control_point2y,Tick):
    def comb(n, k):
        return factorial(n) // (factorial(k) * factorial(n-k))

    def get_bezier_curve(points):
        n = len(points) - 1
        return lambda t: sum(comb(n, i)*t**i * (1-t)**(n-i)*points[i] for i in range(n+1))

    def evaluate_bezier(points, total):
        bezier = get_bezier_curve(points)
        new_points = np.array([bezier(t) for t in np.linspace(0, 1, total)])
        return new_points[:, 0], new_points[:, 1]

    points = np.array([[0, 0], [control_point1x, control_point1y], [control_point2x, control_point2y]])
    x, y = points[:, 0], points[:, 1]
    print(x)
    print(y)
    bx, by = evaluate_bezier(points, Tick)
    speed = []
    
    temp=0
    plt.plot(bx, by, 'b-')
    plt.plot(x, y, 'r.')
    plt.show()
    
    for i in bx,by:
        for j in range(len(i)):
            if temp == 0:
                speed.append(i[j])
            else:
                speed.append(speed[j]/i[j])
        temp += 1
    
    
    
    return bx,by


Mask_Smooth = Calculator_bezier(0.6, 0.65, 0.35, 0.94, 60)
print(Mask_Smooth)

'''

'''
def Calculator_bezier(control_point1x,control_point1y,control_point2x,control_point2y,Tick):
    # find the a & b points
    def get_bezier_coef(points):
        # since the formulas work given that we have n+1 points
        # then n must be this:
        n = len(points) - 1

        # build coefficents matrix
        C = 4 * np.identity(n)
        np.fill_diagonal(C[1:], 1)
        np.fill_diagonal(C[:, 1:], 1)
        C[0, 0] = 2
        C[n - 1, n - 1] = 7
        C[n - 1, n - 2] = 2

        # build points vector
        P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
        P[0] = points[0] + 2 * points[1]
        P[n - 1] = 8 * points[n - 1] + points[n]

        # solve system, find a & b
        A = np.linalg.solve(C, P)
        B = [0] * n
        for i in range(n - 1):
            B[i] = 2 * points[i + 1] - A[i + 1]
        B[n - 1] = (A[n - 1] + points[n]) / 2

        return A, B

    # returns the general Bezier cubic formula given 4 control points
    def get_cubic(a, b, c, d):
        return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

    # return one cubic curve for each consecutive points
    def get_bezier_cubic(points):
        A, B = get_bezier_coef(points)
        return [
            get_cubic(points[i], A[i], B[i], points[i + 1])
            for i in range(len(points) - 1)
        ]

    # evalute each cubic curve on the range [0, 1] sliced in n points
    def evaluate_bezier(points, n):
        curves = get_bezier_cubic(points)
        return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])

    #
    # generate 5 (or any number that you want) random points that we want to fit (or set them youreself)
    points = np.array([[0, 0], [control_point1x, control_point1y], [control_point2x, control_point2y]])

    # fit the points with Bezier interpolation
    # use 50 points between each consecutive points to draw the curve
    path = evaluate_bezier(points, Tick)

    # extract x & y coordinates of points
    x, y = points[:,0], points[:,1]
    px, py = path[:,0], path[:,1]

    # plot
    plt.figure(figsize=(11, 8))
    plt.plot(px, py, 'b-')
    plt.plot(x, y, 'ro')
    plt.show()
    return px,py
Mask_Smooth = Calculator_bezier(0.42, 0, 0.58, 1, 60)
print(Mask_Smooth)
'''
'''
def tri_bezier(p1,p2,p3,p4,t):
    parm_1 = (1-t)**3
    parm_2 = 3*(1-t)**2 * t
    parm_3 = 3 * t**2 * (1-t)
    parm_4 = t**3
 
    px = p1[0] * parm_1 + p2[0] * parm_2 + p3[0] * parm_3 + p4[0] * parm_4
    py = p1[1] * parm_1 + p2[1] * parm_2 + p3[1] * parm_3 + p4[1] * parm_4
    
    return (px,py)

print(tri_bezier(0.42, 0, 0.58, 1, 60 )) 
'''
import matplotlib.pyplot as plt


def bezier_curve(p0, p1, p2, p3, inserted):
    """
    三阶贝塞尔曲线
    p0, p1, p2, p3 - 点坐标，tuple、list或numpy.ndarray类型
    inserted  - p0和p3之间插值的数量
    """
    assert isinstance(p0, (tuple, list, np.ndarray))
    assert isinstance(p0, (tuple, list, np.ndarray))
    assert isinstance(p0, (tuple, list, np.ndarray))
    assert isinstance(p0, (tuple, list, np.ndarray))

    if isinstance(p0, (tuple, list)):
        p0 = np.array(p0)
    if isinstance(p1, (tuple, list)):
        p1 = np.array(p1)
    if isinstance(p2, (tuple, list)):
        p2 = np.array(p2)
    if isinstance(p3, (tuple, list)):
        p3 = np.array(p3)

    points = list()
    for t in np.linspace(0, 1, inserted + 2):
        points.append(p0 * np.power((1 - t), 3) + 3 * p1 * t * np.power((1 - t), 2) + 3 * p2 * (1 - t) * np.power(t,
                                                                                                                  2) + p3 * np.power(
            t, 3))

    return np.vstack(points)


def smoothing_base_bezier(date_x, date_y, k=0.5, inserted=10, closed=False):
    """
     基于三阶贝塞尔曲线的数据平滑算法
    date_x  - x维度数据集，list或numpy.ndarray类型
     date_y  - y维度数据集，list或numpy.ndarray类型
     k   - 调整平滑曲线形状的因子，取值一般在0.2~0.6之间。默认值为0.5
     inserted - 两个原始数据点之间插值的数量。默认值为10
     closed  - 曲线是否封闭，如是，则首尾相连。默认曲线不封闭
     """

    assert isinstance(date_x, (list, np.ndarray))
    assert isinstance(date_y, (list, np.ndarray))

    if isinstance(date_x, list) and isinstance(date_y, list):
        assert len(date_x) == len(date_y), u'x数据集和y数据集长度不匹配'
        date_x = np.array(date_x)
        date_y = np.array(date_y)
    elif isinstance(date_x, np.ndarray) and isinstance(date_y, np.ndarray):
        assert date_x.shape == date_y.shape, u'x数据集和y数据集长度不匹配'
    else:
        raise Exception(u'x数据集或y数据集类型错误')

    # 第1步：生成原始数据折线中点集
    mid_points = list()
    for i in range(1, date_x.shape[0]):
        mid_points.append({
            'start': (date_x[i - 1], date_y[i - 1]),
            'end': (date_x[i], date_y[i]),
            'mid': ((date_x[i] + date_x[i - 1]) / 2.0, (date_y[i] + date_y[i - 1]) / 2.0)
        })

    if closed:
        mid_points.append({
            'start': (date_x[-1], date_y[-1]),
            'end': (date_x[0], date_y[0]),
            'mid': ((date_x[0] + date_x[-1]) / 2.0, (date_y[0] + date_y[-1]) / 2.0)
        })

    # 第2步：找出中点连线及其分割点
    split_points = list()
    for i in range(len(mid_points)):
        if i < (len(mid_points) - 1):
            j = i + 1
        elif closed:
            j = 0
        else:
            continue

        x00, y00 = mid_points[i]['start']
        x01, y01 = mid_points[i]['end']
        x10, y10 = mid_points[j]['start']
        x11, y11 = mid_points[j]['end']
        d0 = np.sqrt(np.power((x00 - x01), 2) + np.power((y00 - y01), 2))
        d1 = np.sqrt(np.power((x10 - x11), 2) + np.power((y10 - y11), 2))
        k_split = 1.0 * d0 / (d0 + d1)

        mx0, my0 = mid_points[i]['mid']
        mx1, my1 = mid_points[j]['mid']

        split_points.append({
            'start': (mx0, my0),
            'end': (mx1, my1),
            'split': (mx0 + (mx1 - mx0) * k_split, my0 + (my1 - my0) * k_split)
        })

    # 第3步：平移中点连线，调整端点，生成控制点
    crt_points = list()
    for i in range(len(split_points)):
        vx, vy = mid_points[i]['end']  # 当前顶点的坐标
        dx = vx - split_points[i]['split'][0]  # 平移线段x偏移量
        dy = vy - split_points[i]['split'][1]  # 平移线段y偏移量

        sx, sy = split_points[i]['start'][0] + dx, split_points[i]['start'][1] + dy  # 平移后线段起点坐标
        ex, ey = split_points[i]['end'][0] + dx, split_points[i]['end'][1] + dy  # 平移后线段终点坐标

        cp0 = sx + (vx - sx) * k, sy + (vy - sy) * k  # 控制点坐标
        cp1 = ex + (vx - ex) * k, ey + (vy - ey) * k  # 控制点坐标

        if crt_points:
            crt_points[-1].insert(2, cp0)
        else:
            crt_points.append([mid_points[0]['start'], cp0, mid_points[0]['end']])

        if closed:
            if i < (len(mid_points) - 1):
                crt_points.append([mid_points[i + 1]['start'], cp1, mid_points[i + 1]['end']])
            else:
                crt_points[0].insert(1, cp1)
        else:
            if i < (len(mid_points) - 2):
                crt_points.append([mid_points[i + 1]['start'], cp1, mid_points[i + 1]['end']])
            else:
                crt_points.append([mid_points[i + 1]['start'], cp1, mid_points[i + 1]['end'], mid_points[i + 1]['end']])
                crt_points[0].insert(1, mid_points[0]['start'])

    # 第4步：应用贝塞尔曲线方程插值
    out = list()
    for item in crt_points:
        group = bezier_curve(item[0], item[1], item[2], item[3], inserted)
        out.append(group[:-1])

    out.append(group[-1:])
    out = np.vstack(out)

    return out.T[0], out.T[1]

if __name__ == '__main__':
    x = np.array([42, 59])
    y = np.array([0, 100])

    plt.plot(x, y, 'ro')
    x_curve, y_curve = smoothing_base_bezier(x, y, k=0.5, closed=True)
    plt.plot(x_curve, y_curve, label='$k=0.5$')
    plt.show()