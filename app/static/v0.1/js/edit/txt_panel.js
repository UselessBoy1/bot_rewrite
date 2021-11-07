function messageBox(msg)
{
    let msgBox = document.querySelector('#txt-panel');
    msgBox.classList.remove('hide');
    let msgBoxTxt = document.querySelector('#txt-in-panel');
    msgBoxTxt.innerText = msg;
}

function closeMessageBox()
{
    let msgBox = document.querySelector('#txt-panel');
    msgBox.classList.add('hide');
}