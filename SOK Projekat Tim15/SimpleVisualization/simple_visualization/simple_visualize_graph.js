function getWidth() {
  return Math.max(
    document.body.scrollWidth,
    document.documentElement.scrollWidth,
    document.body.offsetWidth,
    document.documentElement.offsetWidth,
    document.documentElement.clientWidth
  );
};

function getHeight() {
  return Math.max(
    document.body.scrollHeight,
    document.documentElement.scrollHeight,
    document.body.offsetHeight,
    document.documentElement.offsetHeight,
    document.documentElement.clientHeight
  );
};

//kreiramo svg na kome se sve renderuje
var svg = d3.select("#main_view_svg"),
    width = getWidth(),
    height = getHeight();

var radius = 20;

var tcColours = ['#FAAB36', '#249EA0'];


var simulation = d3.forceSimulation()
					.nodes(nodes_data);

var link_force =  d3.forceLink(links_data)
                        .id(function(d) { return d.id; });

var charge_force = d3.forceManyBody()
    .strength(-3500);

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
    .style("stroke", tcColours[1]);

var tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("white-space", "pre")
    .style("display", "flex")
    .style("border-radius","15px")
    .style("justify-content", "flex-start")
    .style("visibility", "hidden")
    .style("font-family", "Arial")
    .style("font-size", 15)
    .style("font-weight", "bold")
    .style("background", tcColours[0])
    .text("");

var node = g.append("g")
        .attr("class", "nodes")
        .selectAll(".node")
        .data(nodes_data)
        .enter()
        .append("g")
        .attr("class", "node")
        .attr('id', function(d){
          return "v" + d.id})
        .append("circle")
        .attr("stroke-width", 0.5)
        .attr("r", radius)
        .attr("fill", tcColours[0])
        .on("mousedown", function(){return tooltip.style("visibility", "hidden").text("");})
        .on("mouseover", function(d){return tooltip.style("visibility", "visible").text(json_petty(d.atributes));})
        .on("mousemove", function(){return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
        .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

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
    .style("font-size", 20)
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

function json_petty(atr)
{
    var str_json = "\n";
    for (const key in atr) {
            str_json += "\t" + key.charAt(0).toUpperCase() + key.slice(1) + ": " + atr[key] + "\t\n";
        }
     str_json += "\n"
    return str_json;
}

function empty_string(d){
	return d.element_type + ": " + d.name;
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

    label
        .attr("x", function(d){ return d.x; })
        .attr("y", function (d) {return d.y ; });
}
