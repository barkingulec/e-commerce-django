function Copy() {
    let url = document.location.href

    navigator.clipboard.writeText(url).then(function () {
        document.getElementById("share-button").innerHTML = "Copied to Clipboard";
    }, function () {
        alert('Copy error')
    });
}

function showHideForm() {
    document.getElementById("addPostForm").style.bottom="0%"; 
    // if(document.getElementById("addPostForm").style.bottom == '-70%'){
    //     document.getElementById("addPostForm").style.bottom="0%";    
    // }else{
    //     document.getElementById("addPostForm").style.bottom="-70%";  
    // }
}
function hideForm() {
    document.getElementById("addPostForm").style.bottom="-80%"; 
}
function toggleReply(parent_id) {
    const row = document.getElementById(parent_id);

    if (row.classList.contains('d-none')) {
        row.classList.remove('d-none');
    } else {
        row.classList.add('d-none');
    }
}
function showReplies(comment_children) {
    for (const id of comment_children.split("+")) {
        if (id) {
            const row = document.getElementById(id);

            if (row.classList.contains('d-none')) {
                row.classList.remove('d-none');
            } else {
                row.classList.add('d-none');
            }
        }
    }
    }