import cirq
import numpy as np
import pandas as pd
import sympy
import matplotlib.pyplot as plt
import tensorflow_quantum as tfq

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
    
    
    def f(self, w_l, value_l, my_w):
        y = 0
        w = 0
        for j in w_l:
            w += j
        if w <= my_w:
            for i in value_l:
                y += i
        self.y = y
        return y 
    
    def mutate(self, max_y, max_l, y, l, angle, params, mun, k, q, last_growth_rate):
        if y < max_y:
            reduce_rate = np.exp(-(mun/k)**q)
            growth_rate = last_growth_rate
            for i in range(dna_size):  

                        
                if 0 >= angle[params[i]] > -np.pi/4 and max_l[i] == 0:
                    angle[params[i]] -= last_growth_rate*reduce_rate*0.0025*np.pi
                if 0 < angle[params[i]] < np.pi/4 and max_l[i] == 0:
                    angle[params[i]] -= last_growth_rate*reduce_rate*0.0025*np.pi * 2
                if 0 <= angle[params[i]] < np.pi/4 and max_l[i] == 1:
                    angle[params[i]] += last_growth_rate*reduce_rate*0.0025*np.pi
                if 0 > angle[params[i]] > -np.pi/4 and max_l[i] == 1:
                    angle[params[i]] += last_growth_rate*reduce_rate*0.0025*np.pi * 2

                if np.random.rand(1) >= 0.999:
                         angle[params[i]] =0
            # print(reduce_rate)                 
        if y >= max_y:
            growth_rate = ((y - max_y)/max_y + 1)
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
                    
def naspsack(mun, my_weight, max_weight, max_value):
    all_w = np.random.rand(mun) * max_weight
    all_w =np.trunc(all_w).tolist()
    
    all_value = np.random.rand(mun) * max_value
    all_value =np.trunc(all_value).tolist()
    return all_w, all_value, my_weight     

def change(all_w, all_value,l0,l1):
    w_l =[]
    v_l = []
    for i,j in enumerate(l0):
        if j == 1:
            w_l.append(all_w[i])
            v_l.append(all_value[i])
    for i,j in enumerate(l1):
        if j == 1:
            w_l.append(all_w[i+5])
            v_l.append(all_value[i+5])
            
    return w_l, v_l

acc = 0
val =[]
times = []
for h in range(50):
    dna_size = 5

    angle0 = {}
    angle1 = {}

    a = QGA(dna_size)

    max_weight = 500

    params = a.q_circuits()
    for i in range(dna_size):
        angle0.update({params[i]:0})
        angle1.update({params[i]:0})
        
    # print(angle0)
    max_l0 = a.sample(angle0)
    max_l1 = a.sample(angle1)

    # all_weight, all_value, my_weight = naspsack(dna_size, dna_size*max_weight/3, max_weight, max_weight)
    all_weight = [307.0, 98.0, 204.0, 100.0, 405.0, 16.0, 398.0, 271.0, 467.0, 270.0]
    all_value = [281.0, 341.0, 141.0, 466.0, 57.0, 403.0, 409.0, 103.0, 236.0, 164.0]
    my_weight = 2500
    # print("weight:", all_weight)
    # print("value:", all_value)
    max_w_l, max_v_l = change(all_weight, all_value, max_l0, max_l1)

    w = 0


    max_y = a.f(max_w_l, max_v_l, my_weight)
                



    ph_y = [max_y]
    ph_x = [0]

    for i in range(dna_size):
        globals()["list_" + str(i)] = [0]

        
    p = 1
    x = 0
    mun  = 1
    k = 10
    q = 4
    growth_rate0 = 1
    growth_rate1 = 1
    x_times = []
    y_times = []
    for i in range(300):
        # p +=1
        # if p%50== 0 :
            # print(p)
        l0 = a.sample(angle0)
        l1 = a.sample(angle1)
        w_l, v_l = change(all_weight, all_value, l0, l1)
        
        y = a.f(w_l, v_l, my_weight)
        if y <= max_y:
            mun += 1
        else:
            y_times.append(mun)
            mun = 0
            x +=1
            x_times.append(x)
        # print(i,mun)
        angle0, growth_rate0 = a.mutate(max_y, max_l0, y, l0, angle0, params, mun, k, q, growth_rate0)
        angle1, growth_rate1 = a.mutate(max_y, max_l1, y, l1, angle1, params, mun, k, q, growth_rate1)
        
        
        for j in range(dna_size):
            globals()["list_" + str(j)].append(angle0[params[j]]/np.pi)
        if max_y < y:
            max_w_l = w_l
            max_v_l = v_l
            max_l0 = l0
            max_l1 = l1
            max_y = y

        ph_y.append(max_y)
        ph_x.append(i+1)
    lt = [0 for i in range(len(ph_y)-len(y_times))]
    y_times += lt
    val.append(ph_y)
    times.append(y_times)
    if max_y == 2544:
        acc += 1
    print(h,acc)
    
acc = acc/100
print(acc)

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
    # print(h[d[7]])
# plt.subplot(3,1,1)
# max_l=[]
# max_l.append(max_l0)
# max_l.append(max_l1)
# print(max_l, max_y)

# plt.plot(ph_x, ph_y)
# plt.legend()
# plt.savefig('./zmy_ekn1.jpg')
# plt.clf()

# # plt.subplot(3,1,2)
# for i in range(dna_size):
#     plt.plot(ph_x , globals()["list_" + str(i)])
# plt.legend()
# plt.savefig('./zmy_ekn2.jpg')
# plt.clf()
# # plt.subplot(3,1,3)
# plt.bar(x_times, y_times)
# plt.legend()
# plt.savefig('./zmy_ekn3.jpg')