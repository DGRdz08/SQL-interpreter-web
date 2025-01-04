    // --- Suscripción/Modal ---
    const form = document.querySelector('.subscribe-form');
    const modal = document.getElementById('modal');

    form.addEventListener('submit', (event) => {
      event.preventDefault(); // Evita recargar la página

      // Mostrar el modal
      modal.style.display = 'flex';

      // Ocultar el modal después de 1 segundo
      setTimeout(() => {
        modal.style.display = 'none';
        // Resetear el formulario si lo deseas:
        // form.reset();
      }, 1000);
    });
