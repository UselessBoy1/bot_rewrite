var selected_div = null;
var form_div = document.querySelector('.new.div');

function openNewElementForm()
{
    console.log("NONE");
    selected_div = null;
    form_div.classList.remove('hide');
}

function openNewElementFormForDiv(div)
{
    console.log('show2');
    selected_div = div;
    form_div.classList.remove('hide');
}

function closeNewElementForm()
{
    console.log('hide');
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
    if(!selected_div)
    {
        console.log("not UN");
        article.insertBefore(element, selected_div);
    }
    else
    {
        article.insertBefore(element, article.firstChild);
    }
}