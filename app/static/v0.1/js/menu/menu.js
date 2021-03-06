let isMenuVisible = false;

function toggleMenu()
{
    let menuElements = document.querySelectorAll('.menu');
    if(isMenuVisible)
    {
        menuElements.forEach((element) => {
           element.classList.remove('shown');
           element.classList.add('hidden');
        });
    }
    else
    {
        menuElements.forEach((element) => {
            element.classList.remove('hidden');
            element.classList.add('shown');
         });
    }
    isMenuVisible = !isMenuVisible;
}

function hideMenu()
{
    isMenuVisible = false;
    let menuElements = document.querySelectorAll('.menu');
    menuElements.forEach((element) => {
        element.classList.remove('shown');
        element.classList.add('hidden');
     });
}

function addMenuElement(txt, href)
{
    let holder = document.querySelector('.menu.holder');
    let div = document.createElement('div');
    let link = document.createElement('a');
    link.innerText = txt;
    link.href = href;
    link.onclick = hideMenu;
    link.classList.add('menu');
    div.classList.add('menu');
    link.classList.add('link');
    div.classList.add('div');
    if(isMenuVisible)
    {
        div.classList.add('shown');
        link.classList.add('shown');
    }
    else
    {
        div.classList.add('hidden');
        link.classList.add('hidden');
    }
    div.appendChild(link);
    holder.appendChild(div);
    return div;
}

function updateMenu(edit_div, menu_div)
{
    let txt = edit_div.parentNode.querySelector('.contenteditableElement').innerText;
    let data = edit_div.parentNode.querySelector('.data-input').value;
    menu_div.querySelector('.menu.link').innerText = txt;
    menu_div.querySelector('.menu.link').href = data;
}
