$( document ).ready(function() {
    $('#search').keypress(function(){
        $('.post').hide();
        var txt = $('#search').val();
        $('.post-title, .post-meta').each(function(){
        if($(this).text().toUpperCase().indexOf(txt.toUpperCase()) != -1){
            $(this).parent().parent().show();
        }
        });
    });

    $('.BTC').each(function() {
        $(this).text(function( i, val ) {
            return parseInt(val) / 100000000;
        });
    });
    $('.ETH').each(function() {
        $(this).text(function( i, val ) {
            return parseInt(val) / 1000000000000000000;
        });
    });

    $.get("https://api.kraken.com/0/public/Ticker?pair=BTCEUR", function(data) {
        var bine = data.result.XXBTZEUR.c[0]

        $('#btceur').text(bine)
        var tb = parseFloat($('#BTC').text())
        $('#BTCEUR').text(tb * bine);
    });

    $.get("https://api.kraken.com/0/public/Ticker?pair=ETHEUR", function(data) {
        var eine = data.result.XETHZEUR.c[0]

        $('#etheur').text(eine)
        var te = parseFloat($('#ETH').text())
        $('#ETHEUR').text(te * eine);
    });
});
