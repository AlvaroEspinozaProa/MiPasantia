const preguntas = [

    { texto: "¿Te gusta leer libros de historia o filosofía?", area: "Humanidades" },
    { texto: "¿Disfrutás escribir textos o ensayos?", area: "Humanidades" },
    { texto: "¿Te interesa aprender idiomas?", area: "Humanidades" },
    { texto: "¿Te gusta analizar hechos históricos?", area: "Humanidades" },

    { texto: "¿Te interesa ayudar a resolver problemas sociales?", area: "Ciencias Sociales" },
    { texto: "¿Te gustaría estudiar Psicología?", area: "Ciencias Sociales" },
    { texto: "¿Te interesa el Derecho?", area: "Ciencias Sociales" },
    { texto: "¿Te gusta debatir temas de actualidad?", area: "Ciencias Sociales" },

    { texto: "¿Te gustaría trabajar en un hospital?", area: "Ciencias Médicas" },
    { texto: "¿Te interesa cuidar la salud de las personas?", area: "Ciencias Médicas" },
    { texto: "¿Te gusta la Biología?", area: "Ciencias Médicas" },
    { texto: "¿Te interesa investigar enfermedades?", area: "Ciencias Médicas" },

    { texto: "¿Disfrutás resolver problemas matemáticos?", area: "Ciencias Exactas" },
    { texto: "¿Te gusta la Física?", area: "Ciencias Exactas" },
    { texto: "¿Te interesa la Química?", area: "Ciencias Exactas" },
    { texto: "¿Te gusta realizar cálculos?", area: "Ciencias Exactas" },

    { texto: "¿Te gusta programar computadoras?", area: "Tecnología" },
    { texto: "¿Te interesan los avances tecnológicos?", area: "Tecnología" },
    { texto: "¿Te gustaría crear aplicaciones?", area: "Tecnología" },
    { texto: "¿Te gusta reparar computadoras?", area: "Tecnología" },

    { texto: "¿Te gustaría diseñar máquinas?", area: "Ingeniería" },
    { texto: "¿Te interesan los motores?", area: "Ingeniería" },
    { texto: "¿Te gusta construir cosas?", area: "Ingeniería" },
    { texto: "¿Te interesa la robótica?", area: "Ingeniería" },

    { texto: "¿Te gusta dibujar?", area: "Arte" },
    { texto: "¿Te interesa la música?", area: "Arte" },
    { texto: "¿Disfrutás la fotografía?", area: "Arte" },

    { texto: "¿Te gustan los animales?", area: "Ciencias Naturales" },
    { texto: "¿Te interesa cuidar el medio ambiente?", area: "Ciencias Naturales" },
    { texto: "¿Te gustaría trabajar en la naturaleza?", area: "Ciencias Naturales" }

];


let indice = 0;


let puntajes = {

    "Humanidades": 0,
    "Ciencias Sociales": 0,
    "Ciencias Médicas": 0,
    "Ciencias Exactas": 0,
    "Tecnología": 0,
    "Ingeniería": 0,
    "Arte": 0,
    "Ciencias Naturales": 0

};


const carreras = {

    "Humanidades": [
        "Historia",
        "Filosofía",
        "Letras"
    ],

    "Ciencias Sociales": [
        "Psicología",
        "Derecho",
        "Trabajo Social"
    ],

    "Ciencias Médicas": [
        "Medicina",
        "Enfermería",
        "Nutrición"
    ],

    "Ciencias Exactas": [
        "Matemática",
        "Física",
        "Química"
    ],

    "Tecnología": [
        "Programación",
        "Ingeniería en Sistemas",
        "Ciberseguridad"
    ],

    "Ingeniería": [
        "Ingeniería Mecánica",
        "Ingeniería Civil",
        "Ingeniería Industrial"
    ],

    "Arte": [
        "Diseño Gráfico",
        "Arquitectura",
        "Música"
    ],

    "Ciencias Naturales": [
        "Biología",
        "Veterinaria",
        "Agronomía"
    ]

};


/* =========================
      COMENZAR TEST
========================= */

function comenzarTest() {

    document.getElementById("avisoInicial").style.display = "none";

    document.getElementById("test").style.display = "block";

    indice = 0;

    mostrarPregunta();

}


/* =========================
      MOSTRAR PREGUNTA
========================= */

function mostrarPregunta() {

    document.getElementById("pregunta").innerHTML =
        preguntas[indice].texto;

    document.getElementById("contador").innerHTML =
        `Pregunta ${indice + 1} de ${preguntas.length}`;

    document.getElementById("barra").style.width =
        ((indice + 1) / preguntas.length) * 100 + "%";

}


/* =========================
        RESPONDER
========================= */

function responder(si) {

    if (si) {

        puntajes[preguntas[indice].area]++;

    }

    indice++;

    if (indice < preguntas.length) {

        mostrarPregunta();

    } else {

        mostrarResultado();

    }

}


/* =========================
       MOSTRAR RESULTADO
========================= */

function mostrarResultado() {

    document.getElementById("quiz").style.display = "none";

    document.getElementById("resultado").style.display = "block";


    let ranking = Object.entries(puntajes);


    ranking.sort(function (a, b) {

        return b[1] - a[1];

    });


    document.getElementById("primerLugar").innerHTML =
        ranking[0][0];

    document.getElementById("segundoLugar").innerHTML =
        ranking[1][0];

    document.getElementById("tercerLugar").innerHTML =
        ranking[2][0];


    document.getElementById("descripcion1").innerHTML =
        "Es el área que mejor coincide con tus intereses.";

    document.getElementById("descripcion2").innerHTML =
        "También presentás una buena afinidad.";

    document.getElementById("descripcion3").innerHTML =
        "Podría ser una opción interesante para tu futuro.";


    document.getElementById("barra1").style.width =
        (ranking[0][1] / 4) * 100 + "%";

    document.getElementById("barra2").style.width =
        (ranking[1][1] / 4) * 100 + "%";

    document.getElementById("barra3").style.width =
        (ranking[2][1] / 4) * 100 + "%";


    const lista = document.getElementById("listaCarreras");

    lista.innerHTML = "";


    carreras[ranking[0][0]].forEach(function (carrera) {

        lista.innerHTML += `<li>${carrera}</li>`;

    });

}