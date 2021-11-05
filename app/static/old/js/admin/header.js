function createHeaderAfter(txt, element){
    let parent_div = createParentDiv();

    let header_elem = document.createElement('h1');
    header_elem.style.padding = "5px";
    header_elem.style.border = "2px solid #333";
    header_elem.style.borderRadius = '10px';
    header_elem.innerHTML = txt;
    header_elem.contentEditable = true;
    header_elem.addEventListener('keydown', onKeyDown);
    
    parent_div.appendChild(header_elem);
    
    addEditBtns(parent_div);

    article.insertBefore(parent_div, element.nextSibling);
}

function createHeader(txt) {
    let link = document.createElement('a');
    link.href = `#${txt.replaceAll(' ', '')}`;
    link.innerHTML = txt;
    link.className = 'menuBarBtn';
    menuBar.appendChild(link);
    menuBar.appendChild(document.createElement('br'));
    menuBar.appendChild(document.createElement('br'));

    let parent_div = createParentDiv();

    let header_elem = document.createElement('h1');
    header_elem.style.padding = "5px";
    header_elem.style.border = "2px solid #333";
    header_elem.style.borderRadius = '10px';
    header_elem.innerHTML = txt;
    header_elem.contentEditable = true;
    header_elem.id = `${txt.replaceAll(' ', '')}`;
    header_elem.addEventListener('keydown', onKeyDown);
    
    parent_div.appendChild(header_elem);
    
    addEditBtns(parent_div);

    article.appendChild(parent_div);
}