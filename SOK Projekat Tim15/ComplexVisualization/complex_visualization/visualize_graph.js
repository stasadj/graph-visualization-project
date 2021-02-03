


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
  var svg = d3.select("#main_view_svg"), //TODO #main_svg
      width = getWidth(),
      height = getHeight();


var width_rect = 250;
var colorList = [];


//pravimo simulaciju i stavljamo sile
var simulation = d3.forceSimulation().nodes(nodes_data);

var link_force =  d3.forceLink(links_data).id(function(d) { return d.id; });

var charge_force =  d3.forceManyBody().strength(-3500);

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
  .selectAll(".link")
  .data(links_data)
  .enter().append("line")
  .attr('class', 'link')
  .attr("stroke-width", 2)
  .style("stroke", linkColour);


function makeColorTypeList(node){
  const type = node.element_type;
  const isInArray = colorList.some(e => e.hasOwnProperty(type));
  if(!isInArray){
      //pastels
      var hue = 360 * Math.random();
      var saturation = (25 + 70 * Math.random());
      var light = (85 + 10 * Math.random());
      const color = "hsl(" + hue + ',' + saturation + '%,' + light + '%)';
      const colorDarker = "hsl(" + hue + ',' + saturation + '%,' + light + 30 + '%)';
      const el = { type: `${type}`, value: `${color}`, valueDarker: `${colorDarker}`};
      colorList.push(el);
  }
}

function rectColour(d){
  makeColorTypeList(d);
  return colorList.find(x => x.type === d.element_type).value;
}

var node = g.append("g")
      .attr("class", "nodes") //stavljamo koju klasu ce imati element
      .selectAll(".node")
      .data(nodes_data)
      .enter()
      .append("g")
      .attr("class", "node")
      .attr('id', function(d){
          return "v" + d.id});



var clickedNodeId = "";

function addElements(d){
      var widthRect = width_rect;
      var attributes = (Object.entries(d.atributes));
      var categoryNum = attributes.length;
      var textSize = 10;
      var height = categoryNum*textSize + 30;

      d3.select("#v" + d.id)
          .append('rect')
          .attr("stroke", function(){
              return "black";
          })
          .attr("stroke-width", 0.5)
          .attr('width',widthRect)
          .attr('height',height)
          .attr('fill',rectColour)
          .on("click", function(d){
               let temp = "v" + d.id;
               //ako je prvi put kliknut
               console.log(clickedNodeId);
               if(clickedNodeId  !== temp || clickedNodeId === ""){
                   //this postaje crven
                    d3.select(this)
                      .attr("stroke", "red")
                      .attr("stroke-width", 3);
                    //stari postaje Normalan
                   d3.select("#" + clickedNodeId)
                      .attr("stroke", "black")
                      .attr("stroke-width", 0.5);
                   //postavljamo novi crveni kliknut
                    clickedNodeId = "v" + d.id;
               }else{
                   //ako je node vec bio kliknut onda vracamo na default
                     d3.select(this)
                      .attr("stroke", "black")
                      .attr("stroke-width", 0.5);
                      clickedNodeId = ""; //ni jedan nije selektovan
               }

          })
          .on("mouseover", function (d) {
              let temp = "v" + d.id;
              if(clickedNodeId !== temp){
                   d3.select(this)
                      .attr("stroke", function(d){
                          return "black";
                      })
                      .attr("stroke-width", 3);
              }else{
                  d3.select(this)
                      .attr("stroke", "red")
                      .attr("stroke-width", 3);
              }

          })
          .on("mouseout", function(d){
              let temp = "v" + d.id;
              if(clickedNodeId !== temp){
                  d3.select(this)
                      .attr("stroke", "black")
                      .attr("stroke-width", 0.5);
              } else {
                  d3.select(this)
                      .attr("stroke", "red")
                      .attr("stroke-width", 3);
              }
          });


      d3.select("#v" + d.id)
          .append('text')
          .attr('x',widthRect/2)
          .attr('y',15)
          .attr('text-anchor','middle')
          .attr('font-size',textSize)
          .attr('font-family','sans-serif')
          .attr('fill','green')
          .text(function(d){
              return d.element_type + ": " + d.name;
          });

      d3.select("#v" + d.id)
          .append('line')
          .attr('x1',0) //pocetak
          .attr('y1',textSize + 10)
          .attr('x2',widthRect) //kraj
          .attr('y2',textSize + 10)
          .attr('stroke','gray')
          .attr('stroke-width',1);

        for(var i=0;i<categoryNum;i++)
        {
          d3.select("#v" + d.id)
              .append('text')
              .attr('x',5)
              .attr('y',30+i*textSize)
              .attr('text-anchor','start')
              .attr('font-size',textSize)
              .attr('font-family','sans-serif')
              .attr('fill','black')
              .text(function(d){
                  return attributes[i][0] + ": " + attributes[i][1];
              });

        }
  }


  d3.selectAll('.node').each(function(d){
      addElements(d);
  });

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

  function handleMouseOver() {

  }
  //
  // function handleMouseOut() {
  //     //moramo da proverimo da li je kliknut
  //
  //
  // }
  //
  // function handleMouseClick(d,i){
  //     console.log(d.id + " name " + d.name);
  //      d3.select(this)
  //         .attr("stroke", "black")
  //         .attr("stroke-width", 0.5);
  // }

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

      node
          .attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";});
      //  node
      //     .attr("transform", function(d) {return `translate(
      //           ${(d.source.x + d.target.x)/2},
      //           ${(d.source.y + d.target.y)/2})`;
      //     });

      link
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

  }