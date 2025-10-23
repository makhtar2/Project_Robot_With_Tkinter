import tkinter as tk
from tkinter import ttk

# Classe de base : Robot
class Robot:
    DIRECTIONS = ["Nord", "Est", "Sud", "Ouest"]
    MOUVEMENTS = {
        "Nord": (0, 1),
        "Sud": (0, -1),
        "Est": (1, 0),
        "Ouest": (-1, 0)
    }

    def __init__(self, nom, x=0, y=0, dir="Est"):
        self._nom = nom
        self._x = x
        self._y = y
        self._dir = dir

    def avancer(self, pas=1):
        #Avance d'un pas
        dx, dy = self.MOUVEMENTS[self._dir]
        self._x += dx * pas
        self._y += dy * pas

    def droite(self):
        #Tourne à droite 
        i = self.DIRECTIONS.index(self._dir)
        self._dir = self.DIRECTIONS[(i + 1) % 4]

    @property
    def nom(self): return self._nom
    @property
    def position(self): return (self._x, self._y)
    @property
    def direction(self): return self._dir

    def __str__(self):
        return f"{self._nom} → Pos: ({self._x},{self._y}) Dir: {self._dir}"

#Robot NG
class RobotNG(Robot):
    def __init__(self, nom, x=0, y=0, dir="Est"):
        super().__init__(nom, x, y, dir)
        self._turbo = False

    def avancer(self, pas=1):
        #Avance de plusieurs pas. Si turbo active, pas x3
        super().avancer(pas * 3 if self._turbo else pas)

    def gauche(self):
        #Tourne à gauche 
        i = self.DIRECTIONS.index(self._dir)
        self._dir = self.DIRECTIONS[(i - 1) % 4]

    def demi_tour(self):
        #Fait demi-tour
        #Accès direct pour plus d'efficacité
        i = self.DIRECTIONS.index(self._dir)
        self._dir = self.DIRECTIONS[(i + 2) % 4]

    @property
    def turbo(self): return self._turbo

    def activer_turbo(self): self._turbo = True
    def desactiver_turbo(self): self._turbo = False

    def __str__(self):
        return super().__str__() + f" Turbo: {'ON' if self._turbo else 'OFF'}"

