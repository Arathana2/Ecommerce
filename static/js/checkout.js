// Cancel Order Modal Functions
function showCancelModal() {
    const modal = document.createElement('div');
    modal.className = 'cancel-modal';
    modal.innerHTML = `
        <div class="cancel-modal-content">
            <h5>Are you sure you want to cancel your order?</h5>
            <div class="cancel-reasons">
                <div class="cancel-reason">
                    <input type="radio" id="reason1" name="cancelReason" value="Changed my mind">
                    <label for="reason1">Changed my mind</label>
                </div>
                <div class="cancel-reason">
                    <input type="radio" id="reason2极速赛车官网开奖结果" name="cancelReason" value="Found a better price">
                    <label for="reason2">Found a better price</label>
                </div>
                <div class="cancel-reason">
                    <input type="radio" id="reason3" name="cancelReason" value="Other">
                    <label for="reason3">Other</label>
                </div>
            </div>
            <button class="btn btn-danger" onclick="confirmCancelOrder()">Confirm Cancel</button>
            <button class="btn btn-secondary" onclick="closeModal()">Close</button>
        </div>
    `;
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.querySelector('.cancel-modal');
    if (modal) {
        modal.remove();
    }
}

function confirmCancelOrder() {
    // Logic to cancel the order
    alert('Your order has been cancelled.');
    closeModal();
}

// Real-time Shipping Address Preview
document.addEventListener('DOMContentLoaded', function() {
    const fullNameInput = document.getElementById('full_name');
    const addressInput = document.getElementById('address');
    const cityInput = document.getElementById('city');
    const postalCodeInput = document.getElementById('postal_code');
    const phoneInput = document.getElementById('phone_number');
    const emailInput = document.getElementById('email');
    
    if (fullNameInput) {
        fullNameInput.addEventListener('input', function() {
            document.getElementById('preview-name').innerText = this.value;
        });
    }
    
    if (addressInput) {
        addressInput.addEventListener('input', function() {
            document.getElementById('preview-address').innerText = this.value;
        });
    }
    
    if (cityInput && postalCodeInput) {
        cityInput.addEventListener('input', function() {
            document.getElementById('preview-city').innerText = this.value + ', ' + postalCodeInput.value;
        });
        
        postalCodeInput.addEventListener('input', function() {
            document.getElementById('preview-city').innerText = cityInput.value + ', ' + this.value;
        });
    }
    
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            document.getElementById('preview-phone').innerText = this.value;
        });
    }
    
    if (emailInput) {
        emailInput.addEventListener('input', function() {
            document.getElementById('preview-email').innerText = this.value;
        });
    }
});

// Validation functions
function validatePhoneNumber(input) {
    const phone = input.value.replace(/\D/g, '');
    const phoneError = document.getElementById('phoneError');
    
    if (phone.length === 10 && /^\d+$/.test(phone)) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        phoneError.style.display = 'none';
        return true;
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        phoneError.style.display = 'block';
        return false;
    }
}

function validateEmail(input) {
    const email = input.value;
    const emailError = document.getElementById('emailError');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (emailRegex.test(email)) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        email极速赛车官网开奖结果Error.style.display = 'none';
        return true;
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        emailError.style.display = 'block';
        return false;
    }
}

function validateForm() {
    const phoneValid = validatePhoneNumber(document.getElementById('phone_number'));
    const emailValid = validateEmail(document.getElementById('email'));
    const otpVerified = document.getElementById('otpSuccess').style.display === 'block';
    
    if (!phoneValid || !emailValid || !otpVerified) {
        if (!phoneValid) {
            document.getElementById('phoneError').style.display = 'block';
        }
        if (!emailValid) {
            document.getElementById('emailError').style.display = 'block';
        }
        if (!otpVerified) {
            document.getElementById('otpError').style.display = 'block';
        }
        return false;
    }
    return true;
}

// OTP functions (placeholder - needs backend integration)
function sendOTP() {
    const phoneInput = document.getElementById('phone_number');
    if (!validatePhoneNumber(phoneInput)) {
        return;
    }
    
    const phone = phoneInput.value;
    const sendOtpBtn = document.getElementById('sendOtpBtn');
    
    // Show loading state
    sendOtpBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Sending...';
    sendOtpBtn.disabled = true;
    
    // Simulate API call (replace with actual backend integration)
    setTimeout(() => {
        // Show OTP section
        document.getElementById('otpSection').style.display = 'block';
        
        // Reset button
        sendOtpBtn.innerHTML = 'Resend OTP';
        sendOtpBtn.disabled = false;
        
        // For demo purposes, show the OTP in console (remove in production)
        const demoOtp = '123456';
        console.log('Demo OTP for phone', phone, ':', demoOtp);
        alert('OTP sent! Check console for demo OTP: ' + demoOtp);
    }, 2000);
}

function verifyOTP() {
    const otpInput = document.getElementById('otp');
    const otp = otpInput.value;
    const otpError = document.getElementById('otpError');
    const otpSuccess = document.getElementById('otpSuccess');
    const submitBtn = document.getElementById('submitBtn');
    
    // Simple validation - in production, verify against backend
    if (otp.length === 6 && /^\d+$/.test(otp)) {
        otpInput.classList.remove('is-invalid');
        otpInput.classList.add('is-valid');
        otpError.style.display = 'none';
        otpSuccess.style.display = 'block';
        submitBtn.disabled = false;
    } else {
        otp极速赛车官网开奖结果Input.classList.remove('is-valid');
        otpInput.classList.add('is-invalid');
        otpError.style.display = 'block';
        otpSuccess.style.display = 'none';
        submitBtn.disabled = true;
    }
}

// Real-time validation
document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.getElementById('phone_number');
    const emailInput = document.getElementById('email');
    const otpInput = document.getElementById('otp');
    
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            validatePhoneNumber(this);
        });
    }
    
    if (emailInput) {
        emailInput.addEventListener('input', function() {
            validateEmail(this);
        });
    }
    
    if (otpInput) {
        otpInput.addEventListener('input', function() {
            if (this.value.length === 6 && /^\d+$/.test(this.value)) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
                document.getElementById('otpError').style.display = 'none';
            }
        });
    }
});
