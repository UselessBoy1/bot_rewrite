var article = document.querySelector('.article');
var menuBar = document.querySelector('.menuBar');
var is_saving = false;
var save_btn  = document.querySelector('#save');

save_btn.addEventListener('click', () => {
    if(!is_saving){
        is_saving = true;
        save_btn.className = 'chooseBtn savingInProgressBtn';
        save_btn.innerText = 'saving... please wait...';
        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/startsave');
        xhr.onload = () => {
            sendElement(article.childNodes[1]);
        }
        xhr.send(null);
    }
});

function sendEndSave()
{
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/endsave');
    xhr.onload = () => {
        toast('saved!');
        console.log('end save');
        document.querySelector('#save').className = 'chooseBtn';
        save_btn.innerText = 'save';
        is_saving = false;
    }
    xhr.send(null);
}

function sendElement(child)
{
    console.log('send call!');
    if(child == undefined)
    {
        sendEndSave();
        return;
    }
    if(child.tagName !== undefined)
    {
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/save');
        console.log(`open for ${child}`);
        xhr.onload = () => {
            sendElement(child.nextSibling);
        };
        console.log(`if for ${child}`);
        if(child.childNodes[1].tagName.toLowerCase() == 'div')
        {
            xhr.send('code='.concat(child.childNodes[1].childNodes[0].childNodes[0].innerText.replaceAll('\\', '\\\\')));
        }
        else if(child.childNodes[1].tagName.toLowerCase() == 'p')
        {
            xhr.send('text='.concat(child.childNodes[1].innerText));
        }
        else 
        {
            xhr.send('header='.concat(child.childNodes[1].innerText));
        }
    }
    else 
    {
        console.log(`${child.tagName}`);
    }
}

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

function onKeyDown(e) {
    if (e.keyCode === 9) { // tab key
        e.preventDefault();  // this will prevent us from tabbing out of the editor

        // now insert four non-breaking spaces for the tab key
        var editor = e.target;
        var doc = editor.ownerDocument.defaultView;
        var sel = doc.getSelection();
        var range = sel.getRangeAt(0);

        var tabNode = document.createTextNode("\u00a0\u00a0\u00a0\u00a0");
        range.insertNode(tabNode);

        range.setStartAfter(tabNode);
        range.setEndAfter(tabNode); 
        sel.removeAllRanges();
        sel.addRange(range);
    }
}

function editCode() {
    var blocks = document.querySelectorAll('code');
    blocks.forEach(block => {
        removeLeadingWhitespaces(block);
    });
    generatePrism();
}

function createParentDiv()
{
    let parent_div = document.createElement('div');
    let moving_div = document.createElement('div');
    
    moving_div.className = 'moving-div';
    
    let buttonUp = document.createElement('button');
    buttonUp.innerText = 'UP';
    buttonUp.className = 'chooseBtn';
    buttonUp.addEventListener('click', () => {
        moveElementUp(parent_div);
    });

    let buttonDel = document.createElement('button');
    buttonDel.innerText = 'DELETE';
    buttonDel.className = 'chooseBtn';
    buttonDel.addEventListener('click', () => {
        parent_div.remove();
    });

    let buttonDown = document.createElement('button');
    buttonDown.innerText = 'DOWN';
    buttonDown.className = 'chooseBtn';
    buttonDown.addEventListener('click', () => {
        moveElementDown(parent_div);
    });
    
    moving_div.appendChild(buttonUp);
    moving_div.appendChild(buttonDel);
    moving_div.appendChild(buttonDown);

    parent_div.className = 'section-div';
    parent_div.appendChild(moving_div);

    return parent_div;
}

function addEditBtns(parent_div){
    let edit_div = document.createElement('div');
    edit_div.className = 'moving-div';

    let buttonTxt = document.createElement('button');
    buttonTxt.innerText = 'Tt';
    buttonTxt.className = 'chooseBtn';
    buttonTxt.addEventListener('click', () => {
        createTextAfter('text here...', parent_div);
    });

    let buttonHeader = document.createElement('button');
    buttonHeader.innerText = 'H1';
    buttonHeader.className = 'chooseBtn';
    buttonHeader.addEventListener('click', () => {
        createHeaderAfter('header here', parent_div);
    });

    let buttonCode = document.createElement('button');
    buttonCode.innerText = '</>';
    buttonCode.className = 'chooseBtn';
    buttonCode.addEventListener('click', () => {
        createCodeAfter('int main(){\n   // code here :)\n}', parent_div);
    });

    edit_div.appendChild(buttonTxt);
    edit_div.appendChild(buttonHeader);
    edit_div.appendChild(buttonCode);

    parent_div.appendChild(edit_div);
}

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

function moveElementUp(element)
{
    let parent = element.parentNode;
    let prev = element.previousSibling;
    let oldElem = parent.removeChild(element);
    parent.insertBefore(oldElem, prev);
}

function moveElementDown(element)
{
    let parent = element.parentNode;
    let next = element.nextSibling.nextSibling;
    let oldElem = parent.removeChild(element);
    parent.insertBefore(oldElem, next);
}

window.addEventListener('load', () => {
    generateInfa();
});