# Interface Tkinter
class InterfaceDeuxRobots:
    TAILLE_GRILLE = 600
    TAILLE_ROBOT = 15
    ESPACEMENT = 20
    COULEURS = {
        'r1': "#4a90e2",  
        'r2': "#e74c3c",  
        'fond': "#E6E6E6",
        'grille': "#1c1919",
        'ombre': "#1d1d1d",
        'contour': "#404040"
    }

    def __init__(self, robot1, robot2):
        self.r1 = robot1
        self.r2 = robot2
        
        #fenetre et style
        self.fenetre = tk.Tk()
        self.fenetre.title("Simulation de Robots")
        self.fenetre.geometry("800x700")
        
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=("Helvetica", 10))
        self.style.configure("TLabel", font=("Helvetica", 11))
        self.style.configure("Title.TLabel", font=("Helvetica", 14, "bold"))
        
        main_frame = ttk.Frame(self.fenetre, padding="10")
        main_frame.pack(expand=True, fill="both")
        
        ttk.Label(main_frame, text="Simulation de Robots", 
                 style="Title.TLabel").pack(pady=(0, 10))
        
        self.zone = tk.Canvas(main_frame, 
                            width=self.TAILLE_GRILLE, 
                            height=self.TAILLE_GRILLE * 2//3,
                            bg=self.COULEURS['fond'],
                            relief="ridge",
                            bd=2)
        self.zone.pack(pady=10, padx=10)
        
        #Configuration des controles
        controls = ttk.Frame(main_frame)
        controls.pack(pady=10)
        notebook = ttk.Notebook(controls)
        notebook.pack(expand=True, fill="both", padx=5, pady=5)
        tab_r1 = ttk.Frame(notebook, padding=10)
        notebook.add(tab_r1, text="Robot Classique")
        ttk.Label(tab_r1, text=self.r1.nom, 
                 style="Title.TLabel").pack(pady=5)
        ttk.Button(tab_r1, text="Avancer", 
                  command=self.avancer_r1).pack(pady=5, fill="x")
        ttk.Button(tab_r1, text="Tourner à droite", 
                  command=self.droite_r1).pack(pady=5, fill="x")
        tab_r2 = ttk.Frame(notebook, padding=10)
        notebook.add(tab_r2, text="Robot NG")
        ttk.Label(tab_r2, text=self.r2.nom, 
                 style="Title.TLabel").pack(pady=5)
        ttk.Button(tab_r2, text="Avancer", 
                  command=self.avancer_r2).pack(pady=5, fill="x")
        ttk.Button(tab_r2, text="Tourner à droite", 
                  command=self.droite_r2).pack(pady=5, fill="x")
        ttk.Button(tab_r2, text="Tourner à gauche", 
                  command=self.gauche_r2).pack(pady=5, fill="x")
        ttk.Button(tab_r2, text="Demi-tour", 
                  command=self.demi_tour_r2).pack(pady=5, fill="x")
        frame_turbo = ttk.Frame(tab_r2)
        frame_turbo.pack(pady=10, fill="x")
        ttk.Button(frame_turbo, text="Turbo ON", 
                  command=self.turbo_on_r2).pack(side="left", expand=True, padx=2)
        ttk.Button(frame_turbo, text="Turbo OFF", 
                  command=self.turbo_off_r2).pack(side="right", expand=True, padx=2)
        frame_etat = ttk.LabelFrame(main_frame, text="État des Robots", padding=10)
        frame_etat.pack(pady=10, fill="x")
        self.info = ttk.Label(frame_etat, text="", wraplength=self.TAILLE_GRILLE)
        self.info.pack(pady=5)
        
        #grille
        self._dessiner_grille()
        
        self.deplacer()
        self.maj_infos()

        self.fenetre.mainloop()

    def _maj_affichage(self):
        self.deplacer()
        self.maj_infos()

    #Robot 1
    def avancer_r1(self):
        self.r1.avancer()
        self._maj_affichage() 

    def droite_r1(self):
        self.r1.droite()
        self._maj_affichage() 

    #Robot 2
    def avancer_r2(self):
        self.r2.avancer()
        self._maj_affichage() 

    def droite_r2(self):
        self.r2.droite()
        self._maj_affichage() 

    def gauche_r2(self):
        self.r2.gauche()
        self._maj_affichage() 

    def demi_tour_r2(self):
        self.r2.demi_tour()
        self._maj_affichage() 

    def turbo_on_r2(self):
        self.r2.activer_turbo()
        self._maj_affichage() 

    def turbo_off_r2(self):
        self.r2.desactiver_turbo()
        self._maj_affichage() 

    def _dessiner_direction(self, x, y, direction):
        #fleche indiquant la direction du robot
        fleche = self.TAILLE_ROBOT * 0.8
        dx, dy = Robot.MOUVEMENTS[direction]
        self.zone.create_line(x + dx * self.TAILLE_ROBOT, 
                            y - dy * self.TAILLE_ROBOT,
                            x + dx * (self.TAILLE_ROBOT + fleche),
                            y - dy * (self.TAILLE_ROBOT + fleche),
                            arrow="last", width=3,
                            fill=self.COULEURS['contour'],
                            tags="robot") 

    def _dessiner_robot(self, x, y, direction, couleur):
        cx = self.TAILLE_GRILLE//2 + x * self.ESPACEMENT
        cy = self.TAILLE_GRILLE//3 - y * self.ESPACEMENT
        t = self.TAILLE_ROBOT
        
        #Ombre
        offset = 3
        self.zone.create_oval(cx-t+offset, cy-t+offset,
                            cx+t+offset, cy+t+offset,
                            fill=self.COULEURS['ombre'], outline='',
                            tags="robot") # OPTIMISATION: Ajout du tag
        
        #Corps du robot
        self.zone.create_oval(cx-t, cy-t, cx+t, cy+t,
                            fill=couleur,
                            outline=self.COULEURS['contour'],
                            width=2,
                            tags="robot") 
        
        #Effet de brillance
        b = t * 0.6
        self.zone.create_oval(cx-b, cy-b, cx+b, cy+b,
                            fill='', outline='white', width=1,
                            tags="robot") 
        
        #Direction
        self._dessiner_direction(cx, cy, direction)

    def deplacer(self):
        """Met à jour la position des robots sur la grille."""
        self.zone.delete("robot")
        
        #Dessiner les robots
        x1, y1 = self.r1.position
        x2, y2 = self.r2.position
        
        self._dessiner_robot(x1, y1, self.r1.direction, self.COULEURS['r1'])
        self._dessiner_robot(x2, y2, self.r2.direction, self.COULEURS['r2'])

    def _dessiner_grille(self):
        #Dessine une grille
        w, h = self.TAILLE_GRILLE, self.TAILLE_GRILLE * 2//3
        
        self.zone.create_rectangle(0, 0, w, h, 
                                 fill=self.COULEURS['fond'],
                                 outline=self.COULEURS['grille'],
                                 width=2)
        
        # Lignes de la grille
        for i in range(0, h, self.ESPACEMENT):
            self.zone.create_line(0, i, w, i, fill=self.COULEURS['grille'])
        for i in range(0, w, self.ESPACEMENT):
            self.zone.create_line(i, 0, i, h, fill=self.COULEURS['grille'])

    def maj_infos(self):
        self.info.config(text=f"{self.r1}\n{self.r2}")

#affichage des deux robots
if __name__ == "__main__":
    robot1 = Robot("Classique", 0, 0, "Est")
    robot2 = RobotNG("Turbo", 0, 0, "Nord")
    InterfaceDeuxRobots(robot1, robot2)