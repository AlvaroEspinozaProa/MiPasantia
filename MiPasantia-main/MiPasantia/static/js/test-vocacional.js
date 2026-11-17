// Preguntas y carreras recuperadas del test original de MiPasantia.
const areas = {
    "Humanidades": ["Historia", "Filosofía", "Letras"],
    "Ciencias Sociales": ["Psicología", "Derecho", "Trabajo Social"],
    "Ciencias Médicas": ["Medicina", "Enfermería", "Nutrición"],
    "Ciencias Exactas": ["Matemática", "Física", "Química"],
    "Tecnología": ["Programación", "Ingeniería en Sistemas", "Ciberseguridad"],
    "Ingeniería": ["Ingeniería Mecánica", "Ingeniería Civil", "Ingeniería Industrial"],
    "Arte": ["Diseño Gráfico", "Arquitectura", "Música"],
    "Ciencias Naturales": ["Biología", "Veterinaria", "Agronomía"]
};

const preguntas = [
    ["¿Te gusta leer libros de historia o filosofía?", "Humanidades"],
    ["¿Disfrutás escribir textos o ensayos?", "Humanidades"],
    ["¿Te interesa aprender idiomas?", "Humanidades"],
    ["¿Te gusta analizar hechos históricos?", "Humanidades"],
    ["¿Te interesa ayudar a resolver problemas sociales?", "Ciencias Sociales"],
    ["¿Te gustaría estudiar Psicología?", "Ciencias Sociales"],
    ["¿Te interesa el Derecho?", "Ciencias Sociales"],
    ["¿Te gusta debatir temas de actualidad?", "Ciencias Sociales"],
    ["¿Te gustaría trabajar en un hospital?", "Ciencias Médicas"],
    ["¿Te interesa cuidar la salud de las personas?", "Ciencias Médicas"],
    ["¿Te gusta la Biología?", "Ciencias Médicas"],
    ["¿Te interesa investigar enfermedades?", "Ciencias Médicas"],
    ["¿Disfrutás resolver problemas matemáticos?", "Ciencias Exactas"],
    ["¿Te gusta la Física?", "Ciencias Exactas"],
    ["¿Te interesa la Química?", "Ciencias Exactas"],
    ["¿Te gusta realizar cálculos?", "Ciencias Exactas"],
    ["¿Te gusta programar computadoras?", "Tecnología"],
    ["¿Te interesan los avances tecnológicos?", "Tecnología"],
    ["¿Te gustaría crear aplicaciones?", "Tecnología"],
    ["¿Te gusta reparar computadoras?", "Tecnología"],
    ["¿Te gustaría diseñar máquinas?", "Ingeniería"],
    ["¿Te interesan los motores?", "Ingeniería"],
    ["¿Te gusta construir cosas?", "Ingeniería"],
    ["¿Te interesa la robótica?", "Ingeniería"],
    ["¿Te gusta dibujar?", "Arte"],
    ["¿Te interesa la música?", "Arte"],
    ["¿Disfrutás la fotografía?", "Arte"],
    ["¿Te gustan los animales?", "Ciencias Naturales"],
    ["¿Te interesa cuidar el medio ambiente?", "Ciencias Naturales"],
    ["¿Te gustaría trabajar en la naturaleza?", "Ciencias Naturales"]
];

const quiz = document.getElementById("quiz");
const resultado = document.getElementById("resultado");
const pregunta = document.getElementById("pregunta");
let indice = 0;
let puntajes = {};

function mostrarPregunta() {
    pregunta.textContent = preguntas[indice][0];
    document.getElementById("contador").textContent = `Pregunta ${indice + 1} de ${preguntas.length}`;
    document.getElementById("porcentaje").textContent = `${Math.round(indice / preguntas.length * 100)}% completado`;
    document.getElementById("progreso").value = indice;
    pregunta.focus();
}

function mostrarResultado() {
    const ranking = Object.keys(areas).map(area => {
        const total = preguntas.filter(p => p[1] === area).length;
        return {area, puntos: puntajes[area], total, proporcion: puntajes[area] / total};
    }).filter(item => item.puntos > 0).sort((a, b) => b.proporcion - a.proporcion);
    const lista = document.getElementById("ranking");
    lista.replaceChildren();
    document.getElementById("resumen").textContent = ranking.length
        ? "Estas áreas reunieron más respuestas positivas. Si hay empates, mostramos todas las áreas empatadas."
        : "No marcaste intereses positivos esta vez. Podés repetir el test o explorar experiencias para conocer otras opciones.";
    ranking.filter((item, i) => i < 3 || item.proporcion === ranking[2].proporcion).forEach(item => {
        const card = document.createElement("article");
        card.className = "card";
        const titulo = document.createElement("h3");
        titulo.textContent = item.area;
        const detalle = document.createElement("p");
        detalle.textContent = `${item.puntos} de ${item.total} respuestas positivas · Ejemplos: ${areas[item.area].join(", ")}`;
        card.append(titulo, detalle);
        lista.append(card);
    });
    quiz.hidden = true;
    resultado.hidden = false;
    resultado.querySelector("h2").setAttribute("tabindex", "-1");
    resultado.querySelector("h2").focus();
}

function responder(si) {
    if (si) puntajes[preguntas[indice][1]]++;
    indice++;
    if (indice < preguntas.length) mostrarPregunta();
    else mostrarResultado();
}

function reiniciar() {
    indice = 0;
    puntajes = Object.fromEntries(Object.keys(areas).map(area => [area, 0]));
    resultado.hidden = true;
    quiz.hidden = false;
    mostrarPregunta();
}

document.getElementById("si").addEventListener("click", () => responder(true));
document.getElementById("no").addEventListener("click", () => responder(false));
document.getElementById("reiniciar").addEventListener("click", reiniciar);
reiniciar();
