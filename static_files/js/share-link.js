document.addEventListener('DOMContentLoaded', function() {
    const shareLink = document.getElementById('share-link');
    const copyLinkBtn = document.getElementById('copy-link-btn');
    const copyIcon = document.getElementById('copy-icon');
    const copyText = document.getElementById('copy-text');

    if (copyLinkBtn && shareLink) {
        copyLinkBtn.addEventListener('click', function() {
            // Validate URL before copying
            const url = shareLink.value.trim();

            // Basic URL validation
            if (!url || !isValidUrl(url)) {
                console.error('Invalid URL');
                showErrorFeedback();
                return;
            }

            copyToClipboard(url);
        });
    }

    function isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch (error) {
            return false;
        }
    }

    function copyToClipboard(text) {
        // Create a temporary textarea to copy text
        const tempTextArea = document.createElement('textarea');
        tempTextArea.value = text;
        document.body.appendChild(tempTextArea);

        try {
            // Modern clipboard API
            if (navigator.clipboard) {
                navigator.clipboard.writeText(text)
                    .then(updateCopyButton)
                    .catch(handleCopyError);
            } else {
                // Fallback for older browsers
                tempTextArea.select();
                tempTextArea.setSelectionRange(0, 99999); // For mobile

                const successful = document.execCommand('copy');
                if (successful) {
                    updateCopyButton();
                } else {
                    handleCopyError();
                }
            }
        } catch (err) {
            handleCopyError(err);
        } finally {
            document.body.removeChild(tempTextArea);
        }
    }

    function handleCopyError(err) {
        console.error('Copy failed:', err);
        showErrorFeedback();
    }

    function showErrorFeedback() {
        copyIcon.className = 'fas fa-times text-danger';
        copyText.textContent = 'Copy Failed';

        setTimeout(() => {
            copyIcon.className = 'fas fa-copy';
            copyText.textContent = 'Copy';
        }, 2000);
    }

    function updateCopyButton() {
        copyIcon.className = 'fas fa-check text-success';
        copyText.textContent = 'Copied!';

        setTimeout(() => {
            copyIcon.className = 'fas fa-copy';
            copyText.textContent = 'Copy';
        }, 2000);
    }
});