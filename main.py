#vide.py
#coding:utf-8

# Librairies :-----------------------------------------------------------------------------------------------------------

from tkinter import*
from math import*
from csv import*
from time import*
from colour import*

# Set Variables :--------------------------------------------------------------------------------------------------

def zone(a,b) :

	return [(o,i) for o in range(a[0],b[0],5) for i in range(a[1],b[1],5)]

lieu_cdi 		=	[zone((280, 205), (295, 271))	,0]
lieu_ateliers 	= 	[zone((417, 309), (523, 414)) +
				 	 zone((350, 573), (428, 676)) 	,0]
lieu_cantine 	= 	[zone((288, 860), (397, 938))	,0]
lieu_perm 		= 	[zone((366, 285), (390, 320))	,0]
lieu_vie_sco 	= 	[zone((280, 282), (310, 306))	,0]
lieu_gymnase 	= 	[zone(( 12, 427), (173, 546))	,0]
lieu_recre 		= 	[zone((313, 332), (379, 484)) 	,0]
lieu_muscu 		= 	[zone((431, 575), (476, 612)) 	,0]
lieu_internat 	= 	[zone((149,   9), (232, 109))	,0]
lieu_classe 	= 	[zone((351, 523), (506, 556)) + 
				 	 zone((393, 439), (540, 471)) +
					 zone((368, 123), (388, 271)) 	,0]
lieu_labo 		= 	[zone((367,  96), (387, 111)) 	,0]
lieu_couloirs 	= 	[zone((350, 558), (503, 570)) +
					 zone((394, 415), (537, 436)) +
					 zone((313, 270), (363, 286)) 	,0]
lieu_admin 		= 	[zone((515, 887), (581, 969)) +
					 zone((516, 778), (565, 810)) 	,0]
lieu_profs 		= 	[zone((280, 140), (297, 196))	,0]

lieu_all_0 = [lieu_cdi,lieu_ateliers,lieu_cantine,lieu_perm,lieu_vie_sco,lieu_gymnase,lieu_recre,lieu_muscu,
lieu_internat,lieu_classe,lieu_labo,lieu_couloirs,lieu_admin,lieu_profs]
lieu_all = [o for i in lieu_all_0 for o in i[0]]



red = "#ff0000"
blue = "#66ccff"
green = "#66B266"

chart = list(Color("green").range_to(Color("red"),100))

root = Tk()
root.title("Cartographie Sonore BDM")

source = PhotoImage(file="plan.PNG")
source_mur = PhotoImage(file="plan_mur.png")

decibel = StringVar()


# Fonctions :-------------------------------------------------------------------------------------------

def ouverture(root) :
	"""
	Ouverture du fichier csv
	"""
	with open(root,"r",encoding="utf-8") as fichier :
		lecteur = reader(fichier,delimiter=";")
		table = []
		for i in lecteur :
			table.append(i)
		return table


def distance(x1,y1,x2,y2) :
	"""
	calcule la distance entre 2 points
	retourne la distance en METRE
	"""

	delta = sqrt(((x1-x2)**2)+(y1-y2)**2)

	delta = delta * 130 / 580
	return int(round(delta,0))

def attenuation(x1,y1,x2,y2) :

	"""
	equation affine mx+p
	"""
	global source_mur

	if x2 < x1 :
		repx , repy = x1 , y1
		x1 ,y1 = x2 , y2
		x2 , y2 = repx , repy

	if x2 - x1 == 0 :
		x1 = x1+1

	m = (y2-y1)/(x2-x1) # la pente
	p = y1 - m * x1		# le plus
	y = 0 				# y image de x sur la droite mx+p
	rep = 0 			# le nombre de pixel pas blanc sur la droite



	for x in range(x1,x2) :
		y = m*x + p
		y = int(round(y,0))


		if source_mur.get(x,y) < (200,200,200) :
			rep = rep + 1
	return rep


def point_value(source,distance) :
	"""
	source = valeur en DECIBEL de la source de bruit
	distance = distance entre la source et le point en METRE
	value = sortie en DECIBEL
	"""

	if distance == 0 :
		distance = distance+1

	ratio = (1/distance)**2
	value = source + (10*log(ratio,10))
	return int(round(value,0))


def point_total_value(liste,coord) :
	"""
	liste = toute les sources appareillé avec leur valeur
	coord = coordoné du point qu'on determiine la sous forme de TUPLE
	"""

	value = 25 # ------------------ Valeur minimale en decibel (bruit ambient) -----------------------------------

	for i in liste :
		# i[0] = liste des tuple de coord  i[1] = valeur en dB


		if i[1] == "None" :
			continue


		maxi = sqrt(1000**2+700**2)
		for o in i[0] : # pour tt les tuples,o =tuple

			# KNN on determine le point le plus proche
			test_distance = distance(coord[0],coord[1],o[0],o[1])
			if test_distance < maxi :
				maxi = test_distance
				voisin = o

		rep = point_value(	int(i[1]),  distance(coord[0],coord[1],voisin[0],voisin[1])  ) - attenuation(coord[0],coord[1],voisin[0],voisin[1])

		value = 10*log((10**(value/10))+(10**(rep/10)),10)

	return int(round(value,0)) 		


