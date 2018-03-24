
# coding: utf-8

# In[21]:


# 任意选一个你喜欢的整数，这能帮你得到稳定的结果
seed = 6 # todo


# # 欢迎来到线性回归项目
# 
# 若项目中的题目有困难没完成也没关系，我们鼓励你带着问题提交项目，评审人会给予你诸多帮助。
# 
# 所有选做题都可以不做，不影响项目通过。如果你做了，那么项目评审会帮你批改，也会因为选做部分做错而判定为不通过。
# 
# 其中非代码题可以提交手写后扫描的 pdf 文件，或使用 Latex 在文档中直接回答。

# # 1 矩阵运算
# 
# ## 1.1 创建一个 4*4 的单位矩阵

# In[22]:


# 这个项目设计来帮你熟悉 python list 和线性代数
# 你不能调用任何NumPy以及相关的科学计算库来完成作业


# 本项目要求矩阵统一使用二维列表表示，如下：
A = [[1,2,3], 
     [2,3,3], 
     [1,2,5]]

B = [[1,2,3,5], 
     [2,3,3,5], 
     [1,2,5,1]]

# 向量也用二维列表表示
C = [[1],
     [2],
     [3]]

#TODO 创建一个 4*4 单位矩阵
def create_matrix(r, c):
    return [[0 for y in range(c)] for x in range(r)]
I = create_matrix(4, 4)
for i in range(len(I)):
    I[i][i] = 1
print I


# ## 1.2 返回矩阵的行数和列数

# In[23]:


# TODO 返回矩阵的行数和列数
def shape(M):
    if (not M) or (len(M)<1):
        return 0, 0
    return len(M), len(M[0])


# In[24]:


# 运行以下代码测试你的 shape 函数
get_ipython().magic(u'run -i -e test.py LinearRegressionTestCase.test_shape')


# ## 1.3 每个元素四舍五入到特定小数数位

# In[25]:


# TODO 每个元素四舍五入到特定小数数位
# 直接修改参数矩阵，无返回值
from decimal import *
def matxRound(M, decPts=4):
    for row in range(len(M)):
        for col in range(len(M[row])):
            M[row][col] = round(M[row][col], decPts)


# In[26]:


# 运行以下代码测试你的 matxRound 函数
get_ipython().magic(u'run -i -e test.py LinearRegressionTestCase.test_matxRound')


# ## 1.4 计算矩阵的转置

# In[27]:


# TODO 计算矩阵的转置
def transpose(M):
    # 利用zip对每个list成员拼装成新的list
    return [list(col) for col in zip(*M)]
#     rows, cols = shape(M)
#     tmax = create_matrix(cols, rows)
#     for r in range(rows):
#         for c in range(cols):
#             tmax[c][r] = M[r][c]
#     return tmax


# In[28]:


# 运行以下代码测试你的 transpose 函数
get_ipython().magic(u'run -i -e test.py LinearRegressionTestCase.test_transpose')


# ## 1.5 计算矩阵乘法 AB

# In[29]:


# TODO 计算矩阵乘法 AB，如果无法相乘则raise ValueError
def matxMultiply(A, B):
    ra, ca = shape(A)
    rb, cb = shape(B)
    if ca != rb:
        raise ValueError("a.col=%d != %d=b.row" % (ca, rb))
    TB = transpose(B)
    rc, cc = ra, cb
    C = create_matrix(rc, cc)
    for r in range(rc):
        for c in range(cc):
            C[r][c] = sum( [ x*y for x,y in zip(A[r], TB[c]) ] )
            # print(r, c, C[r][c])
    return C


# In[30]:


# 运行以下代码测试你的 matxMultiply 函数
get_ipython().magic(u'run -i -e test.py LinearRegressionTestCase.test_matxMultiply')


