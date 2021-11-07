var article = document.querySelector('article');

function createElement(element)
{
    let div = document.createElement('div');
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
        code.id = element.id;
        code.setAttribute("type", "code");
        code.innerText = element.txt;
        pre.appendChild(code);
        div.appendChild(pre);
        div.addEventListener('focusout', () => generatePrism());
        generatePrism();
        return div;
    }
    else if(element.type == 'header')
    {
        res = document.createElement('h1');
    }
    else if (element.type == 'link')
    {
        res = document.createElement('a');
        res.href = element.data;
        res.classList.add('page-link');
        res.classList.add('menu-edit-place');
        let menu_div = addMenuElement(element.txt, element.data);
        div.addEventListener('focusout', () => updateMenu(div, menu_div));
        div.addEventListener('delete', () => menu_div.remove());
    }
    else if(element.type == 'menu')
    {
        res = document.createElement('p');
        res.classList.add('menu-edit-place');
        let menu_div = addMenuElement(element.txt, element.data);
        div.addEventListener('focusout', () => updateMenu(div, menu_div));
        div.addEventListener('delete', () => menu_div.remove());
    }
    else if(element.type == 'title')
    {
        res = document.createElement('p');
        res.classList.add('title-edit-place');
        document.title = element.txt;
    }
    else
    {
        res = document.createElement('p');
    }
    res.setAttribute("type", element.type);
    res.classList.add(`contenteditableElement`);
    res.id = element.id;
    res.innerHTML = urlify(element.txt);
    div.appendChild(res);
    return div;
}

function load()
{
    
    site_json["site"].forEach(element => {
        article.appendChild(addParent(createElement(element), element.data));
    });
}

load();