// Scripts for the timelapse animation of voyages in the map v1.0.0.

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
            var currentArc = arcs[idx];
            var arcAngle = angles[idx];
            var arcRatio = (currentAngle - lastAngle) / arcAngle;
            var pt = arcAngle > 0.015 * totalAngle
                ? currentArc.interpolate(arcRatio)
                : (arcRatio < 0.5
                    ? [currentArc.start.lon, currentArc.start.lat]
                    : [currentArc.end.lon, currentArc.end.lat]);
            // The perturbation is minimal at the beginning and end of the route,
            // being larger on the middle of the path.
            var factor = time * (1.0 - time);
            return [pt[0] + factor * pLng, pt[1] + factor * pLat];
        };
    };
}

var _rnd128 = function () { return ~~Math.round(128 * Math.random()); };

function Voyage(routeIdx, src, dst, start, finish, data) {
    this.routeIdx = routeIdx;
    this.src = src;
    this.dst = dst;
    this.start = ~~start;
    this.finish = ~~finish;
    this.data = data;
    var self = this;
    this.color = function () {
        return self.data.color || "rgb(" + _rnd128() + "," + _rnd128() + "," + _rnd128() + ")";
    };
}

var LAT_MAX_PERTURBATION = 20;
var LNG_MAX_PERTURBATION = 20;

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
            (Math.random() - 0.5) * LNG_MAX_PERTURBATION,
            (Math.random() - 0.5) * LAT_MAX_PERTURBATION);
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
 * @param {*} timeStepPerSec How much simulate time is increased every real second.
 * @param {*} onRender The callback that renders ongoing voyages. The arguments to the
 * callback are (simulated_time, [{ idx, voyage, position }, ...])
 * @param {*} onPauseChange An optional callback that receives pause state changes.
 */