# ---
# 
# # 2 Gaussign Jordan 消元法
# 
# ## 2.1 构造增广矩阵
# 
# $ A = \begin{bmatrix}
#     a_{11}    & a_{12} & ... & a_{1n}\\
#     a_{21}    & a_{22} & ... & a_{2n}\\
#     a_{31}    & a_{22} & ... & a_{3n}\\
#     ...    & ... & ... & ...\\
#     a_{n1}    & a_{n2} & ... & a_{nn}\\
# \end{bmatrix} , b = \begin{bmatrix}
#     b_{1}  \\
#     b_{2}  \\
#     b_{3}  \\
#     ...    \\
#     b_{n}  \\
# \end{bmatrix}$
# 
# 返回 $ Ab = \begin{bmatrix}
#     a_{11}    & a_{12} & ... & a_{1n} & b_{1}\\
#     a_{21}    & a_{22} & ... & a_{2n} & b_{2}\\
#     a_{31}    & a_{22} & ... & a_{3n} & b_{3}\\
#     ...    & ... & ... & ...& ...\\
#     a_{n1}    & a_{n2} & ... & a_{nn} & b_{n} \end{bmatrix}$

# In[31]:


# TODO 构造增广矩阵，假设A，b行数相同
def augmentMatrix(A, b):
    # print('left:',A, ",right:", b)
    ra, ca = shape(A)
    B = create_matrix(ra, ca+1)
    for r in range(ra):
        for c in range(ca):
            B[r][c] = A[r][c]
        B[r][ca] = b[r][0]
    # print("res:", B)
    return B


# In[32]:


# 运行以下代码测试你的 augmentMatrix 函数
get_ipython().magic(u'run -i -e test.py LinearRegressionTestCase.test_augmentMatrix')


# ## 2.2 初等行变换
# - 交换两行
# - 把某行乘以一个非零常数
# - 把某行加上另一行的若干倍：

# In[33]:


# TODO r1 <---> r2
# 直接修改参数矩阵，无返回值
def swapRows(M, r1, r2):
    # 直接交换引用
    M[r1],M[r2] = M[r2],M[r1]
#     for i in range(len(M[r1])):
#         M[r1][i], M[r2][i] = M[r2][i], M[r1][i]


# In[34]:


# 运行以下代码测试你的 swapRows 函数
get_ipython().magic(u'run -i -e test.py LinearRegressionTestCase.test_swapRows')


# In[35]:


# TODO r1 <--- r1 * scale
# scale为0是非法输入，要求 raise ValueError
# 直接修改参数矩阵，无返回值
def scaleRow(M, r, scale):
    if scale == 0:
        raise ValueError("scale==0")
    for i in range(len(M[r])):
        M[r][i] = scale * M[r][i]    


# In[36]:


# 运行以下代码测试你的 scaleRow 函数
get_ipython().magic(u'run -i -e test.py LinearRegressionTestCase.test_scaleRow')


# In[37]:


# TODO r1 <--- r1 + r2*scale
# 直接修改参数矩阵，无返回值
def addScaledRow(M, r1, r2, scale):
    if scale == 0:
        raise ValueError("scale==0")
    for i in range(len(M[r1])):
        M[r1][i] = scale * M[r2][i] + M[r1][i]


# In[38]:


# 运行以下代码测试你的 addScaledRow 函数
get_ipython().magic(u'run -i -e test.py LinearRegressionTestCase.test_addScaledRow')


# ## 2.3  Gaussian Jordan 消元法求解 Ax = b

# ### 2.3.1 算法
# 
# 步骤1 检查A，b是否行数相同
# 
# 步骤2 构造增广矩阵Ab
# 
# 步骤3 逐列转换Ab为化简行阶梯形矩阵 [中文维基链接](https://zh.wikipedia.org/wiki/%E9%98%B6%E6%A2%AF%E5%BD%A2%E7%9F%A9%E9%98%B5#.E5.8C.96.E7.AE.80.E5.90.8E.E7.9A.84-.7Bzh-hans:.E8.A1.8C.3B_zh-hant:.E5.88.97.3B.7D-.E9.98.B6.E6.A2.AF.E5.BD.A2.E7.9F.A9.E9.98.B5)
#     
#     对于Ab的每一列（最后一列除外）
#         当前列为列c
#         寻找列c中 对角线以及对角线以下所有元素（行 c~N）的绝对值的最大值
#         如果绝对值最大值为0
#             那么A为奇异矩阵，返回None (你可以在选做问题2.4中证明为什么这里A一定是奇异矩阵)
#         否则
#             使用第一个行变换，将绝对值最大值所在行交换到对角线元素所在行（行c） 
#             使用第二个行变换，将列c的对角线元素缩放为1
#             多次使用第三个行变换，将列c的其他元素消为0
#             
# 步骤4 返回Ab的最后一列
# 
# **注：** 我们并没有按照常规方法先把矩阵转化为行阶梯形矩阵，再转换为化简行阶梯形矩阵，而是一步到位。如果你熟悉常规方法的话，可以思考一下两者的等价性。

