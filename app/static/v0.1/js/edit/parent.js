function addParent(element)
{
    let div = document.createElement('div');
    div.classList.add('gray5');
    div.classList.add('edit');
    div.classList.add('div');
    
    element.contentEditable = true;

    div.appendChild(element);

    let dataDiv = document.createElement('div');
    dataDiv.classList.add('edit');
    dataDiv.classList.add('data');

    let label = document.createElement('label');
    label.innerText = "Data:";
    dataDiv.appendChild(label);
    
    let inputData = document.createElement('input');
    inputData.classList.add('edit');
    inputData.classList.add('data-input');
    inputData.innerText = element.data;
    dataDiv.appendChild(inputData);

    div.appendChild(dataDiv);

    let controlsDiv = document.createElement('div');
    controlsDiv.classList.add('edit');
    controlsDiv.classList.add('controls');

    let upBtn = document.createElement('button');
    upBtn.classList.add('edit');
    upBtn.classList.add('btn');
    upBtn.innerText = "UP";
    upBtn.onclick = moveUp;
    controlsDiv.appendChild(upBtn);

    let downBtn = document.createElement('button');
    downBtn.classList.add('edit');
    downBtn.classList.add('btn');
    downBtn.innerText = "DOWN";
    downBtn.onclick = moveDown;
    controlsDiv.appendChild(downBtn);

    let delBtn = document.createElement('button');
    delBtn.classList.add('edit');
    delBtn.classList.add('btn');
    delBtn.innerText = "DELETE";
    delBtn.onclick = deleteDiv;
    controlsDiv.appendChild(delBtn);

    let addOtherBtn = document.createElement('button');
    addOtherBtn.classList.add('edit');
    addOtherBtn.classList.add('btn');
    addOtherBtn.innerText = "UP";
    addOtherBtn.onclick = openNewElementFormForDiv;
    controlsDiv.appendChild(addOtherBtn);

    div.appendChild(controlsDiv);
    return div;
}