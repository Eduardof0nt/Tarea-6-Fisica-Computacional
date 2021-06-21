import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

'''
Se define la función crearPoblacionInicial(cantidad, numeroDeCiudades) donde:
    * cantidad es la cantidad de individuos que se desean crear para la población
    * numeroDeCiudades es la cantidad de ciudades que se van a utilizar en la simulación
Esta función genera una población inicial con individuos con un genoma aleatorio
'''
def crearPoblacionInicial(cantidad, numeroDeCiudades):
    
    #Se genera un arreglo con los índices de las ciudades, estos son los índices con los que se accesan las coordenadas de las ciudades del arreglo que contiene estas coordenadas, cargadas del archivo dado
    indiceCiudades = np.linspace(0, numeroDeCiudades-1,numeroDeCiudades).astype(int)
    
    #Se inicia el arreglo donde se va a contener a la población inicial
    poblacionInicial = []
    
    #Se inicia un ciclo while para generar un individuo con un genoma aleatorio en cada iteración, hasta llegar al número deseado de individuos
    i = 0
    while i < cantidad:
        
        #Se le añade a la población inicial una permutación aleatoria del arreglo indiceCiudades
        poblacionInicial.append(np.random.permutation(indiceCiudades).tolist())
        
        #Se agrega uno al contador
        i += 1
    
    #Se retorna la población generada como un arreglo de Numpy    
    return np.array(poblacionInicial)


'''
Se define la función funcionDeOptimizacion(cromosoma) donde:
    * cromosoma es el cromosoma de un individuo específico (se debe cambiar en el cromosoma los índices por sus respectivas coordenadas de ciudades)
Esta función calcula el valor de ajuste para un individuo
'''
def funcionDeOptimizacion(cromosoma):
    
    #Se define la variable distancia, el la cual se va a guardar el acumulado de las distancias euclidianas entre nodos adyacentes
    distancia = 0
    
    #Se itera sobre los nodos para calcular la distancia que hay entre ellos
    #Se comienza desde -1 ya que este índice indica a Numpy a tomar el último elemento. Esto permite realizar fácilmente el cálculo entre el último y el primer nodo, ya que se toma el nodo actual y el siguiente en la iteración para el cálculo
    for i in range(-1,len(cromosoma)-1):
        #Se calcula la distancia euclidiana y se suma a la variable distancia
        distancia += np.sqrt(np.sum(np.power(cromosoma[i]-cromosoma[i+1],2)))
    
    #Se calcula el inverso de la distnacia y se retorna el valor
    return 1/distancia

'''
Se define la función mutacion(cromosoma, probabilidad) donde:
    * cromosoma es el cromosoma de un individuo específico
    * probabilidad es la probabilidad de que ocurra una mutación
Esta función muta el individuo (cromosoma) ingresado con una cierta probabilidad
'''
def mutacion(cromosoma, probabilidad):
    
    #Primero se genera un número en el intervalo [0;1[ y si este número es menor que el valor de la probabilidad ingresada, se procede a la mutación
    if np.random.random() < probabilidad:
        #Se inician dos variables para contener los índices de los elementos que se van a intercambiar
        indice1 = 0
        indice2 = 0
        #En el caso de que los índices sean iguales, se continúa generando índices aleatorios hasta que sean diferentes
        while indice1 == indice2:
            #Se genera un arrglo con dos números aleatorios entre 0 y la longitud del cromosoma y se asigna cada elemento a la variable respectiva
            indice1, indice2 = np.random.randint(0, len(cromosoma),2)

        #Se intercambian de lugar los elementos en los índices aleatorios obtenidos
        cromosoma[indice1], cromosoma[indice2] = cromosoma[indice2], cromosoma[indice1]
    
    #Se regresa el cromosoma, mutado o no
    return cromosoma

