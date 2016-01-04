$(document).ready(function() {
    $('ul.replace-by-dropdown li').click(function() {
        $('#' + $(this).parent().attr('aria-labelledby')).text($(this).html());
    });


    $('#image-20160103').hide();
});


function add() {
    $.post('/add', {
        a: $('#int_a').value,
        b: $('#int_b').value
    }).done(function(added) {
        $('#the-sum').innerHTML = added['sum'];
    }).fail(function() {
        alert('oh no.');
    });
}


function makeplot_20160103() {
    $('#make-image-20160103').blur();

    $.post('/makeplot_20160103', {
        startyear: $('#start-year-selector').text(),
        endyear: $('#end-year-selector').text(),
        xaxis: $('#x-axis-selector').text(),
        yaxis: $('#y-axis-selector').text()
    }).done(function(plotted) {
        if (plotted['result']) {
            alert(plotted['result'])
        } else {
            d = new Date();
            $('#image-20160103').attr('src', '/static/images/20160103_homefieldadvantage3/temp.png?"'+d.getTime());
            $('#image-20160103').show();
        }
    }).fail(function() {
        alert('oh no.');
    });
}
