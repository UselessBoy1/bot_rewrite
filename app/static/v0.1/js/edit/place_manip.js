function moveUp(div)
{
    if('previousSibling' in div)
    {
        div.previousSibling.backgroundColor = 'white';
        div.parentNode.insertBefore(div, div.previousSibling);
    }
}

function moveDown(div)
{
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
    let prev = div.style.backgroundColor;
    div.style.backgroundColor = '#777';
    setTimeout(() => {
        if(confirm('Do you really want to delete this element?'))
        {
            div.remove();
        }
        else
        {
            div.style.backgroundColor = prev;
        }
    }, 100);
}