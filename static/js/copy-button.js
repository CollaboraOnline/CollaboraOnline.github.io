document.addEventListener("DOMContentLoaded", function () {
    const codeBlocks = document.querySelectorAll('pre');

    // Icon SVGs
    const copyIconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>';
    const checkIconSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';

    codeBlocks.forEach(function (preBlock) {
        let container = preBlock;

        // Handle highlighting wrappers
        if (preBlock.parentNode.classList.contains('highlight')) {
            container = preBlock.parentNode;
        } else if (preBlock.parentNode.tagName === 'DIV' && preBlock.parentNode.style.position === 'relative') {
            container = preBlock.parentNode;
        }

        container.style.position = 'relative';

        if (container.querySelector('.copy-button')) return;

        const button = document.createElement('button');
        button.className = 'copy-button';
        button.title = 'Copy to clipboard';
        button.innerHTML = copyIconSvg;

        container.appendChild(button);

        button.addEventListener('click', function () {
            button.blur(); // Remove focus

            let codeText = preBlock.textContent;

            navigator.clipboard.writeText(codeText).then(function () {
                button.innerHTML = checkIconSvg;
                button.classList.add('copied');

                setTimeout(function () {
                    button.innerHTML = copyIconSvg;
                    button.classList.remove('copied');
                }, 1000);
            }, function (err) {
                console.error('Copy failed: ', err);
            });
        });
    });
});