function AnimationControl(routes, voyages, timeStepPerSec, onRender, onPauseChange) {
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
        if (self._timer != null) {
            self._timer.stop();
        }
        self._timer = d3.timer(tick);
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
            if (!self._paused) {
                self._paused = (nextSimTime >= maxTime - 0.01);
                if (!!onPauseChange && self._paused) onPauseChange(true);
            }
        }
    };
    var tick = function (elapsed) {
        if (self._paused || !document.hasFocus()) {
            lastRealTime = elapsed;
            return;
        }
        // Advance the simulated time in sync with real time.
        var nextSimTime = 0;
        if (lastRealTime != null) {
            var decimalIncrement = (elapsed - lastRealTime) * timeStepPerSec * 0.001;
            var increment = Math.round(decimalIncrement);
            // If the timer ticked too soon, do nothing.
            if (increment < 1) return;
            nextSimTime = lastSimTime + increment;
        } else {
            nextSimTime = lastSimTime + 1;
        }
        setSimTime(nextSimTime);
        lastRealTime = elapsed;
    };
    setStepPerSec(timeStepPerSec);
    self.getModel = function () { return model; };
    self.isPaused = function () { return self._paused; };
    self.dispose = function () {
        if (self._timer) {
            self._timer.stop();
            self._timer = null;
        }
    };
    self.pause = function () {
        if (!self._paused) {
            self._paused = true;
            if (!!onPauseChange) onPauseChange(true);
        }
    };
    self.play = function () {
        if (self._paused) {
            self._paused = false;
            if (lastSimTime >= (maxTime - 0.01)) {
                // Hitting play at the end of the time scale should reset time.
                lastSimTime = minTime - 1;
            }
            if (!!onPauseChange) onPauseChange(false);
        }
    };
    self.stop = function () {
        self._paused = true;
        if (!!onPauseChange) onPauseChange(true);
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
var geoCache = new (function () {
    var self = this;
    self.regionSegments = null;
    self.portSegments = null;
    self.nations = null;
    self.regionNames = null;
    // TODO: load source regions, destination broad regions.
    var callbacks = [];
    var allLoaded = false;

    self.isReady = function () {
        return allLoaded;
    };

    self.onReady = function (f) {
        if (allLoaded) {
            // No need to wait since everything is loaded.
            f();
        } else {
            callbacks.push(f);
        }
    }

    var loaded = function () {
        allLoaded = self.regionSegments && self.portSegments && self.nations && self.regionNames;
        if (allLoaded) {
            for (var i = 0; i < callbacks.length; ++i) {
                callbacks[i]();
            }
            callbacks = [];
        }
    };

    // Load cached data using AJAX.
    if (!self.regionSegments) {
        $.getJSON(STATIC_URL + "maps/js/regional_routes.json", function (data) {
            self.regionSegments = data;
            loaded();
        });
    }
    if (!self.portSegments) {
        $.getJSON(STATIC_URL + "maps/js/port_routes.json", function (data) {
            self.portSegments = data;
            loaded();
        });
    }
    if (!self.regionNames) {
        $.getJSON("/voyage/get-timelapse-regions", function (data) {
            self.regionNames = data;
            loaded();
        });
    }
    if (!self.nations) {
        $.getJSON("/common/nations", function (data) {
            var nations = {};
            for (var key in data) {
                nations[key] = data[key].name;
            }
            self.nations = nations;
            loaded();
        });
    }
})();

/**
 * Sets up the UI to display voyages timelapse animation using D3.js
 * on top of a Leaflet map.
 * @param {*} voyages The set of voyages to display in the animation.
 * @param {*} ui An object containing a Leaflet map entry, 
 * a d3view object which hosts the animation svg elements, and methods
 * initialize(control), setTime(simTime),
 * play, pause, setSelectedRoute(route, circle),
 * @param {*} monthsPerSecond How many months should elapse for each 
 * animation second.
 */
function d3MapTimelapse(voyages, ui, monthsPerSecond) {
    var control = null;

    var render = function (simTime, items) {
        ui.setSelectedRoute(null);
        for (var i = 0; i < items.length; ++i) {
            var item = items[i];
            var pos = item.position;
            item.latLng = L.latLng(pos[1], pos[0]);
            item.point = ui.map.latLngToLayerPoint(item.latLng);
        }
        var updatePos = function (sel) {
            if (sel) {
                return sel.attr("transform", function (d) { return "translate(" + d.point.x + "," + d.point.y + ")"; });
            }
        };
        var selection = ui.d3view.selectAll(".animation_voyage_group")
            .data(items, function (d) { return d.idx; });
        updatePos(selection, true);
        var enterSel = selection
            .enter()
            .append("g")
            .classed("animation_voyage_group", true);
        enterSel
            .append("circle")
            .classed("animation_voyage_inner_circle", true)
            .style("fill", function (d) { return d.voyage.color(); })
            .style("filter", "url(#motionFilter)")
            .attr("r", function (d) {
                var e = parseInt(d.voyage.data.embarked);
                if (e <= 200) return 2;
                return 2 * (1.0 + Math.log2(e / 200));
            });
        updatePos(enterSel, false);
        selection.exit().remove();
        ui.setTime(simTime);
    };
    var init = function () {
        if (!control && geoCache.isReady()) {
            var routes = compileRoutes(geoCache.regionSegments, geoCache.portSegments, voyages);
            var initialized = false;
            control = new AnimationControl(
                routes,
                voyages,
                monthsPerSecond,
                render,
                function (paused) {
                    if (!initialized) return;
                    if (paused) {
                        ui.pause();
                    } else {
                        ui.play();
                    }
                });
            ui.initialize(control);
            initialized = true;
        }
    };
    geoCache.onReady(init);
}

var MONTH_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function TimelineControl(data, parent, onChange) {
    // TODO: Implement a D3.js cumulative line graph with embarked,
    // grouped by major region of disembarkation
    var self = this;
    var NORMAL_HEIGHT = 100;
    var PLOT_LEFT_MARGIN = 220;
    var PLOT_RIGHT_MARGIN = 60;
    var PLOT_VERTICAL_MARGIN = 4;
    // The unicode "ICON" characters below will 
    // render properly with FontAwesome.
    var AFRICA_ICON = "";
    var AMERICA_ICON = "";
    var FLAG_ICON = "";
    var ICONS = [
        { key: 'flag', text: FLAG_ICON, tooltip: gettext('Group by ship nationality') },
        { key: 'destinationRegion', text: AMERICA_ICON, tooltip: gettext('Group by disembarkation broad region') },
        { key: 'sourceRegion', text: AFRICA_ICON, tooltip: gettext('Group by embarkation region') }
    ];
    d3.select("#timeline_slider").remove();
    d3.select("#timeline_slider_tooltip").remove();
    var tooltip = d3.select("body").append("div")
        .attr("id", "timeline_slider_tooltip")
        .attr("class", "tooltip")
        .style("opacity", 0)
        .style("padding", '6px')
        .style("background", 'white');
    var width = 960;
    var left = 40;
    var top = 300 - PLOT_VERTICAL_MARGIN;
    var g = parent
        .append("g")
        .attr("id", "timeline_slider")
        .style("pointer-events", "auto")
        .attr("transform", "translate(" + left + "," + top + ")");

    self.resize = function (w, h) {
        left = (w - width) / 2;
        top = h - NORMAL_HEIGHT - PLOT_VERTICAL_MARGIN;
        g.attr("transform", "translate(" + left + "," + top + ")");
    };

    // Enrich data set with grouping variables.
    for (var i = 0; i < data.length; ++i) {
        var item = data[i];
        item.sourceRegion = gettext(geoCache.regionNames.src[item.regsrc] || 'Other Africa');
        item.destinationRegion = gettext(geoCache.regionNames.dst[item.bregdst] || 'Other');
        item.flag = gettext(geoCache.nations[item.nat_id] || 'Other');
    }

    var currentGroupField = null
    var setCurrentGroupField = null;
    var lastTickPos = 0;
    var createTimelinePlot = function (groupField) {
        $('#timeline_slider').empty();
        // Append background.
        g.append("rect")
            .attr("height", NORMAL_HEIGHT)
            .attr("width", width)
            .attr("fill", "rgba(0, 0, 0, 0.3)")
            .attr("rx", 4)
            .attr("ry", 4);
        g.selectAll('.timeline_group_button')
            .data(ICONS)
            .enter()
            .append('text')
            .attr('id', function (d) { return 'group_field_btn_' + d.key; })
            .attr('font-family', 'FontAwesome')
            .attr('font-size', '24')
            .attr('text-anchor', 'middle')
            .attr('fill', 'gray')
            .attr('transform', function (_, i) { return 'translate(20,' + (2 + 30 * (i + 1)) + ')'; })
            .text(function (d) { return d.text; })
            .on('mouseover', function (d) {
                d3.select(this).style("fill", "red");
                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9);
                tooltip.html(d.tooltip)
                    .style("left", (d3.event.pageX + 40) + "px")
                    .style("top", (d3.event.pageY - 40) + "px");
            })
            .on("mouseout", function (d) {
                d3.select(this).style("fill", d.key == currentGroupField ? "black" : "gray");
                tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
            })
            .on('click', function () {
                if (setCurrentGroupField) {
                    setCurrentGroupField(this.__data__.key);
                }
            });
        var keys = d3.set(data, function (x) { return x[groupField]; }).values();
        var color = d3.scaleOrdinal()
            .domain(keys)
            .range(d3.schemePaired);
        var grouped = d3.nest()
            .key(function (d) { return d[groupField]; })
            .sortValues(function (a, b) { return a.year - b.year; })
            .rollup(function (g) {
                // Build aggregates based on year. 
                var agg = [];
                var lastYear = -1;
                var acc = 0;
                for (var i = 0; i < g.length; ++i) {
                    var d = g[i];
                    acc += d.embarked;
                    if (d.year == lastYear) {
                        agg[agg.length - 1].acc = acc;
                    } else {
                        lastYear = d.year;
                        agg.push({ 'year': lastYear, 'acc': acc });
                    }
                }
                return agg;
            })
            .entries(data);
        var yearData = {}
        for (var i = 0; i < grouped.length; ++i) {
            var grp = grouped[i];
            var values = grp.value;
            for (var j = 0; j < values.length; ++j) {
                // Create an year-based object that contains one property for every group.
                var item = values[j];
                var yearObj = yearData[item.year] || {};
                yearObj[grp.key] = item.acc;
                yearData[item.year] = yearObj;
            }
        }
        var start = d3.min(data, function (d) { return d.year; });
        var end = d3.max(data, function (d) { return d.year; });
        var table = [];
        for (var year = start; year <= end; ++year) {
            var yearObj = {};
            if (table.length > 0) {
                // Copy the values from the previous year.
                yearObj = Object.assign({}, table[table.length - 1]);
            } else {
                // Ensure that all keys have values.
                for (var i = 0; i < keys.length; ++i) {
                    var key = keys[i];
                    if (!yearObj.hasOwnProperty(key)) {
                        yearObj[key] = 0;
                    }
                }
            }
            // Update only the data for groups that had a change on the current year.
            // The previous step ensures that all groups have the correct accumulated
            // value from all previous years.
            yearObj = Object.assign(yearObj, yearData[year]);
            yearObj.year = year;
            // Compute total for the year.
            var yearTotal = 0;
            for (var i = 0; i < keys.length; ++i) {
                var key = keys[i];
                yearTotal += yearObj[key];
            }
            yearObj.total = yearTotal;
            table.push(yearObj);
        }

        var x = d3.scaleLinear()
            .domain(d3.extent(table, function (d) { return d.year; }))
            .range([0, width - PLOT_LEFT_MARGIN - PLOT_RIGHT_MARGIN]);
        var xAxis = d3.axisTop().scale(x).ticks(20).tickFormat(function (d) { return d; });
        var yMaxValue = d3.sum(data, function (d) { return d.embarked; });
        var y = d3.scaleLinear()
            .domain([0, yMaxValue])
            .range([NORMAL_HEIGHT - 2 * PLOT_VERTICAL_MARGIN, PLOT_VERTICAL_MARGIN]);
        var yAxis = d3.axisRight().scale(y).ticks(4);
        var area = d3.area()
            .x(function (d) {
                return x(d.data.year);
            })
            .y0(function (d) { return y(d[0]); })
            .y1(function (d) { return y(d[1]); });
        var stack = d3.stack()
        stack.keys(keys);
        var stackData = stack(table);
        var categories = g.selectAll('.category')
            .data(stackData)
            .enter().append('g')
            .attr('class', function (d) { return 'category ' + d.key; })
            .attr('fill-opacity', 0.5);

        categories.append('path')
            .attr('class', 'area')
            .attr('d', area)
            .attr('transform', 'translate(' + PLOT_LEFT_MARGIN + ', 0)')
            .style('fill', function (d) { return color(d.key); });
        // Labels for categories.
        var paddedHeight = NORMAL_HEIGHT - 2 * PLOT_VERTICAL_MARGIN;
        categories.append('text')
            .datum(function (d) { return d; })
            .attr('transform', function (d, i) { return 'translate(60,' + (PLOT_VERTICAL_MARGIN + i * paddedHeight / keys.length) + ')'; })
            .attr('dy', '1em')
            .style("font-size", "10")
            .style("text-anchor", "start")
            .text(function (d) { return d.key; })
            .attr('fill-opacity', 1);
        categories.append('rect')
            .datum(function (d) { return d; })
            .attr('transform', function (d, i) { return 'translate(40,' + (PLOT_VERTICAL_MARGIN + 2 + i * paddedHeight / keys.length) + ')'; })
            .attr('width', 15)
            .attr('height', Math.min(8, NORMAL_HEIGHT / keys.length - 4))
            .attr('fill', function (d) { return color(d.key); })
            .attr('stroke', 'gray')
            .attr('stroke-width', 1);
        g.append('g')
            .attr('class', 't_axis')
            .attr('transform', 'translate(' + PLOT_LEFT_MARGIN + ',' + (NORMAL_HEIGHT - 5) + ')')
            .attr('color', 'black')
            .call(xAxis);
        g.append('g')
            .attr('class', 'embarked_axis')
            .attr('transform', 'translate(' + (width - PLOT_RIGHT_MARGIN) + ',0)')
            .attr('color', 'black')
            .call(yAxis);
        d3.selectAll('g.tick>text').style('font-size', '10px');

        // Create time indicator bar.
        var tickLine = g.append('line')
            .attr('stroke', 'red')
            .attr('stroke-width', 1)
            .attr('transform', 'translate(' + (PLOT_LEFT_MARGIN + lastTickPos) + ',' + PLOT_VERTICAL_MARGIN + ')')
            .attr('y2', paddedHeight);
        var embCirclePos = function (val) {
            if (val > 0) {
                // Convert a year value to the embarked count value for that year.
                if (val < table[0].year || val > table[table.length - 1].year) {
                    val = 0;
                } else {
                    val = table[val - table[0].year].total;
                }
            }
            return 'translate(' + (width - PLOT_RIGHT_MARGIN) + ',' + y(val) + ')';
        };
        var tickEmbarkedCircle = g.append('circle')
            .attr('r', 2)
            .attr('fill', 'red')
            .attr('transform', embCirclePos(0));
        var _maxTickPos = width - PLOT_LEFT_MARGIN - PLOT_RIGHT_MARGIN;
        self.setTime = function (time) {
            var nextTickPos = ~~Math.round(x(time / 120));
            if (nextTickPos > _maxTickPos) nextTickPos = _maxTickPos;
            if (nextTickPos != lastTickPos) {
                tickLine
                    .attr('transform', 'translate(' + (PLOT_LEFT_MARGIN + nextTickPos) + ',' + PLOT_VERTICAL_MARGIN + ')');
                tickEmbarkedCircle
                    .attr('transform', embCirclePos(~~Math.round(time / 120)));
                lastTickPos = nextTickPos;
            }
        }

        // Create mouse over bar.
        var hoverLine = g.append('line')
            .attr('stroke', 'red')
            .attr('stroke-width', 1)
            .style("stroke-dasharray", ("2, 2"))
            .attr('transform', 'translate(' + PLOT_LEFT_MARGIN + ',' + PLOT_VERTICAL_MARGIN + ')')
            .style('opacity', 0)
            .attr('y2', paddedHeight);
        g.on('mousemove', function () {
            var xCoord = d3.mouse(this)[0];
            if (xCoord >= PLOT_LEFT_MARGIN && xCoord <= (width - PLOT_RIGHT_MARGIN)) {
                hoverLine
                    .style('opacity', '0.8')
                    .attr('transform', 'translate(' + xCoord + ',' + PLOT_VERTICAL_MARGIN + ')');
            } else {
                hoverLine.style('opacity', 0);
            }
        })
            .on('mouseout', function () {
                hoverLine.style('opacity', 0);
            })
            .on('mousedown', function () {
                var xCoord = d3.mouse(this)[0];
                if (xCoord >= PLOT_LEFT_MARGIN && xCoord <= (width - PLOT_RIGHT_MARGIN)) {
                    // Compute xValue to set.
                    onChange(120 * ~~Math.round(x.invert(xCoord - PLOT_LEFT_MARGIN)));
                }
            });
    };

    setCurrentGroupField = function (field) {
        if (currentGroupField != field) {
            createTimelinePlot(field);
            d3.selectAll('#group_field_btn_' + field).attr('fill', 'black');
        }
        currentGroupField = field;
    };

    setCurrentGroupField('flag');
}

