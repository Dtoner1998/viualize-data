$(document).ready(function () {
    // get url
    let currentURL = $(location).attr('pathname');
    if (currentURL != '/factor') {
        return false;
    }
    // begin
    $(".begin").on("input", function () {
        var val = $(this).val();
        var min = $(this).attr("min");

        var max = $(this).attr("max");
        var portion = (val - min) / (max - min);
        $(".indicator_begin").text(val);
        $(".indicator_begin").css("left", portion * ($(".begin").width() - 18));
        // correlation
        var begin = $(".begin").val();
        var end = $(".end").val();
        if (begin > end) {
            $.confirm({
                title: 'Confirm',
                content: 'Please choose begin year bigger than or equal end year!',
                iconClose: true,
                buttons: {
                    ok: {
                        btnClass: 'btn-primay',
                        action: function () {
                            $(".begin").val(min);
                            $(".indicator_begin").text(min);
                            title_factor(min, end);
                            chart_subplotly(disease);
                        }
                    },
                }
            });
            return false;
        }
        title_factor(begin, end);
        chart_subplotly(disease);

    });
    // end
    $(".end").on("input", function () {
        var val = $(this).val();
        var min = $(this).attr("min");
        var max = $(this).attr("max");
        var portion = (val - min) / (max - min);
        $(".indicator_end").text(val);
        $(".indicator_end").css("left", portion * ($(".end").width() - 18));

        var begin = $(".begin").val();
        var end = $(".end").val();
        if (begin > end) {
            $.confirm({
                title: 'Confirm',
                content: 'Please choose begin year bigger than or equal end year!',
                iconClose: true,
                buttons: {
                    ok: {
                        btnClass: 'btn-primay',
                        action: function () {
                            $(".begin").val(min);
                            $(".indicator_begin").text(min);
                            title_factor(min, end);
                            chart_subplotly(disease);
                        }
                    },
                }
            });
            return false;
        }
        title_factor(begin, end);
        chart_subplotly(disease);
    });
    // disease
    var disease = 'influenza'
    $('.disease_select')[0].checked = true;
    $('.disease_select').click(function () {
        if (this.checked) {
            disease = $(this).val().toLowerCase();
            chart_subplotly(disease);
        }
    });
    // year and month 
    var year_month = 'year'
    $('.radioBtnClass').click(function () {
        if (this.checked) {
            year_month = $(this).val();
        }
        chart_subplotly(disease);
    });
    var year_month2 = 'year'
    $('.radioBtnClass1').click(function () {
        if (this.checked) {
            year_month2 = $(this).val();
        }
        chart_subplotly(disease);
    });
    function chart_subplotly(disease) {
        // check time
        var begin = $(".begin").val();
        var end = $(".end").val();

        // subplotly year
        $.ajax({
            url: "/subplotly_year",
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            data: {
                disease: disease,
                begin: begin,
                end: end,
                y_m: year_month
            },
            dataType: "json",
            success: function (data) {
                Plotly.newPlot(`subplotly_y`, data, {});
                $(`#sub_title_year`).html(`Compare  ${disease.split('_').join('  ')} with climate by ${year_month2}ly cases Viet Nam from ${begin}-${end}`);

            },
        })

        //bubble subplot
        $.ajax({
            url: "/subplotly_bubble_year",
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            data: {
                begin: begin,
                end: end,
                y_m: year_month2
            },
            dataType: "json",
            success: function (data) {
                Plotly.newPlot(`bubble_plot`, data, {});
                $(`#sub_title_bubble`).html(`Total number of Influenza, Dengue Fever and Diahhroea cases per ${year_month2} compared with mean climate Viet Nam from ${begin}-${end}`);

            },
        })
        // corr_factor
        $.ajax({
            url: "/corr_factor",
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            data: {
                disease: disease,
                begin: begin,
                end: end,
            },
            dataType: "json",
            success: function (data) {
                Plotly.newPlot(`corr_compare`, data, {});
                $(`#sub_corr_title`).html(`Correlation of Diseases and Weather in Viet Nam from ${begin}-${end}`);
            },
        });
        $.ajax({
            url: "/lag_correlation_disease",
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            data: {
                disease: disease,
                begin: begin,
                end: end,
            },
            dataType: "json",
            success: function (data) {
                Plotly.newPlot(`lag_disease`, data, {});
                $(`#lag_title`).html(`Lag Correlation of ${disease.split('_').join('  ')} in Viet Nam from ${begin}-${end}`);
            },
        });
        // chart compare disease
        $.ajax({
            url: "/compare_disease",
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            data: {
                disease: disease,
                begin: begin,
                end: end,
            },
            dataType: "json",
            success: function (data) {
                Plotly.newPlot(`comp_disease`, data, {});
                $(`#comp_disease_title`).html(`Incidence and death of ${disease.split('_').join('  ')} by monthly total Viet Nam from ${begin}-${end}`);

            },
        });
        $.ajax({
            url: "/disease_and_weather",
            type: "GET",
            contentType: "application/json;charset=UTF-8",
            data: {
                disease: disease,
                begin: begin,
                end: end,
            },
            dataType: "json",
            success: function (data) {
                Plotly.newPlot(`line_bar_disease`, data, {});
                $(`#line_bar_title`).html(`Total ${disease.split('_').join('  ')} cases per year and average weather Viet Nam from ${begin}-${end}`);

            },
        });
    };
    chart_subplotly(disease);
    title_factor(1997, 2019);
    function title_factor(begin, end) {
        $('.title_factor').html(` Explore Disease In Viet Nam From ${begin}-${end}`)
    }

});