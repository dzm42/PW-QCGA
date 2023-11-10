from tkinter import Y
import cirq
import numpy as np
import pandas as pd
import sympy
import matplotlib.pyplot as plt
import tensorflow_quantum as tfq

class QGA(object):
    def __init__(self, dna_size):
        self.dna_size = dna_size
        
    def q_circuits(self):   #构建电路
        circuits = cirq.Circuit()
        qubits = cirq.GridQubit.rect(1,self.dna_size)
        control_params = []
        for i, qubit in enumerate(qubits):
            symbol = sympy.Symbol('q'+str(i))
            circuits.append(cirq.H(qubit))
            circuits.append(cirq.ry(symbol)(qubit))
            circuits.append(cirq.ry(symbol)(qubit))
            circuits.append(cirq.measure(qubit))
            control_params.append(symbol)
        # self.params = control_params
        self.circuit = circuits
        self.control_params = control_params
        return control_params
    
    def sample(self,params):   #产生数列
        # self.q_circuits()
        # h = {}
        l = []
        # for i in range(self.dna_size):
        #     h.update({self.params[i]: 0})
        resolver = cirq.ParamResolver(params)
        output = cirq.sample(program = self.circuit, param_resolver=resolver, repetitions=1).measurements
        for i in output: 
            l.append(output[i][0][0])
        self.l = l
        return  l
    
    
    def fitness(self, x, y):   #适宜度
        f = -20*np.exp(-0.2* (0.5* (x**2 + y**2 ))**0.5)-np.exp(0.5*(np.cos(2*np.pi*x)+np.cos(2*np.pi*y)))+20+np.exp(1)
        return f

    
    def mutate(self, min_y, min_l, y, l, angle, params, mun, k, q, last_growth_rate): #旋转角更新
        if y >= min_y:
            reduce_rate = np.exp(-(mun/k)**q)
            growth_rate = last_growth_rate
            for i in range(dna_size):        
                        
                if 0 >= angle[params[i]] > -np.pi/4 and min_l[i] == 0:
                    angle[params[i]] -= last_growth_rate*reduce_rate*0.0025*np.pi
                if 0 < angle[params[i]] < np.pi/4 and min_l[i] == 0:
                    angle[params[i]] -= last_growth_rate*reduce_rate*0.0025*np.pi * 2
                if 0 <= angle[params[i]] < np.pi/4 and min_l[i] == 1:
                    angle[params[i]] += last_growth_rate*reduce_rate*0.0025*np.pi
                if 0 > angle[params[i]] > -np.pi/4 and min_l[i] == 1:
                    angle[params[i]] += last_growth_rate*reduce_rate*0.0025*np.pi * 2
                # if angle[params[i]] <= -np.pi/8 and min_l[i] == 1:
                #     angle[params[i]] = 0
                # if angle[params[i]] >= np.pi/8 and min_l[i] == 0:
                #     angle[params[i]] = 0
                # if np.random.rand(1) >= 0.999:
                #          angle[params[i]] =0
            # print(reduce_rate)                 
        if y < min_y:
            growth_rate = ((min_y - y)/min_y + 1)
            for i in range(dna_size):
       
                if 0 >= angle[params[i]] > -np.pi/4 and  l[i] == 0:
                    angle[params[i]] -= growth_rate*0.0025*np.pi
                if 0 < angle[params[i]] < np.pi/4 and l[i] == 0:
                    angle[params[i]] -= growth_rate*0.0025*np.pi * 2
                if 0 <= angle[params[i]] < np.pi/4 and l[i] == 1:
                       angle[params[i]] += growth_rate*0.0025*np.pi
                if 0 > angle[params[i]] > -np.pi/4 and l[i] == 1:
                       angle[params[i]] += growth_rate*0.0025*np.pi * 2 
                # if angle[params[i]] <= -np.pi/8 and l[i] == 1:
                #     angle[params[i]] = 0
                # if angle[params[i]] >= np.pi/8 and l[i] == 0:
                #     angle[params[i]] = 0
                # if np.random.rand(1) >= 0.999:
                #          angle[params[i]] = 0

        return angle, growth_rate  

