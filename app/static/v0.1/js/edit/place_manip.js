function moveUp(div)
{
    if(div.querySelector(".contenteditableElement").getAttribute('type') == 'title')
    {
        toast("Permission denied!");
        return;
    }
    if('previousSibling' in div)
    {
        div.previousSibling.backgroundColor = 'white';
        div.parentNode.insertBefore(div, div.previousSibling);
    }
}

function moveDown(div)
{
    if(div.querySelector(".contenteditableElement").getAttribute('type') == 'title')
    {
        toast("Permission denied!");
        return;
    }
    if('nextSibling' in div && typeof div.nextSibling != 'undefined')
    {
        if('nextSibling' in div.nextSibling && typeof div.nextSibling.nextSibling != 'undefined')
        {
            if(div.nextSibling.id !=='none')
            {
                console.log("DOWN");
                div.parentNode.insertBefore(div, div.nextSibling.nextSibling);
            }
        }
    }
}

function deleteDiv(div)
{
    if(div.querySelector(".contenteditableElement").getAttribute('type') == 'title')
    {
        toast("Permission denied!");
        return;
    }
    let prev = div.style.backgroundColor;
    div.style.backgroundColor = '#777';
    setTimeout(() => {
        if(confirm('Do you really want to delete this element?'))
        {
            div.querySelector('.contenteditableElement').dispatchEvent(new Event('delete'));
            div.remove();
        }
        else
        {
            div.style.backgroundColor = prev;
        }
    }, 50);
}