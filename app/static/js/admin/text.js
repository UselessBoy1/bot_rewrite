function createTextAfter(txt, element){
    let parent_div = createParentDiv();

    let paragraph_elem = document.createElement('p');
    paragraph_elem.style.padding = "5px";
    paragraph_elem.style.border = "2px solid #333";
    paragraph_elem.style.borderRadius = '10px';
    paragraph_elem.innerHTML = txt;
    paragraph_elem.contentEditable = true;
    paragraph_elem.addEventListener('keydown', onKeyDown);
    
    parent_div.appendChild(paragraph_elem);
    
    addEditBtns(parent_div);

    article.insertBefore(parent_div, element.nextSibling);
}

function createText(txt) {
    let parent_div = createParentDiv();

    let paragraph_elem = document.createElement('p');
    paragraph_elem.style.padding = "5px";
    paragraph_elem.style.border = "2px solid #333";
    paragraph_elem.style.borderRadius = '10px';
    paragraph_elem.innerHTML = txt;
    paragraph_elem.contentEditable = true;
    paragraph_elem.addEventListener('keydown', onKeyDown);
    
    parent_div.appendChild(paragraph_elem);
    
    addEditBtns(parent_div);

    article.appendChild(parent_div);
}