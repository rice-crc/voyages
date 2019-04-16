// Scripts for the timelapse animation of voyages in the map.

var DEFAULT_TIMER_RESOLUTION = 40; // milliseconds

var _now = function () { return (new Date()).getTime(); };

// Represents a route on the globe using lat/lng coordinates.
function Route(points) {
    var self = this;
    self.points = points;
    var arcs = [];
    var angles = [];
    var totalAngle = 0;
    var latLngs = [];
    for (var j = 0; j < points.length - 1; ++j) {
        var a = { y: points[j][0], x: points[j][1] };
        var b = { y: points[j + 1][0], x: points[j + 1][1] };
        var arc = new GreatCircle(a, b);
        arcs.push(arc);
        angles.push(arc.g);
        totalAngle += arc.g;
        latLngs.push(L.latLng(a.y, a.x));
        if (j == points.length - 2) {
            latLngs.push(L.latLng(b.y, b.x));
        }
    }
    self.latLngs = latLngs;
    // Create an interpolation function with perturbation parameters (pX, pY).
    // The interpolation function receives as argument a number from [0, 1.0]
    // and returns a [lat, lng] pair (Array) corresponding to the perturbed
    // position along the route which corresponds to the given percentage of
    // the path 
    self.createInterpolation = function (pLng, pLat) {
        var lastTime = 0;
        var lastPointIdx = 0;
        var lastAngle = 0;
        if (angles.length == 0) return function () { return [0.0, 0.0] };
        return function (time) {
            if (time < 0) time = 0;
            if (time > 1.0) time = 1.0;
            // Save computation time by using last cached data.
            var from_idx = lastPointIdx;
            var currentAngle = time * totalAngle;
            if (time < lastTime) {
                lastAngle = 0;
                from_idx = 0;
            }
            var idx = from_idx;
            while (idx < angles.length - 1 && lastAngle + angles[idx] < currentAngle) {
                lastAngle += angles[idx];
                ++idx;
            }
            if (idx >= angles.length) idx = angles.length - 1;
            // Update cache.
            lastTime = time;
            lastPointIdx = idx;
            // Compute the result by interpolating on the (now) current arc.
            var pt = arcs[idx].interpolate((currentAngle - lastAngle) / angles[idx]);
            // The perturbation is minimal at the beginning and end of the route,
            // being larger on the middle of the path.
            var factor = time * (1.0 - time);
            return [pt[0] + factor * pLng, pt[1] + factor * pLat];
        };
    };
}

function Voyage(routeIdx, src, dst, start, finish, data) {
    this.routeIdx = routeIdx;
    this.src = src;
    this.dst = dst;
    this.start = ~~start;
    this.finish = ~~finish;
    this.data = data;
    var rnd = function () { return ~~Math.round(128 * Math.random()); };
    this.color = "rgb(" + rnd() + "," + rnd() + "," + rnd() + ")";
}

var LAT_MAX_PERTURBATION = 4;
var LNG_MAX_PERTURBATION = 4;

// Creates an animation model object that is responsible for 
// determining the position of all ships in the given time frame.
function AnimationModel(routes, voyages) {
    var self = this;
    self._routes = [];
    for (var i = 0; i < routes.length; ++i) {
        self._routes.push(new Route(routes[i]));
    }
    self._voyages = [];
    var lastFinish = 0;
    // Initialize voyage interpolation functions.
    for (var i = 0; i < voyages.length; ++i) {
        var v = Object.assign({}, voyages[i]);
        if (v.finish >= lastFinish) {
            lastFinish = v.finish + 1;
        }
        v.duration = v.finish - v.start;
        var route = self._routes[v.routeIdx];
        v.interpolate = route.createInterpolation(
            Math.random() * LNG_MAX_PERTURBATION,
            Math.random() * LAT_MAX_PERTURBATION);
        v.idx = i;
        v.latLngs = route.latLngs;
        self._voyages.push(v);
    }
    // Sort voyages by start time so that determining the active voyages in a given timeframe is much faster.
    self._voyages.sort(function (a, b) { return a.start - b.start; });
    // Cache starting index of voyage for time period.
    var lastTime = 0;
    var lastWindowStart = 0;
    var nvoyages = self._voyages.length;
    self.getWindow = function (time) {
        var result = [];
        if (time == lastFinish) return []; // Ensure that we report empty results at the very end.
        var from_idx = time >= lastTime ? lastWindowStart : 0;
        for (var i = from_idx; i < nvoyages; ++i) {
            var v = self._voyages[i];
            if (v.start > time) break;
            // See if we can shift the cached window start index by one.
            var isFinished = v.finish < time;
            if (from_idx == i && isFinished)++from_idx;
            if (!isFinished) {
                result.push({ idx: v.idx, voyage: v, position: v.interpolate((time - v.start) / v.duration) });
            }
        }
        lastWindowStart = from_idx;
        lastTime = time;
        return result;
    };
    self.getFirstStartTime = function () {
        return nvoyages > 0 ? self._voyages[0].start : 0;
    };
    self.getLastFinishTime = function () {
        return lastFinish;
    };
}

