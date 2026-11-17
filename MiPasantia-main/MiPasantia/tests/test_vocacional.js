const assert = require("assert");
const fs = require("fs");
const vm = require("vm");
const path = require("path");

function elemento() {
    return {
        hidden: false, textContent: "", children: [],
        addEventListener(evento, callback) { this[evento] = callback; },
        append(...hijos) { this.children.push(...hijos); },
        replaceChildren() { this.children = []; },
        querySelector() { return elemento(); },
        setAttribute() {}, focus() {}
    };
}
const elementos = {};
const document = {
    getElementById(id) { return elementos[id] ||= elemento(); },
    createElement() { return elemento(); }
};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, "../static/js/test-vocacional.js"), "utf8"), {document});
for (let i = 0; i < 30; i++) elementos.no.click();
assert.equal(elementos.resultado.hidden, false);
assert.equal(elementos.ranking.children.length, 0);
assert.match(elementos.resumen.textContent, /No marcaste/);
elementos.reiniciar.click();
for (let i = 0; i < 30; i++) elementos.si.click();
assert.equal(elementos.ranking.children.length, 8);
assert.match(elementos.ranking.children[6].children[1].textContent, /3 de 3/);
elementos.reiniciar.click();
elementos.si.click();
for (let i = 1; i < 30; i++) elementos.no.click();
assert.equal(elementos.ranking.children.length, 1);
assert.equal(elementos.ranking.children[0].children[0].textContent, "Humanidades");
console.log("Test vocacional: sin intereses, empate, resultado único y reinicio OK");
