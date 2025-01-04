    // --- Menú Desplegable por clic ---
    const profileButton = document.getElementById('profileButton');
    const dropdownMenu = document.getElementById('dropdownMenu');

    // Variable para saber si el menú está abierto o cerrado
    let menuVisible = false;

    // Al hacer clic en "Usuario"
    profileButton.addEventListener('click', () => {
      menuVisible = !menuVisible; // Toggle: cambia true <-> false
      dropdownMenu.style.display = menuVisible ? 'block' : 'none';
    });

    // Si quieres cerrar el menú al hacer clic en cualquier parte fuera de él:
    document.addEventListener('click', (event) => {
      // Verifica que el clic NO sea dentro de 'profileButton' ni de 'dropdownMenu'
      if (
        !profileButton.contains(event.target) &&
        !dropdownMenu.contains(event.target)
      ) {
        dropdownMenu.style.display = 'none';
        menuVisible = false;
      }
    });
    
    async function checkSession() {
      try {
          const response = await fetch('/auth/session', { method: 'GET' });
          if (!response.ok) {
              window.location.href = '/';
          }
      } catch (err) {
          console.error('Error al verificar la sesión:', err);
          window.location.href = '/';
      }
  }
  
  // Llama a esta función al cargar la página de consulta
  checkSession();
  
  async function loadLogs() {
    try {
      const response = await fetch('/admin/logs', {
        method: 'GET',
        credentials: 'include'
      });
      const data = await response.json();
      const logs = document.getElementById('logs');
      data.forEach(log => {
        const li = document.createElement('li');
        li.textContent = log;
        logs.appendChild(li);
      });
    } catch (err) {
      console.error('Error al obtener los registros:', err);
    }
  }
  loadLogs();
  
  