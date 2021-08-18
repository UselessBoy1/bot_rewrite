const toast = (msg) => {
    let toastDiv = document.querySelector('#toast');
    toastDiv.innerText = msg
    toastDiv.style.marginLeft = -toastDiv.clientWidth/2 + "px"
    toastDiv.className = 'show';
    setTimeout(() => {
        toastDiv.className = '';
    }, 3000);
}

words = {
    "tydzien": {
        "x": "tydzien",
        "234": "tygodnie",
        "0156789": "tygodni"
    }
}

const getPLEnd = (word, num) => {
    let last_digit = [...(num.toString())].pop();
    if(num == 1){
        last_digit = 'x';
    }
    if(num == 11 || num == 12 || num == 13 || num == 14){
        last_digit = '0';
    }
    last_digit = last_digit.toString();
    let found = word;
    Object.keys(words[word]).forEach(key => {
        if(key.includes(last_digit)){
            found = words[word][key];
        }
    });
    return found;
}