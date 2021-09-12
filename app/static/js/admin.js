var article = document.querySelector('.article');

document.querySelector('#addCode').addEventListener('click', () => {
    createCode('#include <iostream>\nint main(){\n   // code here :)\n}');
});

document.querySelector('#addTxt').addEventListener('click', () => {
    createText("text here..");
});

document.querySelector('#save').addEventListener('click', () => {
    let children = article.childNodes;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/startsave');
    xhr.onload = () => {
        var ready = true;
        for(let child of children){
            if(child.tagName !== undefined)
            {
                xhr = new XMLHttpRequest();
                if(child.tagName.toLowerCase() == 'div')
                {
                    xhr.open('POST', '/save');
                    xhr.onload = () => {
                        ready = true;
                    };
                    xhr.send('code='.concat(child.childNodes[0].childNodes[0].innerText));
                    ready = false;
                }
                else 
                {
                    xhr.open('POST', '/save');
                    xhr.onload = () => {
                        ready = true;
                    };
                    xhr.send('text='.concat(child.innerText));
                    ready = false;
                }
            }
        }
        xhr = new XMLHttpRequest();
        xhr.open('GET', '/endsave');
        xhr.onload = () => {
            toast('saved!');
        }
        xhr.send(null);
    }
    xhr.send(null);
    
});

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
    
    removeLeadingWhitespaces(code_elem);
    generatePrism();
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