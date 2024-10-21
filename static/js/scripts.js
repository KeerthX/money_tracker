document.getElementById('investmentForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent default form submission behavior

    const formData = new FormData(this);

    fetch('/investments', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById('investmentTable');

            // Check if the table exists
            if (table) {
                const newRow = document.createElement('tr');
                newRow.innerHTML = `<td>${data.company}</td><td>${data.amount} INR</td><td>${data.units}</td><td>${data.class}</td>`;
                table.appendChild(newRow);

                // Reset form after successful submission
                this.reset();
            } else {
                console.error('Table element not found');
            }
        })
        .catch(error => console.error('Error:', error));
});
