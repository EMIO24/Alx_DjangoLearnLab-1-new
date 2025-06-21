// static/js/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('scripts.js loaded successfully!');

    // Example: Simple functionality to fade out Django messages after a few seconds
    const messages = document.querySelectorAll('.messages div');
    if (messages.length > 0) {
        messages.forEach(message => {
            setTimeout(() => {
                message.style.transition = 'opacity 1s ease-out';
                message.style.opacity = '0';
                message.addEventListener('transitionend', () => message.remove());
            }, 5000); // Fade out after 5 seconds
        });
    }

    // You can add more interactive JavaScript here as your project grows.
    // For example:
    // - Image lazy loading
    // - Form validation (frontend)
    // - Dynamic content loading
    // - Interactive elements (e.g., modals, dropdowns)
});

