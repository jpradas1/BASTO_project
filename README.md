<div id = "header" align = "center">
  <img = src = "https://github.com/jpradas1/BASTO-project/blob/main/Images/encabezado.jpg" width = "800" />
</div>


# **Bastó Project - Team N°3**
______
Somos un grupo de Data Scientists que hemos participado en el programa Henry Projects. Durante un mes, hemos trabajado en colaboración con el equipo de Bastó Ganado Inteligente para desarrollar soluciones basadas en datos que mejoren la gestión del ganado y el pastoreo. Estamos entusiasmados por el impacto que nuestras soluciones pueden tener en la industria ganadera.
______

## **Hablemos de Bastó**

"Bastó" es sistema basado en IoT (Internet de las cosas) que utiliza caravanas inteligentes para implementar una cerca virtual dinámica, la cual monitorea de manera constante la ubicación, salud y bienestar del ganado, permitiendo así un pastoreo de precisión.

La empresa propone una solución para mejorar la producción y el uso de pasturas en grandes potreros, mediante la subdivisión de estos en lotes más pequeños y el control del ganado a través de cercas virtuales y dispositivos inteligentes que monitorean, contienen y dirigen al ganado, optimizando el pastoreo de manera eficiente. Esta tecnología permite reducir costos de infraestructura, mano de obra y tiempo, al tiempo que se mejora la calidad del pastoreo y se aumenta la productividad.

## **El proyecto**

### **Desafío** 

*Estimación biomasa disponible: Con el mapa de dinámica de pastoreo y las imágenes satelitales con NDVI, calcular las superficies consumidas vs la remanente. Objetivo, saber cuánto forraje se dispone y por cuánto tiempo.*

### **Objetivos**

**Específicos del trabajo:**

* Obtener información de las bases de datos ofrecidas por la empresa
* Obtener imágenes satelitales necesarias y utilizar el NDVI para estimar la biomasa disponible en el lote.
* Determinar la biomasa consumida y la biomasa remanente en la zona de pastoreo.
* Crear una [API](https://fastapi-basto-project.onrender.com/docs) que brinde la cantidad días de alimento disponible a partir de parámetros ingresados por el usuario.

**Del equipo:**
* Trabajar en conjunto para analizar los datos y obtener información útil.
* Evaluar los resultados del proyecto y determinar si se cumplen los objetivos establecidos. 
* Proporcionar recomendaciones para mejorar la gestión del pastoreo en la zona de estudio.

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
* Biomasa total (Biomasa * Hectárea)
* Biomasa remanente (Biomasa total - Biomasa consumida)
* Tiempo de disponibilidad de forraje (Biomasa total / (Ración * Cantidad de animales)) Ración: 15 kg para Raza Británica

## **KPIs**
* NDVI saludable: Considerar lotes con NDVI por encima de 0,60 para asegurar la salud y productividad de la vegetación.
* Forraje disponible: Asegurar que la disponibilidad de forraje sea suficiente para alimentar a los animales durante el período de tiempo determinado por el modelo.
* Consumo óptimo: Mantener la biomasa remanente en valores cercanos a 0 luego de terminado el plazo estimado por el modelo.
* Tamaño de rodeo: Establecer qué cantidad de bovinos es ideal poner en un lote de acuerdo a la cantidad de forraje y un tiempo determinado.

## **Roles y responsabilidades**
* **Data Engineers**: Prada Sierra, Juan Camilo; Martinez Torres, Carlos Santiago
* **Data Analyst**: Zarich Santi, Daniela Emilia
* **Data Scientist**: Gutierrez Mas, Gabriel Hernán; Hoyos Hoyos, Pedro

---
<div id = "header" align = "center">
  <h1 align = 'Center'> Stack tecnológico </h1>
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/slack/slack-original.svg' title = 'Slack' alt = 'Slack' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/google/google-original.svg' title = 'Google' alt = 'Google' width = '40' height = '40'/>&nbsp;
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/vscode/vscode-original-wordmark.svg' title = 'VSC' alt = 'VSC' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/windows8/windows8-original.svg' title = 'Windows' alt = 'Windows' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/smartinez24/devicons/blob/master/icons/linux/linux-original.svg' title = 'Linux' alt = 'Linux' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg' title = 'Python' alt = 'Python' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/fastapi/fastapi-original.svg' title = 'fastAPI' alt = 'fastAPI' width = '40' height = '40' />&nbsp;
   <img src = 'https://res.cloudinary.com/practicaldev/image/fetch/s--iWNIikKc--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/u6kmbieir6su8dt70z3l.png' title = 'Render' alt = 'Render' width = '40' height = '40' />&nbsp;
    <img src = 'https://github.com/devicons/devicon/blob/master/icons/github/github-original-wordmark.svg' title = 'Github' alt = 'Github' width = '40' height = '40' />&nbsp;

</div>
