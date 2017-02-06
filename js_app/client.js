

var client = {};


client.init = function(){
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8080/users',
        crossDomain: true,
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(cursed.state.username + ":" + cursed.state.password));
        },
    }).done((data)=>{
        console.log(data);
    });
}
