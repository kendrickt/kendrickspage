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

function scroll_images(id, dir, msg) {
    var images = $(id).children();
    var curr;
    var image;
    for (i = 0; i < images.length; i++) {
        image = images[i];
        if (image.className != 'no-display') {
            curr = i;
            break;
        }
    }
    if (dir == -1 && curr == 0) {
        alert(msg);
        return;
    } else if (dir == 1 && curr == 3) {
        alert(msg);
        return;
    } else if (dir == 1) {
        image = images[curr+1];
    } else {
        image = images[curr-1];
    }
    image.className = '';
    image = images[curr];
    image.className = 'no-display';
}
