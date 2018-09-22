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

    //$('.trumbowyg-textarea').trumbowyg();

    var calculateTotal = function() {
        value = $('#value').val();
        rate = $('#rate').val();

        $('#total').text(value * rate);
    }
    $('#value').keypress(calculateTotal).blur(calculateTotal);
    $('#rate').keypress(calculateTotal).blur(calculateTotal);

    $('.timestamp').each(function() {
        $(this).text(function( i, val ) {
            return val.split(".")[0];
        });
    });

    $.get("https://api.coinmarketcap.com/v1/ticker/pivx/?convert=EUR", function(data) {
        var pivx_eur = data[0].price_eur
        var pivx = $('#PIVX').text();

        $('#pivxeur').text(parseFloat(pivx_eur).toFixed(8));
        $('#PIVXEUR').text((pivx * pivx_eur).toFixed(8));
    });

    $.get("https://api.coinmarketcap.com/v1/ticker/sportyco/?convert=EUR", function(data) {
        var spf_eur = data[0].price_eur
        var spf = $('#SPF').text();

        $('#spfeur').text(parseFloat(spf_eur).toFixed(8));
        $('#SPFEUR').text((spf * spf_eur).toFixed(8));
    });

    $.ajax({
        url: "/api/eur_usd_rate",
        type: 'get',
        success: function (data) {
            var usd_eur = data.USD;

            $.get("https://poloniex.com/public?command=returnTicker", function(data) {
                var usdt_btc = data.USDT_BTC.last;
                var usdt_eth = data.USDT_ETH.last;

                var btc = $('#BTC').text();
                var eth = $('#ETH').text();

                $('#btceur').text((usdt_btc / usd_eur).toFixed(8));
                $('#BTCEUR').text((btc * (usdt_btc / usd_eur)).toFixed(8));

                $('#etheur').text((usdt_eth / usd_eur).toFixed(8));
                $('#ETHEUR').text((eth * (usdt_eth / usd_eur)).toFixed(8));
            });
        }
    });

    $('#send_all').click(function(){
        var tbl = $('#user_list_send_funds > tbody  > tr').get().map(function(row) {
            return $(row).find('td :first-child').get().map(function(cell) {
                var el = $(cell).first();
                if (el.is('input'))
                    return el.val().trim();
                else
                    return el.text().trim();
            });
        });

        var token = $("#token").val();
        var rate = $("#rate").val();

        $.ajax('/api/add_multiple_funds_call/' + token + '/' + rate, {
            data : JSON.stringify(tbl),
            contentType : 'application/json',
            type : 'POST'
            // success: function(data){
            //     var json = $.parseJSON(data);
            //     alert(json.html);
            // },
        });

        //window.location.replace('/user/user_list')
    });

    $("#buy_funds").submit(function(){
        var f = $(this.form);
        var inp = f.find("input.submit_value");
        if (!inp.length) {
            inp = $("<input />")
                .attr("type", "hidden")
                .addClass("submit_value")
                .appendTo(f);
        }
        inp.attr("name", this.name).val(this.value);
        return true;
    });
});
