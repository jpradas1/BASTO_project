<div id = "header" align = "center">
  <img = src = "https://github.com/jpradas1/BASTO-project/blob/main/Images/encabezado.jpg" width = "800" />
</div>


# **Bastó Project - Team N°3**
______
Somos un grupo de Data Scientists que hemos participado en el programa Henry Projects. Durante un mes, hemos trabajado en colaboración con el equipo de Bastó Ganado Inteligente para desarrollar soluciones basadas en datos que mejoren la gestión del ganado y el pastoreo. Estamos entusiasmados por el impacto que nuestras soluciones pueden tener en la industria ganadera.
______

## **Hablemos de Bastó**

[Bastó](https://www.bastó.com.ar/) es sistema basado en IoT (Internet de las cosas) que utiliza caravanas inteligentes para implementar una cerca virtual dinámica, la cual monitorea de manera constante la ubicación, salud y bienestar del ganado, permitiendo así un pastoreo de precisión.

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
* **Data Scientist**: Gutierrez Mas, Gabriel Hernán

---
<div id = "header" align = "center">
  <h1 align = 'Center'> Stack tecnológico </h1>
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/slack/slack-original.svg' title = 'Slack' alt = 'Slack' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/smartinez24/devicons/blob/master/icons/trello/trello-plain.svg' title = 'Trello' alt = 'Trello' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/google/google-original.svg' title = 'Google' alt = 'Google' width = '40' height = '40'/>&nbsp;
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/vscode/vscode-original-wordmark.svg' title = 'VSC' alt = 'VSC' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/windows8/windows8-original.svg' title = 'Windows' alt = 'Windows' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/smartinez24/devicons/blob/master/icons/linux/linux-original.svg' title = 'Linux' alt = 'Linux' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/smartinez24/devicons/blob/master/icons/mongodb/mongodb-original-wordmark.svg' title = 'MongoDB' alt = 'MongoDB' width = '40' height = '40' />&nbsp;
   <img src = 'https://i.pinimg.com/564x/8a/2c/b9/8a2cb9635fd4fe44543f87b9f42ba014.jpg' title = 'Archivos csv' alt = 'Archivos csv' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg' title = 'Python' alt = 'Python' width = '40' height = '40' />&nbsp;
   <img src = 'https://github.com/devicons/devicon/blob/master/icons/fastapi/fastapi-original.svg' title = 'FastAPI' alt = 'FastAPI' width = '40' height = '40' />&nbsp;
   <img src = 'https://res.cloudinary.com/practicaldev/image/fetch/s--iWNIikKc--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/u6kmbieir6su8dt70z3l.png' title = 'Render' alt = 'Render' width = '40' height = '40' />&nbsp;
    <img src = 'https://github.com/devicons/devicon/blob/master/icons/github/github-original-wordmark.svg' title = 'GitHub' alt = 'GitHub' width = '40' height = '40' />&nbsp;

</div>

# Ejecución del Código
> Este proyecto presenta diferentes etapas para la ejecución plena del código, donde finalmente se obtiene el dashboard. Este porceso consta de 2 etapas; primero la extracción, transfomación y carga del dataset a emplear (ETL), el segundo paso conta de la ejecucion de la api mediante [FastAPI](https://fastapi-basto-project.onrender.com/docs) y de la app de [Streamlit](https://basto-project.onrender.com).

## Dataset
> Para este proyecto se extrajo el dataset de 3 fuentes distintas.
>
> ### Auravant
> [Auravant](https://www.auravant.com/) es la herramienta digital la cual nos permite extraer información relevante sobre los campos y lotes, acerca del actual estado de los cultivos y los suelos mediante imágenes satelitales. Principalmente, extraemos de esta herramienta el Índice Verde o Normalized Difference Vegetation Index (NDVI), a través de su [API](https://developers.auravant.com/docs/apis/reference/api_ref_gral/). Para automatizar este proceso de extraer data relevante para el proyecto se crea el script de python
```
auravant_api.py
```
> Este archivo realiza consultas automaticas a la API de auraventa, transformado los datos a DataFrames de pandas para tratar posteriormente con datos como el ID del lote, su nombre, las dimensiones del mismo, su area, y más importante su NDVI.
>
> ### Tablas de Control Forrajero
> Uno de los objetivos fundamentales del proyecto consta en calcular la biomasa de un determinado lote relacionado con un cierto usurio. Sin embargo, es necesario conocer los valores de biomasa para distintos tipos de vegetación. Para ello la página web de [Tablas de Control Forrajero](https://tableroforrajero.crea.org.ar/dashboardcrea2/index.php/crea_session_manager) oferece un extenso dataset sobre la producción mensual de cada vegetación a lo largo de Argentina y parte de Uruguay. Debido a la gran cantidad de datos a descargar se crea el archivo **tcf_scrapping.py** el cual automatiza este proceso de descarga gracias a la librería **Selenium** que emplea el navegador **FireFox** para la obtención de los datos. Para realizar este proceso se ha de correr el siguiente comando:
```
python3 tcf_scraping.py .(pwd)/dataset/
```
> Siendo **.(pwd)/dataset/** el path absoluto a la carpeta de descarga. Por otro lado, este proceso es opción realizarlo, puesto que en el directorio **./dataset/** se encuentra el resultado final de esta ejecución, es decir, el archivo **./dataset/All_Harvest.csv** contiene ya todos los datos necesarios para trabajar.
>
> ### BASTÓ Dataset
> Como último dataset necesario para este proyecto es el dataset proporcionado por la Start-Up argentina BASTÓ. Este dataset no se encuentra en este repositorio por razones de privacidad. Sin embargo, si se llega a contar con esta base de datos en MongoDB, solo es necesario correr el siguiente comando:
```
python3 mongodb.py
```
> 
## FastAPI
> Como se mencionó anteriormente, se ha realizado una [API](https://fastapi-basto-project.onrender.com/docs) con el proposito de que se pueda consumir los datos finales de forma adecuada y eficiente. Para ello se ha hecho un deploy mediante [render](render.com).
> <img src="Images/fastapi.png" width="800">
> 
## Streamlit App
> Por otro lado, como alternativa al usuario se ha creado una [app](https://basto-project.onrender.com) empleado streamlit. En esta app el usuario puede monitorear el estado de los cultivos, asimismo la actidad actual de biomasa en el lote, las areas consumidas por el ganado, además de aquellas areas remanentes.
> 
> <img src="Images/streamlit_1.png" width="350">
> <img src="Images/streamlit_2.png" width="350">
> <img src="Images/streamlit_3.png" width="800">
> 
> En la última imagen se visualiza las área mayormente ocupadas por el ganado (representadas por las regiones más oscuras), contrariamente las áreas claras son aquellas donde el ganado poco ha pastado.
>
> Visualizar el mapa de calor mediante el [render](https://basto-project.onrender.com) puede ser muy lento, por ello si se requiere de rápidas consultas se recomienda correr la app localmente con el siguiente comando:
```
streamlit run Index.py
```
