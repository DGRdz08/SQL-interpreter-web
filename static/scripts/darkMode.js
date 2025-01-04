    //------------------------------------------------
    // TOGGLE DARK MODE
    //------------------------------------------------
    const toggleDarkBtn = document.getElementById('toggleDarkMode');

    toggleDarkBtn.addEventListener('click', () => {
      // Alternar la clase 'dark-mode' en el body
      document.body.classList.toggle('dark-mode');
      
      // Verificar si el body tiene la clase 'dark-mode'
      if (document.body.classList.contains('dark-mode')) {
        // Está en modo oscuro => cambiar texto a "Modo Claro"
        toggleDarkBtn.textContent = 'Modo Claro';
      } else {
        // Está en modo claro => cambiar texto a "Modo Oscuro"
        toggleDarkBtn.textContent = 'Modo Oscuro';
      }
    });