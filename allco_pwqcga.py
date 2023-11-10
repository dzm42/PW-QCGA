import cirq
import numpy as np

import sympy
import matplotlib.pyplot as plt
import tensorflow_quantum as tfq
import pandas as pd

class QGA(object):
    def __init__(self, dna_size):
        self.dna_size = dna_size

    def q_circuits(self):
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
    
    def sample(self,params):
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
    
    
    def fitness(self, task_x, task_y, allocation_x, allocation_y, o0, o1, o2, o3, o4, o5, o6, o7, o8, o9):
        y0 = ((task_x[0] - allocation_x[o0])**2 + (task_y[0] - allocation_y[o0])**2)**(1/2) 
        y1 = ((task_x[1] - allocation_x[o1])**2 + (task_y[1] - allocation_y[o1])**2)**(1/2)
        y2 = ((task_x[2] - allocation_x[o2])**2 + (task_y[2] - allocation_y[o2])**2)**(1/2)
        y3 = ((task_x[3] - allocation_x[o3])**2 + (task_y[3] - allocation_y[o3])**2)**(1/2) 
        y4 = ((task_x[4] - allocation_x[o4])**2 + (task_y[4] - allocation_y[o4])**2)**(1/2) 
        y5 = ((task_x[5] - allocation_x[o5])**2 + (task_y[5] - allocation_y[o5])**2)**(1/2) 
        y6 = ((task_x[6] - allocation_x[o6])**2 + (task_y[6] - allocation_y[o6])**2)**(1/2) 
        y7 = ((task_x[7] - allocation_x[o7])**2 + (task_y[7] - allocation_y[o7])**2)**(1/2)   
        y8 = ((task_x[8] - allocation_x[o8])**2 + (task_y[8] - allocation_y[o8])**2)**(1/2) 
        y9 = ((task_x[9] - allocation_x[o9])**2 + (task_y[9] - allocation_y[o9])**2)**(1/2)
        return y0,y1,y2,y3,y4,y5,y6,y7,y8,y9 
            
                        
 
    
    def mutate(self, min_y, min_l, y, l, angle, params, mun, k, q, last_growth_rate):
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
                if np.random.rand(1) >= 0.999:
                         angle[params[i]] =0
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
                if np.random.rand(1) >= 0.999:
                         angle[params[i]] = 0
        return angle, growth_rate
                    
def location(field_x, field_y, dna_size):
    # task_x = np.trunc(np.random.rand(dna_size) * field_x).tolist()
    # task_y = np.trunc(np.random.rand(dna_size) * field_y).tolist()
    # allocation_x = np.trunc(np.random.rand(4) * field_x).tolist()
    # allocation_y = np.trunc(np.random.rand(4) * field_y).tolist()
    task_x= [25.0, 61.0, 77.0, 76.0, 56.0, 28.0, 76.0, 95.0, 35.0, 52.0]
    task_y=[94.0, 43.0, 99.0, 60.0, 90.0, 61.0, 83.0, 25.0, 32.0, 68.0]
    allocation_x =[21.0, 47.0, 68.0, 89.0]
    allocation_y =[70.0, 55.0, 52.0, 88.0]
    return task_x, task_y, allocation_x, allocation_y   


def change(l):
    if l[0] ==0 and l[1] == 0:
        order=0
    elif l[0] ==1 and l[1] == 0:
        order=1
    elif l[0] ==0 and l[1] == 1:
        order=2
    elif l[0] ==1 and l[1] == 1:
        order=3  

    return order

