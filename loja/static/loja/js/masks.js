// Aplica máscaras de entrada usando IMask (https://imask.js.org/).
// Inclua o IMask antes deste arquivo (ver base.html).
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".mask-telefone").forEach(function (el) {
    IMask(el, { mask: "(00) 0000-0000" });
  });

  document.querySelectorAll(".mask-celular").forEach(function (el) {
    IMask(el, { mask: "(00) 00000-0000" });
  });

  document.querySelectorAll(".mask-cpf").forEach(function (el) {
    IMask(el, { mask: "000.000.000-00" });
  });

  document.querySelectorAll(".mask-cnpj").forEach(function (el) {
    IMask(el, { mask: "00.000.000/0000-00" });
  });

  // Documento dinâmico: vira CPF até 11 dígitos e CNPJ a partir de 12.
  document.querySelectorAll(".mask-documento").forEach(function (el) {
    IMask(el, {
      mask: [
        { mask: "000.000.000-00", maxLength: 11 },
        { mask: "00.000.000/0000-00" },
      ],
      dispatch: function (appended, dynamicMasked) {
        var digitos = (dynamicMasked.value + appended).replace(/\D/g, "");
        return digitos.length > 11
          ? dynamicMasked.compiledMasks[1]
          : dynamicMasked.compiledMasks[0];
      },
    });
  });
});
