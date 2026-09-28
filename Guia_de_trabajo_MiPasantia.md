# Guía de trabajo para MiPasantia

MiPasantia no necesita muchas secciones para demostrar que hubo trabajo. Necesita un recorrido claro: una persona entra, entiende para qué sirve, explora experiencias y, si crea una cuenta, puede compartir la propia.

Esta guía propone una base profesional, no una receta cerrada. Si una función no aporta, se puede sacar; si aparece una idea buena y el equipo puede sostenerla, se puede sumar. Lo importante es no construir todo junto ni dejar funciones a medio camino.

## Antes de escribir código

En una hoja corta, definan:

- Qué problema resuelve MiPasantia para un estudiante.
- Qué puede hacer una visita y qué cambia cuando inicia sesión.
- Cuáles serán las tres secciones imprescindibles de la presentación.
- Qué datos tendrá una experiencia: título, empresa, área, fecha, autor y relato.

No hace falta elegir el diseño final todavía. Sí conviene acordar una paleta, una tipografía y un tono antes de repetir decisiones distintas en cada página.

## Etapa 1: preparar una base que no se rompa

Flask y SQLite alcanzan para este proyecto. Una estructura saludable separa la aplicación, las plantillas y los recursos visuales:

    mipasantia/
    ├── app.py
    ├── requirements.txt
    ├── .env
    ├── database.db
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── explorar.html
    │   └── publicar.html
    └── static/
        ├── css/
        ├── js/
        └── img/

Checklist:

- [ ] Hay un único archivo principal de Flask que se puede ejecutar.
- [ ] Las plantillas están en la carpeta templates.
- [ ] Estilos, scripts e imágenes están en static.
- [ ] Existe un archivo requirements.txt con las bibliotecas necesarias.
- [ ] Existe un archivo .gitignore que ignore .env, __pycache__ y archivos locales que no deban compartirse.
- [ ] Cualquier integrante puede abrir la aplicación siguiendo instrucciones breves.

**Está listo cuando:** alguien que no programó esa parte puede clonar el repositorio, instalar dependencias y abrir la portada.

## Etapa 2: diseñar el recorrido antes de sumar pantallas

Primero hagan funcionar lo mínimo:

1. Una visita ve la portada y explora experiencias.
2. Una visita se registra e inicia sesión.
3. Un usuario identificado publica una experiencia.
4. La experiencia aparece en el listado.
5. Al abrirla, se ve el contenido completo.

Después pueden sumar búsqueda, filtros, perfil u otras ideas.

Checklist:

- [ ] La portada muestra publicaciones reales de la base, no tarjetas escritas a mano.
- [ ] El menú cambia cuando hay una sesión iniciada.
- [ ] Cada tarjeta lleva al detalle correcto usando su identificador.
- [ ] Publicar requiere una sesión.
- [ ] Después de una acción importante aparece un mensaje claro.
- [ ] No hay enlaces ni botones que lleven a una pantalla inexistente.

**Error frecuente:** hacer varios HTML que se ven bien por separado, pero no están conectados. En Flask, los enlaces y formularios deben usar rutas de la aplicación y, cuando corresponda, url_for.

## Etapa 3: datos y seguridad con sentido

SQLite es suficiente si se usa con orden. Una experiencia debería estar asociada a un usuario y, si usan categorías, a una categoría.

Checklist:

- [ ] Las tablas tienen una responsabilidad clara: usuarios, experiencias y categorías si son necesarias.
- [ ] Las consultas SQL reciben valores por parámetros; nunca se arma SQL pegando texto de un formulario.
- [ ] El correo es único.
- [ ] Las contraseñas se guardan usando un **hash** de Werkzeug. No se guardan como texto ni hace falta inventar una encriptación propia.
- [ ] La clave secreta se lee desde una variable de entorno o .env, no queda escrita en el código compartido.
- [ ] Los campos obligatorios se validan también en Python.
- [ ] Si no existe una publicación o alguien intenta entrar a una página privada, el sitio responde con un mensaje entendible.

No hace falta transformar el trabajo en un sistema bancario. Sí deben poder explicar por qué una contraseña no se guarda tal cual y por qué una consulta parametrizada evita errores y problemas de seguridad.

## Etapa 4: interfaz consistente y adaptable

La creatividad es libre, pero las decisiones tienen que repetirse. Una página no debería parecer de otro proyecto.

Punto de partida posible:

