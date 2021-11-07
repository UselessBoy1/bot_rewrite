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

function generateID()
{
    let suffix = (new Date()).getTime();
    return "" + suffix;
}

function getNewElement()
{
    let id = generateID();
    let selected = document.querySelector('#elementType').value;
    let element = {
        txt: "HERE!",
        type: selected,
        data: "",
        id: id
    }
    return element;
}

function newElement()
{
    closeNewElementForm();
    let json = getNewElement();
    let element = addParent(createElement(json), json.data);
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