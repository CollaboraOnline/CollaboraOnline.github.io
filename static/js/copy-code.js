document.addEventListener('DOMContentLoaded', function () {
  const codeBlocks = document.querySelectorAll('pre > code');

  codeBlocks.forEach(function (codeBlock) {
    const pre = codeBlock.parentNode;

    // Create the copy button container
    const button = document.createElement('button');
    button.className = 'copy-code-button';
    button.type = 'button';
    button.ariaLabel = 'Copy code to clipboard';

    // SVG Icons
    const copyIcon = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
      </svg>
    `;

    const checkIcon = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
      </svg>
    `;

    button.innerHTML = copyIcon;

    // Add click event
    button.addEventListener('click', function () {
      const codeToCopy = codeBlock.innerText;

      navigator.clipboard.writeText(codeToCopy).then(function () {
        button.innerHTML = checkIcon;
        button.classList.add('copied');

        setTimeout(function () {
          button.innerHTML = copyIcon;
          button.classList.remove('copied');
        }, 1000);
      }).catch(function (err) {
        console.error('Failed to copy text: ', err);
      });
    });

    // Position the button relative to the pre block
    pre.style.position = 'relative';
    pre.appendChild(button);
  });
});
