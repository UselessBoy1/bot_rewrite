var article = document.querySelector('article');

function createElement(element)
{
    let div = document.createElement('div');
    div.id = element.id;
    div.classList.add('div');
    let res = null;
    if(element.type == 'code')
    {
        div.classList.add('gray2');
        div.classList.add('rounded');
        let pre = document.createElement('pre');
        pre.classList.add(`language-cpp`);
        let code = document.createElement('code');
        code.classList.add(`language-cpp`);
        code.classList.add(`contenteditableElement`);
        code.innerText = element.txt;
        pre.appendChild(code);
        div.appendChild(pre);
        generatePrism();
        return div;
    }
    else if(element.type == 'header')
    {
        res = document.createElement('h3');
    }
    else
    {
        res = document.createElement('p');
    }
    res.classList.add(`contenteditableElement`);
    res.innerHTML = urlify(element.txt);
    div.appendChild(res);
    return div;
}

function load()
{
    site_json["site"].forEach(element => {
        article.appendChild(addParent(createElement(element)));
    });
}

load();