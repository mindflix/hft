import numpy as np

"""
Fonction exemplaire pour appliquer l'algorithme de gradient descendant.
Elle représente l'erreur globale de notre réseau de neurones.
"""


# Cost Function
def fonction(X, Y):
    return X*np.exp(-X**2-Y**2)+(X**2+Y**2)/20


# Gradient de la Cost function
def gradient_fonction(X, Y):
    g_x = np.exp(-X**2-Y**2)+X*-2*X*np.exp(-X**2-Y**2)+X/10
    g_y = -2*Y*X*np.exp(-X**2-Y**2)+Y/10
    return g_x, g_y


# Point de départ aléatoire de notre recherche de minimum local/global
x = np.random.random_integers(-2, 2)+np.random.rand(1)[0]
y = np.random.random_integers(-2, 2)+np.random.rand(1)[0]

# Learning Rate
lr = 0.2
lr2 = 0.9

# Variable permettant d'augmenter l'inertie de notre recherche
correction_x = 0
correction_y = 0

i = 0

while i < 401:
    g_x, g_y = gradient_fonction(x, y)
    correction_x = lr2*correction_x-lr*g_x
    x = x+correction_x
    correction_y = lr2*correction_y-lr*g_y
    y = y+correction_y
    print("itération {:3d}  -> x={:+7.5f} y={:+7.5f}".format(i, x, y))
    i += 1
