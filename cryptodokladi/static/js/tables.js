function format ( d ) {
    table = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">';
    for (i = 0; i < d.length; i++){
        table += 
        '<tr>'+
            '<td>'+d[i].token+'</td>'+
            '<td>'+d[i].value+'</td>'+
            '<td>'+d[i].sender+'</td>'+
            '<td>'+d[i].timestamp+'</td>'+
        '</tr>';
    }
    table += '</table>';

    return table;
}

$(document).ready( function () {
    var table = $('#user-funds').DataTable();

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
                    row.child(format(data)).show();
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