'''
Se define la función InicializacionModificada(cantidad, CoordenadasCiudades) donde:
    * cantidad es la cantidad de individuos que se desean crear en la población
    * CoordenadasCiudades son las coordenadas de las ciudades
Esta función genera una población con un individuo ventajoso
'''
def InicializacionModificada(cantidad, CoordenadasCiudades):
    
    #Se ingresa a una variable la longitud del arrglo de las coordenadas de las ciudades y se inicia la lista para contener la población inicial
    numeroDeCiudades = len(CoordenadasCiudades)
    poblacionInicial = []
    
    #Se inicia el ciclo para crear los individuos de la población
    i = 0
    while i < cantidad:
        
        #Se genera un arreglo con los índices de las ciudades (una lista de 0 hasta la cantidad de ciudades menos 1) y se toma un elemento como el nodo inicial
        indiceCiudades = np.linspace(0, numeroDeCiudades-1,numeroDeCiudades).astype(int).tolist()
        nodoInicial = np.random.randint(0,numeroDeCiudades)
        
        #Se inicia el arreglo en el cual se van a ingresar los índices de las ciudades en orden de cercanía y se ingresa el primer nodo
        individuoActual = []
        individuoActual.append(nodoInicial)
        
        #Se elimina el nodo inicial de la lista de índices de ciudades
        for j in range(0,len(indiceCiudades)):
            if indiceCiudades[j] == nodoInicial:
                indiceCiudades.pop(j)
                break
        
        #Se define la variable nodoPasado para guardar el valor del último índice ingresado para calcular en la siguiente iteración su ciudad más cercano
        nodoPasado = nodoInicial
        #Se continuan las iteraciones hasta que la lista de indiceCiudades esté vacía
        while len(indiceCiudades) > 0:
            #Se ordenan los indices dependiendo de la distancia entre las ciudades en orden ascendente
            indiceCiudades.sort(key=lambda x: np.sqrt(np.sum(np.power(CoordenadasCiudades[x,:]-CoordenadasCiudades[nodoPasado,:],2))), reverse=False)
            #Se elimina primer elemento de la lista y se ingresa a la variable nodoPasado, este luego se agrega a la lista de la población actual
            nodoPasado = indiceCiudades.pop(0)
            individuoActual.append(nodoPasado)
        
        #Si la población no es la primera, se realizan entre 3 y 10 mutaciones (aleatoriamente) en el individuo
        if i != 0:
            for j in range(0,np.random.randint(3,11)):
                #Se utiliza la misma lógica que en la función de mutación
                indice1 = 0
                indice2 = 0
                while indice1 == indice2:
                    indice1, indice2 = np.random.randint(0, len(individuoActual),2)

                poblacionActual[indice1], poblacionActual[indice2] = individuoActual[indice2], individuoActual[indice1]
        
        #Se agrega el individuo generado a la lista de la población inicial
        poblacionInicial.append(individuoActual)
        
        #Se aumenta el contador
        i += 1
    
    #Se retorna la población inicial como un arreglo de Numpy
    return np.array(poblacionInicial)

#----------Inicio del programa-------------------

#Se abre el archivo de las coordenadas de las ciudades y se crea una variable para contener el archvio formateado
archivo = open('CoordenadasCiudades.txt')
CoordenadasCiudades = []

#Se definien los parámetros para la simulación
tamañoDePoblacion = 10
probabilidadDeMutacion = 1
nIter = 100

#Se crea una lista para guardar los mejores individuos (los que lleguen a superar al mejor individuo guardado anterior) y otra para guardar los mejores individuos y los promedio de la función de ajuste de cada iteración
mejorCamino = []
resultados = []

#Se extraen los datos del archivo y se ingresan a una lista
for linea in archivo:
    coordenadas = linea.replace(',', '').replace('[', '').replace(']', '').split(' ')
    CoordenadasCiudades.append([float(coordenadas[0]),float(coordenadas[1])])

#Se convierte la lista de coordenadas a un arreglo de Numpy
CoordenadasCiudades = np.array(CoordenadasCiudades)

#Se define la población inicial
poblacion = crearPoblacionInicial(tamañoDePoblacion,len(CoordenadasCiudades)) #Para la simulación normal
# poblacion = InicializacionModificada(tamañoDePoblacion,CoordenadasCiudades) #Para la simulación con un individuo con ventaja