# ### 2.3.2 算法推演
# 
# 为了充分了解Gaussian Jordan消元法的计算流程，请根据Gaussian Jordan消元法，分别手动推演矩阵A为***可逆矩阵***，矩阵A为***奇异矩阵***两种情况。

# #### 推演示例 
# 
# 
# $Ab = \begin{bmatrix}
#     -7 & 5 & -1 & 1\\
#     1 & -3 & -8 & 1\\
#     -10 & -2 & 9 & 1\end{bmatrix}$
# 
# $ --> $
# $\begin{bmatrix}
#     1 & \frac{1}{5} & -\frac{9}{10} & -\frac{1}{10}\\
#     0 & -\frac{16}{5} & -\frac{71}{10} & \frac{11}{10}\\
#     0 & \frac{32}{5} & -\frac{73}{10} & \frac{3}{10}\end{bmatrix}$
# 
# $ --> $
# $\begin{bmatrix}
#     1 & 0 & -\frac{43}{64} & -\frac{7}{64}\\
#     0 & 1 & -\frac{73}{64} & \frac{3}{64}\\
#     0 & 0 & -\frac{43}{4} & \frac{5}{4}\end{bmatrix}$
# 
# $ --> $
# $\begin{bmatrix}
#     1 & 0 & 0 & -\frac{3}{16}\\
#     0 & 1 & 0 & -\frac{59}{688}\\
#     0 & 0 & 1 & -\frac{5}{43}\end{bmatrix}$
#     
# 
# #### 推演有以下要求:
# 1. 展示每一列的消元结果, 比如3*3的矩阵, 需要写三步
# 2. 用分数来表示
# 3. 分数不能再约分
# 4. 我们已经给出了latex的语法,你只要把零改成你要的数字(或分数)即可
# 5. 检查你的答案, 可以用[这个](http://www.math.odu.edu/~bogacki/cgi-bin/lat.cgi?c=sys), 或者后面通过单元测试后的`gj_Solve`
# 
# _你可以用python的 [fractions](https://docs.python.org/2/library/fractions.html) 模块辅助你的约分_

# #### 以下开始你的尝试吧!

# In[39]:


# 不要修改这里！
from helper import *
A = generateMatrix(3,seed,singular=False)
b = np.ones(shape=(3,1),dtype=int) # it doesn't matter
Ab = augmentMatrix(A.tolist(),b.tolist()) # 请确保你的增广矩阵已经写好了
printInMatrixFormat(Ab,padding=3,truncating=0)


# 请按照算法的步骤3，逐步推演***可逆矩阵***的变换。
# 
# 在下面列出每一次循环体执行之后的增广矩阵。
# 
# 要求：
# 1. 做分数运算
# 2. 使用`\frac{n}{m}`来渲染分数，如下：
#  - $\frac{n}{m}$
#  - $-\frac{a}{b}$
# 
# 
# $ Ab = \begin{bmatrix}
#     0 & 0 & 0 & 0 \\
#     0 & 0 & 0 & 0 \\
#     0 & 0 & 0 & 0 \end{bmatrix}$
# 
# $ --> \begin{bmatrix}
#     0 & 0 & 0 & 0 \\
#     0 & 0 & 0 & 0 \\
#     0 & 0 & 0 & 0 \end{bmatrix}$
#     
# $ --> \begin{bmatrix}
#     0 & 0 & 0 & 0 \\
#     0 & 0 & 0 & 0 \\
#     0 & 0 & 0 & 0 \end{bmatrix}$
#     
# $...$

# $ Ab = \begin{bmatrix}
#   1 &  3 &  5 &  1 \\
#  -9 &  2 &  4 &  1 \\
#  -6 & -9 & -2 &  1 \end{bmatrix}$
# 
# $ --> \begin{bmatrix}
# 1   &    -2/9  &  -4/9   & -1/9 \\
# 0   &    -31/3 &  -14/3  & 1/3  \\
# 0   &    29/9  &  49/9   & 10/9  \end{bmatrix}$
# 
# $ --> \begin{bmatrix}
# 1   &    0     &  -32/93 & -11/93 \\
# 0   &    1     &  14/31  & -1/31  \\
# 0   &    0     &  371/93 & 113/93  \end{bmatrix}$
# 
# $ --> \begin{bmatrix}
# 1   &    0     &  0      & -5/371 \\
# 0   &    1     &  0      & -9/53  \\
# 0   &    0     &  1      & 113/371  \end{bmatrix}$
# 
# 