/**
 * Creates an animation control which initializes a timer and triggers UI
 * updates via callback function.
 * @param {*} routes The set of pre-compiled, smooth, routes as an array of [lng, lat].
 * @param {*} voyages The set of voyages to display.
 * @param {*} timerResolution The interval between timer ticks.
 * @param {*} timeStepPerSec How much simulate time is increased every real second.
 * @param {*} onRender The callback that renders ongoing voyages. The arguments to the
 * callback are (simulated_time, [{ idx, voyage, position }, ...])
 */
function AnimationControl(routes, voyages, timerResolution, timeStepPerSec, onRender) {
    var self = this;
    var model = new AnimationModel(routes, voyages);
    var lastRealTime = null;
    var lastSimTime = -1;
    var maxTime = model.getLastFinishTime();
    var minTime = model.getFirstStartTime();
    self._timer = null;
    self._paused = false;
    var setStepPerSec = function (stepPerSec) {
        timeStepPerSec = stepPerSec || 1;
        timerResolution = timerResolution || DEFAULT_TIMER_RESOLUTION;
        if (timerResolution * timeStepPerSec < 500.0) {
            // Ensure that the resolution is not too fine 
            // (e.g. multiple ticks would be required for
            // an increase in simulated time).
            timerResolution = 500.0 / timeStepPerSec;
        }
        if (self._timer != null) {
            window.clearInterval(self._timer);
        }
        self._timer = window.setInterval(tick, timerResolution);
    }
    var setSimTime = function (nextSimTime) {
        nextSimTime = ~~nextSimTime;
        if (nextSimTime > maxTime) nextSimTime = maxTime;
        if (nextSimTime < minTime) nextSimTime = minTime;
        if (nextSimTime != lastSimTime) {
            // We only bother with updates if the 
            // simulated time has changed.
            var active = model.getWindow(nextSimTime);
            lastSimTime = nextSimTime;
            try {
                onRender(nextSimTime, active);
            } catch (e) {
                console.log('Render error!');
                console.log(e);
            }
            lastRealTime = _now();
            self._paused = self._paused || (nextSimTime >= maxTime - 0.01);
        }
    };
    var tick = function () {
        if (self._paused) return;
        // Advance the simulated time in sync with real time.
        var now = _now();
        var nextSimTime = 0;
        if (lastRealTime != null) {
            // Avoid too large gap between simulated times (which would be
            // indicative that the browser is not able to keep up with our
            // required precision).
            var elapsed = Math.min(5 * timerResolution, now - lastRealTime);
            nextSimTime = Math.round(elapsed * timeStepPerSec * 0.001 + lastSimTime);
        } else {
            nextSimTime = lastSimTime + 1;
        }
        setSimTime(nextSimTime);
    };
    setStepPerSec(timeStepPerSec);
    self.getModel = function () { return model; };
    self.isPaused = function () { return self._paused; };
    self.dispose = function () {
        if (self._timer) {
            window.clearInterval(self._timer);
            self._timer = null;
        }
    };
    self.pause = function () {
        self._paused = true;
    };
    self.play = function () {
        lastRealTime = _now();
        self._paused = false;
    };
    self.stop = function () {
        self._paused = true;
        onRender(minTime, []);
        lastSimTime = minTime - 1;
        lastRealTime = null;
    };
    self.jumpTo = setSimTime;
}

