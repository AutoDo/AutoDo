var tagsToReplace = {
    '"': '&quot;',
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#039;'
};

function replaceTag(tag) {
    var s = tagsToReplace[tag] || tag;
    return s;
}

function safe_tags_replace(str) {
    return str.replace(/[&<>\"\'\{\}]/g, replaceTag);
}

function decodeHtml(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}