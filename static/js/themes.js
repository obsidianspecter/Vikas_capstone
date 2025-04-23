document.addEventListener('DOMContentLoaded', function() {
    // Theme application handling
    const themeModals = document.querySelectorAll('.modal');
    themeModals.forEach(modal => {
        const form = modal.querySelector('form');
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            submitButton.disabled = true;
            submitButton.textContent = 'Applying...';

            fetch(this.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    submitButton.textContent = 'Theme Applied!';
                    submitButton.classList.remove('btn-primary');
                    submitButton.classList.add('btn-success');
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    throw new Error(data.message || 'Failed to apply theme');
                }
            })
            .catch(error => {
                submitButton.disabled = false;
                submitButton.textContent = 'Error - Try Again';
                submitButton.classList.remove('btn-primary');
                submitButton.classList.add('btn-danger');
                console.error('Theme application error:', error);
                
                setTimeout(() => {
                    submitButton.textContent = originalText;
                    submitButton.classList.remove('btn-danger');
                    submitButton.classList.add('btn-primary');
                }, 2000);
            });
        });
    });

    // Category filtering
    const filterButtons = document.querySelectorAll('.filter-btn');
    const themeCards = document.querySelectorAll('.theme-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const category = button.dataset.category;
            
            // Update active state
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Filter themes with animation
            themeCards.forEach(card => {
                card.style.opacity = '0';
                card.style.transform = 'scale(0.95)';
                
                setTimeout(() => {
                    if (category === 'all' || card.dataset.category === category) {
                        card.style.display = 'block';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'scale(1)';
                        }, 50);
                    } else {
                        card.style.display = 'none';
                    }
                }, 200);
            });
        });
    });

    // Initialize tooltips if Bootstrap is present
    if (typeof bootstrap !== 'undefined') {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
    }
}); 