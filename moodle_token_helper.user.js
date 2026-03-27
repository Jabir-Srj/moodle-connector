// ==UserScript==
// @name         Moodle Token Helper
// @namespace    https://github.com/SebaG20xx/moodle-connector-usm
// @version      1.0.0
// @description  Adds a floating button to any Moodle site to capture the mobile web service token for use with moodle-connector.
// @author       Sebastian Guevara (SebaG20xx)
// @match        https://aula.usm.cl/*
// @match        https://mytimes.taylors.edu.my/*
// @grant        GM_xmlhttpRequest
// @grant        GM_setClipboard
// @connect      aula.usm.cl
// @connect      mytimes.taylors.edu.my
// ==/UserScript==

(function () {
    'use strict';

    // ---------------------------------------------------------------------------
    // Floating button
    // ---------------------------------------------------------------------------

    const btn = document.createElement('button');
    btn.textContent = 'Get Token';
    btn.title = 'moodle-connector: capture mobile web service token';
    btn.style.cssText = [
        'position:fixed', 'bottom:20px', 'right:20px', 'z-index:999999',
        'padding:10px 18px', 'background:#0066cc', 'color:#fff',
        'border:none', 'border-radius:8px', 'cursor:pointer',
        'font-size:14px', 'font-family:sans-serif', 'font-weight:600',
        'box-shadow:0 2px 10px rgba(0,0,0,0.25)', 'transition:opacity .2s',
    ].join(';');

    btn.addEventListener('mouseenter', () => btn.style.opacity = '0.85');
    btn.addEventListener('mouseleave', () => btn.style.opacity = '1');
    document.body.appendChild(btn);

    // ---------------------------------------------------------------------------
    // Token capture
    // ---------------------------------------------------------------------------

    btn.addEventListener('click', () => {
        const passport = Date.now();
        const baseUrl  = window.location.origin;
        const launchUrl = (
            `${baseUrl}/admin/tool/mobile/launch.php` +
            `?service=moodle_mobile_app&passport=${passport}&urlscheme=moodlemobile`
        );

        btn.textContent = 'Getting token...';
        btn.disabled = true;

        GM_xmlhttpRequest({
            method:   'GET',
            url:      launchUrl,
            redirect: 'manual',      // do not follow redirects automatically
            onload:   (res) => {
                // Tampermonkey exposes the Location header even for 3xx responses
                const headers  = res.responseHeaders || '';
                const locMatch = headers.match(/^location:\s*(moodlemobile:\/\/.+)$/im);
                const location = locMatch ? locMatch[1].trim()
                    : (res.finalUrl || '');

                if (location.startsWith('moodlemobile://token=')) {
                    handleTokenUrl(location);
                } else {
                    resetBtn();
                    showError(
                        'Token redirect not found.\n' +
                        'Make sure you are logged in and the Mobile App plugin is enabled.'
                    );
                }
            },
            onerror: (err) => {
                resetBtn();
                showError('Request failed: ' + (err.statusText || 'unknown error'));
            },
        });
    });

    // ---------------------------------------------------------------------------
    // Decode moodlemobile://token=<base64>
    // Payload format: SITE_ID:::WS_TOKEN[:::PRIVATE_TOKEN]
    // ---------------------------------------------------------------------------

    function handleTokenUrl(url) {
        try {
            const b64 = url.split('token=')[1];
            const pad = b64.length % 4 ? '='.repeat(4 - b64.length % 4) : '';
            const decoded = atob(b64 + pad);
            const parts   = decoded.split(':::');
            if (parts.length < 2) throw new Error('Unexpected payload: ' + decoded);
            showModal(parts[1]);
        } catch (e) {
            showError('Failed to decode token: ' + e.message);
        }
        resetBtn();
    }

    // ---------------------------------------------------------------------------
    // Modal
    // ---------------------------------------------------------------------------

    function showModal(token) {
        const overlay = el('div', {
            style: [
                'position:fixed', 'inset:0', 'z-index:1000000',
                'background:rgba(0,0,0,0.5)',
                'display:flex', 'align-items:center', 'justify-content:center',
            ].join(';'),
        });

        const modal = el('div', {
            style: [
                'background:#fff', 'border-radius:12px', 'padding:28px',
                'max-width:520px', 'width:90%',
                'box-shadow:0 8px 40px rgba(0,0,0,0.3)',
                'font-family:sans-serif',
            ].join(';'),
        });

        const title = el('h3', {
            style: 'margin:0 0 8px;font-size:18px;color:#111',
            textContent: 'Moodle Token captured',
        });

        const hint = el('p', {
            style: 'margin:0 0 12px;font-size:13px;color:#555',
            textContent: 'Paste this value into config.json under "web_service_token", or copy it for use with moodle-connector.',
        });

        const input = el('input', {
            type: 'text',
            value: token,
            readOnly: true,
            style: [
                'width:100%', 'padding:10px', 'box-sizing:border-box',
                'font-family:monospace', 'font-size:13px',
                'border:1px solid #ccc', 'border-radius:6px',
                'background:#f7f7f7',
            ].join(';'),
        });

        const copyBtn = el('button', {
            textContent: 'Copy to clipboard',
            style: btnStyle('#0066cc'),
        });

        const closeBtn = el('button', {
            textContent: 'Close',
            style: btnStyle('#888'),
        });

        const actions = el('div', {
            style: 'display:flex;gap:10px;margin-top:16px;justify-content:flex-end',
        });

        copyBtn.addEventListener('click', () => {
            GM_setClipboard(token);
            copyBtn.textContent = 'Copied!';
            copyBtn.style.background = '#28a745';
            setTimeout(() => {
                copyBtn.textContent = 'Copy to clipboard';
                copyBtn.style.background = '#0066cc';
            }, 2000);
        });

        closeBtn.addEventListener('click',   () => overlay.remove());
        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

        actions.append(copyBtn, closeBtn);
        modal.append(title, hint, input, actions);
        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        setTimeout(() => { input.focus(); input.select(); }, 50);
    }

    // ---------------------------------------------------------------------------
    // Helpers
    // ---------------------------------------------------------------------------

    function el(tag, props = {}) {
        const node = document.createElement(tag);
        Object.assign(node, props);
        return node;
    }

    function btnStyle(bg) {
        return [
            `background:${bg}`, 'color:#fff', 'border:none',
            'padding:9px 18px', 'border-radius:6px', 'cursor:pointer',
            'font-size:14px', 'font-weight:600',
        ].join(';');
    }

    function resetBtn() {
        btn.textContent = 'Get Token';
        btn.disabled = false;
    }

    function showError(msg) {
        alert('[Moodle Token Helper]\n\n' + msg);
    }

})();
