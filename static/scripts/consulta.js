    //------------------------------------------------
    // DRAG & DROP
    //------------------------------------------------
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');

    dropArea.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', handleFileUpload);

    async function handleFileUpload(e) {
      const file = e.target.files[0];
      if (!file) return;

      if (file.type !== "text/csv" && !file.name.endsWith(".csv")) {
        alert("Asegúrate de subir un archivo .CSV");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("/csv/upload", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();

        if (!response.ok) {
          alert(data.error || "Error al subir el archivo.");
          return;
        }

        document.getElementById("fileInfo").innerText = 
          `Archivo cargado: ${file.name}`;

        // Mostrar columnas
        if (data.columns && data.columns.length > 0) {
          document.getElementById("columnInfo").innerText = 
            "Columnas: " + data.columns.join(", ");
        } else {
          document.getElementById("columnInfo").innerText = "";
        }
      } catch (error) {
        alert("Error al comunicarse con el servidor.");
        console.error(error);
      }
    }

    //------------------------------------------------
    // ENVIAR QUERY
    //------------------------------------------------
    const sendQueryBtn = document.getElementById("sendQueryBtn");
    sendQueryBtn.addEventListener("click", executeQuery);

    async function executeQuery() {
      const query = document.getElementById("queryInput").value.trim();
      const fileInfo = document.getElementById("fileInfo").innerText;

      if (!query) {
        alert("Por favor ingresa un query.");
        return;
      }
      if (!fileInfo) {
        alert("No se ha cargado ningún archivo CSV.");
        return;
      }
      const filename = fileInfo.split(":")[1].trim(); 

      try {
        const response = await fetch("/query/execute", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query_text: query, filename }),
        });

        const data = await response.json();
        if (!response.ok) {
          alert(data.error || "Error al ejecutar el query.");
          return;
        }

        let resultContainer = document.getElementById("results");
        resultContainer.innerHTML = "";

        // Determinar tipo de operación (SELECT, INSERT, etc.)
        const operation = getQueryOperation(query);
        sessionStorage.setItem("lastOperation", operation);
        sessionStorage.setItem("lastFilename", filename);

        // data.data puede ser un array (SELECT) o un objeto con {message} (INSERT/UPDATE/DELETE)
        if (Array.isArray(data.data)) {
          // SELECT
          renderResultTable(data.data);
        } else if (data.data?.message) {
          // INSERT/UPDATE/DELETE
          resultContainer.innerText = data.data.message;
        } else {
          // Podría ser un objeto con {error}, etc.
          if (data.data?.error) {
            resultContainer.innerText = data.data.error;
          } else if (data.message !== "OK") {
            resultContainer.innerText = data.message;
          } else {
            // fallback
            resultContainer.innerText = JSON.stringify(data.data, null, 2);
          }
        }

        // Agregar a historial
        updateHistory(query);

      } catch (error) {
        alert("Error al comunicarse con el servidor.");
        console.error(error);
      }
    }

    function getQueryOperation(query) {
      const upper = query.toUpperCase().trim();
      if (upper.startsWith("SELECT")) return "SELECT";
      if (upper.startsWith("UPDATE")) return "UPDATE";
      if (upper.startsWith("DELETE")) return "DELETE";
      if (upper.startsWith("INSERT")) return "INSERT";
      return "OTRO";
    }

    function renderResultTable(rows) {
      if (rows.length === 0) {
        document.getElementById("results").innerText = "No hay registros";
        return;
      }

      let html = "<table><thead><tr>";
      const columns = Object.keys(rows[0]);
      columns.forEach(col => {
        html += `<th>${col}</th>`;
      });
      html += "</tr></thead><tbody>";

      rows.forEach(row => {
        html += "<tr>";
        columns.forEach(col => {
          html += `<td>${row[col] ?? ""}</td>`;
        });
        html += "</tr>";
      });

      html += "</tbody></table>";
      document.getElementById("results").innerHTML = html;
    }

    //------------------------------------------------
    // HISTORIAL
    //------------------------------------------------
    function updateHistory(query) {
      const historyBody = document.getElementById('historyBody');
      const timestamp = new Date().toLocaleString();

      if (historyBody.children.length === 1 && 
          historyBody.children[0].children[0].innerText === "No hay historial todavía") {
        historyBody.innerHTML = "";
      }

      const newRow = document.createElement("tr");
      newRow.innerHTML = `
        <td>${query}</td>
        <td>${timestamp}</td>
        <td><button onclick="copyQuery('${encodeURIComponent(query)}')">Copiar</button></td>
      `;
      historyBody.appendChild(newRow);
    }

    function copyQuery(encodedQuery) {
      const query = decodeURIComponent(encodedQuery);
      navigator.clipboard.writeText(query)
        .then(() => alert('Query copiado al portapapeles.'))
        .catch(err => console.error('Error al copiar:', err));
    }

    //------------------------------------------------
    // LOGOUT
    //------------------------------------------------
    async function logout() {
      fetch('/logout', { method: 'POST' })
        .then(() => {
          document.getElementById('fileInfo').innerHTML = '';
          document.getElementById('columnInfo').innerHTML = '';
          document.getElementById('results').innerHTML = '';
          const historyBody = document.getElementById('historyBody');
          historyBody.innerHTML = '<tr><td>No hay historial todavía</td><td></td><td></td></tr>';
          // Limpiar sessionStorage
          sessionStorage.removeItem("lastOperation");
          sessionStorage.removeItem("lastFilename");
          window.location.href = '/';
        })
        .catch(err => {
          alert('Error al cerrar sesión.');
          console.error(err);
        });
    }