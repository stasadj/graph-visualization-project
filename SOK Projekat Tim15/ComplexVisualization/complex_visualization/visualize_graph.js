
//dobijamo visinu/sirinu broswer prozora
function getWidth() {
  return Math.max(
    document.body.scrollWidth,
    document.documentElement.scrollWidth,
    document.body.offsetWidth,
    document.documentElement.offsetWidth,
    document.documentElement.clientWidth
  );
}

function getHeight() {
  return Math.max(
    document.body.scrollHeight,
    document.documentElement.scrollHeight,
    document.body.offsetHeight,
    document.documentElement.offsetHeight,
    document.documentElement.clientHeight
  );
}

//kreiramo svg na kome se sve renderuje
var svg = d3.select("svg"),
    width = getWidth(),
    height = getHeight();

var radius = 15;

//el_type, attrs, idv, name



//pravimo simulaciju i stavljamo sile
var simulation = d3.forceSimulation().nodes(nodes_data);

var link_force =  d3.forceLink(links_data).id(function(d) { return d.id; });

var charge_force = d3.forceManyBody().strength(-400);

var center_force = d3.forceCenter(width / 2, height / 2);  //sila u centar containera

simulation.force("charge_force", charge_force)
          .force("center_force", center_force)
          .force("links",link_force);


//stavljamo onTick za updejt rendera
simulation.on("tick", tickActions );

//stavljamo grupu za container za zoom
var g = svg.append("g").attr("class", "everything");

//draw lines for the links
var link = g.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(links_data)
    .enter().append("line")
    .attr("stroke-width", 2)
    .style("stroke", linkColour);


function circleColour(d){
	if(d.element_type === "playlist"){
		return "blue";
	} else if (d.element_type === "artist"){
		return "pink";
	} else{
        return "purple";
    }
}

//draw circles for the nodes
var node = g.append("g")
        .attr("class", "nodes") //stavljamo koju klasu ce imati element
        .selectAll("circle.node")
        .data(nodes_data)
        .enter()
        .append("circle")
        .attr("class", "node")
        .attr("r", radius)
        .attr("fill", circleColour)
        .on("click", handleMouseClick)
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut);


var text = g.append("g")
    .attr("class", "labels")
    .selectAll("g")
    .data(nodes_data)
    .enter()
    .append("g")
    .append("text")
    .attr("x", 14)
    .attr("y", ".31em")
    .style("font-family", "sans-serif")
    .style("font-size", "0.7em")
    .text(function (d) { return d.name; });


//add drag capabilities
var drag_handler = d3.drag()
	.on("start", drag_start)
	.on("drag", drag_drag)
	.on("end", drag_end);

drag_handler(node);

//add zoom capabilities
var zoom_handler = d3.zoom()
    .on("zoom", zoom_actions);

zoom_handler(svg);

var label = node.append("text")
      .text(function(d) {
        return d.name;
      })
      .attr('x', 6)
      .attr('y', 3);



//dodavanje onog tool tipa -- d je node
var div = d3.select("div.tooltip");

function handleMouseOver(d, i) {
    d3.select(this).transition()
        .duration(500)
        .attr("r", 24);
    toolBoxIn(d);
}

function handleMouseOut(d, i) {
    d3.select(this).transition()
        .duration(500)
        .attr("r", 15);
    toolBoxOut(d);
}

function handleMouseClick(d,i){}


//"title": "UKF 2018 DRAMnBASS", "creator": "Spotty", "duration": "1:44:11", "picture": "https://api.deezer.com/playlist/4268172382/image"
function toolBoxIn(d){
    if(d.attrs !== ""){
        div.style("visibility", "visible")
        .transition()
        .duration(200)
        .style("opacity", .9);
        if(d.element_type === "track")
            var html = `Duration: ${d.atributes.duration}`;
        else if(d.element_type === "artist")
            var html = `Name: ${d.atributes.name} <br/>`;
        else{
             var html = `Duration: ${d.atributes.duration}`;
        }

        //uzimamo poziciju misa za koordinate tooltipa
        div.html(html)
        .style("top", (d3.event.pageY + 16) + "px")
        .style("left", (d3.event.pageX + 16) + "px");
    }
}

function toolBoxOut(d){
    div.transition()
        .duration(500)
        .style("opacity", 0)
        .each("end", function(){
        div.style("visibility", "hidden")
        });
}



function linkColour(d){
	return "blue";
}

function drag_start(d) {
 if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

//kako ne bi radio drag van continera
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
    //updejt iscrtanih komponenti na svaki takt
    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    text
        .attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; });
}