var _appendArrHelper = function (source, target, reverse, skipStart, skipLast) {
    skipStart = skipStart || 0;
    skipLast = skipLast || 0;
    var n = source.length;
    if (reverse) {
        for (var i = n - skipStart - 1; i >= skipLast; --i) {
            target.push(source[i]);
        }
    } else {
        for (var i = skipStart; i < n - skipLast; ++i) {
            target.push(source[i]);
        }
    }
};

// flatten an array of arrays.
var _flatten = function (arr) {
    var r = [];
    for (var i = 0; i < arr.length; ++i) {
        var v = arr[i];
        for (var j = 0; j < v.length; ++j) {
            r.push(v[j]);
        }
    }
    return r;
};

function _normSq(v) {
    var r = 0.0;
    for (var i = 0; i < v.length; ++i) {
        var a = v[i];
        r += a * a;
    }
    return r;
}

function _angleInfo(center, p1, p2) {
    var cx = center[0];
    var cy = center[1]
    var v1 = [p1[0] - cx, p1[1] - cy];
    var v2 = [p2[0] - cx, p2[1] - cy];
    var n1 = _normSq(v1);
    var n2 = _normSq(v2);
    var dot = v1[0] * v2[0] + v1[1] * v2[1];
    var sqrtNormProd = Math.sqrt(n1 * n2);
    return { angle: Math.acos(dot / sqrtNormProd), center: center, dot: dot, sqrtNormProd: sqrtNormProd, v1: v1, v2: v2, n1sq: n1, n2sq: n2 };
}

// Given two paths that may form a sharp corner when concatenated,
// compute an index on path2 that is not too far along the path such
// that the angle formed by the concatenation is within a threshold.
function _reduceSharpCorner(lastP1pt, second, reverse, maxPathSector, threshold) {
    if (second.length <= 3) return second;
    // Attempt to find a position further along the second path for which
    // the incidence angle is lower than the given threshold. If not found,
    // the least incidence angle on the initial segment of the path is
    // used instead.
    var p2index = 0;
    threshold = threshold || Math.PI * 0.15;
    var bestIndex = 0;
    var bestAngle = Math.PI;
    maxPathSector = maxPathSector || 0.25;
    reverse = !!reverse;
    while (p2index < second.length * maxPathSector - 1) {
        var a = reverse
            ? _angleInfo(second[second.length - p2index - 2], lastP1pt, second[second.length - 1 - p2index]).angle
            : _angleInfo(second[p2index + 1], lastP1pt, second[p2index]).angle;
        if (a < threshold) {
            bestIndex = p2index;
            break;
        }
        if (a < bestAngle) {
            bestAngle = a;
            bestIndex = p2index;
        }
        ++p2index;
    }
    // Instead of taking a direct jump from the last point in the first path
    // to the path's best incidence point, we include additional points to
    // smooth the curve. Our approach is to use a quadratic scale to ensure
    // matching tangents from both ends of the best incidence point.
    var ai = reverse
        ? _angleInfo(second[second.length - p2index - 2], lastP1pt, second[second.length - 1 - p2index])
        : _angleInfo(second[bestIndex + 1], lastP1pt, second[bestIndex]);
    var endTangentScalar = ai.sqrtNormProd / ai.n2sq;
    var endTangent = [ai.v2[0] * endTangentScalar, ai.v2[1] * endTangentScalar];
    var prefix = [];
    var NUM_POINTS = 10;
    for (var j = NUM_POINTS - 1; j >= 1; --j) {
        var lambda = reverse
            ? (NUM_POINTS - j + 0.0) / NUM_POINTS
            : (j + 0.0) / NUM_POINTS;
        var a = [ai.center[0] + lambda * ai.v1[0], ai.center[1] + lambda * ai.v1[1]];
        var b = [ai.center[0] + lambda * endTangent[0], ai.center[1] + lambda * endTangent[1]];
        var lambda2 = lambda * lambda;
        var pt = [b[0] + lambda2 * (a[0] - b[0]), b[1] + lambda2 * (a[1] - b[1])];
        prefix.push(pt);
    }
    return reverse
        ? second.slice(0, second.length - 1 - p2index).concat(prefix)
        : prefix.concat(second.slice(bestIndex));
}

