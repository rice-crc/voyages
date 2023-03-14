const createLineChart = (data, settings) => {
    const {
        marginLeft = 40,
        marginRight = 40,
        marginBottom = 40,
        marginTop = 40,
        width = 800,
        height = 500,
        stroke = "steelblue",
        strokeLinecap = "round", // stroke line cap of the line
        strokeLinejoin = "round", // stroke line join of the line
        strokeWidth = 1.5 // stroke width of line, in pixels
    } = settings ?? {};
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height]);
    const xFn = entry => entry.x;
    const yFn = entry => entry.y;
    const X = d3.map(data, xFn);
    const Y = d3.map(data, yFn);
    const xScale = d3.scaleLinear()
        .domain(d3.extent(X))
        .range([marginLeft, width - marginRight]);
    const yScale = d3.scaleLinear()
        .domain(d3.extent(Y))
        .range([height - marginBottom, marginTop]);
    const xAxis = d3.axisBottom(xScale).ticks(width / 60);
    const yAxis = d3.axisLeft(yScale).ticks(height / 50);
    const gx = svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(xAxis);
    svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(yAxis);
    const line = d3.line()
        .curve(d3.curveLinear)
        .x(i => xScale(X[i]))
        .y(i => yScale(Y[i]));
    const xr = d3.range(X.length);
    const linePath = svg
        .append("path")
        .attr("stroke", stroke)
        .attr("stroke-width", strokeWidth)
        .attr("stroke-linecap", strokeLinecap)
        .attr("stroke-linejoin", strokeLinejoin)
        .attr("fill", "none")
        .attr("d", line(xr));
    return svg.node();
};