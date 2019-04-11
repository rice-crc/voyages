function setup() {
    var self = this;

    // Keep the line below.
    voyagesMap.addLayer(L.polyline(L.latLng(0, 0), L.latLng(0, 0)));

    var selectedRoute = null;
    var closeToolTip = function() {
        $('#tooltip').hide();
        svg.selectAll('.selected')
            .style('opacity', 0)
            .classed('selected', false);
        if (selectedRoute) {
            voyagesMap.removeLayer(selectedRoute);
            selectedRoute = null;
        }
    };

    // SVG + leaflet integration.
    var map = voyagesMap._map;
    var svg = d3.select(map.getPanes().overlayPane).append("svg");
    var g = svg.append("g").attr("class", "leaflet-zoom-hide");
    // Set SVG size and position within map.
    var positionSvg = function() {
        var bounds = map.getBounds();
        var topLeft = map.latLngToLayerPoint(bounds.getNorthWest());
        var bottomRight = map.latLngToLayerPoint(bounds.getSouthEast());
        svg.attr("width", bottomRight.x - topLeft.x)
           .attr("height", bottomRight.y - topLeft.y)
           .style("left", topLeft.x + "px")
           .style("top", topLeft.y + "px");
        g.attr("transform", "translate(" + -topLeft.x + "," + -topLeft.y + ")");
        if (isPaused) {
            g.selectAll(".animation_voyage_group").each(function() {
                var latLng = $(this).data("latLng");
                if (latLng) {
                    var point = map.latLngToLayerPoint(latLng);
                    d3.select(this).attr("transform", "translate(" + point.x + "," + point.y + ")");
                }
            });
        }
    };
    map.on("zoomend", positionSvg);

    var tooltip = $("#tooltip");

    var animationIndex = 0;
    var isPaused = false;
    var pendingTransitions = 0;
    var years = [];
    var yearStep = function() {};
    var pendingStep = false;
    var animationTime = 0;
    
    // Ensure that each data object has a smooth route
    // and an interpolation method for determining the
    // point along the curve for a constant speed unit
    // time traversal.
    var pathPreload = function(item) {
        if (!item.hasOwnProperty('smoothedRoute')) {
            var path = [];
            for (var j = 0; j < item.route.length; ++j) {
                var pt = item.route[j];
                path.push(L.latLng(pt[0], pt[1]));
            }
            //path = voyagesMap._smoothPolyline(path);
            item.smoothedRoute = path;
            var arcs = [];
            var totalAngle = 0;
            for (var j = 0; j < path.length - 1; ++j) {
                var a = {y: path[j].lat, x: path[j].lng };
                var b = {y: path[j + 1].lat, x: path[j + 1].lng };
                var arc = new GreatCircle(a, b);
                arcs.push(arc);
                totalAngle += arc.g;
            }
            item.interpolate = function(time) {
                if (time < 1.0 && time >= 0) {
                    var angle = totalAngle * time;
                    for (var j = 0; j < arcs.length; ++j) {
                        var arc = arcs[j];
                        if (angle < arc.g) {
                            return arc.interpolate(angle / arc.g);
                        }
                        angle -= arc.g;
                    }
                }
                return [d.destination_lng, d.destination_lat];
            };
        }
    };

    var animation = function(data) {
        $("#timeControls").show();
        // Sort by year, break ties by id.
        years = d3.nest()
            .key(function(d) { return d.year; })
            .sortKeys(d3.ascending)
            .sortValues(function(a, b) { return a.voyage_id - b.voyage_id; })
            .entries(data);
        $("#slider").slider({
            value: 0,
            min: 0,
            max: years.length - 1,
            step: 1,
            slide: function( event, ui ) {
                changePausedState(true);
                g.selectAll(".animation_voyage_group").transition().duration(0);
                g.selectAll(".animation_voyage_group").remove();
                animationIndex = ui.value;
                changePausedState(false);
                if (!pendingStep) {
                    pendingStep = true;
                    window.setTimeout(yearStep, 500);
                }
            }
        });
        yearStep = function() {
            if (animationIndex >= years.length || animationIndex < 0 || isPaused) {
                changePausedState(true);
                return;
            }
            try {
                pendingStep = false;
                $("#slider").slider('value', animationIndex);
                positionSvg();
                var year = years[animationIndex].key;
                var yearData = years[animationIndex].values;
                for (var i = 0; i < yearData.length; ++i) {
                    var item = yearData[i];
                    pathPreload(item);
                }
                $("#yearLabel").text(year);
                var counter = 0;
                animationTime = 0;
                var selection = g.selectAll(".animation_voyage_group")
                    .data(yearData)
                    .enter()
                    .append("g")
                    .classed("animation_voyage_group", true);
                selection
                    .append("circle")
                    .classed("animation_voyage_outer_circle", true)
                    .attr("r", 10)
                    .style("opacity", 0)
                    .on("mouseover", function() {
                        $(this).animate({ opacity: 1 }, 300);
                    })
                    .on("mouseout", function() {
                        if (!d3.select(this).classed("selected")) {
                            $(this).animate({ opacity: 0 }, 300);
                        }
                    })
                    .on("click", function() {
                        closeToolTip();
                        d3.select(this).classed("selected", true);
                        var d = this.__data__;
                        selectedRoute = L.geodesic([d.smoothedRoute], {
                            weight: 3,
                            color: "red",
                            className: "animation_selected_route"
                        });
                        voyagesMap.addLayer(selectedRoute);
                        // Set tooltip content.
                        var content = $("#tooltip_content");
                        content.attr("class", "animation_voyage_content flag_" + d.ship_nationality_id);
                        var template = '<h1>' + (d.ship_name != "" ? d.ship_name : "&nbsp;") + "</h1>";
                        if (d.ship_nationality_name != "") {
                            template += "<h2>" + d.ship_nationality_name + "</h2>";
                        }
                        if (d.ship_ton) {
                            template += "<p>This {ton}ship left {source} with {embarked} enslaved people and arrived in {destination} with {disembarked}.</p>";
                            var tonNum = parseInt(d.ship_ton);
                            template = template.replace("{ton}", tonNum ? (tonNum + ' ton ') : '');
                        } else {
                            template += "<p>This ship left {source} with {embarked} enslaved people and arrived in {destination} with {disembarked}.</p>";
                        }
                        template = template.replace("{source}", d.source_name)
                            .replace("{destination}", d.destination_name)
                            .replace("{embarked}", d.embarked)
                            .replace("{disembarked}", d.disembarked);
                        content.html(template + '<span class="animation_tooltip_moreinfo"><a target="_blank" href="/voyage/' + d.voyage_id + '/variables">' +
                            "More info »</a></span>");
                        // Position and show tooltip.
                        tooltip.show();
                        var rCirc = this.getBoundingClientRect();
                        var rSvg = document.getElementById('map').getBoundingClientRect();
                        var tooltip_width = tooltip.width();
                        var tooltip_height = tooltip.height();
                        var top = rCirc.bottom - rSvg.top + 50;
                        if (top + tooltip_height + 120 > rSvg.bottom) {
                            top -= tooltip_height + 100;
                        }
                        tooltip.animate({
                            left: ((rCirc.left + rCirc.right) / 2 - rSvg.left - tooltip_width / 2 - 20) + "px",
                            top: top + "px",
                            opacity: 0.9
                        }, 800);
                    });
                selection
                    .append("circle")
                    .classed("animation_voyage_inner_circle", true)
                    .attr("r", 2);
                applyTransition(selection, 0);
            } catch (e) {
                console.log(e);
            }
        };
        yearStep();
    };

    var applyTransition = function(selection, startTime) {
        if (animationIndex >= years.length || animationIndex < 0 || isPaused) return;
        var duration = 1500 * (1 - startTime);
        var yearData = years[animationIndex].values;
        pendingTransitions = 0;
        selection.transition()
            .duration(duration)
            .ease("linear")
            .attrTween("transform", function(d, i, a) {
                return tween(d, i, a, yearData.length, startTime, this);
            })
            .each("start", function() {
                ++pendingTransitions;
            })
            .each("end", function() {
                --pendingTransitions;
                d3.select(this).remove();
            });
    };

    var changePausedState = function(state) {
        isPaused = state;
        if (isPaused) {
            $("#pauseBtn").hide();
            $("#playBtn").show();
        } else {
            closeToolTip();
            $("#pauseBtn").show();
            $("#playBtn").hide();
        }
    };

    var tick = function() {
        if (pendingTransitions == 0 && !isPaused) {
            if (++animationIndex < years.length) {
                yearStep();
            }
        }
    };

    var tween = function(d, i, a, count, startTime, dom) {
        if (!d) return function () {};
        pathPreload(d);
        startTime = parseFloat(startTime);
        return function(t) {
            t = startTime + t * (1 - startTime);
            if (t > animationTime) {
                animationTime = t;
            }
            var x = i / (2 * count);
            if (t > x) {
                t = (t - x)/(1 - x);
            } else {
                t = 0;
            }
            if (t >= 1) return "";
            var lngLat = d.interpolate(t);
            if (isNaN(lngLat[0]) || isNaN(lngLat[1])) {
                console.log('Interpolation error');
                return "";
            }
            var latLng = L.latLng(lngLat[1], lngLat[0]);
            $(dom).data("latLng", latLng);
            var point = map.latLngToLayerPoint(latLng);
            return "translate(" + point.x + "," + point.y + ")";
        };
    };

    $("#pauseBtn").click(function(e) {
        changePausedState(true);
        g.selectAll(".animation_voyage_group").transition().duration(0);
        e.preventDefault();
    });
    $("#playBtn").click(function(e) {
        changePausedState(false);
        var selection = g.selectAll(".animation_voyage_group");
        if (selection) {
            applyTransition(selection, animationTime);
        }
        e.preventDefault();
    });
    $('.animation_tooltip_close_button').click(closeToolTip);

    self.timerId = null;
    self.startAnimation = function(data) {
        animation(data);
        svg.attr('visibility', 'visible');
        self.timerId = window.setInterval(tick, 1000);
    };
    self.stopAnimation = function() {
        if (self.timerId) {
            window.clearInterval(self.timerId);
        }
        svg.attr('visibility', 'hidden');
    };
    self.reset = function() {
        animationIndex = 0;
        $("#slider").slider('value', 0);
        $("#yearLabel").text(years.length > 0 ? years[0].key : '');
    };
    return self;
}

var animationHelper = new setup();