/**
 * For compactness, the routes are decomposed in 3 segments.
 * This function compiles a whole path (with any required
 * smoothing at the joints) from these segments.
 * @param {*} regionSegments array[fromRegion][toRegion] gives the
 * smooth segment connecting fromRegion to toRegion.
 * @param {*} portInfo array[{ reg, path, ptype }] 
 * indicates the nearest region and a smooth segment 
 * connecting port to its regional node.
 * @param {*} routeData an array of objects with at least
 * { src, dst } fields.
 * @returns an array in sync with @param routeData which contains
 * a compiled routes (an array of [lng, lat] points).
 */
function compileRoutes(regionSegments, portSegments, routeData) {
    var result = [];
    var sources = portSegments['src'];
    var targets = portSegments['dst'];
    for (var i = 0; i < routeData.length; ++i) {
        var data = routeData[i];
        var srcInfo = sources[data.src];
        var dstInfo = targets[data.dst];
        if (!srcInfo ||
            !dstInfo ||
            !regionSegments[srcInfo.reg] ||
            !regionSegments[srcInfo.reg][dstInfo.reg]) {
            // This is a route we cannot handle...
            result.push([]);
            continue;
        }
        var first = srcInfo.path;
        var second = regionSegments[srcInfo.reg][dstInfo.reg];
        var third = dstInfo.path;
        // Smooth each of the two joins.
        var points = first.slice(0);
        // If the port-to-region/region-to-port segments
        // consist of direct paths, we will calculate the
        // angle formed by the concatenation of the paths
        // and attempt to reduce sharp corners by replacing
        // the joint point by another further along the
        // curve.
        if (points.length == 1) {
            second = _reduceSharpCorner(points[0], second);
        }
        _appendArrHelper(second, points);
        if (third.length == 1) {
            points = _reduceSharpCorner(third[0], points, true);
        }
        _appendArrHelper(third, points, true);
        result.push(points);
    }
    return result;
}

// Cache geo data in the script. 
var geoCache = {
    regionSegments: null,
    portSegments: null,
    nations: null
};

/**
 * Sets up the UI to display voyages timelapse animation using D3.js
 * on top of a Leaflet map.
 * @param {*} voyages The set of voyages to display in the animation.
 * @param {*} ui An object containing a Leaflet map entry, 
 * a d3view object which hosts the animation svg elements, and methods
 * initialize(control), setTime(simTime), showTooltip(data, sourceRect),
 * and closeTooltip.
 * @param {*} monthsPerSecond How many months should elapse for each 
 * animation second.
 */
