![Encabezado](https://github.com/jpradas1/BASTO-project/blob/main/Images/encabezado.jpg)

# **Bastó Project - Team #3**
______
Somos un grupo de Data Scientists e ingresamos en el programa *Henry Projects*, se trata de una iniciativa para que los estudiantes de Henry, en su etapa de proyecto final, tengan la oportunidad de realizar proyectos reales. En nuestro caso nos incorporaramos a la empresa *Bastó Ganado Inteligente*, y por un mes trabajamos en un entorno real.
______

## **Hablemos de Bastó**

Bastó es un sistema basado en IOT (Internet de las cosas) que, a través de caravanas inteligentes, gestiona una cerca virtual dinámica que monitorea de forma constante la ubicación, salud y bienestar del ganado, posibilitando un pastoreo de precisión.

Bastó propone subdividir grandes potreros en lotes más pequeños para lograr una producción más intensiva y un eficiente uso de las pasturas, a través de cercas virtuales controlando al ganado con dispositivos inteligentes que los monitorea, contiene y arrea, gestionando un pastoreo de precisión. Esto es posible ya que se evitaría el alto costo de infraestructura, mano de obra, y tiempo.

## **El proyecto**

El desafío propuesto: 

*Estimación biomasa disponible: Con el mapa de dinámica de pastoreo y las imágenes satelitales con NDVI, calcular las superficies consumidas vs la remanente. Objetivo, saber cuánto forraje se dispone y por cuánto tiempo.*

... 

### **Objetivos**

**Específicos del trabajo:**

* Obtener información de las bases de datos ofrecidas por la empresa
* Obtener imágenes satelitales necesarias y utilizar el NDVI para estimar la biomasa disponible en el lote.
* Crear un modelo de machine learning que determine la biomasa disponible en un cuadrante y por cuánto tiempo
* Determinar la biomasa consumida y la biomasa remanente en la zona de pastoreo.
* Crear una API que brinde la cantidad días de alimento disponible a partir de parámetros ingresados por el usuario.

**Del equipo:**
* Trabajar en conjunto para analizar los datos y obtener información útil.
* Evaluar los resultados del proyecto y determinar si se cumplen los objetivos establecidos. 
* Proporcionar recomendaciones para mejorar la gestión del pastoreo en la zona de estudio en equipo.

### **Alcance y fuera de alcance**

**Alcance:**
* Obtener información útil sobre el forraje en distintas zonas. 
* Obtener las imágenes satelitales necesarias para calcular la biomasa a partir del NDVI.
* Calcular la biomasa consumida y la biomasa remanente para determinar cuánto forraje queda disponible.

**Fuera de alcance:**
* Realizar mediciones de campo para validar las estimaciones de biomasa obtenidas a partir de las imágenes satelitales.
* Realizar un análisis de la calidad nutricional del forraje disponible.
* Evaluar la calidad de las aguas en la zona de pastoreo.

## **Métricas**
* Biomasa total (Biomasa por hectárea * Superficie del lote)
* Biomasa remanente (Biomasa total - Biomasa consumida)
* Tiempo de disponibilidad de forraje (Biomasa total / ración -> 15 kg)

## **KPIs**
* Mantener el NDVI por encima de 0,60 para asegurar la salud y productividad de la vegetación.
* Asegurar que la disponibilidad de forraje sea suficiente para alimentar a los animales durante el período de tiempo determinado por el modelo.
* Mantener la biomasa remanente en valores cercanos a 0 luego de terminado el plazo estimado por el modelo.
* (Cantidad de raciones por lote)

## **Stack tecnológico**
* Python
* MongoDB Compass
* Postman
* Trello
* PowerBI
* Fast API
* Genially

## **Metodología de trabajo**
* Establecer reuniones diarias con el equipo
* Dividir tareas en base a los roles establecidos
* Socializar avances en la investigación
* Buscar/complementar investigación con personas pertinentes/especialistas al tema

## **Roles y responsabilidades**
* **Data Engineers**: Prada Sierra, Juan Camilo; Martinez, Carlos Santiago
* **Data Analyst**: Zarich Santi, Daniela Emilia
* **Data Scientist**: Gutierrez Mas, Gabriel Hernán; Hoyos Hoyos, Pedro

## **Tablas de relaciones**
![Tabla_relaciones](https://github.com/jpradas1/BASTO-project/blob/main/Images/Tabla%20relaciones.jpeg)
