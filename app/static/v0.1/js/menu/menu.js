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
    let menuElements = document.querySelectorAll('.menu');
    menuElements.forEach((element) => {
        element.classList.remove('shown');
        element.classList.add('hidden');
     });
}

function addElement(txt, href)
{
    let holder = document.querySelector('.menu.holder');
    let div = document.createElement('div');
    let link = document.createElement('a');
    link.innerText = txt;
    link.href = href;
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
}