function d3MapTimelapse(voyages, ui, monthsPerSecond) {
    // Get static JSON with precompiled routes.
    // Compile routes from segments.
    var selectedRoute = null;

    var setSelectedRoute = function (route) {
        if (selectedRoute) {
            ui.map.removeLayer(selectedRoute);
        }
        selectedRoute = route;
        if (selectedRoute) {
            ui.map.addLayer(selectedRoute);
        }
    };

    var render = function (simTime, items) {
        setSelectedRoute(null);
        ui.setTime(simTime);
        var modified = [];
        for (var i = 0; i < items.length; ++i) {
            var item = Object.assign({}, items[i]);
            var pos = item.position;
            item.latLng = L.latLng(pos[1], pos[0]);
            item.point = ui.map.latLngToLayerPoint(item.latLng);
            modified.push(item);
        }
        var updatePos = function (sel, applyTransition) {
            if (sel) {
                if (applyTransition) {
                    sel = sel
                        .transition()
                        .duration(DEFAULT_TIMER_RESOLUTION);
                }
                return sel.attr("transform", function (d) { return "translate(" + d.point.x + "," + d.point.y + ")"; });
            }
        };
        var selection = ui.d3view.selectAll(".animation_voyage_group")
            .data(modified, function (d) { return d.idx; });
        updatePos(selection, true);
        var enterSel = selection
            .enter()
            .append("g")
            .classed("animation_voyage_group", true);
        enterSel
            .append("circle")
            .classed("animation_voyage_inner_circle", true)
            .style("fill", function (d) { return d.voyage.color; })
            .attr("r", 3);
        enterSel
            .append("circle")
            .classed("animation_voyage_outer_circle", true)
            .attr("r", 10)
            .style("opacity", 0)
            .on("mouseover", function () {
                $(this).animate({ opacity: 1 }, 300);
            })
            .on("mouseout", function () {
                $(this).animate({ opacity: 0 }, 300);
            })
            .on("click", function () {
                ui.closeTooltip();
                d3.select(".selected").classed("selected", false);
                d3.select(this).classed("selected", true);
                var d = this.__data__;
                var route = L.geodesic([d.voyage.latLngs], {
                    weight: 3,
                    color: "red",
                    className: "animation_selected_route"
                });
                setSelectedRoute(route);
                data = Object.assign({}, d.voyage.data);
                data.source_name = geoCache.portSegments['src'][data.src].name;
                data.destination_name = geoCache.portSegments['dst'][data.dst].name;
                data.ship_nationality_name = (geoCache.nations || {})[data.nat_id] || '';
                ui.showTooltip(data, this.getBoundingClientRect());
            });
        updatePos(enterSel, false);
        selection.exit().remove();
    };
    var control = null;
    var init = function () {
        if (!control && !!geoCache.regionSegments && !!geoCache.portSegments) {
            var routes = compileRoutes(geoCache.regionSegments, geoCache.portSegments, voyages);
            control = new AnimationControl(routes, voyages, DEFAULT_TIMER_RESOLUTION, monthsPerSecond, render);
            ui.initialize(control);
        }
    };
    if (!geoCache.regionSegments) {
        $.getJSON(STATIC_URL + "maps/js/regional_routes.json", function (data) {
            geoCache.regionSegments = data;
            init();
        });
    }
    if (!geoCache.portSegments) {
        $.getJSON(STATIC_URL + "maps/js/port_routes.json", function (data) {
            geoCache.portSegments = data;
            init();
        });
    }
    if (!geoCache.nations) {
        $.getJSON("/common/nations", function (data) {
            for (var key in data) {
                geoCache.nations[key] = data[key].name;
            }
        });
    }
    init();
}

