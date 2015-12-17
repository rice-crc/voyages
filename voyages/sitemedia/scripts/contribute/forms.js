function VoyageSelection(url, initialSelection, allowMultiple) {
    var self = this;
    this.allowMultiple = allowMultiple;
    this.selection = initialSelection || [];

    if (self.selection.length > 0) {
        $('#results_table').show();
    }

    this.lookUp = function () {
        var lookUpId = parseInt($('#voyage_id_input').val());
        if (self.selection.indexOf(lookUpId) != -1) {
            alert(gettext('Voyage already added to selection'));
            return;
        }
        $.post(
            url,
            { "voyage_id": lookUpId },
            function(data) {
                if (data.hasOwnProperty('error')) {
                    alert(data.error);
                } else {
                    self.selection.push(lookUpId);
                    $('#results_table > tbody:last-child').append('<tr id="row_' + data.voyage_id + '"><td>' +
                        data.voyage_id +
                        '</td><td>' + data.captain + '</td>' +
                        '</td><td>' + data.ship + '</td>' +
                        '</td><td>' + data.year_arrived + '</td>' +
                        '<td><a href="#" onclick="selection.remove(' + data.voyage_id + '); return false;">x</a></td></tr>');
                    $('#results_table').show();
                    $('#voyage_id_input').val('');
                }
            });
    };

    this.remove = function(id) {
        var index = self.selection.indexOf(id);
        if (index >= 0) {
            self.selection.splice(index, 1);
        }
        $('#row_' + id).remove();
        if (self.selection.length == 0) $('#results_table').hide();
    };

    this.submitForm = function() {
        $('#delete_ids_hidden').val(self.selection.join());
        $('form').submit();
    };
}