// Authentication JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Form validation for registration
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            const email = document.getElementById('email').value;
            let isValid = true;
            
            // Reset error messages
            document.querySelectorAll('.is-invalid').forEach(el => {
                el.classList.remove('is-invalid');
            });
            
            // Email validation
            if (!validateEmail(email)) {
                document.getElementById('email').classList.add('is-invalid');
                isValid = false;
            }
            
            // Password validation
            if (password.length < 8) {
                document.getElementById('password').classList.add('is-invalid');
                isValid = false;
            }
            
            // Password match validation
            if (password !== confirmPassword) {
                document.getElementById('confirm_password').classList.add('is-invalid');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
    
    // OTP input handling
    const otpInputs = document.querySelectorAll('.otp-input');
    if (otpInputs.length > 0) {
        otpInputs.forEach((input, index) => {
            input.addEventListener('input', function() {
                if (this.value.length === this.maxLength) {
                    // Move to next input
                    if (index < otpInputs.length - 1) {
                        otpInputs[index + 1].focus();
                    }
                }
            });
            
            // Handle backspace
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Backspace' && this.value.length === 0 && index > 0) {
                    otpInputs[index - 1].focus();
                }
            });
        });
    }
    
    // Function to validate email format
    function validateEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }
    
    // Resend OTP functionality
    const resendOTPButton = document.getElementById('resend-otp');
    if (resendOTPButton) {
        resendOTPButton.addEventListener('click', function(e) {
            e.preventDefault();
            this.disabled = true;
            
            // Get email and purpose from data attributes
            const email = this.getAttribute('data-email');
            const purpose = this.getAttribute('data-purpose');
            
            // Send AJAX request to resend OTP
            fetch('/users/resend-otp/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ email, purpose })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showMessage('OTP has been resent to your email', 'success');
                    
                    // Disable button for 30 seconds
                    let countdown = 30;
                    this.textContent = `Resend OTP (${countdown}s)`;
                    
                    const timer = setInterval(() => {
                        countdown--;
                        this.textContent = `Resend OTP (${countdown}s)`;
                        
                        if (countdown <= 0) {
                            clearInterval(timer);
                            this.textContent = 'Resend OTP';
                            this.disabled = false;
                        }
                    }, 1000);
                } else {
                    showMessage(data.message || 'Failed to resend OTP', 'danger');
                    this.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('An error occurred while resending OTP', 'danger');
                this.disabled = false;
            });
        });
    }
    
    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Function to show message
    function showMessage(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        const messageContainer = document.getElementById('message-container');
        if (messageContainer) {
            messageContainer.appendChild(alertDiv);
            
            // Auto dismiss after 5 seconds
            setTimeout(() => {
                alertDiv.classList.remove('show');
                setTimeout(() => {
                    alertDiv.remove();
                }, 300);
            }, 5000);
        }
    }
});