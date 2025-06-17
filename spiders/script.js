document.getElementById('scrape-btn').addEventListener('click', function() {
    fetch('scrape.php', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById('message');
            if (data.status === 'success') {
                messageElement.style.color = 'green';
            } else {
                messageElement.style.color = 'red';
            }
            messageElement.textContent = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('message').textContent = 'An error occurred.';
        });
});