- Azul oscuro para identidad y navegación: #243B53.
- Azul para acciones principales: #2F80ED.
- Fondo claro, textos oscuros y contraste suficiente.
- Una sola familia tipográfica, como Poppins.
- Tarjetas para experiencias, chips para categorías y espacios amplios entre secciones.

Checklist:

- [ ] La navegación nace de una plantilla base y se repite igual.
- [ ] Botones, campos y tarjetas comparten estilo.
- [ ] Cada campo tiene una etiqueta visible.
- [ ] Hay señal visual al pasar, enfocar o presionar un botón.
- [ ] Las pantallas chicas no rompen menú, tarjetas ni formularios.
- [ ] Cuando no hay resultados, la página explica qué pasó y ofrece una salida.
- [ ] El contenido se entiende sin depender solamente de colores o imágenes.

**Prueba rápida:** reduzcan la ventana al ancho de un celular y recorran todo el flujo. Si hay texto cortado, botones fuera de pantalla o formularios incómodos, todavía no está terminado.

## Etapa 5: búsqueda y filtros

Una vez estable el recorrido principal, agreguen exploración. Es una mejora concreta: ayuda a encontrar experiencias por área, empresa o tema.

Pueden resolverlo desde Flask con parámetros en la URL. JavaScript puede acompañar pequeñas interacciones visuales, pero el resultado importante debe sobrevivir a una recarga de página.

Checklist:

- [ ] Se puede buscar por una palabra relevante.
- [ ] Se puede filtrar por categoría; empresa es una ampliación útil.
- [ ] Buscar y filtrar al mismo tiempo no pierde resultados.
- [ ] Se entiende qué filtros están activos.
- [ ] Hay una forma visible de limpiar filtros.
- [ ] Se prueba sin publicaciones, con una, con varias y sin coincidencias.

## Etapa 6: revisar como si fuera ajeno

Antes de presentar, otra persona debería recorrer el sitio sin indicaciones. Anoten dónde pregunta qué hacer o dónde algo no se entiende. Ese registro vale más que sumar una pantalla nueva a último momento.

Checklist final:

- [ ] Registro, inicio y cierre de sesión funcionan.
- [ ] Se pueden crear y ver publicaciones.
- [ ] El detalle corresponde a la tarjeta elegida.
- [ ] Navegación, formularios y mensajes fueron probados.
- [ ] El sitio se ve bien en celular y escritorio.
- [ ] No hay datos confusos, rutas rotas ni botones sin acción.
- [ ] El equipo sabe explicar una decisión visual y una técnica.

## Usar IA sin entregar el control del proyecto

La IA sirve mucho si se usa como ayuda puntual. El problema aparece cuando se pide una web completa, se copia una respuesta enorme y después nadie sabe dónde ponerla ni qué rompió.

Una forma de trabajar que da mejores resultados:

1. Expliquen qué archivo están tocando, qué ya funciona y qué quieren cambiar.
2. Pidan una tarea concreta: una ruta, una consulta, un formulario o una mejora visual.
3. Lean la respuesta antes de pegarla. Si algo no se entiende, pregunten por esa línea.
4. Integren de a poco y prueben el recorrido completo después de cada cambio.
5. Dejen una nota corta en el commit o en un seguimiento: qué hicieron, qué falló y cómo lo resolvieron.

También pueden usarla para revisar: preguntar qué casos faltan en un formulario, por qué una ruta falla o cómo adaptar un estilo a celular. Eso ayuda a pensar, no solamente a producir código.

## Opciones para ampliar, no obligaciones

Elijan una o dos solo si el núcleo funciona y hay tiempo para probarlas:

- Guardar experiencias favoritas.
- Perfil con publicaciones de cada usuario.
- Foro de consultas con moderación básica.
- Panel simple de publicaciones por categoría.
- Directorio de empresas u organizaciones.
- Test de intereses con resultado explicativo.
- Reporte de una publicación inapropiada.
- Borrador antes de publicar.

Cada ampliación debe responder tres preguntas: qué problema resuelve, qué datos necesita y cómo comprobarán que funciona.

## Para la presentación

No memoricen definiciones. Organicen una demostración corta:

1. El problema y para quién pensaron MiPasantia.
2. El recorrido de una visita y de un usuario registrado.
3. Una publicación de prueba desde el formulario hasta el listado.
4. Una decisión técnica que aprendieron a resolver.
5. Una mejora que dejarían para la próxima versión.

Mostrar un problema resuelto con claridad vale más que intentar demostrar diez funciones sin terminar.
