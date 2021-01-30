$(document).ready(function() {
    $('#source_select').change(function() {
       var selected = $(this).val();

       $('#playlist_link').css('display','none');
       $('#xml_file').hide();
       $('#load_data').hide();

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
});