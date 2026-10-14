# 🏢 Proyecto: Simulador de Examen Multiple Choice 30 preguntas para Administración de Consorcios (CABA)

Este repositorio documenta el desarrollo y despliegue de mi primer proyecto integral en **Python**. Se trata de un simulador de examen interactivo basado en la normativa legal y contable de Propiedad Horizontal (Código Civil y Comercial de la Ciudad Autónoma de Buenos Aires), diseñado específicamente para practicar y rendir con éxito ante el Consejo de Administradores.

A lo largo de este proyecto, evolucioné el software desde un script básico de consola hasta transformarlo en una aplicación web moderna y accesible mediante un enlace público.

![Profile Views](https://visitor-badge.laobi.icu/badge?page_id=MarceloNH-IT.MarceloNH-IT&style=flat)


:smile: :clap: **Adjuntos las imágenes por si les sirve el proceso de creación de cada paso para su proyectos** :smile: :clap:



![Descripción de la imagen](Esplicacion%200%20Py.jpg)


![Configuracin IDLE](Esplicacion%200.1%20Py.jpg)


![Vista final del proyecto parte 2](Esplicacion%202%20Py.jpg)


![Estructura del examen](Esplicacion%200.2%20Py.jpg)


![Validación con while](Esplicacion%200.3%20Py.jpg)


![Comando de instalación](Esplicacion%200.4%20Py.jpg)


![Navegación en consola](Esplicacion%200.5%20Py.jpg)


![Generación del exe](Esplicacion%200.6%20Py.jpg)


![Vista de la Web App en navegador](Esplicacion%200.7%20Web%20Py.jpg)


![Archivos creados web y ejecutable](Esplicacion8ArchivoPy.jpg)

:clap: :clap: **La pagina funciona correctamente para practicar el examen.** :clap: :clap:
Muchas gracias por ver mi portafolio. Les envio un saludo grande. 
**todo funcionando**
![Aplicación funcionando en el navegador](Funciona.jpg)

![Diseño](Diseño.jpg)


---

## 🛠️ Fase 1: Desarrollo de la Lógica y Script en Consola (CLI)

### Paso 1: Configuración del Entorno de Desarrollo (IDLE)

Para dar los primeros pasos en la programación, utilicé IDLE, el entorno integrado que viene por defecto al instalar Python en Windows.

* Accedí al menú de Inicio, busqué IDLE y abrí la consola interactiva (`>>>`).
* Creé un nuevo archivo en blanco seleccionando File > New File, lo que abrió el editor de código listo para escribir el script.

### Paso 2: Programación de la Estructura del Examen

Diseñé el cuestionario completo con preguntas de opción múltiple enfocadas en los aspectos legales, administrativos y contables de la propiedad horizontal en CABA.

* Utilicé una estructura de datos basada en una lista de diccionarios en Python, donde cada elemento almacena de forma ordenada la pregunta, sus respectivas opciones y la respuesta correcta.
* El código fuente de esta versión inicial quedó guardado en el archivo simulador_consorcio.py.

### Paso 3: Optimización y Validación con Bucles (while)

Durante las primeras pruebas en la consola, noté un "caso borde": si un usuario ingresaba por error una letra no contemplada, el programa podía fallar o comportarse de manera inesperada.

* Para solucionar esto, implementé una validación de entrada utilizando la estructura de control while.
* Mediante este bucle condicional, el programa evalúa permanentemente la respuesta ingresada y no permite avanzar a la siguiente pregunta a menos que el carácter introducido pertenezca estrictamente a las opciones válidas. En caso contrario, emite un aviso de error amigable y vuelve a solicitar el ingreso correcto.

### Paso 4: Guardado y Ejecución Local (F5)

* Guardé el archivo en mi equipo bajo el nombre simulador_consorcio.py.
* Utilicé la opción Run > Run Module (o la tecla F5 del teclado) para ejecutar el script directamente desde IDLE, verificando que el flujo de preguntas, la validación de errores y el cálculo de la nota final funcionaran a la perfección.

---

## 📦 Fase 2: Empaquetado y Creación del Archivo Ejecutable (.exe)

Para poder compartir la herramienta fácilmente con compañeros de estudio sin necesidad de que tengan Python instalado en sus computadoras, convertí el script en una aplicación independiente de Windows.

### Paso a paso del empaquetado:

1. **Apertura de la Terminal:** Abrí el Símbolo del sistema de Windows (`cmd`).
2. **Instalación de la herramienta de compilación:** Instalé la librería PyInstaller ejecutando el comando: `pip install pyinstaller`
3. **Ubicación en el directorio:** Navegué hasta la carpeta donde se encontraba mi archivo utilizando el comando: `cd C:\Users\Marcelo-Gestiones\OneDrive\Documentos`
4. **Generación del ejecutable:** Compilé el código en un único archivo autónomo ejecutando: `pyinstaller --onefile simulador_consorcio.py`
5. **Resultado:** Dentro de la carpeta generada dist, obtuve mi archivo final `simulador_examen_consorcio.exe`. Este archivo me permitió ejecutar el simulador haciendo un simple doble clic, listo para ser distribuido o copiado a un pendrive.

> **Nota sobre seguridad en Windows:** Como el ejecutable fue creado de forma local y no cuenta con una firma digital comercial corporativa, el sistema operativo puede mostrar una advertencia preventiva de SmartScreen al abrirlo por primera vez. Esto se resuelve de manera sencilla haciendo clic en "Más información" y luego en "Ejecutar de todas formas".

---

## 🌐 Fase 3: Evolución a Aplicación Web (Streamlit)

Para modernizar el proyecto y permitir que cualquier usuario pueda realizar la evaluación de manera interactiva desde cualquier dispositivo y con un solo clic, se migró la herramienta hacia una plataforma web optimizada utilizando Streamlit.

### Paso 1: Creación del Entorno Web (`app_examen.py`)

* Se desarrolló un script integral adaptado a la interfaz gráfica web, implementando componentes visuales avanzados como `st.title`, `st.subheader` y `st.radio` para la navegación dinámica de opciones y contenedores interactivos.
* Se incorporó lógica de calificación automática en tiempo real, provisión de feedback detallado por cada acierto o desvío, cálculo algorítmico de la nota final y efectos visuales interactivos (`st.balloons`) al alcanzar la aprobación del examen.

### Paso 2: Pruebas Locales y Validación del Servidor de Desarrollo

Con el objetivo de garantizar la correcta ubicación de los recursos y asegurar la estabilidad local antes de la puesta en producción, se ejecutaron los siguientes procedimientos técnicos en el Símbolo del sistema (`cmd`):

1. **Posicionamiento en el directorio de trabajo:** 
   `cd C:\Users\Marcelo-Gestiones\OneDrive\Documentos`
2. **Inicialización del entorno local:** 
   Se ejecutó el servicio utilizando la ruta absoluta del intérprete y el ejecutable de Streamlit para asegurar la correcta compilación: 
   `"C:\Users\Marcelo-Gestiones\AppData\Local\Python\pythoncore-3.14-64\Scripts\streamlit.exe" run app_examen.py`
3. **Validación de interfaz:** 
   El sistema levantó de manera automática el servidor de desarrollo local en la dirección `http://localhost:8501`, permitiendo una verificación fluida de la experiencia de usuario y el diseño responsivo.

*(Adjuntar aquí la captura de pantalla correspondiente a la ejecución local o en el navegador)*

### Paso 3: Despliegue en la Nube (Streamlit Community Cloud)

1. Se sincronizó e integró el código fuente principal (`app_examen.py`) junto con el repositorio público alojado en GitHub.
2. Se estableció la vinculación con la infraestructura en la nube de Streamlit Community Cloud, seleccionando el archivo ejecutable de entrada y completando el proceso de despliegue (*Deploy*), lo que generó un canal de acceso web público, seguro y oficial.

> **🔗 Acceso Directo a la Aplicación en Vivo:** 
> Puede probar y evaluar el funcionamiento del simulador en línea ingresando a través del siguiente enlace oficial:
> 👉 **[Simulador de Examen - Consorcio CABA](https://simulador-examen-consorcio-idozsxwpuwmivvsb39p6tm.streamlit.app)**
---



## 🚀 Tecnologías y Herramientas Utilizadas

* **Lenguaje:** Python 3.x
* **Librerías / Frameworks:** Streamlit
* **Empaquetado:** PyInstaller
* **Control de Versiones:** Git y GitHub
* **Entornos:** IDLE, CMD (Símbolo del sistema de Windows), Google Chrome

---

![Configuración del Adaptador de Red Puente](MarceloNoc.jpg)
## 🤝 Conclusión y Contacto

![GitHub Stats](https://github-readme-stats.anuraghazra1.vercel.app/api?username=MarceloNH-IT&show_icons=true&theme=radical)

![Top Languages](https://github-readme-stats.anuraghazra1.vercel.app/api/top-langs/?username=MarceloNH-IT&layout=compact&theme=radical)

![Streak Stats](https://github-readme-streak-stats.herokuapp.com/?user=MarceloNH-IT&theme=radical)

![Profile Views](https://visitor-badge.laobi.icu/badge?page_id=MarceloNH-IT.MarceloNH-IT&style=flat)

* **💼 LinkedIn**: [Horacio Marcelo Nuñez](https://linkedin.com) 
* **📬 Correo Electrónico**: [marcelonh86@gmail.com](marcelonh86@gmail.com)
* **🚀 GitHub**: [@MarceloNunez-NOC](https://github.com/MarceloNunez-NOC)

Agradezco el tiempo de quienes visitan mi portafolio en GitHub. Cada laboratorio refleja mi compromiso con el aprendizaje continuo y la práctica aplicada en IT, redes y administración de sistemas con programacion en python. Mi objetivo es demostrar que puedo diagnosticar, resolver y documentar incidentes de manera profesional, utilizando máquinas virtuales y configuraciones de red y programar de algo simple a cosas complejas. scrip de analisis y diagnostico como resolver incidentes si se me permite. 

Invito a reclutadores y colegas a seguir mis repositorios, donde iré compartiendo nuevos proyectos, certificados y logros. Estoy abierto a colaborar y aportar mi experiencia en entornos que valoren la constancia y la capacidad de resolver problemas.
