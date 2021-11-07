function addParent(element, data)
{
    if(element.querySelector('.page-link') !== null)
    {
        let br1 = document.createElement('br');
        let br2 = document.createElement('br');
        element.insertBefore(br1, element.firstChild);
        element.appendChild(br2);
    }
    return element;
}