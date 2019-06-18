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
  // A good approximation for the length is given by the formula angle * earth radius.
  self.getRouteLength = function() {
    return totalAngle * 6371;
  };
  self.latLngs = latLngs;
  // Create an interpolation function with perturbation parameters (pX, pY).
  // The interpolation function receives as argument a number from [0, 1.0]
  // and returns a [lat, lng] pair (Array) corresponding to the perturbed
  // position along the route which corresponds to the given percentage of
  // the path
  self.createInterpolation = function(pLng, pLat) {
    var lastTime = 0;
    var lastPointIdx = 0;
    var lastAngle = 0;
    if (angles.length == 0)
      return function() {
        return [0.0, 0.0];
      };
    return function(time) {
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
      while (
        idx < angles.length - 1 &&
        lastAngle + angles[idx] < currentAngle
      ) {
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
      var pt = currentArc.interpolate(arcRatio);
      // The perturbation is minimal at the beginning and end of the route,
      // being larger on the middle of the path.
      var factor = time * (1.0 - time);
      return [pt[0] + factor * pLng, pt[1] + factor * pLat];
    };
  };
}

var _rnd128 = function() {
  return ~~Math.round(128 * Math.random());
};

function Voyage(routeIdx, src, dst, start, animationTime, data) {
  this.routeIdx = routeIdx;
  this.src = src;
  this.dst = dst;
  this.start = ~~start;
  this.animationTime = animationTime;
  this.data = data;
  var self = this;
  this.color = function() {
    return (
      self.data.color ||
      "rgb(" + _rnd128() + "," + _rnd128() + "," + _rnd128() + ")"
    );
  };
}

function AnimationOptions(
  shipTrafficBaseLineQuantile,
  latLngMaxPerturb,
  initialSpeed,
  minSpeed,
  maxSpeed,
  voyageLengthBaseLine
) {
  this.latLngMaxPerturb = latLngMaxPerturb || 20;
  this.shipTrafficBaseLineQuantile = shipTrafficBaseLineQuantile || 0.3;
  this.initialSpeed = initialSpeed || 12;
  this.minSpeed = minSpeed || 3;
  this.maxSpeed = maxSpeed || 24;
  this.voyageLengthBaseLine = voyageLengthBaseLine || 12000;
}

