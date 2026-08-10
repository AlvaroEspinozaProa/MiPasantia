# Guía de Trabajo - Future Hub:

Hola equipo. Estuve mirando el código de su proyecto (la base de datos, el app.py y los HTML). 

Primero que nada, los felicito. El nivel que tienen en el Backend es excelente. Haber logrado configurar la base de datos, manejar usuarios, encriptar contraseñas y hacer consultas con JOIN en Python es un montón para esta altura del año. Tremendo laburo.

¿Dónde estamos trabados ahora? Tenemos un cortocircuito entre el cerebro (Python) y la cara de la página (el HTML). Python está yendo a buscar los datos a la base de datos perfecto, pero el archivo index.html lo está ignorando y sigue mostrando esas tarjetas de prueba que escribieron a mano. 

Para destrabar esto, vamos a usar las etiquetas dinámicas de Flask (Jinja2). Les dejo esta guía para que se dividan en dos equipos y lo vayan sacando.

### Equipo 1: La Vidriera Real (Bucle Automático)
Vamos a hacer que la página de inicio muestre las publicaciones reales de la base de datos.

1. Abran el archivo index.html y busquen la parte donde están las tarjetas de prueba.
2. Borren casi todas las tarjetas y dejen solo una como si fuera un "molde".
3. A ese molde lo van a envolver en un bucle de Python directamente en el HTML. Pongan {% for exp in experiencias %} justo arriba del molde, y {% endfor %} justo abajo.
4. Adentro de la tarjeta, borren los textos fijos (ej. "Juan Pérez") y cámbienlos por las variables que vienen de Python. Se escribe así: {{ exp['autor'] }}, {{ exp['titulo'] }}, etc. 

### Equipo 2: Menú de Navegación Inteligente
Si un usuario ya inició sesión y está navegando por la página, no tiene sentido que arriba a la derecha le siga apareciendo el botón de "Iniciar sesión". El menú tiene que darse cuenta de quién está conectado.

1. Vayan al menú de navegación (<nav>) en sus archivos HTML.
2. Vamos a usar un condicional. Pongan esto: {% if session.get('usuario_id') %}.
3. Lo que pongan adentro de ese if, solo lo van a ver los usuarios logueados. Ahí deberían poner un botón para "Publicar", otro de "Mi Perfil" y uno para "Cerrar sesión".
4. Después pongan un {% else %}. Adentro de este, dejen los botones de "Iniciar Sesión" y "Registrarse" (para los visitantes que no entraron a su cuenta).
5. Cierren todo con un {% endif %}.

### Objetivo de esta etapa
El código de Python ya lo tienen impecable, así que no hace falta tocarlo. Concéntrense 100% en el HTML. El objetivo es que cuando apliquen esto, podamos entrar con un usuario de prueba, escribir una publicación nueva, darle a enviar, y ver que aparece solita en la página principal. 

Si Jinja les tira algún error raro en la consola, me dicen y lo miramos en la compu.