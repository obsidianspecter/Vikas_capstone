document.addEventListener('DOMContentLoaded', function() {
    // Handle theme form submissions with AJAX
    const themeForms = document.querySelectorAll('form[action="/set_theme"]');
    
    themeForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const themeId = this.querySelector('input[name="theme_id"]').value;
            const submitButton = this.querySelector('button[type="submit"]');
            
            // Disable the button during submission
            submitButton.disabled = true;
            submitButton.innerHTML = 'Applying...';
            
            fetch('/set_theme', {
                method: 'POST',
                body: new FormData(this),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Re-enable the button with success message
                    submitButton.innerHTML = 'Theme Applied!';
                    submitButton.classList.add('btn-success');
                    
                    // Reset button after 2 seconds
                    setTimeout(() => {
                        submitButton.disabled = false;
                        submitButton.innerHTML = 'Apply Theme';
                        submitButton.classList.remove('btn-success');
                    }, 2000);
                    
                    // Reload the page to apply the new theme
                    setTimeout(() => {
                        window.location.reload();
                    }, 500);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                submitButton.disabled = false;
                submitButton.innerHTML = 'Error - Try Again';
                submitButton.classList.add('btn-danger');
                
                setTimeout(() => {
                    submitButton.innerHTML = 'Apply Theme';
                    submitButton.classList.remove('btn-danger');
                }, 2000);
            });
        });
    });
    
    // Add hover effects for theme cards
    const themeCards = document.querySelectorAll('.card');
    themeCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 16px rgba(0,0,0,0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        });
    });
});