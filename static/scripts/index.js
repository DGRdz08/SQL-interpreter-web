    // Abrir y cerrar modales
    function openModal(id) {
        document.getElementById(id).classList.add('active');
      }
  
      function closeModal(id) {
        document.getElementById(id).classList.remove('active');
      }
  
      // Cambiar entre secciones de login y registro
      function showSection(section) {
        document.querySelectorAll('.modal-tab').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.modal-section').forEach(sec => sec.classList.remove('active'));
  
        document.getElementById(`tab-${section}`).classList.add('active');
        document.getElementById(section).classList.add('active');
      }
  