// Creates an animation model object that is responsible for
// determining the position of all ships in the given time frame.
function AnimationModel(routes, voyages, options) {
  var self = this;
  self._routes = routes;
  self._voyages = [];
  var lastFinish = 0;
  // Initialize voyage interpolation functions.
  for (var i = 0; i < voyages.length; ++i) {
    var v = Object.assign({}, voyages[i]);
    var finish = ~~Math.round(v.start + 120);
    if (finish >= lastFinish) {
      lastFinish = finish + 1;
    }
    var route = self._routes[v.routeIdx];
    v.interpolate = route.createInterpolation(
      (Math.random() - 0.5) * options.latLngMaxPerturb,
      (Math.random() - 0.5) * options.latLngMaxPerturb
    );
    v.idx = i;
    v.latLngs = route.latLngs;
    self._voyages.push(v);
  }
  // Sort voyages by start time so that determining the active voyages in a given timeframe is much faster.
  self._voyages.sort(function(a, b) {
    return a.start - b.start;
  });
  // Cache starting index of voyage for time period.
  var lastTime = 0;
  var lastWindowStart = 0;
  var nvoyages = self._voyages.length;
  self.getWindow = function(time, timeStepPerSec, voyageDurationMultiplier) {
    var result = [];
    if (time == lastFinish) return []; // Ensure that we report empty results at the very end.
    var from_idx = time >= lastTime ? lastWindowStart : 0;
    for (var i = from_idx; i < nvoyages; ++i) {
      var v = self._voyages[i];
      if (v.start > time) break;
      // See if we can shift the cached window start index by one.
      var duration =
        v.animationTime * voyageDurationMultiplier * timeStepPerSec;
      var finish = v.start + ~~duration;
      var isFinished = finish < time;
      if (from_idx == i && isFinished) ++from_idx;
      if (!isFinished) {
        result.push({
          idx: v.idx,
          voyage: v,
          position: v.interpolate((time - v.start) / duration)
        });
      }
    }
    lastWindowStart = from_idx;
    lastTime = time;
    return result;
  };
  self.getFirstStartTime = function() {
    return nvoyages > 0 ? self._voyages[0].start : 0;
  };
  self.getLastStartTime = function() {
    return nvoyages > 0 ? self._voyages[nvoyages - 1].start : 0;
  };
  self.getLastFinishTime = function() {
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
function AnimationControl(
  routes,
  voyages,
  timeStepPerSec,
  onRender,
  onPauseChange,
  options
) {
  var self = this;
  var model = new AnimationModel(routes, voyages, options);
  var lastRealTime = null;
  var lastSimTime = -1;
  var lastActive = null;
  var maxTime = model.getLastFinishTime();
  var minTime = model.getFirstStartTime();
  self._timer = null;
  self._paused = false;
  self.setStepPerSec = function(stepPerSec, voyageDurationMultiplier) {
    self.timeStepPerSec = stepPerSec || 120;
    self.voyageDurationMultiplier = voyageDurationMultiplier || 1.0;
    if (self._timer == null) {
      self._timer = d3.timer(tick);
    }
  };
  var setSimTime = function(nextSimTime) {
    nextSimTime = ~~nextSimTime;
    if (nextSimTime > maxTime) nextSimTime = maxTime;
    if (nextSimTime < minTime) nextSimTime = minTime;
    if (nextSimTime != lastSimTime) {
      // We only bother with updates if the
      // simulated time has changed.
      var active = model.getWindow(
        nextSimTime,
        self.timeStepPerSec,
        self.voyageDurationMultiplier
      );
      lastSimTime = nextSimTime;
      try {
        onRender(nextSimTime, active);
        lastActive = active;
      } catch (e) {
        console.log("Render error!");
        console.log(e);
      }
      if (!self._paused) {
        self._paused = nextSimTime >= maxTime - 0.01;
        if (!!onPauseChange && self._paused) onPauseChange(true);
      }
    }
  };
  var tick = function(elapsed) {
    if (self._paused || !document.hasFocus()) {
      lastRealTime = elapsed;
      return;
    }
    // Advance the simulated time in sync with real time.
    var nextSimTime = 0;
    if (lastRealTime != null) {
      var decimalIncrement =
        (elapsed - lastRealTime) * self.timeStepPerSec * 0.001;
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
  self.setStepPerSec(timeStepPerSec);
  self.getModel = function() {
    return model;
  };
  self.isPaused = function() {
    return self._paused;
  };
  self.dispose = function() {
    if (self._timer) {
      self._timer.stop();
      self._timer = null;
    }
  };
  self.pause = function() {
    if (!self._paused) {
      self._paused = true;
      if (!!onPauseChange) onPauseChange(true);
      if (lastActive) onRender(lastSimTime, lastActive);
    }
  };
  self.play = function() {
    if (self._paused) {
      self._paused = false;
      if (lastSimTime >= maxTime - 0.01) {
        // Hitting play at the end of the time scale should reset time.
        lastSimTime = minTime - 1;
      }
      if (!!onPauseChange) onPauseChange(false);
    }
  };
  self.stop = function() {
    self._paused = true;
    if (!!onPauseChange) onPauseChange(true);
    onRender(minTime, []);
    lastSimTime = minTime - 1;
    lastRealTime = null;
  };
  self.jumpTo = setSimTime;
}

var _appendArrHelper = function(source, target, reverse, skipStart, skipLast) {
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
  var cy = center[1];
  var v1 = [p1[0] - cx, p1[1] - cy];
  var v2 = [p2[0] - cx, p2[1] - cy];
  var n1 = _normSq(v1);
  var n2 = _normSq(v2);
  var dot = v1[0] * v2[0] + v1[1] * v2[1];
  var sqrtNormProd = Math.sqrt(n1 * n2);
  return {
    angle: Math.acos(dot / sqrtNormProd),
    center: center,
    dot: dot,
    sqrtNormProd: sqrtNormProd,
    v1: v1,
    v2: v2,
    n1sq: n1,
    n2sq: n2
  };
}

// Given two paths that may form a sharp corner when concatenated,
// compute an index on path2 that is not too far along the path such
// that the angle formed by the concatenation is within a threshold.
function _reduceSharpCorner(
  lastP1pt,
  second,
  reverse,
  maxPathSector,
  threshold
) {
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
      ? _angleInfo(
          second[second.length - p2index - 2],
          lastP1pt,
          second[second.length - 1 - p2index]
        ).angle
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
    ? _angleInfo(
        second[second.length - p2index - 2],
        lastP1pt,
        second[second.length - 1 - p2index]
      )
    : _angleInfo(second[bestIndex + 1], lastP1pt, second[bestIndex]);
  var endTangentScalar = ai.sqrtNormProd / ai.n2sq;
  var endTangent = [ai.v2[0] * endTangentScalar, ai.v2[1] * endTangentScalar];
  var prefix = [];
  var NUM_POINTS = 10;
  for (var j = NUM_POINTS - 1; j >= 1; --j) {
    var lambda = reverse
      ? (NUM_POINTS - j + 0.0) / NUM_POINTS
      : (j + 0.0) / NUM_POINTS;
    var a = [
      ai.center[0] + lambda * ai.v1[0],
      ai.center[1] + lambda * ai.v1[1]
    ];
    var b = [
      ai.center[0] + lambda * endTangent[0],
      ai.center[1] + lambda * endTangent[1]
    ];
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
 * @param {*} regionSegments object[fromRegion][toRegion] gives the
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
  var sources = portSegments["src"];
  var targets = portSegments["dst"];
  var cached = {}; // Create a cache for src vs dst routes.
  for (var i = 0; i < routeData.length; ++i) {
    var data = routeData[i];
    var srcInfo = sources[data.src];
    var dstInfo = targets[data.dst];
    if (
      !srcInfo ||
      !dstInfo ||
      !regionSegments[srcInfo.reg] ||
      !regionSegments[srcInfo.reg][dstInfo.reg]
    ) {
      // This is a route we cannot handle...
      result.push(new Route([]));
      continue;
    }
    var key = data.src + "_" + data.dst;
    if (!cached.hasOwnProperty(key)) {
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
      var route = new Route(points);
      cached[key] = route;
      result.push(route);
    } else {
      result.push(cached[key]);
    }
  }
  return result;
}

// We use AJAX to fetch several pieces of geo-data used by the animation.
// The routing network must be specified to fetch the correct graph.
var _nationsCache = null;
var _regionNamesCache = null;
var _fetchGeoData = function(networkName) {
  var self = this;
  self.regionSegments = null;
  self.portSegments = null;
  self.nations = _nationsCache;
  self.regionNames = _regionNamesCache;
  var callbacks = [];
  var allLoaded = false;

  self.isReady = function() {
    return allLoaded;
  };

  self.onReady = function(f) {
    if (allLoaded) {
      // No need to wait since everything is loaded.
      f();
    } else {
      callbacks.push(f);
    }
  };

  var loaded = function() {
    allLoaded =
      self.regionSegments &&
      self.portSegments &&
      self.nations &&
      self.regionNames;
    if (allLoaded) {
      for (var i = 0; i < callbacks.length; ++i) {
        callbacks[i]();
      }
      callbacks = [];
    }
  };

  // Load cached data using AJAX.
  if (!self.regionSegments) {
    $.getJSON(
      "/voyage/get-compiled-routes?routeType=regional&networkName=" + networkName,
      function(data) {
        self.regionSegments = data;
        loaded();
      }
    );
  }
  if (!self.portSegments) {
    $.getJSON(
      "/voyage/get-compiled-routes?routeType=port&networkName=" + networkName,
      function(data) {
        self.portSegments = data;
        loaded();
      }
    );
  }
  if (!self.regionNames) {
    $.getJSON("/voyage/get-timelapse-regions", function(data) {
      self.regionNames = data;
      _regionNamesCache = data;
      loaded();
    });
  }
  if (!self.nations) {
    $.getJSON("/common/nations", function(data) {
      var nations = {};
      for (var key in data) {
        nations[key] = data[key].name;
      }
      self.nations = nations;
      _nationsCache = nations;
      loaded();
    });
  }
};

function _getShipCircleRadius(d, baseLine) {
  baseLine = baseLine || 200;
  var e = parseInt(d.voyage.data.embarked);
  if (e <= baseLine) return 2;
  return Math.min(9, 2 * (1.0 + Math.log2(e / baseLine)));
}

/**
 * Sets up the UI to display voyages timelapse animation using D3.js
 * on top of a Leaflet map.
 * @param {*} voyages The set of voyages to display in the animation.
 * @param {*} ui An object containing a Leaflet map entry,
 * a d3view object which hosts the animation svg elements, and methods
 * initialize(control), setTime(simTime),
 * play, pause, setSelectedRoute(route, circle).
 * @param {*} geoCache A cache of geo information that is used by the timelapse.
 * @param {number} shipTrafficBaseLine The number of embarked used as a base
 * line for the smallest radius in the ship's circle.
 * @param {AnimationOptions} options Options that are used to configure the animation.
 */
function d3MapTimelapse(
  voyages,
  ui,
  timeStepPerSec,
  geoCache,
  shipTrafficBaseLine,
  options
) {
  var control = null;
  var initialized = false;

  var render = function(simTime, items) {
    if (!initialized) return;
    ui.prerender();
    ui.setSelectedRoute(null);
    for (var i = 0; i < items.length; ++i) {
      var item = items[i];
      var pos = item.position;
      item.latLng = L.latLng(pos[1], pos[0]);
      item.point = ui.map.latLngToLayerPoint(item.latLng);
    }
    var updatePos = function(sel) {
      if (sel) {
        return sel.attr("transform", function(d) {
          return "translate(" + d.point.x + "," + d.point.y + ")";
        });
      }
    };
    var selection = ui.d3view
      .selectAll(".animation_voyage_group")
      .data(items, function(d) {
        return d.idx;
      });
    var enterSel = selection
      .enter()
      .append("g")
      .classed("animation_voyage_group", true);
    enterSel
      .append("circle")
      .classed("animation_voyage_inner_circle", true)
      .style("fill", function(d) {
        return d.voyage.color();
      })
      .attr("r", function(d) {
        return _getShipCircleRadius(d, shipTrafficBaseLine);
      });
    updatePos(selection, true);
    updatePos(enterSel, false);
    selection.exit().remove();
    ui.setTime(simTime);
  };
  var init = function() {
    if (!control && geoCache.isReady()) {
      var routes = compileRoutes(
        geoCache.regionSegments,
        geoCache.portSegments,
        voyages
      );
      // Rescale times for voyages based on the length of the routes.
      for (var i = 0; i < routes.length; ++i) {
        var r = routes[i];
        voyages[i].animationTime *= Math.min(
          1.0,
          r.getRouteLength() / options.voyageLengthBaseLine
        );
      }
      control = new AnimationControl(
        routes,
        voyages,
        timeStepPerSec,
        render,
        function(paused) {
          if (!initialized) return;
          if (paused) {
            ui.pause();
          } else {
            ui.play();
          }
        },
        options
      );
      ui.initialize(control);
      initialized = true;
    }
  };
  geoCache.onReady(init);
}

// This is a hacky way to get Firefox to allow mouse events over the bounding rect of paths.
// It would be much simpler to set pointer-events to bounding-box (which is supported by Chrome).
function _addIconBackgroundRect(parent, icon) {
  var g = parent.append("g").style("pointer-events", "visible");
  g.append("rect")
    .attr("width", 500)
    .attr("height", 500)
    .attr("fill", "transparent");
  if (icon) {
    g.append("path").attr("d", icon);
  }
  return g;
}

var MONTH_LABELS = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec"
];

// TODO: Remove FontAwesome Regular icons if we do not acquire their Pro license.
// var AFRICA_ICON = "M248 8C111.03 8 0 119.03 0 256s111.03 248 248 248 248-111.03 248-248S384.97 8 248 8zm160 215.5v6.93c0 5.87-3.32 11.24-8.57 13.86l-15.39 7.7a15.485 15.485 0 0 1-15.53-.97l-18.21-12.14a15.52 15.52 0 0 0-13.5-1.81l-2.65.88c-9.7 3.23-13.66 14.79-7.99 23.3l13.24 19.86c2.87 4.31 7.71 6.9 12.89 6.9h8.21c8.56 0 15.5 6.94 15.5 15.5v11.34c0 3.35-1.09 6.62-3.1 9.3l-18.74 24.98c-1.42 1.9-2.39 4.1-2.83 6.43l-4.3 22.83c-.62 3.29-2.29 6.29-4.76 8.56a159.608 159.608 0 0 0-25 29.16l-13.03 19.55a27.756 27.756 0 0 1-23.09 12.36c-10.51 0-20.12-5.94-24.82-15.34a78.902 78.902 0 0 1-8.33-35.29V367.5c0-8.56-6.94-15.5-15.5-15.5h-25.88c-14.49 0-28.38-5.76-38.63-16a54.659 54.659 0 0 1-16-38.63v-14.06c0-17.19 8.1-33.38 21.85-43.7l27.58-20.69a54.663 54.663 0 0 1 32.78-10.93h.89c8.48 0 16.85 1.97 24.43 5.77l14.72 7.36c3.68 1.84 7.93 2.14 11.83.84l47.31-15.77c6.33-2.11 10.6-8.03 10.6-14.7 0-8.56-6.94-15.5-15.5-15.5h-10.09c-4.11 0-8.05-1.63-10.96-4.54l-6.92-6.92a15.493 15.493 0 0 0-10.96-4.54H199.5c-8.56 0-15.5-6.94-15.5-15.5v-4.4c0-7.11 4.84-13.31 11.74-15.04l14.45-3.61c3.74-.94 7-3.23 9.14-6.44l8.08-12.11c2.87-4.31 7.71-6.9 12.89-6.9h24.21c8.56 0 15.5-6.94 15.5-15.5v-21.7C359.23 71.63 422.86 131.02 441.93 208H423.5c-8.56 0-15.5 6.94-15.5 15.5z";
// var AMERICA_ICON = "M248 8C111.03 8 0 119.03 0 256s111.03 248 248 248 248-111.03 248-248S384.97 8 248 8zm82.29 357.6c-3.9 3.88-7.99 7.95-11.31 11.28-2.99 3-5.1 6.7-6.17 10.71-1.51 5.66-2.73 11.38-4.77 16.87l-17.39 46.85c-13.76 3-28 4.69-42.65 4.69v-27.38c1.69-12.62-7.64-36.26-22.63-51.25-6-6-9.37-14.14-9.37-22.63v-32.01c0-11.64-6.27-22.34-16.46-27.97-14.37-7.95-34.81-19.06-48.81-26.11-11.48-5.78-22.1-13.14-31.65-21.75l-.8-.72a114.792 114.792 0 0 1-18.06-20.74c-9.38-13.77-24.66-36.42-34.59-51.14 20.47-45.5 57.36-82.04 103.2-101.89l24.01 12.01C203.48 89.74 216 82.01 216 70.11v-11.3c7.99-1.29 16.12-2.11 24.39-2.42l28.3 28.3c6.25 6.25 6.25 16.38 0 22.63L264 112l-10.34 10.34c-3.12 3.12-3.12 8.19 0 11.31l4.69 4.69c3.12 3.12 3.12 8.19 0 11.31l-8 8a8.008 8.008 0 0 1-5.66 2.34h-8.99c-2.08 0-4.08.81-5.58 2.27l-9.92 9.65a8.008 8.008 0 0 0-1.58 9.31l15.59 31.19c2.66 5.32-1.21 11.58-7.15 11.58h-5.64c-1.93 0-3.79-.7-5.24-1.96l-9.28-8.06a16.017 16.017 0 0 0-15.55-3.1l-31.17 10.39a11.95 11.95 0 0 0-8.17 11.34c0 4.53 2.56 8.66 6.61 10.69l11.08 5.54c9.41 4.71 19.79 7.16 30.31 7.16s22.59 27.29 32 32h66.75c8.49 0 16.62 3.37 22.63 9.37l13.69 13.69a30.503 30.503 0 0 1 8.93 21.57 46.536 46.536 0 0 1-13.72 32.98zM417 274.25c-5.79-1.45-10.84-5-14.15-9.97l-17.98-26.97a23.97 23.97 0 0 1 0-26.62l19.59-29.38c2.32-3.47 5.5-6.29 9.24-8.15l12.98-6.49C440.2 193.59 448 223.87 448 256c0 8.67-.74 17.16-1.82 25.54L417 274.25z";
// var FLAG_ICON = "M349.565 98.783C295.978 98.783 251.721 64 184.348 64c-24.955 0-47.309 4.384-68.045 12.013a55.947 55.947 0 0 0 3.586-23.562C118.117 24.015 94.806 1.206 66.338.048 34.345-1.254 8 24.296 8 56c0 19.026 9.497 35.825 24 45.945V488c0 13.255 10.745 24 24 24h16c13.255 0 24-10.745 24-24v-94.4c28.311-12.064 63.582-22.122 114.435-22.122 53.588 0 97.844 34.783 165.217 34.783 48.169 0 86.667-16.294 122.505-40.858C506.84 359.452 512 349.571 512 339.045v-243.1c0-23.393-24.269-38.87-45.485-29.016-34.338 15.948-76.454 31.854-116.95 31.854z";
var SVG_ICONS = {
  AFRICA_ICON:
    "M248 8C111.04 8 0 119.03 0 256s111.04 248 248 248 248-111.03 248-248S384.96 8 248 8zm0 448c-110.28 0-200-89.72-200-200S137.72 56 248 56c10.92 0 21.55 1.12 32 2.81v21.7c0 8.56-6.94 15.5-15.5 15.5h-24.21c-5.18 0-10.02 2.59-12.89 6.9l-8.08 12.11c-2.14 3.21-5.4 5.5-9.14 6.44l-14.45 3.61a15.492 15.492 0 0 0-11.74 15.04v4.4c0 8.56 6.94 15.5 15.5 15.5h90.09c4.11 0 8.05 1.63 10.96 4.54l6.92 6.92c2.91 2.91 6.85 4.54 10.96 4.54h10.09c8.56 0 15.5 6.94 15.5 15.5 0 6.67-4.27 12.59-10.6 14.7l-47.31 15.77c-3.9 1.3-8.15 1-11.83-.84l-14.72-7.36a54.682 54.682 0 0 0-24.43-5.77h-.89c-11.82 0-23.32 3.83-32.78 10.93l-27.58 20.69A54.545 54.545 0 0 0 152 283.31v14.06c0 14.49 5.76 28.38 16 38.63a54.641 54.641 0 0 0 38.63 16h25.88c8.56 0 15.5 6.94 15.5 15.5v29.88c0 12.25 2.85 24.33 8.33 35.29 4.7 9.4 14.31 15.34 24.82 15.34 9.28 0 17.94-4.64 23.09-12.36l13.03-19.55a159.608 159.608 0 0 1 25-29.16c2.47-2.26 4.14-5.26 4.76-8.56l4.3-22.83c.44-2.33 1.41-4.53 2.83-6.43l18.74-24.98c2.01-2.68 3.1-5.95 3.1-9.3V303.5c0-8.56-6.94-15.5-15.5-15.5h-8.21c-5.18 0-10.02-2.59-12.89-6.9l-13.24-19.86c-5.67-8.5-1.7-20.07 7.99-23.3l2.65-.88c4.54-1.51 9.52-.85 13.5 1.81l18.21 12.14a15.532 15.532 0 0 0 15.53.97l15.39-7.7c5.25-2.62 8.57-7.99 8.57-13.86v-6.93c0-8.56 6.94-15.5 15.5-15.5h18.44c3.82 15.41 6.07 31.43 6.07 48C448 366.28 358.28 456 248 456z",
  AMERICA_ICON:
    "M248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm-32 50.8v11.3c0 11.9-12.5 19.6-23.2 14.3l-24-12c14.9-6.4 30.7-10.9 47.2-13.6zm32 369.8V456c-110.3 0-200-89.7-200-200 0-29.1 6.4-56.7 17.6-81.7 9.9 14.7 25.2 37.4 34.6 51.1 5.2 7.6 11.2 14.6 18.1 20.7l.8.7c9.5 8.6 20.2 16 31.6 21.8 14 7 34.4 18.2 48.8 26.1 10.2 5.6 16.5 16.3 16.5 28v32c0 8.5 3.4 16.6 9.4 22.6 15 15.1 24.3 38.7 22.6 51.3zm42.7 22.7l17.4-46.9c2-5.5 3.3-11.2 4.8-16.9 1.1-4 3.2-7.7 6.2-10.7l11.3-11.3c8.8-8.7 13.7-20.6 13.7-33 0-8.1-3.2-15.9-8.9-21.6l-13.7-13.7c-6-6-14.1-9.4-22.6-9.4H232c-9.4-4.7-21.5-32-32-32s-20.9-2.5-30.3-7.2l-11.1-5.5c-4-2-6.6-6.2-6.6-10.7 0-5.1 3.3-9.7 8.2-11.3l31.2-10.4c5.4-1.8 11.3-.6 15.5 3.1l9.3 8.1c1.5 1.3 3.3 2 5.2 2h5.6c6 0 9.8-6.3 7.2-11.6l-15.6-31.2c-1.6-3.1-.9-6.9 1.6-9.3l9.9-9.6c1.5-1.5 3.5-2.3 5.6-2.3h9c2.1 0 4.2-.8 5.7-2.3l8-8c3.1-3.1 3.1-8.2 0-11.3l-4.7-4.7c-3.1-3.1-3.1-8.2 0-11.3L264 112l4.7-4.7c6.2-6.2 6.2-16.4 0-22.6l-28.3-28.3c2.5-.1 5-.4 7.6-.4 78.2 0 145.8 45.2 178.7 110.7l-13 6.5c-3.7 1.9-6.9 4.7-9.2 8.1l-19.6 29.4c-5.4 8.1-5.4 18.6 0 26.6l18 27c3.3 5 8.4 8.5 14.1 10l29.2 7.3c-10.8 84-73.9 151.9-155.5 169.7z",
  FLAG_ICON:
    "M344.348 74.667C287.742 74.667 242.446 40 172.522 40c-28.487 0-53.675 5.322-76.965 14.449C99.553 24.713 75.808-1.127 46.071.038 21.532.999 1.433 20.75.076 45.271-1.146 67.34 12.553 86.382 32 93.258V500c0 6.627 5.373 12 12 12h8c6.627 0 12-5.373 12-12V378.398c31.423-14.539 72.066-29.064 135.652-29.064 56.606 0 101.902 34.667 171.826 34.667 51.31 0 91.933-17.238 130.008-42.953 6.589-4.45 10.514-11.909 10.514-19.86V59.521c0-17.549-18.206-29.152-34.122-21.76-36.78 17.084-86.263 36.906-133.53 36.906zM48 28c11.028 0 20 8.972 20 20s-8.972 20-20 20-20-8.972-20-20 8.972-20 20-20zm432 289.333C456.883 334.03 415.452 352 371.478 352c-63.615 0-108.247-34.667-171.826-34.667-46.016 0-102.279 10.186-135.652 26V106.667C87.117 89.971 128.548 72 172.522 72c63.615 0 108.247 34.667 171.826 34.667 45.92 0 102.217-18.813 135.652-34.667v245.333z"
};

function TimelineControl(data, parent, onChange, ui, geoCache) {
  // A D3.js cumulative stacked area graph with embarked counts as Y-axes,
  // grouped by major region of disembarkation/embarkation or flag.
  var self = this;
  var NORMAL_HEIGHT = 100;
  var PLOT_LEFT_MARGIN = 280;
  var PLOT_RIGHT_MARGIN = 60;
  var PLOT_VERTICAL_MARGIN = 4;
  var ICONS = [
    {
      key: "flag",
      path: ui.flagIcon,
      tooltip: gettext("Group by ship nationality")
    },
    {
      key: "sourceRegion",
      path: ui.embarkationIcon,
      tooltip: gettext("Group by embarkation region")
    },
    {
      key: "destinationRegion",
      path: ui.disembarkationIcon,
      tooltip: gettext("Group by disembarkation broad region")
    }
  ];

  // Method to destroy the UI elements that make up the timeline control.
  self.dispose = function() {
    d3.select("#timeline_slider").remove();
  };
  self.dispose();

  var width = 960;
  var left = 40;
  var top = 300 - PLOT_VERTICAL_MARGIN;
  var INITIAL_OPACITY = 0.5;
  var g = parent
    .append("g")
    .attr("id", "timeline_slider")
    .classed("timeline_slider_group", true)
    .attr("transform", "translate(" + left + "," + top + ")");

  self.resize = function(w, h) {
    left = (w - width) / 2;
    top = h - NORMAL_HEIGHT - PLOT_VERTICAL_MARGIN;
    g.attr("transform", "translate(" + left + "," + top + ")");
  };

  // Enrich data set with grouping variables.
  var regNames = geoCache.regionNames;
  var regValues = {};
  var getRegionName = function(set, pk, fallback) {
    var match = set[pk];
    var good = !!match && !!match.name && !!match.value;
    if (good) {
      regValues[match.name] = match.value;
    } else {
      regValues[fallback] = 999999; // fallback appears last
    }
    return gettext(good ? match.name : fallback);
  };
  for (var i = 0; i < data.length; ++i) {
    var item = data[i];
    if (ui.networkName == "intra") {
      item.sourceRegion = getRegionName(
        regNames.dst, // This is not a typo: dst holds Broad Regions and they are the same for embk/disbk
        item.bregsrc,
        "Other"
      );
    } else {
      item.sourceRegion = getRegionName(
        regNames.src,
        item.regsrc,
        "Other Africa"
      );
    }
    item.destinationRegion = getRegionName(regNames.dst, item.bregdst, "Other");
    item.flag = gettext(geoCache.nations[item.nat_id] || "Other");
  }

  var currentGroupField = null;
  var setCurrentGroupField = null;
  var lastTickPos = 0;
  var lastSetTime = -1;
  var createTimelinePlot = function(groupField) {
    $("#timeline_slider").empty();
    // Append background.
    g.append("rect")
      .attr("height", NORMAL_HEIGHT)
      .attr("width", width)
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("id", "timelapse-timeline-bg");
    for (var i = 0; i < ICONS.length; ++i) {
      var icon = ICONS[i];
      var btn = _addIconBackgroundRect(g, icon.path)
        .datum(icon)
        .classed("timeline_group_button", true)
        .on("mouseenter", function(d) {
          d3.select(this)
            .selectAll("path")
            .style("fill", "red");
          ui.showTooltip(d.tooltip);
        })
        .on("mouseleave", function(d) {
          d3.select(this)
            .selectAll("path")
            .style("fill", d.key == groupField ? "black" : "gray");
          ui.hideTooltip();
        })
        .on("click", function(d) {
          if (setCurrentGroupField) {
            setCurrentGroupField(d.key);
          }
        })
        .attr("transform", "translate(7," + (8 + 30 * i) + ")scale(0.05)");
      btn
        .selectAll("path")
        .attr("fill", icon.key == groupField ? "black" : "gray");
    }
    var accVar = groupField == "destinationRegion" ? "disembarked" : "embarked";
    var grouped = d3
      .nest()
      .key(function(d) {
        return d[groupField];
      })
      .sortValues(function(a, b) {
        return a.year - b.year;
      })
      .rollup(function(g) {
        // Build aggregates based on year.
        var agg = [];
        var lastYear = -1;
        var acc = 0;
        for (var i = 0; i < g.length; ++i) {
          var d = g[i];
          acc += d[accVar];
          if (d.year == lastYear) {
            agg[agg.length - 1].acc = acc;
          } else {
            lastYear = d.year;
            agg.push({ year: lastYear, acc: acc });
          }
        }
        return agg;
      })
      .entries(data);
    if (groupField == "flag") {
      var otherFlag = gettext("Other");
      grouped.sort(function(a, b) {
        if (a.key == otherFlag) return 1;
        if (b.key == otherFlag) return -1;
        return (
          b.value[b.value.length - 1].acc - a.value[a.value.length - 1].acc
        );
      });
    } else {
      grouped.sort(function(a, b) {
        return regValues[a.key] - regValues[b.key];
      });
    }
    var keys = d3
      .set(grouped, function(grp) {
        return grp.key;
      })
      .values();
    var color = d3
      .scaleOrdinal()
      .domain(keys)
      .range(d3.schemeSet1);
    // Update color for voyages.
    for (var i = 0; i < data.length; ++i) {
      var item = data[i];
      item.color = color(item[groupField]);
    }
    var yearData = {};
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
    var start = d3.min(data, function(d) {
      return d.year;
    });
    var end = d3.max(data, function(d) {
      return d.year;
    });
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

    var x = d3
      .scaleLinear()
      .domain(
        d3.extent(table, function(d) {
          return d.year;
        })
      )
      .range([0, width - PLOT_LEFT_MARGIN - PLOT_RIGHT_MARGIN]);
    var xAxis = d3
      .axisBottom()
      .scale(x)
      .ticks(20)
      .tickFormat(function(d) {
        return d;
      });
    var yMaxValue = d3.sum(data, function(d) {
      return d.embarked;
    });
    var y = d3
      .scaleLinear()
      .domain([0, yMaxValue])
      .range([
        NORMAL_HEIGHT - 2 * PLOT_VERTICAL_MARGIN - 16, // 16 is the offset for the x-axis label
        PLOT_VERTICAL_MARGIN
      ]);
    var yAxis = d3
      .axisRight()
      .scale(y)
      .ticks(4);
    var area = d3
      .area()
      .x(function(d) {
        return x(d.data.year);
      })
      .y0(function(d) {
        return y(d[0]);
      })
      .y1(function(d) {
        return y(d[1]);
      });
    var stack = d3.stack();
    stack.keys(keys);
    var stackData = stack(table);
    var categories = g
      .selectAll(".category")
      .data(stackData)
      .enter()
      .append("g")
      .attr("class", function(d) {
        return "category " + d.key;
      });

    categories
      .append("path")
      .attr("class", "area")
      .attr("d", area)
      .attr("transform", "translate(" + PLOT_LEFT_MARGIN + ", 0)")
      .style("pointer-events", "none")
      .style("fill", function(d) {
        return color(d.key);
      });
    // Labels for categories.
    var paddedHeight = NORMAL_HEIGHT - 2 * PLOT_VERTICAL_MARGIN;
    var paddedHeightLine = paddedHeight - 20; // 25 is the offset for the x-axis label
    categories
      .append("text")
      .datum(function(d) {
        return d;
      })
      .attr("transform", function(d, i) {
        return (
          "translate(60," +
          (PLOT_VERTICAL_MARGIN + (i * paddedHeight) / keys.length) +
          ")"
        );
      })
      .attr("dy", "1em")
      .style("text-anchor", "start")
      .attr("class", "timelapse-timeline-group-label")
      .text(function(d) {
        return d.key;
      });
    categories
      .append("rect")
      .datum(function(d) {
        return d;
      })
      .attr("transform", function(d, i) {
        return (
          "translate(40," +
          (PLOT_VERTICAL_MARGIN + 2 + (i * paddedHeight) / keys.length) +
          ")"
        );
      })
      .attr("width", 15)
      .attr("height", Math.min(8, NORMAL_HEIGHT / keys.length - 4))
      .attr("fill", function(d) {
        return color(d.key);
      })
      .attr("stroke", "gray")
      .attr("stroke-width", 1);
    g.append("g")
      .attr("class", "t_axis")
      .attr(
        "transform",
        "translate(" +
        PLOT_LEFT_MARGIN +
        "," +
        (NORMAL_HEIGHT - 25) + // 25 is the offset for the x-axis label
          ")"
      )
      .attr("color", "black")
      .call(xAxis);
    g.append("g")
      .attr("class", "embarked_axis")
      .attr("transform", "translate(" + (width - PLOT_RIGHT_MARGIN) + ",0)")
      .attr("color", "black")
      .call(yAxis);
    categories
      .on("mouseenter", function(d) {
        ui.showTooltip(d.key);
      })
      .on("mouseleave", function() {
        ui.hideTooltip();
      });
    d3.selectAll("g.tick>text").style("font-size", "10px");

    // Create time indicator bar.
    var tickLine = g
      .append("line")
      .classed("timelapse_slider_x_axis_bar", true)
      .attr("stroke", "black")
      .attr("stroke-width", 2)
      .attr(
        "transform",
        "translate(" +
          (PLOT_LEFT_MARGIN + lastTickPos) +
          "," +
          PLOT_VERTICAL_MARGIN +
          ")"
      )
      .attr("y2", paddedHeightLine)
      .style("stroke-opacity", "0.6");
    var embCirclePos = function(val) {
      if (val > 0) {
        // Convert a year value to the embarked count value for that year.
        if (val < table[0].year || val > table[table.length - 1].year) {
          val = 0;
        } else {
          val = table[val - table[0].year].total;
        }
      }
      return (
        "translate(" + (width + 1 - PLOT_RIGHT_MARGIN) + "," + y(val) + ")"
      );
    };
    var tickEmbarkedCircle = g
      .append("circle")
      .classed("timelapse_slider_y_axis_circle", true)
      .attr("r", 3)
      .attr("fill", "black")
      .attr("transform", embCirclePos(0))
      .style("opacity", "0.8");
    var _maxTickPos = width - PLOT_LEFT_MARGIN - PLOT_RIGHT_MARGIN;
    self.setTime = function(time) {
      var nextTickPos = ~~Math.round(x(time / 120));
      if (nextTickPos > _maxTickPos) nextTickPos = _maxTickPos;
      if (nextTickPos != lastTickPos) {
        tickLine.attr(
          "transform",
          "translate(" +
            (PLOT_LEFT_MARGIN + nextTickPos) +
            "," +
            PLOT_VERTICAL_MARGIN +
            ")"
        );
        tickEmbarkedCircle.attr(
          "transform",
          embCirclePos(~~Math.round(time / 120))
        );
        lastTickPos = nextTickPos;
        lastSetTime = time;
      }
    };
    if (lastSetTime >= 0) {
      lastTickPos = -1;
      self.setTime(lastSetTime);
    }

    // Add a Y-axis label.
    g.append("text")
      .attr(
        "transform",
        "translate(" + PLOT_LEFT_MARGIN + "," + PLOT_VERTICAL_MARGIN + ")"
      )
      .attr("dy", "1em")
      .attr("class", "timelapse-timeline-title-label")
      .text(
        gettext("Accumulated captives") +
          " (" +
          (groupField != "destinationRegion"
            ? gettext("embarked")
            : gettext("disembarked")) +
          ")"
      );

    // Create mouse over bar.
    var hoverLine = g.append("g")
      .classed("timelapse_slider_x_axis_hover", true)
      .attr(
        "transform",
        "translate(" + PLOT_LEFT_MARGIN + "," + PLOT_VERTICAL_MARGIN + ")"
      )
      .style("opacity", 0);
    hoverLine
      .append("rect")
      .attr("x", -1)
      .attr("width", 2)
      .attr("height", paddedHeightLine)
      .attr("fill", "white");
    hoverLine
      .append("line")
      .attr("stroke", "red")
      .attr("stroke-width", 2)
      .style("stroke-dasharray", "2, 2")
      .attr("y2", paddedHeightLine);
    g.on("mousemove", function() {
      var xCoord = d3.mouse(this)[0];
      if (xCoord >= PLOT_LEFT_MARGIN && xCoord <= width - PLOT_RIGHT_MARGIN) {
        hoverLine
          .style("opacity", "0.8")
          .attr(
            "transform",
            "translate(" + xCoord + "," + PLOT_VERTICAL_MARGIN + ")"
          );
      } else {
        hoverLine.style("opacity", 0);
      }
    })
      .on("mouseleave", function() {
        hoverLine.style("opacity", 0);
      })
      .on("mousedown", function() {
        var update = function() {
          var xCoord = d3.mouse(this)[0];
          if (
            xCoord >= PLOT_LEFT_MARGIN &&
            xCoord <= width - PLOT_RIGHT_MARGIN
          ) {
            // Compute xValue to set.
            onChange(120 * ~~Math.round(x.invert(xCoord - PLOT_LEFT_MARGIN)));
          }
        }.bind(this);
        update();
        ui.map.dragging.disable();
        hoverLine.style("visibility", "hidden");
        // Track mouse movements until mouse up.
        var w = d3
          .select(window)
          .on("mousemove", update)
          .on("mouseup", function() {
            w.on("mousemove", null).on("mouseup", null);
            ui.map.dragging.enable();
            hoverLine.style("visibility", "visible");
          });
        d3.event.preventDefault();
        d3.event.stopPropagation();
      });
  };

  setCurrentGroupField = function(field) {
    if (currentGroupField != field) {
      createTimelinePlot(field);
      d3.selectAll("#group_field_btn_" + field + ">path").attr("fill", "black");
    }
    currentGroupField = field;
  };

  setCurrentGroupField("flag");
}

var _cachedGeoData = {};

function AnimationHelper(data, networkName, options) {
  var self = this;
  var geoCache = _cachedGeoData[networkName] || new _fetchGeoData(networkName);
  _cachedGeoData[networkName] = geoCache;
  // Keep the line below.
  voyagesMap.addLayer(L.polyline(L.latLng(0, 0), L.latLng(0, 0)));
  options = options || new AnimationOptions();

  // We add both an SVG as well as a Canvas element to the map.
  // The idea is to run the animation on the canvas, which is much
  // faster and use the SVG when paused to allow UI interaction.
  // Luckily D3.js is powerful enough that we can reuse most of
  // the code and render the ship's circles on each target with
  // only minor changes.
  var map = voyagesMap._map;
  var svg = d3.select(map.getPanes().overlayPane).append("svg");
  var canvas = d3.select(map.getPanes().overlayPane).append("canvas");
  canvas.attr("id", "timelapse_animation_canvas");
  var ctxCanvas = canvas.node().getContext("2d");
  // We create a virtual node that will be used for D3.js to
  // produce the DOM elements for ships when the animation is
  // running. The elements produced by D3.js are then rendered
  // directly on the Canvas.
  var faux = d3.select(document.createElement("faux"));
  faux.attr("id", "faux_node");
  var mapContainer = map.getContainer();
  var controlLayer = d3
    .select(mapContainer)
    .append("svg")
    .attr("id", "timelapse_control_layer")
    .classed("timelapse_control_group", true)
    .classed("leaflet-control", true)
    .attr("width", 0)
    .style("pointer-events", "none");
  var ctrlBackground = controlLayer
    .on("mouseenter", function() {
      map.doubleClickZoom.disable();
      ctrlBackground
        .transition()
        .duration(300)
        .style("opacity", 1.0);
    })
    .on("mouseleave", function() {
      map.doubleClickZoom.enable();
      ctrlBackground
        .transition()
        .duration(300)
        .style("opacity", 0.5);
    })
    .append("rect")
    .attr("width", 0)
    .attr("height", 0)
    .attr("fill", "rgba(255, 255, 255, 0.5)")
    .attr("rx", 4)
    .attr("ry", 4)
    .style("opacity", 0)
    .style("pointer-events", "all");
  var tooltip = d3
    .select(mapContainer)
    .append("div")
    .attr("id", "timeline_slider_tooltip")
    .attr("class", "tooltip")
    .style("opacity", 0)
    .style("padding", "6px")
    .style("background", "white");
  var showTooltip = function(html, offsetX, offsetY) {
    var pos = d3.mouse(mapContainer);
    tooltip
      .transition()
      .duration(200)
      .style("opacity", 0.9);
    tooltip
      .html(html)
      .style("left", pos[0] + (offsetX || 40) + "px")
      .style("top", pos[1] + (offsetY || -40) + "px");
  };
  var hideTooltip = function() {
    tooltip
      .transition()
      .duration(500)
      .style("opacity", 0);
  };

  var g = svg.append("g").attr("class", "leaflet-zoom-hide");

  var hoverRed = function(e, tooltipHtml, tooltipOffsetX, tooltipOffsetY) {
    var colorize = function(sel, c) {
      sel
        .transition()
        .duration(300)
        .style("fill", c);
    };
    return e
      .on("mouseenter", function() {
        var self = d3.select(this);
        if (self.classed("timelapse_btn_disabled")) return;
        colorize(self, "red");
        colorize(self.selectAll("path"), "red");
        if (tooltipHtml) {
          showTooltip(tooltipHtml, tooltipOffsetX, tooltipOffsetY);
        }
      })
      .on("mouseleave", function() {
        var self = d3.select(this);
        colorize(self, "black");
        colorize(self.selectAll("path"), "black");
        if (tooltipHtml) {
          hideTooltip();
        }
      });
  };

  // Set SVG size and position within map.
  var bounds = null;
  var topLeft = null;
  var positionSvg = function() {
    if (!self.control) return;
    bounds = map.getBounds();
    topLeft = map.latLngToLayerPoint(bounds.getNorthWest());
    var bottomRight = map.latLngToLayerPoint(bounds.getSouthEast());
    var hostWidth = bottomRight.x - topLeft.x;
    var hostHeight = bottomRight.y - topLeft.y;
    // Set position of SVG and Canvas to align with the map.
    svg
      .attr("width", hostWidth)
      .attr("height", hostHeight)
      .style("left", topLeft.x + "px")
      .style("top", topLeft.y + "px");
    canvas
      .attr("width", hostWidth)
      .attr("height", hostHeight)
      .style("left", topLeft.x + "px")
      .style("top", topLeft.y + "px");
    // Apply a transform so that when drawing the ships'
    // circles, they geo-coordinates match.
    ctxCanvas.transform(1, 0, 0, 1, -topLeft.x, -topLeft.y);
    g.attr("transform", "translate(" + -topLeft.x + "," + -topLeft.y + ")");
    if (self.control && self.control.isPaused()) {
      // This code is necessary when the user zooms the map with the
      // animation paused. The points have to be re-computed with
      // respect to the map. When the animation is running, we do
      // not bother to update the position of emitted nodes since
      // those nodes are short lived.
      g.selectAll(".animation_voyage_group").each(function() {
        var latLng = this.__data__.latLng;
        if (latLng) {
          var point = map.latLngToLayerPoint(latLng);
          this.__data__.point = point;
          d3.select(this).attr("transform", function(d) {
            return "translate(" + point.x + "," + point.y + ")";
          });
        }
      });
    }
    // Position the UI controls.
    var size = map.getSize();
    controlLayer.attr("width", size.x).attr("height", size.y);
    // ctrlBackground.attr(
    //   "transform",
    //   "translate(" + (size.x / 2 - 60) + ", 15)"
    // );
    // yearLabel.attr("transform", "translate(" + size.x / 2 + ", 50)");
    // playPauseBtn.attr(
    //   "transform",
    //   "translate(" + (size.x / 2 - 7) + ", 55) scale(0.04)"
    // );
    // speedUpBtn.attr(
    //   "transform",
    //   "translate(" + (size.x / 2 + 26) + ", 55) scale(0.04)"
    // );
    // speedDownBtn.attr(
    //   "transform",
    //   "translate(" + (size.x / 2 - 45) + ", 55) scale(0.04)"
    // );
    if (ui.timeline) {
      ui.timeline.resize(size.x, size.y);
    }
  };

  var ui = {};

  // Handle selected ship route display.
  var selectedRoute = null;
  var setSelectedRoute = function(route, circle) {
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

  var closeVoyageInfoDialog = function() {
    // notify vue v-voyage-info component to update its prop "isVisible"
    Vue.set(searchBar.timelapse, "isVisible", false);
  };

  var addInteractiveUI = function() {
    g.selectAll(".animation_voyage_group:not(.interactive_voyage_node)")
      .attr("id", function(d) {
        return "animation_voyage_id_" + d.voyage.data.voyage_id;
      })
      .classed("interactive_voyage_node", true)
      .append("circle")
      .classed("animation_voyage_outer_circle", true)
      .attr("r", 10)
      .style("opacity", 0)
      .on("mouseover", function() {
        $(this).animate({ opacity: 1 }, 100);
      })
      .on("mouseout", function() {
        if (ui.clickedCircle != this) {
          $(this).animate({ opacity: 0 }, 100);
        }
      })
      .on("click", function() {
        closeVoyageInfoDialog();
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
        data.source_name = geoCache.portSegments["src"][data.src].name;
        data.destination_name = geoCache.portSegments["dst"][data.dst].name;
        data.ship_nationality_name =
          (geoCache.nations || {})[data.nat_id] || "";

        // notify vue v-voyage-info component to update its props "data" and "isVisible"
        Vue.set(searchBar.timelapse, "data", data);
        Vue.set(searchBar.timelapse, "isVisible", true);
      });
  };

  map.on("zoomend", positionSvg);
  $(window).resize(positionSvg);

  // Set up ui object and hook events.
  ui = {
    map: map,
    d3view: faux,
    monthsPerSecond: options.initialSpeed,
    setSelectedRoute: setSelectedRoute,
    showTooltip: showTooltip,
    hideTooltip: hideTooltip,
    networkName: networkName,
    flagIcon: SVG_ICONS.FLAG_ICON,
    // TODO [Yang/Domingos]: Find appropriate Icons for Intra-American
    embarkationIcon: /*networkName == "intra" ? : */ SVG_ICONS.AFRICA_ICON,
    disembarkationIcon: /*networkName == "intra" ? : */ SVG_ICONS.AMERICA_ICON
  };
  var updateControls = function() {
    if (self.control.isPaused()) {
      // playPauseBtn.selectAll("path").attr("d", PLAY_PATH);
    } else {
      closeVoyageInfoDialog();
      // playPauseBtn.selectAll("path").attr("d", PAUSE_PATH);
    }
  };
  ui.pause = function() {
    if (!!self.control && !self.control.isPaused()) {
      self.control.pause();
      addInteractiveUI();
    }
    updateControls();
  };
  ui.play = function() {
    if (!!self.control && self.control.isPaused()) {
      self.control.play();
    }
    updateControls();
  };
  var maxYear = 0;
  ui.initialize = function(control) {
    self.control = control;
    maxYear = ~~Math.floor(control.getModel().getLastStartTime() / 120);
    // Initialize plot slider.
    ui.timeline = new TimelineControl(
      data,
      controlLayer,
      control.jumpTo,
      ui,
      geoCache
    );
    // hoverRed(playPauseBtn);
    // hoverRed(speedDownBtn, gettext("Slow down the clock"));
    // hoverRed(speedUpBtn, gettext("Speed up the clock"));

    // notify vue v-play component to update its props "ui" and "control"
    Vue.set(searchBar.timelapse, "ui", ui);
    Vue.set(searchBar.timelapse, "control", control);

    // playPauseBtn.on("click", function() {
    //   if (control.isPaused()) {
    //     ui.play();
    //   } else {
    //     ui.pause();
    //   }
    // });

    // notify vue v-speed component to update its props "ui" and "options"
    Vue.set(searchBar.timelapse, "options", options);

    var updateSpeed = function(speed) {
      speed = Math.min(options.maxSpeed, Math.max(options.minSpeed, speed));
      ui.monthsPerSecond = speed;
      control.setStepPerSec(speed * 10, Math.max(1.0, 12 / speed));
      // speedDownBtn.classed("timelapse_btn_disabled", speed == options.minSpeed);
      // speedUpBtn.classed("timelapse_btn_disabled", speed == options.maxSpeed);
    };
    // speedDownBtn.on("click", function() {
    //   if (ui.monthsPerSecond > options.minSpeed) {
    //     updateSpeed(ui.monthsPerSecond / 2);
    //   }
    // });
    // speedUpBtn.on("click", function() {
    //   if (ui.monthsPerSecond < options.maxSpeed) {
    //     updateSpeed(ui.monthsPerSecond * 2);
    //   }
    // });
  };
  ui.prerender = function() {
    // When the animation is running, D3.js will be used to
    // modify the DOM on our faux element. When paused, it
    // will modify the DOM of the SVG element.
    ui.d3view = self.control.isPaused() ? g : faux;
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
    // We specify the animationTime in seconds and let the control
    // figure out how many frames that would take.
    var animationTime = 1.6 + 0.4 * Math.random();
    var v = new Voyage(i, item.src, item.dst, start, animationTime, item);
    voyages.push(v);
  }
  // Should be called when the helper will no longer be used.
  self.dispose = function() {
    if (self.control) {
      closeVoyageInfoDialog();
      self.control.stop();
      self.control.dispose();
    }
    if (ui.timeline) {
      ui.timeline.dispose();
    }
    d3.select("#timeline_slider_tooltip").remove();
    d3.select("#timelapse_control_layer").remove();
    d3.select("#timelapse_animation_canvas").remove();
    d3.select("#faux_node").remove();
  };
  var shipTrafficBaseLine = d3.quantile(
    $.map(voyages, function(v) {
      return v.data.embarked;
    }).sort(function(a, b) {
      return a - b;
    }),
    options.shipTrafficBaseLineQuantile
  );
  ui.setTime = function(time) {
    // Update slider and label.
    ui.timeline.setTime(time);
    // Due to the artificially inflated length of voyages, the simulated
    // time might go beyond the last year of the real simulated range.
    // Here we limit the maximum displayed time and let the animation
    // continue to finish the last voyages routes.
    var maxTime = (maxYear + 1) * 120 - 1;
    if (time > maxTime) time = maxTime;
    var yearVal = ~~Math.floor(time / 120);

    // notify vue v-year component to update its prop "currentYear"
    Vue.set(searchBar.timelapse, "currentYear", yearVal)

    if (time % (10 * ui.monthsPerSecond) == 0) positionSvg();
    closeVoyageInfoDialog();
    if (self.control.isPaused()) {
      addInteractiveUI();
    } else if (topLeft) {
      // We have to manually draw the elements that correspond to
      // the D3.js generated virtual DOM elements.
      g.selectAll(".animation_voyage_group").remove();
      ctxCanvas.clearRect(
        topLeft.x,
        topLeft.y,
        canvas.attr("width"),
        canvas.attr("height")
      );
      ctxCanvas.filter = "blur(0.7px)";
      // It is more efficient to draw elements with the same color together.
      var nested = d3
        .nest()
        .key(function(d) {
          return d.voyage.color();
        })
        .entries(faux.selectAll(".animation_voyage_group").data());
      for (var i = 0; i < nested.length; ++i) {
        ctxCanvas.beginPath();
        ctxCanvas.fillStyle = nested[i].key;
        var values = nested[i].values;
        for (var j = 0; j < values.length; ++j) {
          var d = values[j];
          var pt = d.point;
          var r = _getShipCircleRadius(d, shipTrafficBaseLine);
          ctxCanvas.moveTo(pt.x + r, pt.y);
          ctxCanvas.arc(pt.x, pt.y, r, 0, 2 * Math.PI);
        }
        ctxCanvas.fill();
      }
    }
  };
  d3MapTimelapse(
    voyages,
    ui,
    ui.monthsPerSecond * 10,
    geoCache,
    shipTrafficBaseLine,
    options
  );
}
