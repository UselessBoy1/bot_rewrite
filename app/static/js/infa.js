var article = document.querySelector('.article');

function removeLeadingWhitespaces(block) {
    // remove leading and trailing white space.
    var code = block.innerHTML
                    .split('\n')
                    .filter(l => l.trim().length > 0)
                    .join('\n');

    // find the first non-empty line and use its
    // leading whitespace as the amount that needs to be removed
    var firstNonEmptyLine = block.textContent
                                .split('\n')
                                .filter(l => l.trim().length > 0)[0];

    // using regex get the first capture group
    var leadingWhiteSpace = firstNonEmptyLine.match(/^([ ]*)/);

    // if the capture group exists, then use that to
    // replace all subsequent lines.
    if(leadingWhiteSpace && leadingWhiteSpace[0]) {
    var whiteSpace = leadingWhiteSpace[0];
    code = code.split('\n')
                .map(l => l.replace(new RegExp('^' + whiteSpace + ''), ''))
                .join('\n');
    }

    // update the inner HTML with the edited code
    block.innerHTML = code;
}

function createCode(code) {
    let div_elem = document.createElement('div');
    div_elem.className = 'code-div';
    let pre_elem = document.createElement('pre');
    let code_elem = document.createElement('code');
    code_elem.className = 'language-cpp';
    code_elem.innerHTML = code.replaceAll('<', '&lt;').replaceAll('>', '&gt;');
    pre_elem.appendChild(code_elem);
    div_elem.appendChild(pre_elem);
    article.appendChild(div_elem);
    removeLeadingWhitespaces(code_elem);
    generatePrism();
}

function createText(txt) {
    let paragraph_elem = document.createElement('p');
    paragraph_elem.innerHTML = urlify(txt);
    article.appendChild(paragraph_elem);
}


onload = () => {
    generateInfa();
    
    var blocks = document.querySelectorAll('code');
    blocks.forEach(block => {
        removeLeadingWhitespaces(block);
    });

};