rl  = []
val = []
times = []
for h in range(50):
    dna_size = 2

    angle_0 = {}
    angle_1 = {}
    angle_2 = {}
    angle_3 = {}
    angle_4 = {}
    angle_5 = {}
    angle_6 = {}
    angle_7 = {}
    angle_8 = {}
    angle_9 = {}

    a = QGA(dna_size)

    params = a.q_circuits()
    for i in range(dna_size):
        angle_0.update({params[i]:0})
    for i in range(dna_size):
        angle_1.update({params[i]:0})
    for i in range(dna_size):
        angle_2.update({params[i]:0})    
    for i in range(dna_size):
        angle_3.update({params[i]:0})   
    for i in range(dna_size):
        angle_4.update({params[i]:0})   
    for i in range(dna_size):
        angle_5.update({params[i]:0})
    for i in range(dna_size):
        angle_6.update({params[i]:0})
    for i in range(dna_size):
        angle_7.update({params[i]:0})
    for i in range(dna_size):
        angle_8.update({params[i]:0})
    for i in range(dna_size):
        angle_9.update({params[i]:0})
        
    # print(angle_0)

    min_l_0 = a.sample(angle_0)
    min_l_1 = a.sample(angle_1)
    min_l_2 = a.sample(angle_2)
    min_l_3 = a.sample(angle_3)
    min_l_4 = a.sample(angle_4)
    min_l_5 = a.sample(angle_5)
    min_l_6 = a.sample(angle_6)
    min_l_7 = a.sample(angle_7)
    min_l_8 = a.sample(angle_8)
    min_l_9 = a.sample(angle_9)



    task_x, task_y, allocation_x, allocation_y = location(1000, 100, dna_size)
    # print("task_x:",task_x)
    # print("task_y:",task_y)
    # print("allocation_x",allocation_x)
    # print("allocation_y",allocation_y)


    mo0 = change(min_l_0)
    mo1 = change(min_l_1)
    mo2 = change(min_l_2)
    mo3 = change(min_l_3)
    mo4 = change(min_l_4)
    mo5 = change(min_l_5)
    mo6 = change(min_l_6)
    mo7 = change(min_l_7)
    mo8 = change(min_l_8)
    mo9 = change(min_l_9)

    my0,my1,my2,my3,my4,my5,my6,my7,my8,my9 = a.fitness(task_x, task_y, allocation_x, allocation_y,mo0,mo1,mo2,mo3,mo4,mo5,mo6,mo7,mo8,mo9)

    min_y = my0+my1+my2+my3+my4+my5+my6+my7+my8+my9

    ph_y = [min_y]
    ph_x = [0]

    for i in range(dna_size):
        globals()["list0_" + str(i)] = [0]
    for i in range(dna_size):
        globals()["list1_" + str(i)] = [0]
    for i in range(dna_size):
        globals()["list2_" + str(i)] = [0]
    for i in range(dna_size):
        globals()["list3_" + str(i)] = [0]
    for i in range(dna_size):
        globals()["list4_" + str(i)] = [0]   

    # print(globals)
        
    p = 0
    x = 0
    mun  = 1
    k = 10
    q = 6
    growth_rate_0 = 1
    growth_rate_1 = 1
    growth_rate_2 = 1
    growth_rate_3 = 1
    growth_rate_4 = 1
    growth_rate_5 = 1
    growth_rate_6 = 1
    growth_rate_7 = 1
    growth_rate_8 = 1
    growth_rate_9 = 1


    x_times = []
    y_times = []
    for i in range(300):
        p +=1
        if p%300 == 0 :
            print(h)
            
        l_0 = a.sample(angle_0)
        l_1 = a.sample(angle_1)
        l_2 = a.sample(angle_2)
        l_3 = a.sample(angle_3)
        l_4 = a.sample(angle_4)
        l_5 = a.sample(angle_5)
        l_6 = a.sample(angle_6)
        l_7 = a.sample(angle_7)
        l_8 = a.sample(angle_8)
        l_9 = a.sample(angle_9)
        
        o0 = change(l_0)
        o1 = change(l_1)
        o2 = change(l_2)
        o3 = change(l_3)
        o4 = change(l_4)
        o5 = change(l_5)
        o6 = change(l_6)
        o7 = change(l_7)
        o8 = change(l_8)
        o9 = change(l_9)

        
        y0,y1,y2,y3,y4,y5,y6,y7,y8,y9 = a.fitness(task_x, task_y, allocation_x, allocation_y,o0,o1,o2,o3,o4,o5,o6,o7,o8,o9)
        y = y0+y1+y2+y3+y4+y5+y6+y7+y8+y9
        
        if y >= min_y:
            mun += 1
        else:
            y_times.append(mun)
            mun = 1
            x +=1
            x_times.append(x)
        # print(i,mun)
        angle_0, growth_rate_0 = a.mutate(my0, min_l_0, y0, l_0, angle_0, params, mun, k, q, growth_rate_0)
        angle_1, growth_rate_1 = a.mutate(my1, min_l_1, y1, l_1, angle_1, params, mun, k, q, growth_rate_1)
        angle_2, growth_rate_2 = a.mutate(my2, min_l_2, y2, l_2, angle_2, params, mun, k, q, growth_rate_2)
        angle_3, growth_rate_3 = a.mutate(my3, min_l_3, y3, l_3, angle_3, params, mun, k, q, growth_rate_3)
        angle_4, growth_rate_4 = a.mutate(my4, min_l_4, y4, l_4, angle_4, params, mun, k, q, growth_rate_4)
        angle_5, growth_rate_5 = a.mutate(my5, min_l_5, y5, l_5, angle_5, params, mun, k, q, growth_rate_5)
        angle_6, growth_rate_6 = a.mutate(my6, min_l_6, y6, l_6, angle_6, params, mun, k, q, growth_rate_6)
        angle_7, growth_rate_7 = a.mutate(my7, min_l_7, y7, l_7, angle_7, params, mun, k, q, growth_rate_7)
        angle_8, growth_rate_8 = a.mutate(my8, min_l_8, y8, l_8, angle_8, params, mun, k, q, growth_rate_8)
        angle_9, growth_rate_9 = a.mutate(my9, min_l_9, y9, l_9, angle_9, params, mun, k, q, growth_rate_9)

        
        
        for j in range(dna_size):
            globals()["list0_" + str(j)].append(angle_0[params[j]]/np.pi)
        for j in range(dna_size):
            globals()["list1_" + str(j)].append(angle_1[params[j]]/np.pi)
        for j in range(dna_size):
            globals()["list2_" + str(j)].append(angle_2[params[j]]/np.pi)
        for j in range(dna_size):
            globals()["list3_" + str(j)].append(angle_3[params[j]]/np.pi)
        for j in range(dna_size):
            globals()["list4_" + str(j)].append(angle_4[params[j]]/np.pi)

        if min_y > y:
            min_l_0 = l_0
            min_l_1 = l_1
            min_l_1 = l_2
            min_l_1 = l_3
            min_l_1 = l_4
            min_l_1 = l_5
            min_l_1 = l_6
            min_l_1 = l_7
            min_l_1 = l_8
            min_l_1 = l_9
            
            mo0 =o0
            mo1 =o1
            mo2 =o2
            mo4 =o4
            mo5 =o5
            mo6 =o6       
            mo7 =o7
            mo8 =o8
            mo9 =o9
            
            min_y = y

        ph_y.append(min_y)
        ph_x.append(i+1)
     
    order = [mo0,mo1,mo2,mo3,mo4,mo5,mo6,mo7,mo8,mo9] 
    lt = [0 for i in range(len(ph_y)-len(y_times))]
    y_times += lt
    val.append(ph_y)
    times.append(y_times)
    right = 0
    
    for i, classify in enumerate(order):
        if classify == 0 and (i == 0 or i == 5):
            right += 1
        if classify == 1 and (i == 8 or i == 9):
            right += 1
        if classify == 2 and (i == 1 or i == 3 or i == 7):
            right += 1
        if classify == 3 and (i == 2 or i == 4 or i == 6):
            right += 1
    r = right/10
    rl.append(r)

