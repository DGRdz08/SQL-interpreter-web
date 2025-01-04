    //------------------------------------------------
    // DESCARGAR PDF
    //------------------------------------------------
    const downloadBtn = document.getElementById("downloadBtn");
    downloadBtn.addEventListener("click", downloadPDF);

    async function downloadPDF() {
      let operation = sessionStorage.getItem("lastOperation") || "SELECT";
      let filename = sessionStorage.getItem("lastFilename") || "";
      const results = document.getElementById('results').innerText;

      const payload = (operation === "SELECT")
        ? { operation, results } 
        : { operation, filename };

      fetch('/query/download-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error("Error al generar PDF");
        }
        return response.blob();
      })
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'resultados.pdf';
        a.click();
        window.URL.revokeObjectURL(url);
      })
      .catch(err => {
        alert('Hubo un error al descargar el PDF.');
        console.error(err);
      });
    }