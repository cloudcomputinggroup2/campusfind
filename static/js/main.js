/**
 * CampusFind JavaScript Utilities
 * Interactive client-side features: Image previews, clipboard copy, live filters
 */

document.addEventListener('DOMContentLoaded', function() {
    // 1. Live Image Upload Preview
    const imageInput = document.getElementById('item-image-input');
    const previewContainer = document.getElementById('image-preview-wrapper');
    const previewImg = document.getElementById('image-preview-img');
    const placeholderText = document.getElementById('image-placeholder-text');

    if (imageInput && previewImg) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Check file size (< 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    alert('File size exceeds 5MB limit. Please select a smaller photo.');
                    imageInput.value = '';
                    return;
                }
                const reader = new FileReader();
                reader.onload = function(event) {
                    previewImg.src = event.target.result;
                    previewImg.classList.remove('d-none');
                    if (placeholderText) placeholderText.classList.add('d-none');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // 2. Copy to Clipboard Functionality
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const textToCopy = this.getAttribute('data-copy-text') || window.location.href;
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalHtml = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check2"></i> Copied!';
                this.classList.add('btn-success');
                setTimeout(() => {
                    this.innerHTML = originalHtml;
                    this.classList.remove('btn-success');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy: ', err);
            });
        });
    });

    // 3. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 6000);
    });

    // 4. Form Submit Spinner Protection
    const standardForms = document.querySelectorAll('form:not(.no-spin)');
    standardForms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...';
                // Reset after 8s just in case
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 8000);
            }
        });
    });
});
