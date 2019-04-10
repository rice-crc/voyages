// Scripts for the timelapse animation of voyages in the map.

// Represents a route on the globe using lat/lng coordinates.
function Route(points) {
    var self = this;
    self.points = points;
    var arcs = [];
    var angles = [];
    var totalAngle = 0;
    for (var j = 0; j < points.length - 1; ++j) {
        var a = { y: points[j].lat, x: points[j].lng };
        var b = { y: points[j + 1].lat, x: points[j + 1].lng };
        var arc = new GreatCircle(a, b);
        arcs.push(arc);
        angles.push(arc.g);
        totalAngle += arc.g;
    }
    // Create an interpolation function with perturbation parameters (pX, pY).
    // The interpolation function receives as argument an integer from [0, 100]
    // and returns a [lat, lng] pair (Array) corresponding to the perturbed
    // position along the route which corresponds to the given percentage of
    // the path 
    self.createInterpolation = function (pLng, pLat) {
        var lastTime = 0;
        var lastPointIdx = 0;
        var lastAngle = 0;
        return function (time) {
            if (time < 0) time = 0;
            if (time > 100) time = 100;
            // Save computation time by using last cached data.
            var from_idx = time >= lastTime ? lastPointIdx : 0;
            var currentAngle = time * totalAngle * 0.01;
            var idx = from_idx;
            while (lastAngle + angles[idx] < currentAngle && idx < angles.length) {
                lastAngle += angles[idx];
                ++idx;
            }
            // Update cache.
            lastTime = time;
            lastPointIdx = idx;
            lastAngle = currentAngle;
            // Compute the result by interpolating on the (now) current arc.
            var pt = arcs[idx].interpolate((currentAngle - angles[idx]) / angles[idx]);
            // The perturbation is minimal at the beginning and end of the route,
            // being larger on the middle of the path.
            time *= 0.01;
            var factor = time * (1.0 - time);
            return [pt[0] + factor * pLng, pt[1] + factor * pLat];
        };
    };
}

function Voyage(routeIdx, start, finish, data) {
    this.routeIdx = routeIdx;
    this.start = start;
    this.finish = finish;
    this.data = data;
}

var LAT_MAX_PERTURBATION = 6;
var LNG_MAX_PERTURBATION = 4;

// Creates an animation helper object that is responsible for 
// determining the position of all ships in the given time frame.
function AnimationHelper(routes, voyages) {
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
        if (v.finish > lastFinish) {
            lastFinish = v.finish;
        }
        v.duration = v.finish - v.start;
        v.interpolate = self._routes[v.routeIdx].createInterpolation(
            Math.random() * LNG_MAX_PERTURBATION,
            Math.random() * LAT_MAX_PERTURBATION);
        v.idx = i;
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
    var helper = new AnimationHelper(routes, voyages);
    var lastRealTime = null;
    var lastSimTime = -1;
    var maxTime = helper.getLastFinishTime();
    var minTime = helper.getFirstStartTime();
    timerResolution = timerResolution || 200;
    if (timerResolution * timeStepPerSec < 1000.0) {
        // Ensure that the resolution is not too fine 
        // (e.g. multiple ticks would be required for
        // an increase in simulated time).
        timerResolution = 1000.0 / timeStepPerSec;
    }
    var tick = function () {
        if (self._paused) return;
        // Advance the simulated time in sync with real time.
        var now = Date.now().getTime();
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
        if (nextSimTime > maxTime) nextSimTime = maxTime;
        if (nextSimTime < minTime) nextSimTime = minTime;
        if (nextSimTime > lastSimTime) {
            // We only bother with updates if the 
            // simulated time actually increased.
            var active = helper.getWindow(nextSimTime);
            lastSimTime = nextSimTime;
            lastRealTime = now;
            onRender(nextSimTime, active);
        }
    };
    self._timer = window.setInterval(tick, timerResolution);
    self._paused = false;
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
        lastRealTime = Date.now();
        self._paused = false;
    };
    self.stop = function () {
        self._paused = true;
        lastRealTime = null;
        lastSimTime = -1;
    };
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
};

var _applySmoothJoint = function (current, added, reverseAdded) {
    if (first.length <= 1 || added.length <= 1) {
        _appendArrHelper(added, current, reverseAdded);
        return;
    }
    var segment = [
        current[current.length - 2], 
        current[current.length - 1],
        added[reverseAdded ? added.length - 1 : 0],
        added[reverseAdded ? added.length - 2 : 1]
    ];
    var smooth = voyagesMap._getCurvePoints(_flatten(segment), null, 4);
    // Remove last two points from current path since they will be smoothed.
    current.splice(current.length - 2, 2);
    // Append joint.
    for (var i = 0; i < smooth.length - 1; i += 2) {
        current.push([smooth[i], smooth[i + 1]]);
    }
    // Append added segment except for first two points used for smoothing.
    _appendArrHelper(added, current, reverseAdded, 2, 0);
};

/**
 * For compactness, the routes are decomposed in 3 segments.
 * This function compiles a whole path (with any required
 * smoothing at the joints) from these segments.
 * @param {*} regionSegments array[fromRegion][toRegion] gives the
 * smooth segment connecting fromRegion to toRegion.
 * @param {*} portSegments array[port] is a smooth segment 
 * connecting port to its regional node. The segment is reversed
 * if the path is going from the regional node to the port.
 * @param {*} routeData an array of objects with at least
 * { src, dest } fields.
 * @returns an array in sync with @param routeData which contains
 * a compiled routes (an array of [lng, lat] points).
 */
function compileRoutes(regionSegments, portFromSegments, routeData) {
    var result = [];
    for (var i = 0; i < routeData.length; ++i) {
        var data = routeData[i];        
        var first = portFromSegments[data.src];
        var second = regionSegments[data.src][data.dest];
        var third = portFromSegments[data.dest];
        // Smooth each of the two joins.
        var points = first.slice(0);
        _applySmoothJoint(points, second, false);
        _applySmoothJoint(points, third, true);
        result.push(points);
    }
    return result;
}