import numpy as np
import matplotlib.pyplot as plt
import array as arr
import math





# Define constants
rho = 1000  # Water density (kg/m^3)
mu = 0.001  # Dynamic viscosity of water (Pa·s)
swimmer_mass = 70  # Swimmer's mass (kg)
A_hand = 0.02  # Area of hand (m^2)
A_body = 0.5  # Frontal area of swimmer's body (m^2)
C_D_hand = 1.2  # Drag coefficient for the hand
C_D_body = 1.44  # Drag coefficient for the body: .89 for butterfly, 1.1 for backstroke, 1.44 for breaststroke, .92 for freestyle/front crawl
C_L_hand = 0.8  # Lift coefficient for the hand
v_swimmer = 2.0  # Swimmer's velocity (m/s)
v_rel_hand = 5  # Relative velocity of hand to water (m/s)
angle_hand = 30  # Angle of attack for the hand (degrees)
dt = 0.01  # Time step (s)
T_cycle = 1.4  # Stroke cycle time (s)
L = 100.0 #race distance (m)
maxP = 1000.0 #maximum power by a swimmer (W)
maxv = ((2*maxP)/(rho*C_D_body*A_body))**(1/3) #maximum speed limited by maximum power#
SF1 = 1.4 #max stroke frequency
SL1 =  1.4 #max stroke length
eta0 = 0.5
sf0 = 1.2
t1 = 10
dt1 = 0.1
D = 0.0
t = 0.0
W = 0.0
v = 0.0
vavg = 0.0
alpha = 0.1
x = arr.array('f', [])
y = arr.array('f', [])
z = arr.array('f', [])

# Helper function to calculate force components
def calc_drag_force(C_D, A, v_rel):
    return 0.5 * C_D * rho * A * v_rel**2

def calc_lift_force(C_L, A, v_rel, angle):
    angle_rad = np.radians(angle)
    return 0.5 * C_L * rho * A * v_rel**2 * np.sin(angle_rad)



# Calculate drag and lift forces on the hand
F_drag_hand = calc_drag_force(C_D_hand, A_hand, v_rel_hand)
F_lift_hand = calc_lift_force(C_L_hand, A_hand, v_rel_hand, angle_hand)

# Calculate total propulsion force from the hand (assuming lift is effective forward force)
F_prop_hand =  F_drag_hand - F_lift_hand



def SF(t, t1): # (t^-1)
   return SF1 * (1 - 0.0002 * (t - t1)**2)

def SL(t, t1): # (m)
   return SL1 * (1 - 0.0003 * (t - t1)**2)

def eta(sf):
   return eta0*(1-(sf-sf0)/sf0)

'''
#Solve for work done
while(D<L):
   t = t + dt
   sf = SF(t)
   sl = SL(t)
   v_new = sf * sl #if v <= maxv else maxv
   v = alpha * v_new + (1 - alpha) * v
   vavg = vavg + v * dt
   F_d = 0.5 * rho * v**2 * C_D_body * A_body
   P = F_d * v
   Ptotal = 1 / (1 - eta(sf)) * P
   W = W + Ptotal * dt
   D = D + v * dt
   x.append(t)
   y.append(v)
   z.append(Ptotal /1000)

vavg = vavg / t

plt.plot(x, y, color = 'green', label = 'speed')
plt.plot(x, z, color = 'r', label = 'energy')
#plt.ylim(0,8)
#plt.xlim(0,100)
plt.xlabel('time')
#plt.ylabel('speed')
plt.title('time vs speed and energy')
plt.legend()
plt.show()
'''

#min W for t1
while(t1<100):
   t1 = t1 + dt1
   while(D<L):
       t = t + dt
       sf = SF(t, t1)
       sl = SL(t, t1)
       v = sf * sl
       vavg = vavg + v * dt
       F_d = 0.5 * rho * v**2 * C_D_body * A_body
       P = F_d * v
       Ptotal = 1 / (1 - eta(sf)) * P
       W = W + Ptotal * dt
       D = D + v * dt
   x.append(t1)
   y.append(W/10000)
   z.append(t)
   t = 0.0
   v = 0.0
   W = 0.0
   D = 0.0

plt.plot(x, y, color = 'r', label = 'energy')
plt.plot(x, z, color = 'g', label = 'total time')
plt.xlabel('t1')
plt.ylabel('energy used/total time')
plt.show()



# Calculate drag force on the body
F_drag_body = calc_drag_force(C_D_body, A_body, vavg)

# Calculate net force and power output
F_net = F_prop_hand - F_drag_body
P_net = F_prop_hand * vavg

# Efficiency: Useful power (propulsion) over total power expenditure
P_total = (F_prop_hand+F_drag_body) * vavg
efficiency = P_net / P_total if P_total != 0 else 0


# Results
print("Results:")
print(f"Drag force on the hand: {F_drag_hand:.2f} N")
print(f"Lift force on the hand: {F_lift_hand:.2f} N")
print(f"Propulsive force from the hand: {F_prop_hand:.2f} N")
print(f"Drag force on the body: {F_drag_body:.2f} N")
print(f"Net force: {F_net:.2f} N")
print(f"Net power output: {P_net:.2f} W")
print(f"Efficiency: {efficiency * 100:.2f}%")
print(f"Average speed: {vavg} m/s")
