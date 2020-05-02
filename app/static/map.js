//US Map
    map_dims = document.getElementById('USMap').getBoundingClientRect()
    map_width = map_dims.width.toString()
    map_height = map_dims.height.toString()
    active = d3.select(null);
    var map_svg = d3.select("div#USMap")
                .append("svg")
                .attr("preserveAspectRatio", "xMinYMin meet")
                .attr("viewBox", "0 0 " + map_width + " " + map_height)
                .classed("svg-content", true);


      map_svg.append('rect')
            .attr('class', 'background center-container')
            .attr('height', map_height)
            .attr('width', map_width)
            .on('click', clicked);

    var projection = d3.geoAlbersUsa()
                       .scale(map_width*1.35)
                       .translate([map_width / 2, map_height / 2]);
        
    var path = d3.geoPath()
                 .projection(projection);

    d3.queue()
      .defer(d3.json, "static/us.json")
      .await(ready);

    var g = map_svg.append("g")
            .attr('class', 'center-container center-items us-state')
           

    //Represents current transformation of map
    current_transform = null
    current_scale = null

    default_date = "4/28/20"

    //Allows python variables from Flask server to be received
    $.extend({
        getFlaskVars: function(url) {
            var response = null;
            $.ajax({
                url: url,
                type: 'GET',
                dataType: 'json',
                async: false,
                success: function(data) {
                    response = data;
                }
            });
            return response;
        }
    });

    //Allows json POST request to be sent to Flask server to be received
    $.extend({
        postFlaskVars: function(url,json_data) {
            var response = null;
            $.ajax({
                url: url,
                type: 'POST',
                data: JSON.stringify(json_data),
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                async: false,
                success: function(data) {
                    response = data;
                }
            });
            return response;
        }
    });

/*$.ajax({
          type: "POST",
          url: "/getdata",
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(asdf),
          success: function(x) {
            console.log(x)
           },
          dataType: "json"
        });
*/

    function ready(error, us) {
        
/*            var results = $.getFlaskVars("/getmapdata");
            console.log(results)*/
            var county_colorings = $.postFlaskVars("/getmapdata",{"date": default_date});
            console.log(county_colorings)
            console.log(county_colorings["90021"])
            if (error) throw error;
             g.append("g")
                .attr("id", "counties")
                .selectAll("path")
                .data(topojson.feature(us, us.objects.counties).features)
                .enter().append("path")
                .style("fill",function(d) {
                    return county_colorings[d.id]
                })
                .attr("d", path)
                .attr("class", "county-boundary")
                .on("click", reset);

            g.append("g")
                .attr("id", "states")
                .selectAll("path")
                .data(topojson.feature(us, us.objects.states).features)
                .enter().append("path")
                .attr("d", path)
                .attr("class", "state")
                .on("click", clicked);


            g.append("path")
                .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
                .attr("id", "state-borders")
                .attr("d", path);

    }

    function clicked(d) {
            if (d3.select('.background').node() === this) return reset();

            if (active.node() === this) return reset();

            active.classed("active", false);
            active = d3.select(this).classed("active", true);

            var bounds = path.bounds(d),
                dx = bounds[1][0] - bounds[0][0],
                dy = bounds[1][1] - bounds[0][1],
                x = (bounds[0][0] + bounds[1][0]) / 2,
                y = (bounds[0][1] + bounds[1][1]) / 2,
                scale = .9 / Math.max(dx / map_width, dy / map_height),
                translate = [map_width / 2 - scale * x, map_height / 2 - scale * y];
                current_scale = scale
                current_transform = translate

            g.transition()
                .duration(750)
                .style("stroke-width", 1.5 / scale + "px")
                .attr("transform", "translate(" + translate + ")scale(" + scale + ")");
        }


        function reset() {
            active.classed("active", false);
            active = d3.select(null);
            g.transition()
                .delay(100)
                .duration(750)
                .style("stroke-width", "1.5px")
                .attr("transform", "translate(" - current_transform + ")scale(" - current_scale + ")");

        }