#Se inicia el contador y se inicia el ciclo de iteraciones
n = nIter
while n >= 0:
    #Se convierte la población hasta el momento en una lista (una copia) y se define la variable para acumular la suma de los valores de ajuste para calcular su promedio
    caminos = poblacion.tolist()
    promedioGeneracional = 0
    #Se itera sobre la población para calcular el valor de ajuste de cada individuoy calcular el promedio generacional
    for i in range(0,len(caminos)):
        #Se guarda en la variable camino el camino en el índice actual y su valor de ajuste y se suma el valor de ajuste al acumulador
        caminos[i] = (caminos[i],funcionDeOptimizacion(caminos[i]))
        promedioGeneracional += caminos[i][1]
    
    #Se divide la suma total de valores de ajuste entre el total de individuos para calcular el promedio generacional
    promedioGeneracional /= len(caminos)
    
    #Se ordenan los individuos por su función de ajuste    
    caminos.sort(key=lambda x: x[1], reverse=True)

    #Se guarda el valor de ajuste del mejor individuo y se guarda el promedio genracional en la lista de resultados
    mejorValorAjuste = caminos[0][1]
    resultados.append([promedioGeneracional,mejorValorAjuste])
    
    #Si no ha habido un mejor camino, solamente se añade el mejor camino actual a la lista, si no fuera el caso y además el valor de ajuste del mejor individuo es mayor al del mejor individuo hasta el momento, este se añade al arreglo de mejorCamino
    if mejorCamino == []:
        mejorCamino.append((caminos[0][0], mejorValorAjuste))
    elif mejorValorAjuste > mejorCamino[len(mejorCamino)-1][1]:
        mejorCamino.append((caminos[0][0], mejorValorAjuste))
    
    #Se aplican las mutaciones a cada individuo de la población, dependiendo de la probabilidad
    for i in range(0,len(poblacion)):
        poblacion[i] = mutacion(poblacion[i],probabilidadDeMutacion)
    
    #Se reduce el contador en 1
    n -= 1

#Se convierten los resultados a un arreglo de Numpy
resultados = np.array(resultados)

#Se mapean los índices en el cromosoma de los mejores caminos a las respectivas coordenadas de cada ciudad
coordenadasMejorCamino = []
for camino in mejorCamino:
    caminoAlter = camino[0].copy()
    caminoAlter.append(caminoAlter[0])
    coordenadasMejorCamino.append(CoordenadasCiudades[caminoAlter])

#Se muestra al usuario la longitud del camino con la menor distancia
print('El camino más corto encontrado fue de {0:.2f}'.format(1/mejorCamino[len(mejorCamino)-1][1]))

#Se genera un arreglo de Numpy con el mejor individuo encontrado en la simulación y se guarda a un archivo de texto
listaParaGuardar = np.array(mejorCamino[len(mejorCamino)-1][0])
np.savetxt('caminoMásCorto_AGE.txt',listaParaGuardar, fmt='%d')

#Se grafican los resultados
#Se crea el gráfico con los respectivos parámetros
global ax
fig, ax = plt.subplots()
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_title('Resultados de la Simulación')
#Se muestra como primero de los mejores caminos encontrados (el peor de los mejores) como gráfico inicial
ax.plot(coordenadasMejorCamino[0][:,0], coordenadasMejorCamino[0][:,1])
ax.scatter(CoordenadasCiudades[:,0],CoordenadasCiudades[:,1],s=300,color='red')
ax.scatter(coordenadasMejorCamino[0][0,0],coordenadasMejorCamino[0][0,1],s=300,color='green')

#Se define un slider para controlar el mejor individuo encontrado (hasta el momento de su iteración) que se muestra
axcolor = 'lightgoldenrodyellow'
ax.margins(x=0)
plt.subplots_adjust(left=0.25, bottom=0.25)
axTiempo = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
slider_tiempo = Slider(
    ax=axTiempo,
    label='Mejor solución',
    valmin=1,
    valmax=len(mejorCamino),
    valinit=0,
    valstep=1
)

#Se define una función para cambiar el mejor camino que se mestra
def cambiarTiempo(tiempo):
    global ax
    ax.clear()
    ax.plot(coordenadasMejorCamino[tiempo-1][:,0], coordenadasMejorCamino[tiempo-1][:,1])
    ax.scatter(CoordenadasCiudades[:,0],CoordenadasCiudades[:,1],s=300,color='red')
    ax.scatter(coordenadasMejorCamino[tiempo-1][0,0],coordenadasMejorCamino[tiempo-1][0,1],s=300,color='green')

#Se añade la función al slider como callback function
slider_tiempo.on_changed(cambiarTiempo)


#Gráficas de los valores de ajuste promedio y mejor por generación
fig1, ax1 = plt.subplots()
ax1.set_xlabel('Generación')
ax1.set_ylabel('Valor promedio de la función de optimización')
ax1.plot(np.linspace(0, nIter,nIter+1).astype(int),resultados[:,0])
ax1.set_title('Resultados de la Simulación por Generación')

fig2, ax2 = plt.subplots()
ax2.set_xlabel('Generación')
ax2.set_ylabel('Mejor valor de la función de optimización')
ax2.plot(np.linspace(0, nIter,nIter+1).astype(int),resultados[:,1])
ax2.set_title('Resultados del Mejor Individuo por Generación')

#Se muestran las gráficas
plt.show()