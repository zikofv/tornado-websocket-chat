$(function() {
    if ("WebSocket" in window) {
        ws = new WebSocket("ws://" + document.domain + ":8888/ws");
        ws.onmessage = function (msg) {
            message = JSON.parse(msg.data);
            if (message.operation == "chat"){
              $("p#log").append(message.chat + '<hr />');
            }
            else{
              if (message.operation == "js_op"){
                $("#" + message.id).removeClass();
                $("#" + message.id)[message.method](message.parameters);
              }
            }
        };
    };

    $('#chat_form input[name=text]').focus();

    $("#chat_form").on('submit', function(e){
        e.preventDefault();
        var input = $('#chat_form input[name=text]');
        var message = $(input).val();
        $(input).val('');
        ws.send(JSON.stringify({'operation' : 'chat', 'chat': message}));
    });

    $(".js_op").on("click", function(e){
        e.preventDefault();
        ws.send(JSON.stringify({'operation' : 'js_op', 'operation_index': this["id"]}));
    });

    window.onbeforeunload = function() {
        ws.onclose = function () {};
        ws.close();
    };
});
