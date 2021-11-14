function urlify(text)
{
    let urlRegex = /(https?:\/\/[\S]+)/
    let t =  text.replace(urlRegex, (url) => 
    {
        let name = url;
        if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) 
        {
            name='link' 
        }
        return `<a href=${url}>${name}</a>`;
    });
    return t;
}

function toast(msg) 
{
    let toastDiv = document.querySelector('#toast');
    toastDiv.innerText = msg
    toastDiv.style.marginLeft = -toastDiv.clientWidth/2 + "px"
    toastDiv.className = 'show';
    setTimeout(() => {
        toastDiv.className = '';
    }, 3000);
}
