// These d3.js charting functions are heavily inspired by samples found in
// https://observablehq.com/

const _createChartCore = (data, { xScaleCore, plot }, settings) => {
    const {
        marginLeft = 40,
        marginRight = 40,
        marginBottom = 40,
        marginTop = 40,
        width = 800,
        height = 500,
        isPercentage = false,
        isCategorical = false
    } = settings ?? {};
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height]);
    const xFn = entry => entry.x;
    const yFn = entry => entry.y;
    const X = d3.map(data, xFn);
    const Y = d3.map(data, yFn);
    const xScale = xScaleCore(X, [marginLeft, width - marginRight]);
    const yScale = d3.scaleLinear()
        .domain(d3.extent(Y))
        .range([height - marginBottom, marginTop]);
    let xAxis = d3.axisBottom(xScale);
    if (isCategorical) {
        const MAX_TICKS = 30;
        if (X.length > MAX_TICKS) {
            // Avoid placing too many ticks.
            const tvals = [];
            const step = Math.round(X.length / MAX_TICKS);
            for (let i = 0; i < X.length; i += step) {
                tvals.push(X[i]);
            }
            xAxis = xAxis.tickValues(tvals);
        }
    } else {
        xAxis = xAxis.ticks(width / 60);
    }
    let yAxis = d3.axisRight(yScale)
        .tickSize(width - marginRight);
    if (isPercentage) {
        yAxis = yAxis.tickFormat(d3.format(".0%"));
    }
    svg
        .attr("transform", `translate(${marginLeft},0)`)
        .call(yAxis)
        .call(g => g.select(".domain")
            .remove())
        .call(g => g.selectAll(".tick line")
            .attr("stroke-opacity", 0.5)
            .attr("stroke-dasharray", "2,2"))
        .call(g => g.selectAll(".tick text")
            .attr("x", 4)
            .attr("dy", -4));
    const gx = svg.append("g")
        .classed("xAxis", true)
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(xAxis);
    plot(svg, X, Y, xScale, yScale);
    return svg.node();
}; 

const createLineChart = (data, settings) => {
    const {
        stroke = "steelblue",
        strokeLinecap = "round", // stroke line cap of the line
        strokeLinejoin = "round", // stroke line join of the line
        strokeWidth = 1.5 // stroke width of line, in pixels
    } = settings ?? {};
    return _createChartCore(
        data, {
            xScaleCore: (X, range) => d3.scaleLinear().domain(d3.extent(X)).range(range),
            plot: (svg, X, Y, xScale, yScale) => {
                const xr = d3.range(X.length);
                const line = d3.line()
                    .curve(d3.curveLinear)
                    .x(i => xScale(X[i]))
                    .y(i => yScale(Y[i]));
                const linePath = svg
                    .append("path")
                    .attr("stroke", stroke)
                    .attr("stroke-width", strokeWidth)
                    .attr("stroke-linecap", strokeLinecap)
                    .attr("stroke-linejoin", strokeLinejoin)
                    .attr("fill", "none")
                    .attr("d", line(xr));
            }
        },
        settings);
}

const createBarChart = (data, settings) => {
    const { 
        color = "steelblue",
        xPadding = 0.1
    } = settings ?? {};
    return _createChartCore(
        data, { 
            xScaleCore: (X, range) => d3.scaleBand(X, range).padding(xPadding),
            plot: (svg, X, Y, xScale, yScale) => {
                const bar = svg.append("g")
                    .attr("fill", color)
                    .selectAll("rect")
                    .data(d3.range(X.length))
                    .join("rect")
                        .attr("x", i => xScale(X[i]))
                        .attr("y", i => yScale(Y[i]))
                        .attr("height", i => yScale(d3.min(Y)) - yScale(Y[i]))
                        .attr("width", xScale.bandwidth());
                svg.select('.xAxis')
                    .call(g => g.selectAll("text")
                        .style("text-anchor", "end")
                        .attr("dx", "-.8em")
                        .attr("dy", ".15em")
                        .attr("transform", "rotate(-45)"));
            }
        },
        {isCategorical: true, ...settings});
}