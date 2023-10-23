import cirq
import numpy as np
from pandas import MultiIndex
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

def change(all_w, all_value,l):
    w_l =[]
    v_l = []
    for i,j in enumerate(l):
        if j == 1:
            w_l.append(all_w[i])
            v_l.append(all_value[i])
    return w_l, v_l

dna_size = 10

angle = {}
a = QGA(dna_size)

max_weight = 500

params = a.q_circuits()
for i in range(dna_size):
    angle.update({params[i]:0})
print(angle)
max_l = a.sample(angle)

# all_weight, all_value, my_weight = naspsack(dna_size, dna_size*max_weight/3, max_weight, max_weight)
all_weight = [307.0, 98.0, 204.0, 100.0, 405.0, 16.0, 398.0, 271.0, 467.0, 270.0]
all_value = [281.0, 341.0, 141.0, 466.0, 57.0, 403.0, 409.0, 103.0, 236.0, 164.0]
my_weight = 2500
print("weight:", all_weight)
print("value:", all_value)
max_w_l, max_v_l = change(all_weight, all_value, max_l)


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
growth_rate = 1
x_times = []
y_times = []
for i in range(300):
    p +=1
    if p%50== 0 :
        print(p)
    l = a.sample(angle)
    w_l, v_l = change(all_weight, all_value, l)
    y = a.f(w_l, v_l, my_weight)
    if y <= max_y:
        mun += 1
    else:
        y_times.append(mun)
        mun = 0
        x +=1
        x_times.append(x)
    # print(i,mun)
    angle, growth_rate = a.mutate(max_y, max_l, y, l, angle, params, mun, k, q, growth_rate)
    for j in range(dna_size):
        globals()["list_" + str(j)].append(angle[params[j]]/np.pi)
    if max_y < y:
        max_w_l = w_l
        max_v_l = v_l
        max_l = l
        max_y = y

    ph_y.append(max_y)
    ph_x.append(i+1)

print(max_l, max_y)
    # print(h[d[7]])
# plt.subplot(3,1,1)
plt.plot(ph_x, ph_y)
plt.legend()
plt.savefig('./zmy_kn1.jpg')
plt.clf()

# plt.subplot(3,1,2)
for i in range(dna_size):
    plt.plot(ph_x , globals()["list_" + str(i)])
plt.legend()
plt.savefig('./zmy_kn2.jpg')
plt.clf()
# plt.subplot(3,1,3)
plt.bar(x_times, y_times)
plt.legend()
plt.savefig('./zmy_kn3.jpg')