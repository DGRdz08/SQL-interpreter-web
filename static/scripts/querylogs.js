fetch('/admin/logs')
.then(response => response.json())
.then(data => {
  const tableBody = document.getElementById('logTable');
  tableBody.innerHTML = '';
  data.forEach(log => {
    const row = `
      <tr>
        <td>${log.id}</td>
        <td>${log.user_type}</td>
        <td>${log.user_id}</td>
        <td>${log.query_text}</td>
        <td>${log.url}</td>
        <td>${log.ip}</td>
        <td>${log.browser}</td>
        <td>${log.so}</td>
        <td>${log.timestamp}</td>
      </tr>`;
    tableBody.innerHTML += row;
  });
});