ls = [0 for i in range(len(val[0])-len(rl))] 
rl = rl + ls


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
              'acr':rl
              }).to_excel('/mnt/c/Users/73410/Desktop/Q.xlsx', index = False)
    
# order =[]
# order.append(mo0)
# order.append(mo1)
# order.append(mo2)
# order.append(mo3)
# order.append(mo4)
# order.append(mo5)
# order.append(mo6)
# order.append(mo7)
# order.append(mo8)
# order.append(mo9)


# location_x0 = []
# location_y0 = []
# location_x1 = []
# location_y1 = []
# location_x2 = []
# location_y2 = []
# location_x3 = []
# location_y3 = []

# for i, classify in enumerate(order):
#     if classify == 0:
#         location_x0.append(task_x[i])
#         location_y0.append(task_y[i])
        
#     if classify == 1:
#         location_x1.append(task_x[i])
#         location_y1.append(task_y[i])
        
#     if classify == 2:
#         location_x2.append(task_x[i])
#         location_y2.append(task_y[i])
        
#     if classify == 3:
#         location_x3.append(task_x[i])
#         location_y3.append(task_y[i])  
        
# plt.scatter(allocation_x[0], allocation_y[0], edgecolors = 'green', marker ='o', c = '')        
# plt.scatter(location_x0, location_y0, c = 'green',marker ='.' )
# plt.scatter(allocation_x[1], allocation_y[1], edgecolors = 'blue', marker ='o', c = '')        
# plt.scatter(location_x1, location_y1, c = 'blue',marker ='.')
# plt.scatter(allocation_x[2], allocation_y[2], edgecolors = 'red', marker ='o', c = '')        
# plt.scatter(location_x2, location_y2, c = 'red',marker ='.')
# plt.scatter(allocation_x[3], allocation_y[3], edgecolors = 'black', marker ='o', c = '')        
# plt.scatter(location_x3, location_y3, c = 'black',marker ='.')
# plt.legend()
# plt.savefig('./zmy_alloc_e1.jpg')
# plt.clf()

# plt.plot(ph_x, ph_y)
# plt.legend()
# plt.savefig('./zmy_alloc_e2.jpg')
# plt.clf()

# # plt.subplot(3,1,2)
# for i in range(dna_size):
#     plt.plot(ph_x , globals()["list0_" + str(i)], color='red')
# for i in range(dna_size):
#     plt.plot(ph_x , globals()["list1_" + str(i)],color='black')
# for i in range(dna_size):
#     plt.plot(ph_x , globals()["list2_" + str(i)],color='blue')
# for i in range(dna_size):
#     plt.plot(ph_x , globals()["list3_" + str(i)],color='green')
# for i in range(dna_size):
#     plt.plot(ph_x , globals()["list4_" + str(i)],color='pink')
# plt.legend()
# plt.savefig('./zmy_alloc_e3.jpg')
# plt.clf()
# # plt.subplot(3,1,3)

# plt.bar(x_times, y_times)
# plt.legend()
# plt.savefig('./zmy_alloc_e4.jpg')
# print(params)