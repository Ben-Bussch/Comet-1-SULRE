#n_bolts = 5 #number of bolts
#bolt_size = 4 #size of bolt, metric (ex M4)
#bolt_grade = 12.9 #bolt grade
#MEOP = 60e5 #max operating pressure, Pa
from math import pi
from math import log
import numpy as np
import matplotlib.pyplot as plt

"""
In reference to: https://static1.squarespace.com/static/60d8d9b060e90a67c5c69db4/t/62997fbfa1150834ce0a9556/1654226881895/How+to+Design+Pressure+Vessels%2C+Propellant+Tanks%2C+and+Rocket+Motor+Casings.pdf
"""

def bulkhead_force(dcasing,MEOP):
    pf = ((0.25*pi)*(dcasing**2)*MEOP)
    #print(pf)
    return pf

def structural_force(amax, mass):
    fmax = mass*amax
    return fmax


def bolt_force(Ft,n):
    """Calculates the total force on each bolt"""
    Fb = Ft/n 
    return Fb

def bolt_area_tot(bminor, n):
    a = (n*(pi*0.25))*(bminor**2)
    return a

def bolt_shear(Ft, tba):
    Qb = Ft / tba
    return(Qb)

def bolt_tearout(Fb, bmajor,t, E1, E2):
    Emin1 = E1 - (bmajor/2)
    Emin2 = E2 - (bmajor/2)
    Qto = Fb/(((Emin1+Emin2)/2)*(2*t))
    return(Qto)

def tensile_stress(Ft, ocasing,n,bmajor,t, lvl2): 
    if not lvl2:
        Qt = Ft/((((ocasing-t)*pi)-(n*bmajor))*t)
    if lvl2:
        Qt = Ft/((((ocasing-t)*pi)-(n/2*bmajor))*t)
    return(Qt)

def uniaxial_stress_concentration(Qt, bmajor):
    Qmax = 3*Qt
    #from stress-intensity factor: https://www.fracturemechanics.org/hole.html
    return Qmax


def bearing_stress(Fb,bmajor,t):
    Qbear = Fb/(bmajor*t)
    return(Qbear)

def bolt_grade_calc(grade):
    per = grade %1
    TS = (grade-per)*100
    YTSb = TS*per
    YTSb = np.round(YTSb,6)
    return YTSb

def bolt_minor(bolt_size):
    per = (0.0392*log(bolt_size))+0.756
    #minord = majord*per
    "List of minor diameteres, index is major diameter in mm"
    minor_list = [0,0.729,1.567, 2.459, 3.242, 4.134,4.917,5.917,6.647,7.647,8.376,9.376,10.106]
    minord = minor_list[int(bolt_size)]
    return(minord)


