let socket;
$(document).ready(function(){
    $("#searchbar").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#useroverview div").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    socket = io.connect('http://' + document.domain + ':' + location.port + '/home');
    socket.on('connect', function() {
        console.log('Connected');
    });
    socket.on('newusercredit', function (m) {
        //$('#' + m.userid + ' #credit').text((m.credit / 100).toFixed(2) + '\u20AC');
        location.reload();
    })
});