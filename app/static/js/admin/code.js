function createCodeAfter(code, element) {
    let parent_div = createParentDiv();

    let div_elem = document.createElement('div');
    div_elem.className = 'code-div';
    
    let pre_elem = document.createElement('pre');
    let code_elem = document.createElement('code');
    
    code_elem.className = 'language-cpp';
    code_elem.contentEditable = true
    code_elem.addEventListener('focusout', editCode);
    code_elem.addEventListener('keydown', onKeyDown);
    code_elem.innerHTML = code.replaceAll('<', '&lt;').replaceAll('>', '&gt;');
    
    pre_elem.appendChild(code_elem);
    
    div_elem.appendChild(pre_elem);
    
    parent_div.appendChild(div_elem);
    
    addEditBtns(parent_div);

    article.insertBefore(parent_div, element.nextSibling);
    
    removeLeadingWhitespaces(code_elem);
    generatePrism();
}

function createCode(code) {
    let parent_div = createParentDiv();

    let div_elem = document.createElement('div');
    div_elem.className = 'code-div';
    
    let pre_elem = document.createElement('pre');
    let code_elem = document.createElement('code');
    
    code_elem.className = 'language-cpp';
    code_elem.contentEditable = true
    code_elem.addEventListener('focusout', editCode);
    code_elem.addEventListener('keydown', onKeyDown);
    code_elem.innerHTML = code.replaceAll('<', '&lt;').replaceAll('>', '&gt;');
    
    pre_elem.appendChild(code_elem);
    
    div_elem.appendChild(pre_elem);
    
    parent_div.appendChild(div_elem);
    
    article.appendChild(parent_div);
    
    addEditBtns(parent_div);

    removeLeadingWhitespaces(code_elem);
    generatePrism();
}