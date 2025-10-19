"""
Calculation file for ExA Air Task Blimp Design by Oliver Jiang
"""
import math 
import numpy as np
import matplotlib.pyplot as plt

# parameters to adjust
k = 5   # lineness ratio
u = 15  # operating speed in m/s
rho_air = 0.91  # density of air at 3km height in kg/m^3
rho_he = 0.15   # density of helium at 3km height
C_D = 0.05  # drag coefficient
sunlight_time = 8   # hours with sunlight

motor_type = "PMSM" 
motor_density = {"PMSM":3000, "BLDC":2000}    # power density of motor in W/kg

panel_type = "SM" 
panel_density = {"XR": 300/4.7, "SM": 520/7.2} # power density of panel in W/kg

base_power = 40 # given in the task description
base_mass = 1

#battery_mass = 300

avionics_mass = 1  # avi-electronics devices mass in kg

balloon_type = "TPU"
balloon_density = {"TPU": 0.2} # area density of surface material in kg/m^2


def ellipsoid_area(D,k):
    a = D/2
    b = D/2
    c = a * k
    p = 1.6075
    term1 = (a ** p) * (b ** p)
    term2 = (a ** p) * (c ** p)
    term3 = (b ** p) * (c ** p)
    surface_area = 4 * math.pi * ((term1 + term2 + term3) / 3) ** (1 / p)
    return surface_area


# calculation returns total weight and thrust
def calculation(D): # D is diameter
    L = D * k   # length in meter
    V = (4/3) * math.pi * (D/2)**2 * (L/2)    # volumn of balloon in m^3
    drag = 0.5 * rho_air * u**2 * V**(2/3) *C_D # drag force
    thrust = drag   # thrust by motor = drag
    motor_power = thrust * u    # P = Fv
   
    motor_mass = 4.8

    panel_power = motor_power * (24/sunlight_time) + base_power # power produced by panel to operate
   
    panel_mass = panel_power / panel_density[panel_type]
   
    battery_cap = (motor_power+40) * (24-sunlight_time)
    battery_num = battery_cap/5120
    battery_mass = battery_num * 50
    balloon_area = ellipsoid_area(D, k)   # balloon surface area in m^2

    balloon_mass = balloon_area * balloon_density[balloon_type]
    he_mass = rho_he * V

    cabin_mass = 158
    total_mass = base_mass + panel_mass + battery_mass + motor_mass + avionics_mass + balloon_mass + he_mass + cabin_mass
    total_weight = total_mass * 9.81
    upthrust = rho_air * V * 9.81
    return V, drag, motor_power, panel_power, panel_mass, balloon_mass, total_weight, upthrust

# visualization
D_list = np.linspace(0,10,num=5000)
weights = []
upthrusts = []
final_d = 0
final_V = 0
final_weight = 0
final_battery_cap = 0
final_motor_power = 0
final_panel_power = 0
final_ballon_mass = 0
for D in D_list:
    V, drag, motor_power, panel_power, panel_mass, balloon_mass, total_weight, upthrust = calculation(D)
    weights.append(total_weight)
    upthrusts.append(upthrust)
    if abs(total_weight - upthrust) < 5:
        final_d = D
        #final_drag = drag
        final_weight = total_weight
        final_motor_power = motor_power
        final_panel_power = panel_power
        final_ballon_mass = balloon_mass
        final_V = V


plt.figure()  
plt.ylim(0,30000)
plt.xlim(0,10)
plt.xlabel('diameter (m)')
plt.ylabel('weight or thrust (N)')

plt.title(f"Weight = Upthrust = {final_weight:.2f} N when diameter is {final_d:.2f} m")
plt.scatter(final_d, final_weight, color = 'black', zorder = 3, label = 'Equilibrium point')
plt.plot(D_list, weights, label='Weight', color='blue')  
plt.plot(D_list, upthrusts, label='Upthrust', color='red')  

plt.vlines(x = final_d, ymin = 0, ymax = final_weight, color = 'black', linestyle = '--')
description =   (f"motor power = {final_motor_power:.1f} W\n"
                 f"panel_power = {final_panel_power:.1f} W\n"
                 f"balloon mass = {final_ballon_mass:.1f} kg\n"
                 f"balloon volumn = {final_V:.1f} m^3"
                )
plt.text(0.3,9000,description)
plt.legend()
plt.show()
