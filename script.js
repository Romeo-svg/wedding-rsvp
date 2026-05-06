document.getElementById('rsvpForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const name = document.getElementById('guestName').value;
    const email = document.getElementById('guestEmail').value;
    const status = document.getElementById('statusMessage');
    
    status.innerText = "Sending your RSVP...";

    // Pointing to your LIVE Render URL instead of localhost[cite: 2]
    fetch('https://wedding-rsvp-py.onrender.com/submit-rsvp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            name: name, 
            email: email 
        }),
    })
    .then(response => response.json())
    .then(data => {
        status.innerText = data.message;
        if(data.status === "success") {
            document.getElementById('rsvpForm').reset();
        }
    })
    .catch((error) => {
        status.innerText = "Error: Could not connect to the server!";
        console.error('Fetch error:', error);
    });
});
