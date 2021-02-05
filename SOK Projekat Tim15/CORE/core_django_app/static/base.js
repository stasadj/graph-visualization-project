var selected_node_id = 0;

function handleMouseClick(d) {

    d3.selectAll('.node').each(function(d){
            d3.select(`#v${d.id} > *`)
                .attr("stroke", "black")
                .attr("stroke-width", 0.5);
    });

    if (selected_node_id  === d.id){
        selected_node_id = 0;
    }
    else {
        selected_node_id = d.id;

        d3.select(`#v${selected_node_id} > *`)
            .attr("stroke", function(d){
                 return "black";
            })
            .attr("stroke-width", 3);
    }

    $('.jqtree-element').each(function() {
        var node = $('#tree_view').tree('getNodeByHtmlElement', $(this));
        if (node.id === selected_node_id) {
            $(this).css('background-color', '#eb9334');
            node.selected = true;
        } else {
            $(this).css('background-color', 'transparent');
            node.selected = false;
        }
        });

    st = d.id + " " + d.name + "<br>";
    attributes = d.atributes;

    Object.keys(attributes).forEach(function(key) {
        st += key + " " + attributes[key] + "<br>";
    });

    $("#selected_info").html(st);


}

$(document).ready(function() {
    $('#source_select').change(function() {
        var selected = $(this).val();

        $('#playlist_link').css('display','none');
        $('#xml_file').hide();
        $('#load_data').hide();
        $('#message1').hide();
         $('#visualization_form').hide();

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


    d3.selectAll('.node').on("click", handleMouseClick);

});