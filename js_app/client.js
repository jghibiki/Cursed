

var client = {
    updating: false
};


client.init = function(){

    $.ajax({
        type: 'POST',
        url: 'http://localhost:8080/users',
        crossDomain: true,
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            username: cursed.state.username,
            current_map: ""
        }),
        beforeSend: function (xhr) {
            xhr.setRequestHeader ("Authorization", "Basic " + btoa(cursed.state.username + ":" + cursed.state.password));
        },
    }).done((data)=>{
        client.request("/users", null, (data)=>{console.log(data); });
        client.timer = setInterval(client.update, 1000);
    });
}

client.update= function(){
    if(!client.updating){
        client.updating = true;
        client.request('/hash', null, (data)=>{
            for(var module of cursed.modules.live){
                module.update(data);
            }
        });
        client.updating = false;
    }
}

client.request = function(url, payload, callback){
    if(payload === null || payload === undefined || payload === ""){
        if(typeof(callback) === "function"){
            $.ajax({
                type: 'GET',
                url: 'http://localhost:8080' + url,
                crossDomain: true,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader ("Authorization", "Basic " + btoa(cursed.state.username + ":" + cursed.state.password));
                },
            })
            .done(callback);
        }
        else{
            $.ajax({
                type: 'GET',
                url: 'http://localhost:8080' + url,
                crossDomain: true,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader ("Authorization", "Basic " + btoa(cursed.state.username + ":" + cursed.state.password));
                },
            });
        }
    }
    else{
        if(typeof(callback) === "function"){
            $.ajax({
                type: 'POST',
                url: 'http://localhost:8080/users',
                crossDomain: true,
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(payload),
                beforeSend: function (xhr) {
                    xhr.setRequestHeader ("Authorization", "Basic " + btoa(cursed.state.username + ":" + cursed.state.password));
                }
            })
            .done(callback);
        }
        else {
            $.ajax({
                type: 'POST',
                url: 'http://localhost:8080/users',
                crossDomain: true,
                dataType: "json",
                contentType: "application/json",
                data: JSON.stringify(payload),
                beforeSend: function (xhr) {
                    xhr.setRequestHeader ("Authorization", "Basic " + btoa(cursed.state.username + ":" + cursed.state.password));
                }
            });
        }
    }
}
