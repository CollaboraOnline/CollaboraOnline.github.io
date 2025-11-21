const fs = require('fs');
const fetch = require('node-fetch');

const REPO = 'CollaboraOnline/online';
const PER_PAGE = 100;
const API_URL = `https://api.github.com/repos/${REPO}/contributors`;

let page = 1;
let fetchError = false;

async function fetchContributors(page) {
    const maxAttempts = 4;
    const baseDelay = 600; // ms

    const headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    };
    // Allow increasing rate limits by providing a token in env: GITHUB_TOKEN
    if (process.env.GITHUB_TOKEN) {
        headers['Authorization'] = `token ${process.env.GITHUB_TOKEN}`;
    }

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            const response = await fetch(`${API_URL}?per_page=${PER_PAGE}&page=${page}`, { headers });
            if (!response.ok) {
                const text = await response.text().catch(() => '');
                const err = new Error(`HTTP ${response.status} ${response.statusText} - ${text}`);
                // If 404, probably no more pages — return empty array to terminate normally
                if (response.status === 404) return [];
                throw err;
            }
            return await response.json();
        } catch (error) {
            const isLast = attempt === maxAttempts;
            console.error(`Error fetching page ${page} (attempt ${attempt}/${maxAttempts}):`, error.message);
            if (isLast) return null;
            const delay = Math.round(baseDelay * Math.pow(1.8, attempt) + Math.random() * 200);
            await new Promise(r => setTimeout(r, delay));
        }
    }
}

async function getAllContributors() {
    let contributors = [];
    let morePages = true;

    while (morePages) {
        console.log(`Fetching page ${page}...`);
        const data = await fetchContributors(page);
        if (data === null) {
            // fatal error fetching this page after retries
            console.error(`Failed to fetch page ${page} after retries — stopping fetch.`);
            morePages = false;
            fetchError = true;
            break;
        }
        if (!Array.isArray(data) || data.length === 0) {
            morePages = false;
        } else {
            contributors = contributors.concat(data);
            page++;
        }
    }

    // Sort contributors by contributions
    contributors.sort((a, b) => b.contributions - a.contributions);

    // Generate HTML content
    let htmlContent = `
<div class="contributors-list" style="display: flex; flex-wrap: wrap; gap: 50px; justify-content: center; padding: 20px 0px;">
`;

    contributors.forEach(contributor => {
        htmlContent += `
<div class="contributor" style="width: 140px; text-align: center; font-family: Arial, sans-serif;">
    <img src="${contributor.avatar_url}" alt="${contributor.login}" style="border-radius: 50%; width: 100px; height: 100px; box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);">
    <h3 style="font-size: 1rem; margin: 10px 0 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${contributor.login}</h3>
    <p style="font-size: 0.9rem; margin: 0;">Contributions: ${contributor.contributions}</p>
</div>
`;
    });

    htmlContent += `</div>`;

    // If fetching failed, abort
    if (fetchError) {
        console.error('One or more pages failed to fetch after retries — aborting without writing file.');
        return;
    }

    const generatedList = htmlContent;
    try {
        const shortcodeDir = 'layouts/shortcodes';
        const shortcodePath = `${shortcodeDir}/contributors-list.html`;
        if (!fs.existsSync(shortcodeDir)) fs.mkdirSync(shortcodeDir, { recursive: true });
        const shortcodeContent = `${generatedList}`;
        fs.writeFileSync(shortcodePath, shortcodeContent, 'utf8');
        console.log('Shortcode written to', shortcodePath);
    } catch (e) {
        console.error('Failed to write shortcode file:', e.message);
        // Do not abort — we still attempt to update the content file, but warn.
    }
    // Target content file
    const outPath = 'content/post/contributors.md';

    const startMarker = '<!-- CONTRIBUTORS-START -->';
    const endMarker = '<!-- CONTRIBUTORS-END -->';

    if (fs.existsSync(outPath)) {
        const existing = fs.readFileSync(outPath, 'utf8');
        const markerRegex = /<!-- CONTRIBUTORS-START -->[\s\S]*?<!-- CONTRIBUTORS-END -->/;
        const replacement = startMarker + '\n\n' + '{{< contributors-list >}}' + '\n\n' + endMarker;

        if (markerRegex.test(existing)) {
            const newContent = existing.replace(markerRegex, replacement);
            if (newContent === existing) {
                console.log('No changes detected in contributors region.');
                return;
            }
            fs.writeFileSync(outPath, newContent, 'utf8');
            console.log('Contributors region (markers) updated in', outPath);
            return;
        }

        // If no markers, prefer inserting before the first <script> tag
        const scriptIdx = existing.search(/<script[\s\S]*?>/i);
        const replacementBlock = '\n\n' + startMarker + '\n\n' + '{{< contributors-list >}}' + '\n\n' + endMarker + '\n';
        if (scriptIdx !== -1) {
            const before = existing.slice(0, scriptIdx);
            const after = existing.slice(scriptIdx);
            const newContent = before + replacementBlock + after;
            fs.writeFileSync(outPath, newContent, 'utf8');
            console.log('Contributors region inserted before first <script> tag in', outPath);
            return;
        }

        const contribListRegex = /<div class="contributors-list"[\s\S]*?<\/div>/;
        if (contribListRegex.test(existing)) {
            const newContent = existing.replace(contribListRegex, replacement);
            fs.writeFileSync(outPath, newContent, 'utf8');
            console.log('Replaced existing contributors-list block in', outPath);
            return;
        }

        const startHeader = '## Meet Our Contributors:';
        const startHIdx = existing.indexOf(startHeader);
        if (startHIdx !== -1) {
            const afterStart = startHIdx + startHeader.length;
            const nextHeaderIdx = existing.indexOf('\n## ', afterStart);
            const before = existing.slice(0, afterStart);
            const after = nextHeaderIdx === -1 ? existing.slice(afterStart) : existing.slice(nextHeaderIdx);
            const cleanedAfter = after.replace(/<div class="contributors-list"[\s\S]*?<\/div>/g, '');
            const newContent = before + '\n\n' + replacement + cleanedAfter;
            fs.writeFileSync(outPath, newContent, 'utf8');
            console.log('Contributors list inserted after header in', outPath);
            return;
        }

        const supportersAnchor = '#supporters-section';
        const supportersIdx = existing.indexOf(supportersAnchor);
        if (supportersIdx !== -1) {
            const before = existing.slice(0, supportersIdx);
            const after = existing.slice(supportersIdx);
            const newContent = before + replacementBlock + after;
            fs.writeFileSync(outPath, newContent, 'utf8');
            console.log('Contributors list inserted before supporters section in', outPath);
            return;
        }

        const finalContent = existing + '\n\n' + replacementBlock;
        fs.writeFileSync(outPath, finalContent, 'utf8');
        console.log('Contributors list appended to end of', outPath);
        return;
    } else {
        // File doesn't exist — create minimal file with markers
        const content = startMarker + '\n\n' + '{{< contributors-list >}}' + '\n\n' + endMarker + '\n';
        fs.writeFileSync(outPath, content, 'utf8');
        console.log('Created new contributors file with markers at', outPath);
    }
}

// Run the function to fetch and generate the contributors section
getAllContributors();