# ### 2.3.3 实现 Gaussian Jordan 消元法

# In[40]:


# TODO 实现 Gaussain Jordan 方法求解 Ax = b

""" Gaussian Jordan 方法求解 Ax = b.
    参数
        A: 方阵 
        b: 列向量
        decPts: 四舍五入位数，默认为4
        epsilon: 判读是否为0的阈值，默认 1.0e-16
        
    返回列向量 x 使得 Ax = b 
    返回None，如果 A，b 高度不同
    返回None，如果 A 为奇异矩阵
"""
from fractions import Fraction
# bShow = True将展示消元步骤。（分数形式）
def printMatix(M, bShow=False):
    if not bShow:
        return
    r,c = shape(M)
    print("[")
    for i in range(r):
        row = "" #"["
        for j in range(c):
            # row += ("{},".format(M[i][j]))
            row += ("{}\t".format(M[i][j]))
        print(row)
    print("]")


def matrixSort(M, beg=0):
    rm, cm = shape(M)
    for c in range(beg, cm):
        cmax, rnum = -1, 0
        for r in range(c, rm):
            if abs(M[r][c]) > cmax:
                cmax = abs(M[r][c])
                rnum = r
        if cmax > 0:
            swapRows(M, c, rnum)
            printMatix(M)


# 用于打印推导步骤(分数形式)
def gj_Solve_demo_show(A, b, decPts=4, epsilon = 1.0e-16):
    ra, ca = shape(A)
    rb, cb = shape(b)
    if ra != rb:
        raise ValueError("row not equal")
    AT = transpose(A)
    for row in AT:
        cmax = max([abs(x) for x in row])
        if abs(cmax) < epsilon: # 奇异矩阵
            # print("singular.cmax:", cmax, ",row:", row)
            return None
    Ab = augmentMatrix(A, b)

    # 使用第一个行变换，将绝对值最大值所在行交换到对角线元素所在行（行c）
    matrixSort(Ab)

    for c in range(ca):
        # 使用第二个行变换，将列c的对角线元素缩放为1
        if abs(Ab[c][c]) == 0:
            matrixSort(Ab, c)
        if abs(Ab[c][c]) == 0:
            return None
        scaleRow(Ab, c, Fraction(1, Ab[c][c]))
        # 多次使用第三个行变换，将列c的其他元素消为0
        for i in range(ra):
            if i != c and abs(Ab[i][c])!=0:
                addScaledRow(Ab, i, c, -1 * Ab[i][c])
        printMatix(Ab)
    matxRound(Ab)
    # printMatix(Ab)
    return [[x] for x in transpose(Ab)[-1]]


def gj_Solve(A, b, decPts=4, epsilon = 1.0e-16):
    ra, ca = shape(A)
    rb, cb = shape(b)
    if ra != rb:
        raise ValueError("row not equal")
    Ab = augmentMatrix(A, b)
    for c in range(0, ca):
        # 倒置矩阵，使用内建方法操作
        # 寻找列c中 对角线以及对角线以下所有元素（行 c~N）的绝对值的最大值
        AbT = transpose(Ab)
        maxVal = max(AbT[c][c:], key=abs)
        if abs(maxVal) < epsilon:
            return None
        # 使用第一个行变换，将绝对值最大值所在行交换到对角线元素所在行（行c）
        maxIdx = AbT[c][c:].index(maxVal) + c
        swapRows(Ab, c, maxIdx)
        # 使用第二个行变换，将列c的对角线元素缩放为1
        scaleRow(Ab, c, 1.0/(Ab[c][c]))
        # 多次使用第三个行变换，将列c的其他元素消为0
        for i in range(0, ra):
            if i != c and abs(Ab[i][c])!=0:
                addScaledRow(Ab, i, c, -1 * Ab[i][c])

    matxRound(Ab)
    return [[x] for x in transpose(Ab)[-1]]


# In[41]:


# 运行以下代码测试你的 gj_Solve 函数
get_ipython().magic(u'run -i -e test.py LinearRegressionTestCase.test_gj_Solve')


