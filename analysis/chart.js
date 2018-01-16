// 各区
var dom    = document.getElementById("container1");
var chart1 = echarts.init(dom);

var type1  = [];
var data1  = [];
for (var i in area) {
    type1[i] = area[i].area;
    data1[i] = {value: area[i].total, name: area[i].area}
}

option = {
    title : {
        text: '区域职位发布情况',
        subtext: 'PHP',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: type1,
    },
    series : [
        {
            name: '访问来源',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data: data1,
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};
chart1.setOption(option, true);

// ------------------------------------------------------

// 各商圈
var dom    = document.getElementById("container2");
var chart2 = echarts.init(dom);
var type2  = [];
var data2  = [];

for (var i in business) {
    type2[i] = business[i].business;
    data2[i] = business[i].total;
}

option = {
    title: {
        text: "商业区职位发布情况 (前30)"
    },
    tooltip: {},
    legend: {
        data:['PHP']
    },
    xAxis: {
        data: type2,
        axisLabel: {
            interval:0,
        },
    },
    yAxis: {},
    series: [{
        name: 'PHP',
        type: 'bar',
        data: data2
    }]
};

chart2.setOption(option, true);

// ------------------------------------------------------

// 各行业
var dom    = document.getElementById("container3");
var chart3 = echarts.init(dom);
var type3  = [];
var data3  = [];

for (var i in industry) {
    type3[i] = industry[i].type;
    data3[i] = industry[i].total;
}

option = {
    title: {
        text: '行业职位发布情况',
        subtext: 'PHP'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data:['PHP'],
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
    },
    yAxis: {
        type: 'category',
        data: type3,
        boundaryGap: [0, 0.01],
        axisLabel: {
            interval:0,
        },
    },
    series: [
        {
            name: 'PHP',
            type: 'bar',
            data: data3,
        }
    ]
};

chart3.setOption(option, true);

// ------------------------------------------------------

// 各商圈工作年限分布
var dom    = document.getElementById("container4");
var chart4 = echarts.init(dom);
var data   = [];
var legend = [];

for (var i in data4) {
    data.push({name: i, type: 'bar', data: data4[i]});
    legend.push(i);
}

option = {
    title: {
        text: '商业区工作年限职位发布情况 (前15)',
        subtext: 'PHP'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: legend,
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    yAxis: {
        type: 'value',
    },
    xAxis: {
        type: 'category',
        data: type4,
        boundaryGap: [0, 0.01],
        axisLabel: {
            interval:0,
        },
    },
    series: data,
};

chart4.setOption(option, true);

// ------------------------------------------------------

// 各商圈薪资分布
var dom    = document.getElementById("container5");
var chart5 = echarts.init(dom);
var data   = [];
var legend5 = [];

for (var i in data5) {
    data.push({name: i, type: 'bar', data: data5[i]});
    legend5.push(i);
}

option = {
    title: {
        text: '商业区工作年限薪资情况 (前15)',
        subtext: 'PHP'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: legend5,
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    yAxis: {
        type: 'value',
    },
    xAxis: {
        type: 'category',
        data: type5,
        boundaryGap: [0, 0.01],
        axisLabel: {
            interval:0,
        },
    },
    series: data,
};

chart5.setOption(option, true);

// ------------------------------------------------------

// 行业职位分布
var dom    = document.getElementById("container6");
var chart6 = echarts.init(dom);
var data   = [];
var legend6 = [];

for (var i in data6) {
    data.push({name: i, type: 'bar', data: data6[i]});
    legend6.push(i);
}

option = {
    title: {
        text: '行业工作年限职位发布情况',
        subtext: 'PHP'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: legend6,
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
    },
    yAxis: {
        type: 'category',
        data: industry6,
        boundaryGap: [0, 0.01],
        axisLabel: {
            interval:0,
        },
    },
    series: data,
};

chart6.setOption(option, true);

// ------------------------------------------------------

// 行业薪资分布
var dom    = document.getElementById("container7");
var chart7 = echarts.init(dom);
var data   = [];
var legend7 = [];

for (var i in data7) {
    data.push({name: i, type: 'bar', data: data7[i]});
    legend7.push(i);
}

option = {
    title: {
        text: '行业工作年限薪资情况',
        subtext: 'PHP'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: legend7,
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
    },
    yAxis: {
        type: 'category',
        data: industry7,
        boundaryGap: [0, 0.01],
        axisLabel: {
            interval:0,
        },
    },
    series: data,
};

chart7.setOption(option, true);
