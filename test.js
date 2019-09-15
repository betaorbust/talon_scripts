// For scraping MDN to get alllll the Javascript methods
function getRules() {
    return [...$0.querySelectorAll('dt a code')]
        .map((t) => t.innerHTML)
        .reduce((acc, cur) => {
            acc[
                cur
                    .replace(/([A-Z]+)/g, ' $1')
                    .replace(/([A-Z][a-z])/g, ' $1')
                    .trim()
                    .replace('.prototype', '')
                    .replace('.', ' dot ')
                    .replace(/[^a-z A-Z0-9]/g, '')
                    .replace(/  /g, ' ')
                    .toLowerCase()
            ] = cur.replace(/^.*\.prototype/, '');
            return acc;
        }, {});
}

function formatWithLeft(obj) {
    return Object.entries(obj)
        .map(([key, value]) => `"${key}":  ["${value}", Key("left")],`)
        .join('\n');
}
