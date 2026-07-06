document.addEventListener("DOMContentLoaded", function () {
    const chartDom = document.getElementById('main-graph');
    const searchInput = document.getElementById('entity-search');
    const roleFilter = document.getElementById('role-filter');
    if (!chartDom || !searchInput || !roleFilter) return;

    const myChart = echarts.init(chartDom);
    const dataUrl = chartDom.getAttribute('data-api-url');
    const producerDetailBase = chartDom.getAttribute('data-producer-url') || '/governance-map/producers/';
    const consumerDetailBase = chartDom.getAttribute('data-consumer-url') || '/governance-map/consumers/';
    const endpointDetailBase = chartDom.getAttribute('data-endpoint-url') || '/governance-map/endpoints/';
    
    // Pristine master dataset storage reference
    let masterData = { nodes: [], edges: [] };

    // Common configurations shared across canvas re-renders
    const commonSeriesConfig = {
        type: 'graph',
        layout: 'force',
        draggable: true,
        roam: true,
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: [0, 10],
        categories: [
            { name: 'Producers', itemStyle: { color: '#000000' } },
            { name: 'Endpoints', itemStyle: { color: '#00a86b' } },
            { name: 'Consumers', itemStyle: { color: '#ff9900' } }
        ],
        label: {
            show: true,
            position: 'right',
            formatter: '{b}',
            textStyle: { fontStyle: 'normal', fontSize: 12 }
        },
        force: { repulsion: 600, edgeLength: 160, gravity: 0.08 },
        lineStyle: { color: '#bbb', width: 1.5, curveness: 0.12 }
    };

    // 1. Ingest Data from Django Backend REST Endpoint
    fetch(dataUrl)
        .then(response => response.json())
        .then(data => {
            masterData.nodes = data.nodes;
            masterData.edges = data.edges;
            
            // Initial payload initialization: Render out full entity mesh map
            runCombinedFilters('', 'ALL');
        })
        .catch(error => console.error("Error loading network graph configurations:", error));

    // 2. Dual-Input Relationship Filtration Engine
    function runCombinedFilters(textValue, selectedRole) {
        const textQuery = textValue.trim().toLowerCase();

        // Short-Circuit evaluation: Revert straight to base schema layout if filters are clear
        if (textQuery === '' && selectedRole === 'ALL') {
            myChart.setOption({
                series: [{ ...commonSeriesConfig, data: masterData.nodes, links: masterData.edges }]
            }, { notMerge: true });
            return;
        }

        // STEP A: Evaluate and cross-reference edge lines based on user query states
        const finalEdgesToRender = masterData.edges.filter(edge => {
            const sourceNode = masterData.nodes.find(n => n.id === edge.source);
            const targetNode = masterData.nodes.find(n => n.id === edge.target);
            
            if (!sourceNode || !targetNode) return false;

            // Compute role condition intersection
            const matchesRole = selectedRole === 'ALL' || 
                sourceNode.category.toString() === selectedRole || 
                targetNode.category.toString() === selectedRole;

            // Compute fuzzy text search input substring matching
            const matchesText = textQuery === '' || 
                edge.source.toLowerCase().includes(textQuery) || 
                edge.target.toLowerCase().includes(textQuery) ||
                sourceNode.name.toLowerCase().includes(textQuery) ||
                targetNode.name.toLowerCase().includes(textQuery);

            return matchesRole && matchesText;
        });

        // STEP B: Generate unique active layout node ID sets from the filtered edge paths
        const activeNodeIds = new Set();
        finalEdgesToRender.forEach(edge => {
            activeNodeIds.add(edge.source);
            activeNodeIds.add(edge.target);
        });

        // STEP C: Trace context dependencies (Ensure Endpoints always show who owns them)
        masterData.edges.forEach(edge => {
            if (activeNodeIds.has(edge.target) && edge.label.formatter === 'owner') {
                activeNodeIds.add(edge.source);
                if (!finalEdgesToRender.some(e => e.source === edge.source && e.target === edge.target)) {
                    finalEdgesToRender.push(edge);
                }
            }
        });

        // STEP D: Map tracking IDs cleanly back to the immutable master storage arrays
        const finalNodesToRender = masterData.nodes.filter(node => activeNodeIds.has(node.id));

        // Inject modified dataset arrays back to the active ECharts layer view
        myChart.setOption({
            series: [{
                ...commonSeriesConfig,
                data: finalNodesToRender,
                links: finalEdgesToRender
            }]
        }, { notMerge: true });
    }

    // 3. Handle Event Triggers (Updates seamlessly on click or immediate keystroke)
    searchInput.addEventListener('input', function () {
        runCombinedFilters(searchInput.value, roleFilter.value);
    });

    roleFilter.addEventListener('change', function () {
        runCombinedFilters(searchInput.value, roleFilter.value);
    });

    // 4. Handle Node Clicks to Route Users via Developer Portal Navigation
    myChart.on('click', { dataType: 'node' }, function (params) {
        const nodeId = params.data.id;
        const categoryIndex = params.data.category;

        if (categoryIndex === 0) {
            window.location.href = `${producerDetailBase}${encodeURIComponent(nodeId)}/`;
        } else if (categoryIndex === 1) {
            window.location.href = `${endpointDetailBase}${encodeURIComponent(nodeId)}/`;
        } else if (categoryIndex === 2) {
            window.location.href = `${consumerDetailBase}${encodeURIComponent(nodeId)}/`;
        }
    });

    // Keep layout fully responsive on browser resizing changes
    window.addEventListener('resize', () => myChart.resize());
});