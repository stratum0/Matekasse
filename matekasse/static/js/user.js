let socket;
$(document).ready(function () {
    socket = io.connect('http://' + document.domain + ':' + location.port + '/user');
    socket.on('newcredit', function (m) {
        $('#' + m.userid + ' #credit').text((m.credit / 100).toFixed(2) + '\u20AC');
        if (m.credit < 0) {
            $('#delete').removeAttr("style").hide();
        } else {
            $('#delete').show();
        }
    });


});
function credit(userid, creditvalue) {
    socket.emit('credit', {userid: userid, creditvalue: creditvalue});
}

function buyitem(userid, itemid) {
    socket.emit('buyitem', {userid: userid, itemid: itemid})
}

function transfer(userid) {
    socket.emit('transfer', {userid: userid, beneficary: $('#beneficary').val(), sum: $('#sum').val()})
}