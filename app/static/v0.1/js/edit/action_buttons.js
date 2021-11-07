function showAllPages()
{
    let showMsg = "";
    site_json['other'].forEach(other => {
        showMsg += `${other.txt} -> ${other.id}\n`;
    });
    messageBox(showMsg);
}

function copySiteID()
{
    let txtToCopy = `/${site_json['id']}`
    navigator.clipboard.writeText(txtToCopy);
    toast(`Copied! ${txtToCopy}`);
}

function copyID(div)
{
    let txtToCopy = "#" + div.querySelector('.contenteditableElement').id;
    navigator.clipboard.writeText(txtToCopy);
    toast(`Copied! ${txtToCopy}`);
}