var pwd = "";

var wrong_times = 0;

function removeWrongTime()
{
    wrong_times--;
    if(wrong_times > 0)
    {
        setTimeout(() => {
            removeWrongTime();
        }, 10000);
    }
}

function save()
{
    if(wrong_times >= 5)
    {
        toast("You've been temporarily blocked!");
        return;
    }
    let saving_panel = document.querySelector('#saving-panel');
    saving_panel.classList.remove('hide');
    let new_site_json = {
        "id": site_json['id'],
        "site": [],
        "pwd": pwd
    }
    let num = 0;
    article.childNodes.forEach((node) => {
        if('querySelector' in node && typeof node.querySelector !== 'undefined' && node.id != 'none')
        {
            let type = node.querySelector('.contenteditableElement').getAttribute("type");
            let txt = node.querySelector('.contenteditableElement').innerText;
            let id = node.querySelector('.contenteditableElement').id;
            let data = node.querySelector('.data-input').value;
            new_site_json['site'].push({type: type, txt: txt, id:id, data: data, num: num});
            num++;
        }
    });
    let xhr = new XMLHttpRequest();
    let url = "/save";

    xhr.onload = () =>
    {
        if(xhr.status != 200)
        {
            if(wrong_times < 5)
            {
                wrong_times++;
                let input = prompt("Password:", "");
                if(input != null && input != "")
                {
                    pwd = input;
                    save();
                }
                else
                {
                    saving_panel.classList.add('hide');
                    toast("Wrong auth!");
                }
            }
            else
            {
                setTimeout(() => {
                    removeWrongTime();
                }, 10000);
                saving_panel.classList.add('hide');
                toast("You've been blocked!");
            }
        }
        else
        {
            saving_panel.classList.add('hide');
            toast("Saved");
            setTimeout(() => {
                location.reload()
            }, 1000);
        }
    }

    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(new_site_json));
}