def bolt_calculator(n,bolt_size, Second_level, grade, MEOP, dcasing, ocasing,E_dist,E_dist_2, Material):
    """ENSURE NO OVERLAP BETWEEN FIRST AND SECOND LEVEL OF BOLTS"""
    if not Second_level:
        E_dist_2 = E_dist
    
    if Material == "Alu":
        """Aluminium 6061-T6 properties"""
        TYS = 310 #Ultimate Tensile strength the casing in Mpa in this case as we're struggleing :,(
        BYS = 386 #Bearing Yield strength of the casing in Mpa
        ST =  207 #Shear strenght of the casing in MPa
    if Material == "Comp":
        TYS = (2)**(1/2)/2*240
        BYS = 70
        ST = 25
    
    "Converting to SI units"
    MEOP = MEOP*1E5
    TYS  = TYS *1E6
    BYS = BYS *1E6
    ST = ST* 1E6
    dcasing = dcasing*1E-3
    ocasing =ocasing*1E-3
    E_dist = E_dist*1E-3
    E_dist_2 = E_dist_2*1E-3
    
    t = ((ocasing-dcasing)/2) #thickness of casing in m
    bmajor = bolt_size*1E-3 #bolt major diameter, m
    bminor = bolt_minor(bolt_size)*1E-3 #bolt mainor diameter, m
    
    UTSb = bolt_grade_calc(grade)*1E6 #Ultimate tensile strength of bolts
    STb= 0.75*UTSb
    
    
    "Calculating Total force on Bulkhead"
    Ft = bulkhead_force(dcasing,MEOP)
    #print(Ft)
    "Calculating the force ber bolt"
    Fb = bolt_force(Ft,n)
    #print("Force per bolt: ", Fb," N")
    
    "Calculating total bolt area (tba)"
    tba = bolt_area_tot(bminor, n)
    
    
    
    "Calculating shear stress on bolts"
    Qb_shear = bolt_shear(Ft, tba)
    #print("Shear stress in bolts:", Qb_shear, "Pa")
    SF_shear = STb/Qb_shear
    #print("Shear Safety Factor: ", SF_shear)
    
    
    
    "Calculating bolt-tearout stress"
    Qc_shear = bolt_tearout(Fb, bmajor,t, E_dist, E_dist_2)
    #print("bolt-tearout stress: ", Qc_shear, "Pa")
    SF_tearout = ST/Qc_shear
    #print("Tearout Safety Factor: ", SF_tearout)
    "Safety Factors: "
    
    
    "Calculating Casing Tensile Stress: "
    Qc_tensile = tensile_stress(Ft, ocasing,n,bmajor,t, Second_level)
    Qc_tensile = uniaxial_stress_concentration(Qc_tensile, bmajor) #adds stress concentration from hole shape
    #print("Casing Tensile stress: ", Qc_tensile  , "Pa")
    SF_tensile = TYS/Qc_tensile 
    #print("Tensile stress Safety Factor: ", SF_tensile)
    
    
    "Calculating compressive (Bearing) Stress:"

    Qc_compressive = bearing_stress(Fb, bmajor, t)
    #print("Compressive (Bearing) Stress: ", Qc_compressive, "Pa")
    SF_compressive = BYS/Qc_compressive
    #print("Compressive (Bearing) Stress Safety Factor: ", SF_compressive)
    return(SF_shear, SF_tearout, SF_tensile, SF_compressive)
    
"A 2-level study of number of bolts"  
n_min = 2
n_max = 40
n_list = np.linspace(n_min, n_max, 20)
print(n_list)

bolt_size_min = 1
bolt_size_max = 12
bolt_list = np.linspace(bolt_size_min, bolt_size_max, 12)
print(bolt_list)


Second_level = True #true or false for second level

grade = 12.9 #Bolt Grade
MEOP =  48 #the maximum expected operating pressure in bar
ocasing = 127 #outer casing diameter in mm
dcasing = ocasing-2*3.175 #inner casing diameter in mm
E_dist = 9 #Distance between center of bolt and edge of tank in mm
E_dist_2 = 18 #Distance for second level between center of bolt and edge of tank in mm

Material = "Alu"

SFs = np.empty(shape=(len(n_list),len(bolt_list)))
#print(SFs)


SF_bolt = []
SF_n = []

SF_max = 0
for  count, n  in enumerate(n_list):
    for count2, bolt_size in enumerate(bolt_list):
        SF_list = bolt_calculator(n,bolt_size, Second_level, grade, MEOP, dcasing, ocasing,E_dist,E_dist_2, Material)
        SF_min = min(SF_list)
        SFs[count, count2] = SF_min
        if SF_min > SF_max:
            SF_max = SF_min
            bolt_size_opt = bolt_size
            n_opt = n
        if SF_min > 2:
            print("Configuration: ", n, " Number of M",bolt_size," Bolts, SF: ",SF_min)


#print(SFs)
print("Optimal Configuration: ", n_opt, " Number of M",bolt_size_opt," Bolts, SF: ",SF_max )
    

x, z = np.meshgrid(bolt_list,n_list)      

info_str = "Material: "+Material+" OD (mm): "+str(ocasing)+" ID (mm)"+str(dcasing)+" P Max (bar): "+str(MEOP)

plt.figure(figsize=(5,5),dpi=300)
plt.contourf(x,z,SFs) 
plt.title("Bolt Safety-factor Analysis")
plt.xlabel('Bolt Size (major diameter)')
plt.ylabel('Number of Bolts')
plt.colorbar(label="Safety Factor")

#print(x)
#print(SF_n)
#3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection = "3d")
ax.set_xlabel('Bolt Size (major diameter)')
ax.set_ylabel('Number of Bolts')
ax.set_zlabel('Lowest Safety Factor')
ax.plot_surface(x,z,SFs)
plt.show()
    
