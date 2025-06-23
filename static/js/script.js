document.getElementById('table-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const table = document.querySelector('form table');
    const rows = table.querySelectorAll('tr');
    const data = [];


    // main logic for extracting table from html
    for (let i = 2; i < rows.length; i++) {  // skip header rows
        const cells = rows[i].querySelectorAll('td');
        if (cells.length === 0) continue;

        const rowLabel = cells[0].innerText.trim();
        const rowData = { label: rowLabel };

        for (let j = 1; j < cells.length; j++) {
            const input = cells[j].querySelector('input');
            if (input) {
                rowData[`col${j}`] = input.value;
            }
        }

        data.push(rowData);
    }

    fetch('/submit-table', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ table: data })
    })
    .then(response => response.text())
    .then(message => {
        alert(message);
    })
    .catch(error => console.error('Error:', error));
});
