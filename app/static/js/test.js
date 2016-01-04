$(document).ready(function() {
});




function add() {
    $.post('/add', {
        a: +document.getElementById('int_a').value,
        b: +document.getElementById('int_b').value
    }).done(function(added) {
        document.getElementById('the-sum').innerHTML = added['sum'];
    }).fail(function() {
        alert('oh no.');
    });
}
