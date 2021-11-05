var article = document.querySelector('article');

function createElement(element)
{
    let div = document.createElement('div');
    div.id = element.id;
    div.classList.add('div');
    if(element.type == 'code')
    {
        div.classList.add('gray2');
        div.classList.add('rounded');
        let pre = document.createElement('pre');
        pre.classList.add(`language-cpp`);
        let code = document.createElement('code');
        code.classList.add(`language-cpp`);
        code.innerText = element.txt;
        pre.appendChild(code);
        div.appendChild(pre);
    }
    else
    {
        div.classList.add(`${element.type}`);
        div.innerHTML = urlify(element.txt);
    }
    generatePrism();
    return div;
}

function load()
{
    site_json["site"].forEach(element => {
        article.appendChild(addParent(createElement(element)));
    });
}