def draw_data() :

	global chart
	global can
	global mesure_all

	can.delete(ALL)

	rep = appairage(mesure_all,temps.curselection()[0]+1 ,mode.curselection()[0]+2)


	for i in range(70) : # x du point 
		for o in range(100) : # y du point 

			value = point_total_value(rep,(i*10,o*10))

			can.create_line(i*10,o*10,10+i*10,10+o*10,width=10,fill=chart[value],tags=str(i)+str("")+str(o))
			root.update()

	can.create_image(0,0,anchor=NW,image=source)

def appairage(liste,heure,donne) :
	"""
	liste = liste des mesure
	heure = heure demandé
	donne = mini maxi ou moyenne = 2 , 3 , 4 
	"""

	for i in liste :
		if int(i[1]) == heure :

			if i[0] == "CDI" :
				lieu_cdi[1] = i[donne]

			if i[0] == "Ateliers" :
				lieu_ateliers[1] = i[donne]

			if i[0] == "Cantine" :
				lieu_cantine[1] = i[donne]

			if i[0] == "Permanence" :
				lieu_perm[1] = i[donne]

			if i[0] == "Vie Scolaire" :
				lieu_vie_sco[1] = i[donne]

			if i[0] == "Gymnase" :
				lieu_gymnase[1] = i[donne]

			if i[0] == "Cours" :
				lieu_recre[1] = i[donne]
			
			if i[0] == "Salle de muscu" :
				lieu_muscu[1] = i[donne]

			if i[0] == "Internat" :
				lieu_internat[1] = i[donne]

			if i[0] == "Salle de classe" :
				lieu_classe[1] = i[donne]
			
			if i[0] == "Laboratoire" :
				lieu_labo[1] = i[donne]

			if i[0] == "Couloirs" :
				lieu_couloirs[1] = i[donne]

			if i[0] == "Administration" :
				lieu_admin[1] = i[donne]
			
			if i[0] == "Salle des Profs" :
				lieu_profs[1] = i[donne]

	lieu_all_0 = [lieu_cdi,lieu_ateliers,lieu_cantine,lieu_perm,lieu_vie_sco,lieu_gymnase,lieu_recre,lieu_muscu,
	lieu_internat,lieu_classe,lieu_labo,lieu_couloirs,lieu_admin,lieu_profs]

	return lieu_all_0


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

# Main root :----------------------------------------------------------------------------------------------




mesure_all = ouverture("mesure.csv")
mesure_all.pop(0)

frame_dessin = Frame(root,height=1000,width=700)
frame_dessin.pack(side="left")


can_vertical_scroll = Scrollbar(frame_dessin)
can_vertical_scroll.pack(side="left",fill=BOTH)

can = Canvas(frame_dessin,height=1000,width=700,bg=green,scrollregion=(0,0,700,1000),yscrollcommand=can_vertical_scroll.set)
can.pack()

can_vertical_scroll.config(command = can.yview)


def mmove(event):
	global chart
	global mesure_all

	#print(event.x, event.y)

	rep = appairage(mesure_all,temps.curselection()[0]+1 ,mode.curselection()[0]+2)

	val = point_total_value(rep,(event.x,event.y))
	decibel.set(val)

	color.configure(bg= chart[val])


root.bind('<Button-1>', mmove)



can.create_image(0,0,anchor=NW,image=source_mur)


for i in lieu_all :
	can.create_line(i[0]-1,i[1]-1,i[0]+1,i[1]+1,width=5,fill=green)



frame_config = Frame(root,height=1000,width=300,bg="yellow")
frame_config.pack(side="right",fill=BOTH,expand=1)

color = Canvas(frame_config,height=20,width=20)
color.pack(anchor="nw")

color_label = Label(frame_config,textvariable=decibel)
color_label.pack(anchor="nw")

temps  = Listbox(frame_config,selectmode="single",exportselection=False)
temps.pack(anchor="ne")

temps.insert(0,"Avant les cours")
temps.insert(1,"Pendant les cours")
temps.insert(2,"Interclasse")
temps.insert(3,"Recréation")  # mettre les noms propres
temps.insert(4,"Pause méridienne")
temps.insert(5,"Sortie des cours")
temps.selection_set(0)


mode = Listbox(frame_config,selectmode="single",exportselection=False)
mode.pack(anchor="ne")

mode.insert(0,"Minimum")
mode.insert(1,"Maximum")
mode.insert(2,"Moyenne")
mode.selection_set(2)


draw_button = Button(frame_config,text="Dessiner",command=draw_data)
draw_button.pack(anchor="center")


root.mainloop()