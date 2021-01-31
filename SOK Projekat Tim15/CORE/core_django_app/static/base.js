$(document).ready(function() {
    $('#source_select').change(function() {
        var selected = $(this).val();

        $('#playlist_link').css('display','none');
        $('#xml_file').hide();
        $('#load_data').hide();
        $('#message1').hide();

        if (selected === 'XMLDataLoader') {
            $('#xml_file').show();
            $('#load_data').show();
        }

        if (selected === 'DeezerDataLoader') {
            $('#playlist_link').css('display','block');
            $('#playlist_link').width('98%');
            $('#load_data').show();
        }

    });

    $('#visualization_select').change(function() {
        var selected = $(this).val();

        $('#visualize_bttn').attr('disabled');

        if (selected === 'SimpleVisualization') {
            $('#visualize_bttn').removeAttr('disabled');
        }

        if (selected === 'ComplexVisualization') {
            $('#visualize_bttn').removeAttr('disabled');
        }

    });

    $('').submit(function(event) {
        event.preventDefault();
        var formData = new FormData($(this)[0]);

        $.post({
				url: '/load/data',
				data: formData,
				success: function(pacijent) {
					alert("OK")
				}
			});
    });

    $('').submit(function(event) {
        event.preventDefault();
        var serializedData = $(this).serialize();

        $.post({
				url: '/visualize/data',
				data: serializedData,
				success: function(pacijent) {
					alert("OK")
				}
			});
    });
});