# ## (选做) 2.4 算法正确判断了奇异矩阵：
# 
# 在算法的步骤3 中，如果发现某一列对角线和对角线以下所有元素都为0，那么则断定这个矩阵为奇异矩阵。
# 
# 我们用正式的语言描述这个命题，并证明为真。
# 
# 证明下面的命题：
# 
# **如果方阵 A 可以被分为4个部分: ** 
# 
# $ A = \begin{bmatrix}
#     I    & X \\
#     Z    & Y \\
# \end{bmatrix} , \text{其中 I 为单位矩阵，Z 为全0矩阵，Y 的第一列全0}$，
# 
# **那么A为奇异矩阵。**
# 
# 提示：从多种角度都可以完成证明
# - 考虑矩阵 Y 和 矩阵 A 的秩
# - 考虑矩阵 Y 和 矩阵 A 的行列式
# - 考虑矩阵 A 的某一列是其他列的线性组合

# TODO 证明：

# # 3  线性回归

# ## 3.1 随机生成样本点

# In[46]:


# 不要修改这里！
# 运行一次就够了！
from helper import *
from matplotlib import pyplot as plt
get_ipython().magic(u'matplotlib inline')

X,Y = generatePoints(seed,num=100)

## 可视化
plt.xlim((-5,5))
plt.xlabel('x',fontsize=18)
plt.ylabel('y',fontsize=18)
plt.scatter(X,Y,c='b')
plt.show()


# ## 3.2 拟合一条直线
# 
# ### 3.2.1 猜测一条直线

# In[45]:


#TODO 请选择最适合的直线 y = mx + b
m1 = 3.9
b1 = 7.7

# 不要修改这里！
plt.xlim((-5,5))
x_vals = plt.axes().get_xlim()
y_vals = [m1*x+b1 for x in x_vals]
plt.plot(x_vals, y_vals, '-', color='r')

plt.xlabel('x',fontsize=18)
plt.ylabel('y',fontsize=18)
plt.scatter(X,Y,c='b')

plt.show()


# ### 3.2.2 计算平均平方误差 (MSE)

# 我们要编程计算所选直线的平均平方误差(MSE), 即数据集中每个点到直线的Y方向距离的平方的平均数，表达式如下：
# $$
# MSE = \frac{1}{n}\sum_{i=1}^{n}{(y_i - mx_i - b)^2}
# $$

# In[52]:


# TODO 实现以下函数并输出所选直线的MSE

def calculateMSE(X,Y,m,b):
    if len(X)!=len(Y) or len(X)==0:
        raise ValueError
    squa_list = [ (Y[i] - m*X[i] -b)**2 for i in range(0, len(X)) ]
    return sum(squa_list)*1.0/len(squa_list)

print(calculateMSE(X,Y,m1,b1))


# ### 3.2.3 调整参数 $m, b$ 来获得最小的平方平均误差
# 
# 你可以调整3.2.1中的参数 $m1,b1$ 让蓝点均匀覆盖在红线周围，然后微调 $m1, b1$ 让MSE最小。

# ## 3.3 (选做) 找到参数 $m, b$ 使得平方平均误差最小
# 
# **这一部分需要简单的微积分知识(  $ (x^2)' = 2x $ )。因为这是一个线性代数项目，所以设为选做。**
# 
# 刚刚我们手动调节参数，尝试找到最小的平方平均误差。下面我们要精确得求解 $m, b$ 使得平方平均误差最小。
# 
# 定义目标函数 $E$ 为
# $$
# E = \frac{1}{2}\sum_{i=1}^{n}{(y_i - mx_i - b)^2}
# $$
# 
# 因为 $E = \frac{n}{2}MSE$, 所以 $E$ 取到最小值时，$MSE$ 也取到最小值。要找到 $E$ 的最小值，即要找到 $m, b$ 使得 $E$ 相对于 $m$, $E$ 相对于 $b$ 的偏导数等于0. 
# 
# 因此我们要解下面的方程组。
# 
# $$
# \begin{cases}
# \displaystyle
# \frac{\partial E}{\partial m} =0 \\
# \\
# \displaystyle
# \frac{\partial E}{\partial b} =0 \\
# \end{cases}
# $$
# 
# ### 3.3.1 计算目标函数相对于参数的导数
# 首先我们计算两个式子左边的值
# 
# 证明/计算：
# $$
# \frac{\partial E}{\partial m} = \sum_{i=1}^{n}{-x_i(y_i - mx_i - b)}
# $$
# 
# $$
# \frac{\partial E}{\partial b} = \sum_{i=1}^{n}{-(y_i - mx_i - b)}
# $$

