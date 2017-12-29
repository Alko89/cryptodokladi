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

    $('#btceur').text(function() {
        var btctoeur

        $.get("https://api.kraken.com/0/public/Ticker?pair=BTCEUR", function(data) {
            btctoeur = data.result.XXBTZEUR.c[0]
        });

        return btctoeur
    });
    $('#etheur').text(function() {
        var ethtoeur

        $.get("https://api.kraken.com/0/public/Ticker?pair=ETHEUR", function(data) {
            ethtoeur = data.result.XETHZEUR.c[0]
        });

        return ethtoeur
    });
});