var MONTH_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function AnimationHelper(data, monthsPerSecond) {
    var self = this;
    // Keep the line below.
    voyagesMap.addLayer(L.polyline(L.latLng(0, 0), L.latLng(0, 0)));

    var map = voyagesMap._map;
    var svg = d3.select(map.getPanes().overlayPane).append("svg");
    var g = svg.append("g").attr("class", "leaflet-zoom-hide");
    var tooltip = $('#tooltip');
    var tooltipShown = false;

    // Set SVG size and position within map.
    var positionSvg = function () {
        var bounds = map.getBounds();
        var topLeft = map.latLngToLayerPoint(bounds.getNorthWest());
        var bottomRight = map.latLngToLayerPoint(bounds.getSouthEast());
        svg.attr("width", bottomRight.x - topLeft.x)
            .attr("height", bottomRight.y - topLeft.y)
            .style("left", topLeft.x + "px")
            .style("top", topLeft.y + "px");
        g.attr("transform", "translate(" + -topLeft.x + "," + -topLeft.y + ")");
        if (self.control && self.control.isPaused()) {
            g.selectAll(".animation_voyage_group").each(function () {
                var latLng = this.__data__.latLng;
                if (latLng) {
                    var point = map.latLngToLayerPoint(latLng);
                    this.__data__.point = point;
                    d3.select(this)
                        .attr("transform", function (d) { return "translate(" + point.x + "," + point.y + ")"; });
                }
            });
        }
    };

    var closeTooltip = function () {
        tooltip.hide();
        svg.selectAll('.selected')
            .style('opacity', 0)
            .classed('selected', false);
        tooltipShown = false;
    };

    var showTooltip = function (d, rCirc) {
        // Set tooltip content.
        tooltipShown = true;
        var content = $("#tooltip_content");
        content.attr("class", "animation_voyage_content flag_" + d.nat_id);
        var shipName = (d.ship_name || '').trim();
        var template = '<h1>' + (shipName != "" ? shipName : gettext("[Unknown ship name]")) + "</h1>";
        if (d.ship_nationality_name != "") {
            template += "<h2>" + d.ship_nationality_name + "</h2>";
        }
        if (d.ship_ton) {
            template += gettext("<p>This {ton}ship left {source} with {embarked} enslaved people and arrived in {destination} with {disembarked}.</p>");
            var tonNum = parseInt(d.ship_ton);
            template = template.replace("{ton}", tonNum ? (tonNum + ' ' + gettext('ton') + ' ') : '');
        } else {
            template += gettext("<p>This ship left {source} with {embarked} enslaved people and arrived in {destination} with {disembarked}.</p>");
        }
        template = template.replace("{source}", d.source_name)
            .replace("{destination}", d.destination_name)
            .replace("{embarked}", d.embarked)
            .replace("{disembarked}", d.disembarked);
        content.html(template + '<span class="animation_tooltip_moreinfo"><a target="_blank" href="/voyage/' + d.voyage_id + '/variables">' +
            gettext("More info") + " »</a></span>");
        // Position and show tooltip.
        tooltip.show();
        var rSvg = map.getContainer().getBoundingClientRect();
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
    }

    map.on("zoomend", positionSvg);

    // Create ui object and hook events.
    // TODO: implement UI that allows changing months per second.
    var ui = {
        map: map,
        d3view: g,
        monthsPerSecond: monthsPerSecond || 12,
        showTooltip: showTooltip,
        closeTooltip: closeTooltip
    };
    ui.initialize = function (control) {
        var updateControls = function () {
            if (control.isPaused()) {
                $("#pauseBtn").hide();
                $("#playBtn").show();
            } else {
                closeTooltip();
                $("#pauseBtn").show();
                $("#playBtn").hide();
            }
        };
        $('.animation_tooltip_close_button').click(closeTooltip);
        $("#playBtn").click(function (e) { control.play(); updateControls(); });
        $("#pauseBtn").click(function (e) { control.pause(); updateControls(); });
        // Initialize slider.
        var model = control.getModel();
        var minTime = model.getFirstStartTime();
        var maxTime = model.getLastFinishTime();
        $("#slider").slider({
            value: minTime,
            min: minTime,
            max: maxTime,
            step: 1,
            slide: function (_, sliderCtrl) {
                control.jumpTo(sliderCtrl.value);
            }
        });
        self.control = control;
    };
    ui.setTime = function (time) {
        // Update slider and label.
        $("#slider").slider('value', time);
        // TODO: monthly
        $("#yearLabel").text(
            ui.monthsPerSecond == 1
                ? Math.round(time / 120) + "-" + gettext(MONTH_LABELS[~~Math.round(time / 10) % 12])
                : Math.round(time / 120));
        positionSvg();
        if (tooltipShown) closeTooltip();
    };
    // Process data, we will use the simple formula 10 * (12 * year + month)
    // as the voyage "time". Voyages without month values will get a
    // random one assigned for better voyage distribution.
    var voyages = [];
    for (var i = 0; i < data.length; ++i) {
        var item = data[i];
        var year = parseInt(item.year);
        var month = parseInt(item.month);
        if (!(month <= 12 && month >= 1)) {
            // Randomize month.
            month = Math.round(Math.random() * 120);
        } else {
            // Randomize "day" of month.
            month = 10 * (month - 1) + Math.round(Math.random() * 5);
        }
        var start = year * 120 + month;
        // For now we set the duration to have a slight random
        // deviation for more natural movement.
        var duration = (10 + Math.random() * 8) * ui.monthsPerSecond;
        var v = new Voyage(i, item.src, item.dst, start, start + duration, item);
        voyages.push(v);
    }
    // Should be called when the helper will no longer be used.
    self.dispose = function () {
        if (self.control) {
            closeTooltip();
            self.control.stop();
            self.control.dispose();
        }
    };
    d3MapTimelapse(voyages, ui, ui.monthsPerSecond * 10);
}