def change(dna_size, l_0, l_1, bound): #将数组转化为十进制
    x = 0
    for i,K in enumerate(l_0[::-1]):
        x += (2**i)*K
    for i,K in enumerate(l_1[::-1]):
        x += (2**(i+5))*K
        
        
    x = x/(2**(dna_size*2)-1)*(bound[1]-bound[0])-4

    return x


acc = 0
times = []
val = []
for h in range(50):
    dna_size = 5

    anglex_0 = {}
    anglex_1 = {}
    angley_0 = {}
    angley_1 = {}

    a = QGA(dna_size)

    params = a.q_circuits()
    for i in range(dna_size):
        anglex_0.update({params[i]:0})
    for i in range(dna_size):
        anglex_1.update({params[i]:0})
        
    for i in range(dna_size):
        angley_0.update({params[i]:0})
    for i in range(dna_size):
        angley_1.update({params[i]:0})   
        
        

    min_lx_0 = a.sample(anglex_0)
    min_lx_1 = a.sample(anglex_1)

    min_ly_0 = a.sample(angley_0)
    min_ly_1 = a.sample(angley_1)

    bound =[-4, 4]

    min_x= change(dna_size, min_lx_0, min_lx_1, bound)
    min_y= change(dna_size, min_ly_0, min_ly_1, bound)



    min_z = a.fitness(min_x, min_y)



    ph_z = [min_z]
    ph_mun = [0]     #适宜度数值进化过程

    for i in range(dna_size):
        globals()["list_" + str(i)] = [0]  #旋转角进化过程
        
    p = 0
    time_s = 0
    mun  = 1
    k0 = 10 
    q0 = 4
    k1 = 15 
    q1 = 4

    growth_rate_x0 = 1
    growth_rate_x1 = 1
    growth_rate_y0 = 1
    growth_rate_y1 = 1


    x_times = []
    y_times = []       #每次更新间隔次数

    x_lab = [min_x]
    y_lab = [min_y]
    z_lab = [min_z]        #进化过程图像

    for i in range(300):
        # p +=1
        # if p%50 == 0 :
        #     print(p)
        lx_0 = a.sample(anglex_0)
        lx_1 = a.sample(anglex_1)
        ly_0 = a.sample(angley_0)
        ly_1 = a.sample(angley_1)
        
        x= change(dna_size, lx_0, lx_1,bound)
        y= change(dna_size, ly_0, ly_1,bound)
        
        z = a.fitness(x, y)
        if z >= min_z:
            mun += 1
        else:
            y_times.append(mun)
            mun = 1
            time_s +=1
            x_times.append(time_s)
        # print(i,mun)
        anglex_0, growth_rate_x0 = a.mutate(min_z, min_lx_0, z, lx_0, anglex_0, params, mun, k0, q0, growth_rate_x0)
        anglex_1, growth_rate_x1 = a.mutate(min_z, min_lx_1, z, lx_1, anglex_1, params, mun, k1, q1, growth_rate_x1)
        
        angley_0, growth_rate_y0 = a.mutate(min_z, min_ly_0, z, ly_0, angley_0, params, mun, k0, q0, growth_rate_y0)
        angley_1, growth_rate_y1 = a.mutate(min_z, min_ly_1, z, ly_1, angley_1, params, mun, k1, q1, growth_rate_y1)
        
        
        
        for j in range(dna_size):
            globals()["list_" + str(j)].append(anglex_0[params[j]]/np.pi)
        if min_z > z:
            min_lx_0 = lx_0
            min_lx_1 = lx_1
            min_ly_0 = ly_0
            min_ly_1 = ly_1
            
            min_x, min_y, min_z = x, y, z
        x_lab.append(min_x)
        y_lab.append(min_y)
        z_lab.append(min_z)


        ph_z.append(min_z)
        ph_mun.append(i+1)
    lt = [0 for i in range(len(ph_z)-len(y_times))]
    y_times += lt
    val.append(ph_z)
    times.append(y_times)
    
    if min_z <= 0.1:
        acc += 1
    print(h, acc/(h+1))

