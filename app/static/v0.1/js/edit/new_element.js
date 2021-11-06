var selected_div = null;
var form_div = document.querySelector('.new.div');

function openNewElementForm()
{
    selected_div = null;
    form_div.classList.remove('hide');
}

function openNewElementFormForDiv(div)
{
    selected_div = div;
    form_div.classList.remove('hide');
}

function closeNewElementForm()
{
    form_div.classList.add('hide');
}

function getNewElement()
{
    let selected = document.querySelector('#elementType').value;
    console.log(selected);
    let element = {
        txt: "HERE!",
        type: selected,
        data: selected
    }
    return element;
}

function newElement()
{
    closeNewElementForm();
    let element = addParent(createElement(getNewElement()));
    if(selected_div !== null)
    {
        if('nextSibling' in selected_div)
        {
            article.insertBefore(element, selected_div.nextSibling);
        }
        else
        {
            article.insertBefore(element, selected_div);
        }
    }
    else
    {
        article.insertBefore(element, article.firstChild);
    }
}