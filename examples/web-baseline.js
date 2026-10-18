const form = document.getElementById('profile-form');
const submitBtn = document.getElementById('submit-btn');
const btnIcon = document.getElementById('btn-icon');
const btnText = document.getElementById('btn-text');
const emailInput = document.getElementById('email');
const emailError = document.getElementById('email-error');

emailInput.addEventListener('invalid', (e) => {
    e.preventDefault();
    emailInput.setAttribute('aria-invalid', 'true');
    emailError.textContent = 'Please provide a valid email format.';
    emailError.style.display = 'block';
});

emailInput.addEventListener('input', () => {
    emailInput.removeAttribute('aria-invalid');
    emailError.textContent = '';
    emailError.style.display = 'none';
});

// 🛡️ Sentinel: Clone original children to avoid innerHTML XSS risks
// ⚡ Bolt: No need to deep clone nodes, keeping the references is sufficient and faster
const originalIconNodes = Array.from(btnIcon.childNodes);
const originalText = btnText.textContent;

// 🛡️ Sentinel: Create SVG elements securely using DOM API
const spinnerCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
spinnerCircle.setAttribute('cx', '12');
spinnerCircle.setAttribute('cy', '12');
spinnerCircle.setAttribute('r', '10');
spinnerCircle.setAttribute('stroke', 'currentColor');
spinnerCircle.setAttribute('stroke-width', '4');
spinnerCircle.setAttribute('fill', 'none');
spinnerCircle.setAttribute('stroke-dasharray', '31.4 31.4');
spinnerCircle.setAttribute('stroke-linecap', 'round');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    if (submitBtn.getAttribute('aria-disabled') === 'true') {
        return;
    }

    // Set loading state
    submitBtn.setAttribute('aria-disabled', 'true');
    submitBtn.style.opacity = '0.7';
    submitBtn.style.cursor = 'wait';

    btnIcon.replaceChildren(spinnerCircle);
    btnIcon.classList.add('spinner-icon');
    btnText.textContent = 'Saving...';

    // Simulate async network request
    setTimeout(() => {
        // Restore original state
        submitBtn.removeAttribute('aria-disabled');
        submitBtn.style.opacity = '';
        submitBtn.style.cursor = 'pointer';

        btnIcon.replaceChildren(...originalIconNodes);
        btnIcon.classList.remove('spinner-icon');
        btnText.textContent = originalText;

        // Show a success message briefly (for actual UX feedback beyond button reverting)
        const successMsg = document.createElement('p');
        successMsg.textContent = 'Profile saved successfully.';
        successMsg.style.color = 'var(--color-emphasis)';
        successMsg.style.fontWeight = '600';
        successMsg.style.marginTop = '1rem';
        successMsg.setAttribute('aria-live', 'polite');
        successMsg.setAttribute('role', 'status');

        form.appendChild(successMsg);
        setTimeout(() => form.removeChild(successMsg), 3000);
    }, 1500);
});

// Accessible disabled states: prevent click and keyboard activation while maintaining focusability
submitBtn.addEventListener('click', (e) => {
     if (submitBtn.getAttribute('aria-disabled') === 'true') {
         e.preventDefault();
     }
});
submitBtn.addEventListener('keydown', (e) => {
    if ((e.key === 'Enter' || e.key === ' ') && submitBtn.getAttribute('aria-disabled') === 'true') {
        e.preventDefault();
    }
});

// Keyboard shortcut for power users
form.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault();
        submitBtn.click();
    }
});
