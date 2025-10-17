"""
Calculation file for ExA Air Task Blimp Design by Oliver Jiang
"""
import math 
import numpy as np
import matplotlib.pyplot as plt

# parameters to adjust
k = 4   # lineness ratio
u = 10  # operating speed in m/s
rho_air = 0.91  # density of air at 3km height in kg/m^3
rho_he = 0.15   # density of helium at 3km height
C_D = 0.05  # drag coefficient
sunlight_time = 8   # hours with sunlight

motor_type = "PMSM" 
motor_density = {"PMSM":3000, "BLDC":2000}    # power density of motor in W/kg

panel_type = "Renogy" 
panel_density = {"Renogy": 200/4.9} # power density of panel in W/kg

base_power = 40 # given in the task description
base_mass = 1

battery_type = "LFP" 
battery_density = {"LFP": 150, "Li3": 230}  # power density of battery in Wh/kg

avionics_mass = 10   # avi-electronics devices mass in kg

balloon_type = "PET"
balloon_density = {"PET": 0.06} # area density of surface material in kg/m^2

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
def calculation(D):
    L = D * k   # length in meter
    V = 2 * math.pi * (D**3) / 3    # volumn of balloon in m^3
    drag = 0.5 * rho_air * u**2 * V**(2/3) *C_D # drag force
    thrust = drag   # thrust by motor = drag
    motor_power = thrust * u    # P = Fv
    #print(f"power provided by the motor is {motor_power:.3f} W")

    motor_mass = motor_power / motor_density[motor_type]
    
    panel_power = motor_power * (24/sunlight_time) + base_power # power produced by panel to operate
    
    panel_mass = panel_power / panel_density[panel_type]

    battery_cap = ( motor_power + base_power ) * ( 24 - sunlight_time ) # battery capacity in Wh to support operation during night time

    battery_mass = battery_cap / battery_density[battery_type]

    balloon_area = ellipsoid_area(D, k)   # balloon surface area in m^2

    balloon_mass = balloon_area * balloon_density[balloon_type]
    he_mass = rho_he * V

    total_mass = base_mass + panel_mass + battery_mass + motor_mass + avionics_mass + balloon_mass + he_mass
    total_weight = total_mass * 9.81
    upthrust = rho_air * V * 9.81
    return total_weight, upthrust, battery_cap, thrust



# visualization
D_list = np.linspace(0,8,num=800)
weights = []
upthrusts = []
final_d = 0
final_weight = 0
final_battery_cap = 0
final_thrust = 0
for D in D_list:
    total_weight, upthrust, battery_cap, thrust = calculation(D)
    weights.append(total_weight)
    upthrusts.append(upthrust)
    if abs(total_weight - upthrust) < 5:
        final_d = D
        final_weight = total_weight
        final_battery_cap = battery_cap
        final_thrust = thrust

plt.figure()  
plt.ylim(0,10000)
plt.xlim(0,8)
plt.xlabel('diameter (m)')
plt.ylabel('weight or thrust (N)')

plt.title(f"Weight = Upthrust = {final_weight:.2f} N when diameter is {final_d:.2f} m")
plt.scatter(final_d, final_weight, color = 'black', zorder = 3, label = 'Equilibrium point')
plt.plot(D_list, weights, label='Weight', color='blue')  
plt.plot(D_list, upthrusts, label='Upthrust', color='red')  

plt.vlines(x = final_d, ymin = 0, ymax = final_weight, color = 'black', linestyle = '--')
description = (f"motor type = {motor_type}\n"
               f"panel type = {panel_type}\n"
               f"battery type = {battery_type}\n"
               f"balloon type = {balloon_type}\n"
               f"battery capacity = {final_battery_cap/1000:.1f} kWh\n"
               f"thrust = {final_thrust:.1f} N")
plt.text(0.3,2000,description)
plt.legend()
plt.show()