# print(min_z)
pd.DataFrame({'val_0':val[0],'val_1':val[1],'val_2':val[2],'val_3':val[3],'val_4':val[4],'val_5':val[5],'val_6':val[6],'val_7':val[7],
              'val_8':val[8],'val_9':val[9],'val_10':val[10],'val_11':val[11],'val_12':val[12],'val_13':val[13],'val_14':val[14],
              'val_15':val[15],'val_16':val[16],'val_17':val[17],'val_18':val[18],'val_19':val[19],'val_0':val[20],'val_21':val[21],
              'val_22':val[22],'val_23':val[23],'val_24':val[24],'val_25':val[25],'val_26':val[26],'val_27':val[27],'val_28':val[28],
              'val_29':val[29],'val_30':val[30],'val_31':val[31],'val_32':val[32],'val_33':val[33],'val_34':val[34],'val_35':val[35],
              'val_36':val[36],'val_37':val[37],'val_38':val[38],'val_39':val[39],'val_40':val[40],'val_41':val[41],'val_42':val[42],
              'val_43':val[43],'val_44':val[44],'val_45':val[45],'val_46':val[46],'val_47':val[47],'val_48':val[48],'val_49':val[49],
              'num_0':times[0],'num_1':times[1],'num_2':times[2],'num_3':times[3],'num_4':times[4],'num_5':times[5],'num_6':times[6],
              'num_7':times[7],'num_8':times[8],'num_9':times[9],'num_10':times[10],'num_11':times[11],'num_12':times[12],'num_13':times[13],
              'num_14':times[14],'num_15':times[15],'num_16':times[16],'num_17':times[17],'num_18':times[18],'num_19':times[19],
              'num_20':times[20],'num_21':times[21],'num_22':times[22],'num_23':times[23],'num_24':times[24],'num_25':times[25],
              'num_26':times[26],'num_27':times[27],'num_28':times[28],'num_29':times[29],'num_30':times[30],'num_31':times[31],
              'num_32':times[32],'num_33':times[33],'num_34':times[34],'num_35':times[35],'num_36':times[36],'num_37':times[37],
              'num_38':times[38],'num_39':times[39],'num_40':times[40],'num_41':times[41],'num_42':times[42],'num_43':times[43],
              'num_44':times[44],'num_45':times[45],'num_46':times[46],'num_47':times[47],'num_48':times[48],'num_49':times[49],
              'acc':acc
              }).to_excel('/mnt/c/Users/73410/Desktop/Q.xlsx', index = False) 

# x0 = np.linspace(-4, 4, 200)
# y0 = np.linspace(-4, 4, 200)
# x0, y0 = np.meshgrid(x0, y0)
# z0 = -20*np.exp(-0.2* (0.5* (x0**2 + y0**2 ))**0.5)-np.exp(0.5*(np.cos(2*np.pi*x0)+np.cos(2*np.pi*y0)))+20+np.exp(1) #Ackley's Function
# fig = plt.figure()
# bx = fig.add_subplot(projection ='3d')
# ax = fig.gca(projection ='3d')

# ax.plot_surface(x0, y0, z0, cstride =1, rstride = 1,cmap ='Blues_r', alpha=0.5)
# bx.scatter(x_lab, y_lab, z_lab, c ='red',marker='x')
# # plt.scatter(x_lab, y_lab, c ='black')

# plt.legend()
# plt.savefig('./zmy_ackleye1.jpg')
# plt.clf()


# plt.plot(ph_mun, ph_z)
# plt.legend()
# plt.savefig('./zmy_ackleye2.jpg')
# plt.clf()

# # plt.subplot(3,1,2)
# for i in range(dna_size):
#     plt.plot(ph_mun , globals()["list_" + str(i)])
# plt.legend()
# plt.savefig('./zmy_ackleye3.jpg')
# plt.clf()
# # plt.subplot(3,1,3)
# # print(x_times,y_times)

# plt.bar(x_times, y_times)
# plt.legend()
# plt.savefig('./zmy_ackleye4.jpg')