# TODO 证明:

# ### 3.3.2 实例推演
# 
# 现在我们有了一个二元二次方程组
# 
# $$
# \begin{cases}
# \displaystyle
# \sum_{i=1}^{n}{-x_i(y_i - mx_i - b)} =0 \\
# \\
# \displaystyle
# \sum_{i=1}^{n}{-(y_i - mx_i - b)} =0 \\
# \end{cases}
# $$
# 
# 为了加强理解，我们用一个实际例子演练。
# 
# 我们要用三个点 $(1,1), (2,2), (3,2)$ 来拟合一条直线 y = m*x + b, 请写出
# 
# - 目标函数 $E$, 
# - 二元二次方程组，
# - 并求解最优参数 $m, b$

# TODO 写出目标函数，方程组和最优参数

# ### 3.3.3 将方程组写成矩阵形式
# 
# 我们的二元二次方程组可以用更简洁的矩阵形式表达，将方程组写成矩阵形式更有利于我们使用 Gaussian Jordan 消元法求解。
# 
# 请证明 
# $$
# \begin{bmatrix}
#     \frac{\partial E}{\partial m} \\
#     \frac{\partial E}{\partial b} 
# \end{bmatrix} = X^TXh - X^TY
# $$
# 
# 其中向量 $Y$, 矩阵 $X$ 和 向量 $h$ 分别为 :
# $$
# Y =  \begin{bmatrix}
#     y_1 \\
#     y_2 \\
#     ... \\
#     y_n
# \end{bmatrix}
# ,
# X =  \begin{bmatrix}
#     x_1 & 1 \\
#     x_2 & 1\\
#     ... & ...\\
#     x_n & 1 \\
# \end{bmatrix},
# h =  \begin{bmatrix}
#     m \\
#     b \\
# \end{bmatrix}
# $$

# TODO 证明:

# 至此我们知道，通过求解方程 $X^TXh = X^TY$ 来找到最优参数。这个方程十分重要，他有一个名字叫做 **Normal Equation**，也有直观的几何意义。你可以在 [子空间投影](http://open.163.com/movie/2010/11/J/U/M6V0BQC4M_M6V2AJLJU.html) 和 [投影矩阵与最小二乘](http://open.163.com/movie/2010/11/P/U/M6V0BQC4M_M6V2AOJPU.html) 看到更多关于这个方程的内容。

# ### 3.4 求解 $X^TXh = X^TY$ 
# 
# 在3.3 中，我们知道线性回归问题等价于求解 $X^TXh = X^TY$ (如果你选择不做3.3，就勇敢的相信吧，哈哈)

# In[55]:


# TODO 实现线性回归
'''
参数：X, Y 存储着一一对应的横坐标与纵坐标的两个一维数组
返回：m，b 浮点数
'''
def linearRegression(X,Y):
    X = [ [x,1] for x in X ]
    XT = transpose(X)
    A = matxMultiply(XT, X)
    Y = [ [y] for y in Y ]
    b = matxMultiply(XT, Y)
    h = gj_Solve(A, b)
    return h[0][0], h[1][0]

m2,b2 = linearRegression(X,Y)
assert isinstance(m2,float),"m is not a float"
assert isinstance(b2,float),"b is not a float"
print(m2,b2)


# 你求得的回归结果是什么？
# 请使用运行以下代码将它画出来。

# In[57]:


# 请不要修改下面的代码
x1,x2 = -5,5
y1,y2 = x1*m2+b2, x2*m2+b2

plt.xlim((-5,5))
plt.xlabel('x',fontsize=18)
plt.ylabel('y',fontsize=18)
plt.scatter(X,Y,c='b')
plt.plot((x1,x2),(y1,y2),'r')
plt.title('y = {m:.4f}x + {b:.4f}'.format(m=m2,b=b2))
plt.show()


# 你求得的回归结果对当前数据集的MSE是多少？

# In[58]:


print(calculateMSE(X,Y,m2,b2))

