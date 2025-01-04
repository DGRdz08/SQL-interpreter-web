    // Iniciar sesión
    async function loginUser(event, userType) {
        event.preventDefault();
        const username = document.getElementById(`${userType}-username`).value;
        const password = document.getElementById(`${userType}-password`).value;
  
        const resp = await fetch('/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password, user_type: userType })
        });
        const data = await resp.json();
  
        if (data.redirect) {
          window.location.href = data.redirect;
        } else {
          alert(data.error || "Error al iniciar sesión");
        }
      }

    // Registrar usuario
    async function registerUser(event) {
        event.preventDefault();
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
  
        const resp = await fetch('/auth/register/client', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, email, password })
        });
        const data = await resp.json();
  
        if (data.redirect) {
          window.location.href = data.redirect;
        } else {
          alert(data.error || "Error al registrarse");
        }
      }

      // Cerrar sesión
      async function logout() {
        try {
          const response = await fetch('/auth/logout', { method: 'POST' });
          const data = await response.json();
      
          if (data.redirect) {
            window.location.href = data.redirect; // Redirige a la página de inicio
          } else {
            alert(data.error || "Error al cerrar sesión.");
          }
        } catch (error) {
          alert("Error al cerrar sesión.");
          console.error(error);
        }
      }