function AnimationHelper(data, monthsPerSecond) {
    var self = this;
    // Keep the line below.
    voyagesMap.addLayer(L.polyline(L.latLng(0, 0), L.latLng(0, 0)));

    var map = voyagesMap._map;
    var svg = d3.select(map.getPanes().overlayPane).append("svg");
    d3.select("#timelapse_control_layer").remove();
    var controlLayer = d3.select(map.getContainer())
        .append("svg")
        .attr('id', 'timelapse_control_layer')
        .attr('width', 0)
        .style("pointer-events", "none");
    var yearLabel = controlLayer
        .style('position', 'absolute')
        .append('text')
        .attr('font-family', 'Roboto')
        .attr('font-size', '36')
        .attr('text-anchor', 'middle')
        .text("");
    // It is normal for the characters below to look like a box, don't replace them
    // unless you know how they will render using FontAwesome.
    var playText = "";
    var pauseText = "";
    var playPauseBtn = controlLayer.append('text')
        .style("pointer-events", "auto")
        .attr('font-family', 'FontAwesome')
        .attr('font-size', '24')
        .attr('text-anchor', 'middle')
        .text(pauseText);
    var defs = svg.append("defs");
    var filter = defs.append("filter")
        .attr("id", "motionFilter") // Unique Id to blur effect
        // Increase the width of the filter region to remove blur "boundary"
        .attr("width", "300%")
        // Put center of the "width" back in the middle of the element
        .attr("x", "-100%")
        .append("feGaussianBlur") // Append a filter technique
        .attr("class", "blurValues") // Needed to select later on
        .attr("in", "SourceGraphic"); // Apply blur on the applied element;

    var setBlurFilter = function (val) {
        return filter.attr("stdDeviation", val || "0.5");
    }
    setBlurFilter();

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
        var size = map.getSize();
        controlLayer.attr("width", size.x)
            .attr("height", size.y);
        yearLabel.attr("transform", "translate(" + (size.x / 2) + ", 50)");
        playPauseBtn.attr("transform", "translate(" + (size.x / 2) + ", 80)");
        if (ui.timeline) {
            ui.timeline.resize(size.x, size.y);
        }
    };

    var ui = {};
    var selectedRoute = null;
    var setSelectedRoute = function (route, circle) {
        if (ui.clickedCircle) {
            $(ui.clickedCircle).animate({ opacity: 0 }, 300);
        }
        ui.clickedCircle = circle || null;
        if (selectedRoute) {
            map.removeLayer(selectedRoute);
        }
        selectedRoute = route;
        if (selectedRoute) {
            map.addLayer(selectedRoute);
        }
    };

    var closeTooltip = function () {
        tooltip.hide();
        svg.selectAll('.selected')
            .style('opacity', 0)
            .classed('selected', false);
        tooltipShown = false;
        setSelectedRoute(null);
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
        template = template.replace("{source}", gettext(d.source_name))
            .replace("{destination}", gettext(d.destination_name))
            .replace("{embarked}", d.embarked)
            .replace("{disembarked}", d.disembarked);
        content.html(template + '<span class="animation_tooltip_moreinfo"><a target="_blank" href="/voyage/' + d.voyage_id + '/variables">' +
            gettext("More info") + " »</a></span>");
        // Position and show tooltip.
        tooltip.show();
        var rSvg = map.getContainer().getBoundingClientRect();
        var tooltipWidth = tooltip.width();
        var tooltipHeight = tooltip.height();
        var top = rCirc.bottom - rSvg.top + 100;
        if (top + tooltipHeight + 170 > rSvg.bottom) {
            top -= tooltipHeight + 100;
        }
        tooltip.animate({
            left: ((rCirc.left + rCirc.right) / 2 - rSvg.left - tooltipWidth / 2 - 20) + "px",
            top: top + "px",
            opacity: 0.9
        }, 800);
    }

    var addInteractiveUI = function () {
        g.selectAll(".animation_voyage_group:not(.interactive_voyage_node)")
            .classed('interactive_voyage_node', true)
            .append("circle")
            .classed("animation_voyage_outer_circle", true)
            .attr("r", 10)
            .style("opacity", 0)
            .on("mouseover", function () {
                $(this).animate({ opacity: 1 }, 300);
            })
            .on("mouseout", function () {
                if (ui.clickedCircle != this) {
                    $(this).animate({ opacity: 0 }, 300);
                }
            })
            .on("click", function () {
                closeTooltip();
                d3.select(".selected").classed("selected", false);
                d3.select(this).classed("selected", true);
                var d = this.__data__;
                var route = L.geodesic([d.voyage.latLngs], {
                    weight: 3,
                    color: "red",
                    className: "animation_selected_route"
                });
                setSelectedRoute(route, this);
                data = Object.assign({}, d.voyage.data);
                data.source_name = geoCache.portSegments['src'][data.src].name;
                data.destination_name = geoCache.portSegments['dst'][data.dst].name;
                data.ship_nationality_name = (geoCache.nations || {})[data.nat_id] || '';
                showTooltip(data, this.getBoundingClientRect());
            });
    };

    map.on("zoomend", positionSvg);
    $(window).resize(positionSvg);

    // Set up ui object and hook events.
    // TODO: implement UI that allows changing months per second.
    ui = {
        map: map,
        d3view: g,
        monthsPerSecond: monthsPerSecond || 12,
        setSelectedRoute: setSelectedRoute
    };
    var updateControls = function () {
        if (self.control.isPaused()) {
            setBlurFilter("0.0");
            playPauseBtn.text(playText);
        } else {
            closeTooltip();
            setBlurFilter();
            playPauseBtn.text(pauseText);
        }
    };
    ui.pause = function () {
        if (!!self.control && !self.control.isPaused()) {
            self.control.pause();
            addInteractiveUI();
        }
        updateControls();
    };
    ui.play = function () {
        if (!!self.control && self.control.isPaused()) {
            self.control.play();
        }
        updateControls();
    };
    ui.initialize = function (control) {
        self.control = control;
        // Initialize plot slider.
        ui.timeline = new TimelineControl(data, controlLayer, control.jumpTo);
        playPauseBtn
            .on("mouseover", function () {
                d3.select(this).style("fill", "red");
            })
            .on("mouseout", function () {
                d3.select(this).style("fill", "black");
            })
            .on("click", function () {
                if (control.isPaused()) {
                    ui.play();
                } else {
                    ui.pause();
                }
            })
        $('.animation_tooltip_close_button').click(closeTooltip);
    };
    ui.setTime = function (time) {
        // Update slider and label.
        ui.timeline.setTime(time);
        var yearText = ui.monthsPerSecond == 1
            ? Math.round(time / 120) + "-" + gettext(MONTH_LABELS[~~Math.round(time / 10) % 12])
            : Math.round(time / 120);
        yearLabel.text(yearText);
        positionSvg();
        if (tooltipShown) closeTooltip();
        if (self.control.isPaused()) {
            addInteractiveUI();
        }
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