var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var radius = 15;

var tcColours = ['#FDBB30', '#EE3124', '#EC008C', '#F47521', '#7AC143', '#00B0DD'];

var randomTcColour = function() {
  return Math.floor(Math.random() * tcColours.length);
};

var simulation = d3.forceSimulation()
					.nodes(nodes_data);

var link_force =  d3.forceLink(links_data)
                        .id(function(d) { return d.id; });

var charge_force = d3.forceManyBody()
    .strength(-100);

var center_force = d3.forceCenter(width / 2, height / 2);

simulation
    .force("charge_force", charge_force)
    .force("center_force", center_force)
    .force("links",link_force)
 ;

simulation.on("tick", tickActions );

var g = svg.append("g")
    .attr("class", "everything");

var link = g.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(links_data)
    .enter().append("line")
      .attr("stroke-width", 2)
      .style("stroke", tcColours[randomTcColour()]);

var node = g.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(nodes_data)
        .enter()
        .append("circle")
        .attr("r", radius)
        .attr("fill", tcColours[randomTcColour()]);

var label = g.append("g")
    .attr("class", "label")
    .selectAll(null)
    .data(nodes_data)
    .enter()
    .append("text")
    .text(empty_string)
    .style("text-anchor", "middle")
    .style("fill", "#555")
    .style("font-family", "Arial")
    .style("font-size", 12)
    .style("font-weight", "bold");

var drag_handler = d3.drag()
	.on("start", drag_start)
	.on("drag", drag_drag)
	.on("end", drag_end);


drag_handler(node);
drag_handler(label);

var zoom_handler = d3.zoom()
    .on("zoom", zoom_actions);

zoom_handler(svg);

function empty_string(d){
	if(d.name ==""){
		return d.element_type;
	} else {
		return d.name;
	}
}

function drag_start(d) {
 if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function drag_drag(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function drag_end(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

function zoom_actions(){
    g.attr("transform", d3.event.transform)
}

function tickActions() {

       node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    label.attr("x", function(d){ return d.x; })
        .attr("y", function (d) {return d.y ; });
}