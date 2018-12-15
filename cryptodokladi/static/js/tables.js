function format ( name, d ) {
    table = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">';
    for (i = 0; i < d.length; i++){
        table += 
            '<tr>' +
            '<td>' + d[i].token + '</td>';
        if (d.user == d.sender) {
            table +=
                '<td>' + (- d[i].value.toFixed(8)) +'</td>' +
                '<td>' + d[i].user + '</td>';
        }
        else {
            table +=
                '<td>' + d[i].value.toFixed(8) + '</td>' +
                '<td>' + d[i].sender + '</td>';
        }
        table +=
            '<td>' + d[i].timestamp + '</td>'+
            '</tr>';
    }
    table += '</table>';

    return table;
}

$(document).ready( function () {
    $('.user-table').DataTable();

    $('.transactions-table').DataTable({
        "iDisplayLength": 10,
        "searching": false,
        "lengthChange": false,
        "fnDrawCallback": function ( oSettings ) {
            $(oSettings.nTHead).hide();
        }
    });

    var table = $('#user-funds').DataTable({
        "aLengthMenu": [[50, 100, 500, -1], [50, 100, 500, "All"]],
        "iDisplayLength": 50,

        "footerCallback": function ( row, data, start, end, display ) {
            var api = this.api(), data;

            var sumVal = function ( c ) {
                return api
                        .column( c )
                        .data()
                        .reduce( function (a, b) {
                            return parseFloat(a) + parseFloat(b.replace('/', '0'));
                        }, 0 );
            }

            // Update footers
            $( api.column( 1 ).footer() ).html(
                sumVal(1).toFixed(8)
            );
            $( api.column( 2 ).footer() ).html(
                sumVal(2).toFixed(8)
            );
            $( api.column( 3 ).footer() ).html(
                sumVal(3).toFixed(8)
            );
            $( api.column( 4 ).footer() ).html(
                sumVal(4).toFixed(8)
            );
            $( api.column( 5 ).footer() ).html(
                sumVal(5).toFixed(8)
            );
            $( api.column( 6 ).footer() ).html(
                sumVal(6).toFixed(8)
            );
        }
    });

    $('#user-funds tbody').on('click', 'tr', function () {
        var tr = $(this)
        var row = table.row( tr );
 
        if ( row.child.isShown() ) {
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            var name = tr.find("a").text();

            $.ajax('/api/user_transactions/' + name, {
                contentType : 'application/json',
                type : 'GET',
                success: function(data){
                    row.child(format(name, data)).show();
                    tr.addClass('shown');
                },
            });
        }
    } );

    /* Create export buttons */
    TableExport(document.getElementsByTagName("table"), {
        formats: ['csv', 'txt']
    });
});
