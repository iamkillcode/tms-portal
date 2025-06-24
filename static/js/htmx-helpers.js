/* HTMX Helper functions */

// Process HTMX triggers from server response
function processHtmxTriggers(triggers) {
    if (!triggers) return;
    
    try {
        // If it's a string, try to parse it as JSON
        const triggerObj = typeof triggers === 'string' ? 
            JSON.parse(triggers) : triggers;
        
        // Dispatch events for each trigger
        Object.keys(triggerObj).forEach(triggerName => {
            const detail = triggerObj[triggerName];
            document.body.dispatchEvent(
                new CustomEvent(triggerName, { detail })
            );
        });
    } catch (e) {
        // If it's not valid JSON, it might be a simple event name
        if (typeof triggers === 'string') {
            document.body.dispatchEvent(
                new CustomEvent(triggers)
            );
        }
        console.error('Error processing HTMX triggers:', e);
    }
}

// Add HTMX trigger manually
function triggerHtmxEvent(eventName, detail = {}) {
    document.body.dispatchEvent(
        new CustomEvent(eventName, { detail })
    );
}

// Create an HTMX swap indicator
function createSwapIndicator(message = 'Loading...') {
    const indicator = document.createElement('div');
    indicator.className = 'htmx-indicator';
    indicator.innerHTML = `
        <div class="spinner-border spinner-border-sm text-primary" role="status">
            <span class="visually-hidden">${message}</span>
        </div>
        <span class="ms-2">${message}</span>
    `;
    return indicator;
}

// Add global HTMX event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Log HTMX events in debug mode
    if (window.htmxDebug) {
        document.body.addEventListener('htmx:beforeRequest', e => console.log('HTMX Request:', e.detail));
        document.body.addEventListener('htmx:afterRequest', e => console.log('HTMX Response:', e.detail));
        document.body.addEventListener('htmx:responseError', e => console.error('HTMX Error:', e.detail));
    }
    
    // Process triggers from HTMX responses
    document.body.addEventListener('htmx:afterOnLoad', function(evt) {
        const triggerHeader = evt.detail.xhr?.getResponseHeader('HX-Trigger');
        if (triggerHeader) {
            processHtmxTriggers(triggerHeader);
        }
    });
});
