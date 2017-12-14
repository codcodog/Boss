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
        text: '各区职位发布情况',
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
        text: name + "各商业区职位发布情况 / 前30"
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
        text: '各行业职位发布情况',
        subtext: 'PHP'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
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
