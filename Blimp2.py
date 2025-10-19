import math 
import numpy as np
import matplotlib.pyplot as plt

# parameters to adjust
lineness_ratio = 5.25   # lineness ratio
speed = 15  # operating speed in m/s
rho_air = 0.91  # density of air at 3km height in kg/m^3
rho_he = 0.1786   # density of helium at 3km height
drag_coefficient = 0.04  # drag coefficient
sunlight_time = 8   # hours with sunlight
base_power = 40
base_mass = 1
avionics_mass = 10
extra_power = 200
cabin_mass = 158
motor_mass = 4.8

class Blimp:
    def __init__(self, D, k, u, C_D):
        self.D = D
        self.k = k
        self.u = u
        self.C_D = C_D
    
    def get_surface_area(self):
        a = self.D/2
        b = self.D/2
        c = a * self.k
        p = 1.6075
        term1 = (a ** p) * (b ** p)
        term2 = (a ** p) * (c ** p)
        term3 = (b ** p) * (c ** p)
        surface_area = 4 * math.pi * ((term1 + term2 + term3) / 3) ** (1 / p)
        return surface_area

    def get_volume(self):
        L = self.D * self.k
        V = (4/3) * math.pi * (self.D/2)**2 * (L/2)
        return V
    
    def get_drag(self):
        return 0.5 * rho_air * self.u**2 * math.pi * (self.D/2)**2 * self.C_D

    def get_motor_power(self):
        power = self.get_drag() * self.u
        return power

    def get_total_power(self):
        return self.get_motor_power() + base_power + extra_power
        
    def get_panel_power(self):
        return self.get_total_power() * (24/sunlight_time)
    
    def get_panel_num(self):
        return math.ceil(self.get_panel_power()/430)
    
    def get_panel_mass(self):
        return self.get_panel_num() * 7.2
    
    def get_battery_power(self):
        return self.get_total_power() * (24 - sunlight_time)
    
    def get_battery_num(self):
        return math.ceil(self.get_battery_power() / 5120)
    
    def get_battery_mass(self):
        return self.get_battery_num() * 50
    
    def get_balloon_mass(self):
        return self.get_surface_area() * 0.2
    
    def get_He_mass(self):
        return rho_he * self.get_volume()
    
    def get_total_weight(self):
        M = base_mass + self.get_panel_mass() + self.get_battery_mass() + motor_mass * 2 + avionics_mass + self.get_balloon_mass() + self.get_He_mass() + cabin_mass
        return M * 9.81
    
    def get_upthrust(self):
        return rho_air * self.get_volume() * 9.81
    
myBlimp = Blimp(D = 8, k = lineness_ratio, u = speed, C_D = drag_coefficient)

print(myBlimp.get_volume())
print(myBlimp.get_total_weight())

D_list = np.linspace(7,9,num = 1000)
final_diameters = []
weights = []
upthrusts = []
for diameter in D_list:
    test_blimp = Blimp(D = diameter, k = lineness_ratio, u = speed, C_D = drag_coefficient)
    weight = test_blimp.get_total_weight()
    upthrust = test_blimp.get_upthrust()
    weights.append(weight)
    upthrusts.append(upthrust)
    if abs(weight - upthrust) < 1:
        final_diameters.append(diameter)

eq_diameter = final_diameters[0]
eq_blimp = Blimp(D = eq_diameter, k = lineness_ratio, u = speed, C_D = drag_coefficient)
eq_weight = eq_blimp.get_total_weight()
description = (f"balloon volume = {eq_blimp.get_volume():.1f} m^3\n"
                f"balloon mass = {eq_blimp.get_balloon_mass():.1f}kg \n"
                f"drag force = {eq_blimp.get_drag():.1f} N\n"
                f"total power = {eq_blimp.get_total_power():.1f} W\n"
                f"panel mass = {eq_blimp.get_panel_mass():.1f} kg\n"
                f"battery mass = {eq_blimp.get_battery_mass():.1f} kg\n")
plt.figure()  
plt.ylim(0,20000)
plt.xlim(7,9)
plt.xlabel('diameter (m)')
plt.ylabel('weight or thrust (N)')

plt.title(f"weight = upthrust = {eq_weight/1000:.3f} kN, equilibrium diameter = {eq_diameter:.3f} m")
plt.plot(D_list, weights, label='Weight', color='blue')  
plt.plot(D_list, upthrusts, label='Upthrust', color='red')  

plt.scatter(eq_diameter, eq_blimp.get_upthrust(), color = 'black', zorder = 3, label = 'Equilibrium point')
plt.vlines(x = eq_diameter, ymin = 0, ymax = eq_blimp.get_upthrust(), color = 'black', linestyle = '--')
plt.text(7.05,1000,description)
plt.legend()
plt.show()

    
